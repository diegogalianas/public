SELECT
  DIV(CAST(TransactionDT AS INT64), 86400) AS dia_relativo,
  COUNT(*) AS total_transacciones,
  COUNTIF(isFraud = 1) AS fraudes,
  ROUND(
    SAFE_DIVIDE(COUNTIF(isFraud = 1), COUNT(*)) * 100,
    3
  ) AS porcentaje_fraude
FROM `fraud-detection-eda.fraud_detection.transaction_raw`
GROUP BY dia_relativo
ORDER BY dia_relativo;