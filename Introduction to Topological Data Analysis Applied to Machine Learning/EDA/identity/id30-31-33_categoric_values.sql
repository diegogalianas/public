WITH valores AS (
  SELECT 'DeviceInfo' AS variable, DeviceInfo AS valor
  FROM `fraud-detection-eda.fraud_detection.identity_raw`
  WHERE DeviceInfo IS NOT NULL

  UNION ALL

  SELECT 'id_33', id_33
  FROM `fraud-detection-eda.fraud_detection.identity_raw`
  WHERE id_33 IS NOT NULL

  UNION ALL

  SELECT 'id_31', id_31
  FROM `fraud-detection-eda.fraud_detection.identity_raw`
  WHERE id_31 IS NOT NULL

  UNION ALL

  SELECT 'id_30', id_30
  FROM `fraud-detection-eda.fraud_detection.identity_raw`
  WHERE id_30 IS NOT NULL
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
    100 * frecuencia /
    SUM(frecuencia) OVER (PARTITION BY variable),
    2
  ) AS porcentaje
FROM frecuencias
QUALIFY ROW_NUMBER() OVER (
  PARTITION BY variable
  ORDER BY frecuencia DESC
) <= 15
ORDER BY variable, frecuencia DESC;