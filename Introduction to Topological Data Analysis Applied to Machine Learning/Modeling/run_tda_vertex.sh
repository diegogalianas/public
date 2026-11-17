cat << 'EOF' > run_tda_vertex.sh
#!/usr/bin/env bash
set -euo pipefail

REGION="europe-west4"
JOB_NAME="tfm-tda-centroid-extraction"
IMAGE_URI="europe-docker.pkg.dev/vertex-ai/training/scikit-learn-cpu.0-23:latest"
MACHINE_TYPE="n1-standard-8"

echo "=== 1. Creating Python script for TDA extraction ==="
cat << 'PYTHON_SCRIPT' > /tmp/tda_extraction.py
import os
import json
import xgboost as xgb
import pandas as pd
import numpy as np
import pyarrow.parquet as pq
from sklearn.preprocessing import StandardScaler
from ripser import ripser

print("-> Reading TDA Train dataset from GCS...")
dataset = pq.ParquetDataset("/tmp/tda_data/")
df = dataset.read().to_pandas()

if 'isFraud' in df.columns:
    y_true = df['isFraud'].values
    X = df.drop(columns=['isFraud'])
else:
    raise ValueError("Column 'isFraud' not found in train dataset.")

print("-> Loading XGBoost baseline model for clean error classification...")
booster = xgb.Booster()
booster.load_model("/tmp/model/xgboost_baseline.json")
booster.feature_names = list(X.columns)

# Run inference on Train data
dtest = xgb.DMatrix(X, feature_names=list(X.columns))
y_probs = booster.predict(dtest)
y_pred = (y_probs >= 0.5).astype(int)

df['y_true'] = y_true
df['y_pred'] = y_pred
df['y_prob'] = y_probs

# Classify error types safely
conditions = [
    (df['y_true'] == 0) & (df['y_pred'] == 0),
    (df['y_true'] == 0) & (df['y_pred'] == 1), # False Positives
    (df['y_true'] == 1) & (df['y_pred'] == 0), # False Negatives
    (df['y_true'] == 1) & (df['y_pred'] == 1)  # True Positives
]
choices = ['TN', 'FP', 'FN', 'TP']
df['error_type'] = np.select(conditions, choices, default='UNK').astype(str)

print("\n=== Prediction Error Breakdown in Train Set ===")
print(df['error_type'].value_counts())

# Select Top 20 features
top_20_features = [
    'V258', 'V218', 'V264', 'V294', 'V70', 'V257', 'V91', 'V201', 
    'C4', 'V158', 'V308', 'C8', 'card6', 'V187', 'C14', 'V317', 
    'V102', 'V90', 'V327', 'V163'
]
available_features = [f for f in top_20_features if f in df.columns]

# Intelligent Subsampling (10k TNs + 100% errors)
df_fp = df[df['error_type'] == 'FP']
df_tp = df[df['error_type'] == 'TP']
df_fn = df[df['error_type'] == 'FN']
df_tn_sample = df[df['error_type'] == 'TN'].sample(n=min(10000, sum(df['error_type'] == 'TN')), random_state=42)

df_tda_sample = pd.concat([df_fp, df_tp, df_fn, df_tn_sample])

if 'TransactionID' not in df_tda_sample.columns and df_tda_sample.index.name == 'TransactionID':
    df_tda_sample = df_tda_sample.reset_index()
elif 'TransactionID' not in df_tda_sample.columns:
    df_tda_sample = df_tda_sample.reset_index().rename(columns={'index': 'TransactionID'})

cols_to_keep = ['TransactionID'] + available_features + ['y_true', 'y_pred', 'y_prob', 'error_type']
cols_to_keep = [c for c in cols_to_keep if c in df_tda_sample.columns]
df_tda_cloud = df_tda_sample[cols_to_keep]

print(f"\n-> Subsampled Point Cloud Shape: {df_tda_cloud.shape}")

metadata_cols = ['TransactionID', 'y_true', 'y_pred', 'y_prob', 'error_type']
feature_cols = [col for col in df_tda_cloud.columns if col not in metadata_cols]
X_raw = df_tda_cloud[feature_cols].fillna(0)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_raw.values)

# Safe point cap for Ripser in memory
max_points = 5000
np.random.seed(42)
if X_scaled.shape[0] > max_points:
    indices = np.random.choice(X_scaled.shape[0], max_points, replace=False)
    X_subset = X_scaled[indices]
else:
    X_subset = X_scaled

print("-> Computing Persistent Homology and Cocycles via Ripser on Train Set...")
result = ripser(X_subset, maxdim=1, do_cocycles=True)
diagrams = result['dgms']
cocycles = result['cocycles']

print("-> Extracting H1 Centroids from topological loops...")
dgm_h1 = diagrams[1]
cocs_h1 = cocycles[1]
centroids_dict = {}

if len(dgm_h1) > 0:
    h1_persistence = dgm_h1[:, 1] - dgm_h1[:, 0]
    sorted_h1_indices = np.argsort(h1_persistence)[::-1]
    top_k = 5

    for rank in range(min(top_k, len(dgm_h1))):
        loop_idx = sorted_h1_indices[rank]
        cocycle = cocs_h1[loop_idx]
        
        if len(cocycle) > 0:
            flat_indices = np.unique(cocycle[:, :2].astype(int))
            centroid = np.mean(X_subset[flat_indices], axis=0)
            centroids_dict[f"dist_to_h1_loop_{rank + 1}"] = centroid.tolist()
            print(f"  -> Centroid #{rank + 1} calculated using {len(flat_indices)} points (Persistence: {h1_persistence[loop_idx]:.3f})")

print("-> Exporting centroid and scaler metadata to JSON...")
metadata_payload = {
    "feature_cols": feature_cols,
    "scaler_mean": scaler.mean_.tolist(),
    "scaler_scale": scaler.scale_.tolist(),
    "centroids": centroids_dict
}

local_json_path = "/tmp/tda_centroids.json"
with open(local_json_path, "w") as f:
    json.dump(metadata_payload, f)

print("-> Uploading centroids JSON to processed_tda bucket...")
os.system("gsutil cp /tmp/tda_centroids.json gs://fraud-detection-imf/processed_tda/tda_centroids.json")
print("=== TDA Centroid Extraction Job Completed Successfully! ===")
PYTHON_SCRIPT

echo "=== 2. Uploading extraction script to GCS ==="
gsutil cp /tmp/tda_extraction.py gs://fraud-detection-imf/modeling/tda_extraction.py

echo "=== 3. Submitting Custom Job to Vertex AI (${JOB_NAME}) ==="
JOB_ID=$(gcloud ai custom-jobs create \
    --region="${REGION}" \
    --display-name="${JOB_NAME}" \
    --worker-pool-spec="machine-type=${MACHINE_TYPE},replica-count=1,container-image-uri=${IMAGE_URI}" \
    --command="bash","-c","python3 -m pip install --quiet xgboost scikit-learn pandas numpy pyarrow fastparquet ripser persim && mkdir -p /tmp/tda_data /tmp/model && gsutil -m cp gs://fraud-detection-imf/processed_tda/train_dataset.parquet/*.parquet /tmp/tda_data/ && gsutil cp gs://fraud-detection-imf/models/baseline/xgboost_baseline.json /tmp/model/xgboost_baseline.json && python3 /tmp/tda_extraction.py" \
    --format="value(name)")

echo "Job successfully created with ID: ${JOB_ID}"
echo "=== Streaming live logs from Vertex AI... ==="
gcloud ai custom-jobs stream-logs "${JOB_ID}" --region="${REGION}"
EOF

chmod +x run_tda_vertex.sh
./run_tda_vertex.sh