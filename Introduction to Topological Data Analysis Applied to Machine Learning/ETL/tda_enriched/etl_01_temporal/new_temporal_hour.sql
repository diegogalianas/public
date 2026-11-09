SELECT 
    DT_hour,
    COUNT(*) AS total_transactions,
    SUM(CAST(isFraud AS INT64)) AS fraud_count,
    ROUND(AVG(CAST(isFraud AS FLOAT64)) * 100, 2) AS fraud_rate_percentage
FROM `fraud-detection-eda.fraud_detection.01_temporal_view`
GROUP BY DT_hour
ORDER BY DT_hour ASC;