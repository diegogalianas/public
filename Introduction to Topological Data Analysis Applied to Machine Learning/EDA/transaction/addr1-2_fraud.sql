SELECT
  variable,
  valor,
  COUNT(*) AS total_transacciones,
  COUNTIF(isFraud = 1) AS fraudes,
  ROUND(
    SAFE_DIVIDE(COUNTIF(isFraud = 1), COUNT(*)) * 100,
    3
  ) AS tasa_fraude
FROM `fraud-detection-eda.fraud_detection.transaction_raw`
CROSS JOIN UNNEST([
  STRUCT('addr1' AS variable, CAST(addr1 AS STRING) AS valor),
  STRUCT('addr2' AS variable, CAST(addr2 AS STRING) AS valor)
])
WHERE valor IS NOT NULL
GROUP BY variable, valor
HAVING COUNT(*) >= 100
ORDER BY variable, tasa_fraude DESC;