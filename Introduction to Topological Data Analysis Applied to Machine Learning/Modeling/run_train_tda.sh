cat << 'EOF' > run_train_tda.sh
#!/usr/bin/env bash
set -euo pipefail

REGION="europe-west4"
JOB_NAME="tfm-xgboost-tda-clean-training"
IMAGE_URI="europe-docker.pkg.dev/vertex-ai/training/tf-cpu.2-11.py310:latest"
MACHINE_TYPE="n1-standard-8"

echo "=== Submitting Custom Job to Vertex AI: ${JOB_NAME} ==="

JOB_ID=$(gcloud ai custom-jobs create \
    --region="${REGION}" \
    --display-name="${JOB_NAME}" \
    --worker-pool-spec="machine-type=${MACHINE_TYPE},replica-count=1,container-image-uri=${IMAGE_URI}" \
    --command="bash","-c","python3 -m pip install --quiet xgboost pyarrow scikit-learn google-cloud-storage && mkdir -p /tmp/train_data /tmp/test_data && gsutil -m cp gs://fraud-detection-imf/processed_tda/train_tda_enriched.parquet/*.parquet /tmp/train_data/ && gsutil -m cp gs://fraud-detection-imf/processed_tda/test_tda_enriched.parquet/*.parquet /tmp/test_data/ && gsutil cp gs://fraud-detection-imf/modeling/train_tda.py /tmp/train_tda.py && python3 /tmp/train_tda.py --train_path=/tmp/train_data --test_path=/tmp/test_data --model_output_dir=gs://fraud-detection-imf/models/tda_clean/ --scale_pos_weight=27.43" \
    --format="value(name)")

echo "Job successfully created with ID: ${JOB_ID}"
echo "=== Streaming live logs... ==="

gcloud ai custom-jobs stream-logs "${JOB_ID}" --region="${REGION}"
EOF

chmod +x run_train_tda.sh
./run_train_tda.sh