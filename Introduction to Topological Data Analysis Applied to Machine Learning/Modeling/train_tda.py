import os
import argparse
import json
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import roc_auc_score, precision_recall_curve, auc, classification_report, confusion_matrix, f1_score
from google.cloud import storage

def parse_args():
    parser = argparse.ArgumentParser(description="Vertex AI XGBoost TDA-Enhanced Training")
    parser.add_argument("--train_path", type=str, required=True, help="GCS path to training parquet")
    parser.add_argument("--test_path", type=str, required=True, help="GCS path to testing parquet")
    parser.add_argument("--model_output_dir", type=str, required=True, help="GCS directory to save trained model")
    parser.add_argument("--scale_pos_weight", type=float, default=27.43, help="Imbalance ratio weight for XGBoost")
    return parser.parse_args()

def main():
    args = parse_args()
    print("=== Starting Vertex AI TDA-Enhanced XGBoost Training Job ===")
    print(f"Train Path: {args.train_path}")
    print(f"Test Path: {args.test_path}")
    print(f"Scale Pos Weight: {args.scale_pos_weight}")

    # 1. Load Parquet Datasets from GCS
    print("\n[1/5] Loading Parquet datasets into memory...")
    train_df = pd.read_parquet(args.train_path)
    test_df = pd.read_parquet(args.test_path)

    # 2. Separate Target (isFraud) and Features (now includes TDA features)
    target_col = "isFraud"
    feature_cols = [c for c in train_df.columns if c != target_col]

    X_train, y_train = train_df[feature_cols], train_df[target_col].astype(int)
    X_test, y_test = test_df[feature_cols], test_df[target_col].astype(int)

    print(f"Training Matrix Shape (with TDA features): {X_train.shape}")
    print(f"Testing Matrix Shape (with TDA features):  {X_test.shape}")

    # 3. Configure XGBoost Classifier
    print("\n[2/5] Initializing XGBoost Classifier with Imbalance Handling...")
    model = xgb.XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=args.scale_pos_weight,
        tree_method="hist",  # Optimized for large multi-feature tables
        random_state=42,
        n_jobs=-1
    )

    # 4. Train Model
    print("\n[3/5] Fitting XGBoost TDA-Enhanced Model...")
    model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        verbose=50
    )

    # 5. Model Evaluation Out-Of-Time (Test Set)
    print("\n[4/5] Evaluating Out-Of-Time Model Performance...")
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    y_pred_binary = (y_pred_proba >= 0.5).astype(int)

    # Calculate Standard Metrics
    roc_auc = roc_auc_score(y_test, y_pred_proba)
    precision, recall, thresholds = precision_recall_curve(y_test, y_pred_proba)
    pr_auc = auc(recall, precision)
    cm_default = confusion_matrix(y_test, y_pred_binary)

    # --- OPTIMIZACIÓN DE UMBRAL (F1-Score) ---
    print("\n[Optimization] Calculating Optimal Decision Threshold...")
    f1_scores = 2 * (precision * recall) / (precision + recall + 1e-8)
    best_index = np.argmax(f1_scores)
    best_threshold = thresholds[best_index] if best_index < len(thresholds) else 0.5
    best_f1 = f1_scores[best_index]

    y_pred_optimized = (y_pred_proba >= best_threshold).astype(int)
    cm_optimized = confusion_matrix(y_test, y_pred_optimized)

    metrics = {
        "ROC_AUC": float(roc_auc),
        "PR_AUC": float(pr_auc),
        "Default_Threshold": 0.5,
        "Default_Confusion_Matrix": cm_default.tolist(),
        "Optimal_Threshold": float(best_threshold),
        "Optimal_F1_Score": float(best_f1),
        "Optimal_Confusion_Matrix": cm_optimized.tolist()
    }

    print("\n=== TDA-ENHANCED MODEL RESULTS ===")
    print(f"ROC-AUC Score: {roc_auc:.4f}")
    print(f"PR-AUC Score:  {pr_auc:.4f}")
    print(f"\n--- Threshold 0.5 (Default) ---")
    print("Confusion Matrix:")
    print(cm_default)
    print(classification_report(y_test, y_pred_binary))

    print(f"\n--- Optimal Threshold ({best_threshold:.4f}) ---")
    print(f"Max F1-Score: {best_f1:.4f}")
    print("Confusion Matrix (Optimized):")
    print(cm_optimized)
    print(classification_report(y_test, y_pred_optimized))

    # 6. Save Model Artifacts to GCS
    print("\n[5/5] Saving model and metrics to Google Cloud Storage...")
    os.makedirs("/tmp/model", exist_ok=True)
    
    # Save Model JSON
    model_file = "/tmp/model/xgboost_tda.json"
    model.save_model(model_file)
    
    # Save Metrics JSON
    metrics_file = "/tmp/model/metrics.json"
    with open(metrics_file, "w") as f:
        json.dump(metrics, f, indent=4)

    # Upload to GCS destination
    storage_client = storage.Client()
    bucket_name = args.model_output_dir.replace("gs://", "").split("/")[0]
    prefix = "/".join(args.model_output_dir.replace("gs://", "").split("/")[1:])

    bucket = storage_client.bucket(bucket_name)
    
    blob_model = bucket.blob(os.path.join(prefix, "xgboost_tda.json"))
    blob_model.upload_from_filename(model_file)

    blob_metrics = bucket.blob(os.path.join(prefix, "metrics.json"))
    blob_metrics.upload_from_filename(metrics_file)

    print(f"Artifacts successfully uploaded to: {args.model_output_dir}")
    print("=== Training Completed Successfully ===")

if __name__ == "__main__":
    main()