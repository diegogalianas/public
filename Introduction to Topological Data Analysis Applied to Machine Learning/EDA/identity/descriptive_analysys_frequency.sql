WITH valores AS (
  SELECT 'id_03' AS variable, CAST(id_03 AS STRING) AS valor
  FROM `fraud-detection-eda.fraud_detection.identity_raw`
  WHERE id_03 IS NOT NULL

  UNION ALL

  SELECT 'id_04', CAST(id_04 AS STRING)
  FROM `fraud-detection-eda.fraud_detection.identity_raw`
  WHERE id_04 IS NOT NULL

  UNION ALL

  SELECT 'id_09', CAST(id_09 AS STRING)
  FROM `fraud-detection-eda.fraud_detection.identity_raw`
  WHERE id_09 IS NOT NULL

  UNION ALL

  SELECT 'id_10', CAST(id_10 AS STRING)
  FROM `fraud-detection-eda.fraud_detection.identity_raw`
  WHERE id_10 IS NOT NULL

  UNION ALL

  SELECT 'id_11', CAST(id_11 AS STRING)
  FROM `fraud-detection-eda.fraud_detection.identity_raw`
  WHERE id_11 IS NOT NULL

  UNION ALL

  SELECT 'id_13', CAST(id_13 AS STRING)
  FROM `fraud-detection-eda.fraud_detection.identity_raw`
  WHERE id_13 IS NOT NULL
),
frecuencias AS (
  SELECT
    variable,
    valor,
    COUNT(*) AS frecuencia
  FROM valores
  GROUP BY variable, valor
)
SELECT
  variable,
  valor,
  frecuencia,
  ROUND(
    100 * frecuencia / SUM(frecuencia) OVER (PARTITION BY variable),
    2
  ) AS porcentaje
FROM frecuencias
QUALIFY ROW_NUMBER() OVER (
  PARTITION BY variable
  ORDER BY frecuencia DESC
) <= 10
ORDER BY variable, frecuencia DESC;