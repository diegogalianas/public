#!/usr/bin/env bash
# ==============================================================================
# Script to launch XGBoost Baseline Training on Vertex AI
# ==============================================================================

set -euo pipefail

REGION="europe-west4"
JOB_NAME="tfm-xgboost-baseline-training"
IMAGE_URI="europe-docker.pkg.dev/vertex-ai/training/scikit-learn-cpu.0-23:latest"
MACHINE_TYPE="n1-standard-8"

echo "=== Submitting Custom Job to Vertex AI: ${JOB_NAME} ==="

# 1. Submit the custom training job to Vertex AI
JOB_ID=$(gcloud ai custom-jobs create \
    --region="${REGION}" \
    --display-name="${JOB_NAME}" \
    --worker-pool-spec="machine-type=${MACHINE_TYPE},replica-count=1,container-image-uri=${IMAGE_URI}" \
    --command="bash","-c","python3 -m pip install pyarrow fastparquet && mkdir -p /tmp/train_data /tmp/test_data && gsutil -m cp gs://fraud-detection-imf/processed/baseline_train_dataset.parquet/*.parquet /tmp/train_data/ && gsutil -m cp gs://fraud-detection-imf/processed/baseline_test_dataset.parquet/*.parquet /tmp/test_data/ && gsutil cp gs://fraud-detection-imf/modeling/train_baseline.py /tmp/train_baseline.py && python3 /tmp/train_baseline.py --train_path=/tmp/train_data --test_path=/tmp/test_data --model_output_dir=gs://fraud-detection-imf/models/baseline/ --scale_pos_weight=27.43" \
    --format="value(name)")

echo "Job successfully created with ID: ${JOB_ID}"
echo "=== Streaming live logs... ==="

# 2. Attach live output stream directly to the terminal
gcloud ai custom-jobs stream-logs "${JOB_ID}" --region="${REGION}"