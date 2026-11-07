DECLARE null_profile_sql STRING;

SET null_profile_sql = (
  SELECT STRING_AGG(
    FORMAT("""
      SELECT
        '%s' AS variable,
        COUNTIF(`%s` IS NULL) AS nulos,
        COUNT(*) AS total,
        ROUND(
          SAFE_DIVIDE(COUNTIF(`%s` IS NULL), COUNT(*)) * 100,
          2
        ) AS porcentaje_nulos
      FROM `fraud-detection-eda.fraud_detection.identity_raw`
    """, column_name, column_name, column_name),
    " UNION ALL "
  )
  FROM `fraud-detection-eda.fraud_detection.INFORMATION_SCHEMA.COLUMNS`
  WHERE table_name = 'identity_raw'
);

EXECUTE IMMEDIATE
  null_profile_sql || ' ORDER BY porcentaje_nulos DESC';