SELECT
  'card3' AS variable,
  CAST(card3 AS STRING) AS categoria,
  COUNT(*) AS total_transacciones,
  COUNTIF(isFraud = 1) AS fraudes,
  ROUND(
    SAFE_DIVIDE(COUNTIF(isFraud = 1), COUNT(*)) * 100,
    3
  ) AS porcentaje_fraude
FROM `fraud-detection-eda.fraud_detection.transaction_raw`
GROUP BY card3

UNION ALL

SELECT
  'card4',
  CAST(card4 AS STRING),
  COUNT(*),
  COUNTIF(isFraud = 1),
  ROUND(SAFE_DIVIDE(COUNTIF(isFraud = 1), COUNT(*)) * 100, 3)
FROM `fraud-detection-eda.fraud_detection.transaction_raw`
GROUP BY card4

UNION ALL

SELECT
  'card5',
  CAST(card5 AS STRING),
  COUNT(*),
  COUNTIF(isFraud = 1),
  ROUND(SAFE_DIVIDE(COUNTIF(isFraud = 1), COUNT(*)) * 100, 3)
FROM `fraud-detection-eda.fraud_detection.transaction_raw`
GROUP BY card5

UNION ALL

SELECT
  'card6',
  CAST(card6 AS STRING),
  COUNT(*),
  COUNTIF(isFraud = 1),
  ROUND(SAFE_DIVIDE(COUNTIF(isFraud = 1), COUNT(*)) * 100, 3)
FROM `fraud-detection-eda.fraud_detection.transaction_raw`
GROUP BY card6

ORDER BY variable, total_transacciones DESC;