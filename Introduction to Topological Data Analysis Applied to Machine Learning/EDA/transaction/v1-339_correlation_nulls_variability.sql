DECLARE sql_query STRING;

SET sql_query = (
  SELECT STRING_AGG(
    FORMAT("""
      SELECT
        '%s' AS variable,
        COUNT(*) AS total_registros,
        COUNTIF(`%s` IS NULL) AS valores_nulos,
        ROUND(
          100 * COUNTIF(`%s` IS NULL) / COUNT(*), 2
        ) AS porcentaje_nulos,
        COUNT(DISTINCT `%s`) AS valores_distintos,
        STDDEV_POP(`%s`) AS desviacion_estandar
      FROM `fraud-detection-eda.fraud_detection.transaction_raw`
    """,
    column_name,
    column_name,
    column_name,
    column_name,
    column_name
    ),
    " UNION ALL "
  )
  FROM `fraud-detection-eda.fraud_detection.INFORMATION_SCHEMA.COLUMNS`
  WHERE REGEXP_CONTAINS(column_name, r'^V[0-9]+$')
);

EXECUTE IMMEDIATE FORMAT("""
  CREATE TEMP TABLE estadisticas_v AS
  %s
""", sql_query);

SELECT *
FROM estadisticas_v
ORDER BY porcentaje_nulos DESC, desviacion_estandar ASC;