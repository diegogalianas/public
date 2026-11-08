WITH domains AS (
  SELECT
    'P_emaildomain' AS variable,
    P_emaildomain AS dominio,
    isFraud
  FROM `fraud-detection-eda.fraud_detection.transaction_raw`

  UNION ALL

  SELECT
    'R_emaildomain' AS variable,
    R_emaildomain AS dominio,
    isFraud
  FROM `fraud-detection-eda.fraud_detection.transaction_raw`
)

SELECT
  variable,
  COALESCE(dominio, 'NULL') AS dominio,
  COUNT(*) AS total_transacciones,
  SUM(isFraud) AS transacciones_fraudulentas,
  ROUND(
    SAFE_DIVIDE(SUM(isFraud), COUNT(*)) * 100,
    3
  ) AS tasa_fraude
FROM domains
GROUP BY variable, dominio
ORDER BY variable, total_transacciones DESC;