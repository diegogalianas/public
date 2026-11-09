cat << 'EOF' > run_tda_subsampling.sh
#!/usr/bin/env bash
set -euo pipefail

echo "=== 1. Installing required Python libraries ==="
python3 -m pip install --quiet xgboost scikit-learn pandas numpy pyarrow fastparquet

echo "=== 2. Creating isolated working directories ==="
mkdir -p /tmp/tda_subsample/data /tmp/tda_subsample/model

echo "=== 3. Downloading test dataset & baseline model from GCS ==="
gcloud storage cp gs://fraud-detection-imf/processed/baseline_test_dataset.parquet/*.parquet /tmp/tda_subsample/data/
gcloud storage cp gs://fraud-detection-imf/models/baseline/xgboost_baseline.json /tmp/tda_subsample/model/

echo "=== 4. Running intelligent subsampling script ==="
python3 - << 'PYTHON_SCRIPT'
import os
import xgboost as xgb
import pandas as pd
import numpy as np
import pyarrow.parquet as pq

print("-> Reading test dataset...")
dataset = pq.ParquetDataset("/tmp/tda_subsample/data/")
df = dataset.read().to_pandas()

if 'isFraud' in df.columns:
    y_true = df['isFraud'].values
    X = df.drop(columns=['isFraud'])
else:
    raise ValueError("Column 'isFraud' not found in test dataset.")

print("-> Loading XGBoost baseline model for error classification...")
booster = xgb.Booster()
booster.load_model("/tmp/tda_subsample/model/xgboost_baseline.json")
booster.feature_names = list(X.columns)

# Run inference
dtest = xgb.DMatrix(X, feature_names=list(X.columns))
y_probs = booster.predict(dtest)
y_pred = (y_probs >= 0.5).astype(int)

df['y_true'] = y_true
df['y_pred'] = y_pred
df['y_prob'] = y_probs

# Classify error types safely for NumPy 2.x
conditions = [
    (df['y_true'] == 0) & (df['y_pred'] == 0),
    (df['y_true'] == 0) & (df['y_pred'] == 1), # False Positives
    (df['y_true'] == 1) & (df['y_pred'] == 0), # False Negatives
    (df['y_true'] == 1) & (df['y_pred'] == 1)  # True Positives
]
choices = ['TN', 'FP', 'FN', 'TP']
df['error_type'] = np.select(conditions, choices, default='UNK').astype(str)

print("\n=== Prediction Error Breakdown in Full Test Set ===")
print(df['error_type'].value_counts())

# Select Top 20 features based on our feature importance analysis
top_20_features = [
    'V258', 'V218', 'V264', 'V294', 'V70', 'V257', 'V91', 'V201', 
    'C4', 'V158', 'V308', 'C8', 'card6', 'V187', 'C14', 'V317', 
    'V102', 'V90', 'V327', 'V163'
]
available_features = [f for f in top_20_features if f in df.columns]

# Intelligent Subsampling: Keep all FPs, all TPs, all FNs, and a balanced sample of TNs (e.g., 5,000 points max)
df_fp = df[df['error_type'] == 'FP']
df_tp = df[df['error_type'] == 'TP']
df_fn = df[df['error_type'] == 'FN']
df_tn_sample = df[df['error_type'] == 'TN'].sample(n=min(5000, sum(df['error_type'] == 'TN')), random_state=42)

df_tda_sample = pd.concat([df_fp, df_tp, df_fn, df_tn_sample])

# Keep only features + metadata columns
cols_to_keep = available_features + ['y_true', 'y_pred', 'y_prob', 'error_type']
df_tda_cloud = df_tda_sample[cols_to_keep]

print(f"\n-> Subsampled Point Cloud Shape: {df_tda_cloud.shape}")
print(df_tda_cloud['error_type'].value_counts())

# Export locally
output_parquet = "tda_point_cloud_sample.parquet"
df_tda_cloud.to_parquet(output_parquet, index=False)
print(f"-> Saved locally as {output_parquet}")
PYTHON_SCRIPT

echo "=== 5. Uploading subsampled point cloud to GCS ==="
gcloud storage cp tda_point_cloud_sample.parquet gs://fraud-detection-imf/processed/tda_point_cloud_sample.parquet

echo "=== Subsampling completed successfully! ==="
EOF

chmod +x run_tda_subsampling.sh
./run_tda_subsampling.sh