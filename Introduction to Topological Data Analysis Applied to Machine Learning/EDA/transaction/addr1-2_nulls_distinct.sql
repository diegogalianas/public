SELECT
  variable,
  COUNT(*) AS total_transacciones,
  COUNTIF(valor IS NULL) AS valores_nulos,
  COUNT(DISTINCT valor) AS valores_distintos,
  ROUND(
    SAFE_DIVIDE(COUNTIF(valor IS NULL), COUNT(*)) * 100,
    3
  ) AS porcentaje_nulos
FROM `fraud-detection-eda.fraud_detection.transaction_raw`
CROSS JOIN UNNEST([
  STRUCT('addr1' AS variable, CAST(addr1 AS STRING) AS valor),
  STRUCT('addr2' AS variable, CAST(addr2 AS STRING) AS valor)
])
GROUP BY variable
ORDER BY variable;