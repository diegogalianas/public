SELECT 
    COUNT(*) AS total_records,
    MIN(TransactionDT) AS min_transaction_dt,
    MAX(TransactionDT) AS max_transaction_dt,
    AVG(TransactionDT) AS avg_transaction_dt
FROM `fraud-detection-eda.fraud_detection.joined_view`;