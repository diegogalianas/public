CREATE OR REPLACE EXTERNAL TABLE `fraud-detection-eda.fraud_detection.joined_view`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://fraud-detection-imf/processed/joined_dataset.parquet/*.parquet']
);