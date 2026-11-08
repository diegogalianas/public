DECLARE query STRING;

SET query = (
  SELECT STRING_AGG(
    FORMAT("""
      SELECT
        '%s' AS variable,

        COUNTIF(`%s` IS NULL) AS registros_nulos,
        COUNTIF(`%s` IS NOT NULL) AS registros_disponibles,

        SAFE_DIVIDE(
          COUNTIF(`%s` IS NULL AND isFraud = 1),
          COUNTIF(`%s` IS NULL)
        ) * 100 AS tasa_fraude_nulos,

        SAFE_DIVIDE(
          COUNTIF(`%s` IS NOT NULL AND isFraud = 1),
          COUNTIF(`%s` IS NOT NULL)
        ) * 100 AS tasa_fraude_disponibles,

        (
          SAFE_DIVIDE(
            COUNTIF(`%s` IS NULL AND isFraud = 1),
            COUNTIF(`%s` IS NULL)
          ) -
          SAFE_DIVIDE(
            COUNTIF(`%s` IS NOT NULL AND isFraud = 1),
            COUNTIF(`%s` IS NOT NULL)
          )
        ) * 100 AS diferencia_puntos_porcentuales

      FROM `fraud-detection-eda.fraud_detection.transaction_raw`
    """,
      column_name,
      column_name, column_name,
      column_name, column_name,
      column_name, column_name,
      column_name, column_name,
      column_name, column_name
    ),
    ' UNION ALL '
  )
  FROM `fraud-detection-eda.fraud_detection.INFORMATION_SCHEMA.COLUMNS`
  WHERE STARTS_WITH(column_name, 'V')
);

EXECUTE IMMEDIATE query;