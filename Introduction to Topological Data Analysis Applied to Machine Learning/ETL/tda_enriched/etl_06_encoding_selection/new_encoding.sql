SELECT 
    column_name, 
    data_type 
FROM `fraud-detection-eda.fraud_detection.INFORMATION_SCHEMA.COLUMNS` 
WHERE table_name = '06_encoding_selection_view' 
  AND data_type = 'STRING';