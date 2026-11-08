SELECT
  COUNT(*) AS total_transacciones,
  COUNTIF(isFraud = 1) AS fraudes,
  COUNT(DISTINCT card1) AS valores_distintos,
  ROUND(AVG(CAST(isFraud AS FLOAT64)) * 100, 3)
    AS tasa_fraude_global,
  ROUND(AVG(card1), 2) AS media,
  APPROX_QUANTILES(card1, 100)[OFFSET(25)] AS q1,
  APPROX_QUANTILES(card1, 100)[OFFSET(50)] AS mediana,
  APPROX_QUANTILES(card1, 100)[OFFSET(75)] AS q3
FROM `fraud-detection-eda.fraud_detection.transaction_raw`;