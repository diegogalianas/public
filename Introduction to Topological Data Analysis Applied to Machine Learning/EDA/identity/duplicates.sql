SELECT
  COUNT(*) AS total_registros,
  COUNT(DISTINCT TransactionID) AS transaction_id_unicos,
  COUNTIF(TransactionID IS NULL) AS transaction_id_nulos,
  COUNT(*) - COUNTIF(TransactionID IS NULL)
    - COUNT(DISTINCT TransactionID) AS registros_duplicados_adicionales
FROM
  `fraud-detection-eda.fraud_detection.identity_raw`;