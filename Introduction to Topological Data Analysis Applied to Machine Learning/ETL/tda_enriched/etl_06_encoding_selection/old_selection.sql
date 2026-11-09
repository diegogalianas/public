SELECT 
    '05_tda_view (Pre-encoding)' AS stage,
    COUNT(*) AS total_records,
    (SELECT COUNT(*) FROM `fraud-detection-eda.fraud_detection.INFORMATION_SCHEMA.COLUMNS` WHERE table_name = '05_tda_view') AS total_columns
FROM `fraud-detection-eda.fraud_detection.05_tda_view`
UNION ALL
SELECT 
    '06_encoding_selection_view (Encoded Step)' AS stage,
    COUNT(*) AS total_records,
    (SELECT COUNT(*) FROM `fraud-detection-eda.fraud_detection.INFORMATION_SCHEMA.COLUMNS` WHERE table_name = '06_encoding_selection_view') AS total_columns
FROM `fraud-detection-eda.fraud_detection.06_encoding_selection_view`;