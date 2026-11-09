SELECT 
    COUNT(*) AS total_records,
    ROUND(AVG(TransactionAmt), 2) AS global_avg_amt,
    ROUND(STDDEV(TransactionAmt), 2) AS global_std_amt,
    MIN(TransactionAmt) AS min_amt,
    MAX(TransactionAmt) AS max_amt
FROM `fraud-detection-eda.fraud_detection.03_email_view`;