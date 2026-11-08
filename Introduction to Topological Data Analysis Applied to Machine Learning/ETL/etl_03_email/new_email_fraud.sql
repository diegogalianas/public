SELECT 
    P_emaildomain_bin,
    COUNT(*) AS total_transactions,
    SUM(CAST(isFraud AS INT64)) AS fraud_count,
    ROUND(AVG(CAST(isFraud AS FLOAT64)) * 100, 2) AS fraud_rate_percentage
FROM `fraud-detection-eda.fraud_detection.03_email_view`
GROUP BY P_emaildomain_bin
ORDER BY fraud_rate_percentage DESC;