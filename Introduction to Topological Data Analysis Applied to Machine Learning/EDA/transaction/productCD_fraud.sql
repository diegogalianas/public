SELECT
  ProductCD,
  COUNT(*) AS total_transacciones,
  COUNTIF(isFraud = 1) AS fraudes,
  ROUND(
    SAFE_DIVIDE(COUNTIF(isFraud = 1), COUNT(*)) * 100,
    3
  ) AS porcentaje_fraude
FROM `fraud-detection-eda.fraud_detection.transaction_raw`
GROUP BY ProductCD
ORDER BY total_transacciones DESC;