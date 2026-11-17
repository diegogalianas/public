SELECT 
    '04_user_aggregations_no_leak_view (Pre-encoding)' AS stage,
    COUNT(*) AS total_records,
    (SELECT COUNT(*) FROM `fraud-detection-eda.fraud_detection.INFORMATION_SCHEMA.COLUMNS` WHERE table_name = '04_user_aggregations_no_leak_view') AS total_columns
FROM `fraud-detection-eda.fraud_detection.04_user_aggregations_no_leak_view`
UNION ALL
SELECT 
    '05_encoding_selection_no_leak_view (Encoded Step)' AS stage,
    COUNT(*) AS total_records,
    (SELECT COUNT(*) FROM `fraud-detection-eda.fraud_detection.INFORMATION_SCHEMA.COLUMNS` WHERE table_name = '05_encoding_selection_no_leak_view') AS total_columns
FROM `fraud-detection-eda.fraud_detection.05_encoding_selection_no_leak_view`;