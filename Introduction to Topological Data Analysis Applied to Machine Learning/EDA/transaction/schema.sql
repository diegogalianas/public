SELECT
    column_name,
    ordinal_position,
    data_type,
    is_nullable
FROM
    `fraud-detection-eda.fraud_detection.INFORMATION_SCHEMA.COLUMNS`
WHERE
    table_name = 'transaction_raw'
ORDER BY
    ordinal_position;