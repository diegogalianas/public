DECLARE query_sql STRING;

SET query_sql = (
  SELECT STRING_AGG(
    FORMAT("""
      SELECT
        '%s' AS variable,
        COUNT(`%s`) AS valores_no_nulos,
        AVG(`%s`) AS media,
        STDDEV(`%s`) AS desviacion_estandar,
        MIN(`%s`) AS minimo,
        APPROX_QUANTILES(`%s`, 100)[OFFSET(25)] AS q1,
        APPROX_QUANTILES(`%s`, 100)[OFFSET(50)] AS mediana,
        APPROX_QUANTILES(`%s`, 100)[OFFSET(75)] AS q3,
        MAX(`%s`) AS maximo
      FROM `fraud-detection-eda.fraud_detection.identity_raw`
    """,
      column_name, column_name, column_name,
      column_name, column_name, column_name,
      column_name, column_name, column_name
    ),
    ' UNION ALL '
  )
  FROM `fraud-detection-eda.fraud_detection.INFORMATION_SCHEMA.COLUMNS`
  WHERE table_name = 'identity_raw'
    AND data_type = 'FLOAT64'
);

EXECUTE IMMEDIATE query_sql;