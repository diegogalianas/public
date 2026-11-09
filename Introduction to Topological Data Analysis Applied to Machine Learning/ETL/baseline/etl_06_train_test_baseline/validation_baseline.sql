SELECT 
    'Baseline Train (Days 1-145)' AS partition_name,
    COUNT(*) AS total_records,
    SUM(CAST(isFraud AS INT64)) AS fraud_count,
    ROUND(AVG(CAST(isFraud AS FLOAT64)) * 100, 2) AS fraud_rate_percentage,
    MIN(DT_day_continuous) AS min_day,
    MAX(DT_day_continuous) AS max_day
FROM `fraud-detection-eda.fraud_detection.baseline_train_view`
UNION ALL
SELECT 
    'Baseline Test (Days 146-182)' AS partition_name,
    COUNT(*) AS total_records,
    SUM(CAST(isFraud AS INT64)) AS fraud_count,
    ROUND(AVG(CAST(isFraud AS FLOAT64)) * 100, 2) AS fraud_rate_percentage,
    MIN(DT_day_continuous) AS min_day,
    MAX(DT_day_continuous) AS max_day
FROM `fraud-detection-eda.fraud_detection.baseline_test_view`;