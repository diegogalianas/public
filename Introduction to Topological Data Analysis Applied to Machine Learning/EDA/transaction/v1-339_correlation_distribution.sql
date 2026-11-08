DECLARE sql_query STRING;

SET sql_query = (
  SELECT STRING_AGG(
    FORMAT("""
      SELECT
        '%s' AS variable,
        CORR(
          SAFE_CAST(`%s` AS FLOAT64),
          SAFE_CAST(isFraud AS FLOAT64)
        ) AS correlacion
      FROM `fraud-detection-eda.fraud_detection.transaction_raw`
    """, column_name, column_name),
    " UNION ALL "
  )
  FROM `fraud-detection-eda.fraud_detection.INFORMATION_SCHEMA.COLUMNS`
  WHERE REGEXP_CONTAINS(column_name, r'^V[0-9]+$')
);

EXECUTE IMMEDIATE FORMAT("""
  CREATE TEMP TABLE correlaciones_v AS
  %s
""", sql_query);

SELECT
  CASE
    WHEN ABS(correlacion) >= 0.20 THEN '1. >= 0.20'
    WHEN ABS(correlacion) >= 0.10 THEN '2. 0.10 - 0.20'
    WHEN ABS(correlacion) >= 0.05 THEN '3. 0.05 - 0.10'
    ELSE '4. < 0.05'
  END AS intervalo,
  COUNT(*) AS numero_variables,
  ROUND(100 * COUNT(*) / SUM(COUNT(*)) OVER(), 2) AS porcentaje
FROM correlaciones_v
GROUP BY intervalo
ORDER BY intervalo;