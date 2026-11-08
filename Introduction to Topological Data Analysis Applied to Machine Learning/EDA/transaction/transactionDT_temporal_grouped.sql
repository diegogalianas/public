SELECT
  DIV(CAST(TransactionDT AS INT64), 86400) AS dia_relativo,
  COUNT(*) AS numero_transacciones,
  ROUND(AVG(TransactionAmt), 2) AS importe_medio
FROM `fraud-detection-eda.fraud_detection.transaction_raw`
WHERE TransactionDT IS NOT NULL
GROUP BY dia_relativo
ORDER BY dia_relativo;