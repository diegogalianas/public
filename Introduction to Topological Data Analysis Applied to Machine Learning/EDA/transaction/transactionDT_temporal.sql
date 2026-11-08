SELECT
  COUNT(*) AS total_registros,
  COUNTIF(TransactionDT IS NULL) AS valores_nulos,
  MIN(TransactionDT) AS minimo,
  MAX(TransactionDT) AS maximo,
  ROUND(AVG(TransactionDT), 2) AS media,
  APPROX_QUANTILES(TransactionDT, 4)[OFFSET(1)] AS q1,
  APPROX_QUANTILES(TransactionDT, 4)[OFFSET(2)] AS mediana,
  APPROX_QUANTILES(TransactionDT, 4)[OFFSET(3)] AS q3,
  COUNT(DISTINCT TransactionDT) AS valores_distintos
FROM `fraud-detection-eda.fraud_detection.transaction_raw`;