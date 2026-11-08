SELECT 
    COUNT(*) AS total_records,
    MIN(DT_hour) AS min_hour,
    MAX(DT_hour) AS max_hour,
    MIN(DT_day_of_week) AS min_day_of_week,
    MAX(DT_day_of_week) AS max_day_of_week,
    MIN(DT_day_continuous) AS min_day_continuous,
    MAX(DT_day_continuous) AS max_day_continuous
FROM `fraud-detection-eda.fraud_detection.01_temporal_view`;