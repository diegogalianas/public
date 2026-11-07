DECLARE query_sql STRING;

SET query_sql = (
  SELECT STRING_AGG(
    FORMAT("""
      SELECT
        '%s' AS variable,
        '%s' AS tipo_dato,
        COUNT(DISTINCT `%s`) AS valores_distintos,
        COUNTIF(`%s` IS NULL) AS valores_nulos,
        ROUND(
          SAFE_DIVIDE(
            COUNT(DISTINCT `%s`),
            COUNT(`%s`)
          ) * 100, 2
        ) AS porcentaje_distintos
      FROM `fraud-detection-eda.fraud_detection.identity_raw`
    """,
      column_name,
      data_type,
      column_name,
      column_name,
      column_name,
      column_name
    ),
    ' UNION ALL '
  )
  FROM `fraud-detection-eda.fraud_detection.INFORMATION_SCHEMA.COLUMNS`
  WHERE table_name = 'identity_raw'
    AND column_name != 'TransactionID'
);

EXECUTE IMMEDIATE query_sql;