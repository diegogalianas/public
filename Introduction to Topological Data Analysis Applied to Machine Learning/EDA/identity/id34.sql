SELECT
  id_34 AS valor,
  COUNT(*) AS frecuencia,
  ROUND(
    COUNT(*) * 100 / SUM(COUNT(*)) OVER (),
    2
  ) AS porcentaje
FROM `fraud-detection-eda.fraud_detection.identity_raw`
WHERE id_34 IS NOT NULL
GROUP BY id_34
ORDER BY frecuencia DESC;