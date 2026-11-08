SELECT
    COUNT(*) AS total_registros,
    COUNT(DISTINCT TransactionID) AS transaction_id_unicos,
    COUNTIF(TransactionID IS NULL) AS transaction_id_nulos,
    COUNT(*)
        - COUNT(DISTINCT TransactionID)
        - COUNTIF(TransactionID IS NULL) AS registros_duplicados_adicionales
FROM
    `fraud-detection-eda.fraud_detection.transaction_raw`;