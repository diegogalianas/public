DECLARE query_sql STRING;

SET query_sql = (
  SELECT STRING_AGG(
    FORMAT("""
      SELECT
        '%s' AS variable,
        CAST(`%s` AS STRING) AS valor,
        COUNT(*) AS frecuencia,
        ROUND(
          COUNT(*) * 100.0 /
          SUM(COUNT(*)) OVER (),
          2
        ) AS porcentaje
      FROM `fraud-detection-eda.fraud_detection.identity_raw`
      WHERE `%s` IS NOT NULL
      GROUP BY `%s`
    """,
      column_name,
      column_name,
      column_name,
      column_name
    ),
    ' UNION ALL '
  )
  FROM `fraud-detection-eda.fraud_detection.INFORMATION_SCHEMA.COLUMNS`
  WHERE table_name = 'identity_raw'
    AND (
      data_type = 'BOOL'
      OR column_name IN (
        'id_12',
        'id_15',
        'id_16',
        'id_23',
        'id_27',
        'id_28',
        'id_29',
        'DeviceType'
      )
    )
);

EXECUTE IMMEDIATE query_sql;