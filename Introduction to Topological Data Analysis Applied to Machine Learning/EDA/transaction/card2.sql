SELECT
  card2,
  COUNT(*) AS total_transacciones,
  COUNTIF(isFraud = 1) AS fraudes,
  ROUND(
    SAFE_DIVIDE(COUNTIF(isFraud = 1), COUNT(*)) * 100,
    3
  ) AS tasa_fraude
FROM `fraud-detection-eda.fraud_detection.transaction_raw`
GROUP BY card2
HAVING COUNT(*) >= 100
ORDER BY tasa_fraude DESC;