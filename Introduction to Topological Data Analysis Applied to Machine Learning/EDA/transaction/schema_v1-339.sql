
DECLARE columnas STRING;
DECLARE consulta STRING;

-- Obtener dinámicamente las columnas V1-V339
SET columnas = (
  SELECT STRING_AGG(
    FORMAT(
      "STRUCT('%s' AS variable, SAFE_CAST(`%s` AS FLOAT64) AS valor)",
      column_name,
      column_name
    ),
    ", "
    ORDER BY ordinal_position
  )
  FROM `fraud-detection-eda.fraud_detection.INFORMATION_SCHEMA.COLUMNS`
  WHERE REGEXP_CONTAINS(column_name, r'^V[0-9]+$')
);

-- Generar el perfil estadístico de todas las variables
SET consulta = FORMAT("""
  WITH datos AS (
    SELECT
      v.variable,
      v.valor
    FROM `fraud-detection-eda.fraud_detection.transaction_raw`,
    UNNEST([%s]) AS v
  )

  SELECT
    variable,
    COUNT(*) AS registros_totales,
    COUNT(valor) AS registros_validos,
    COUNTIF(valor IS NULL) AS registros_nulos,
    ROUND(100 * SAFE_DIVIDE(COUNTIF(valor IS NULL), COUNT(*)), 2)
      AS porcentaje_nulos,
    COUNTIF(valor = 0) AS valores_cero,
    ROUND(100 * SAFE_DIVIDE(COUNTIF(valor = 0), COUNT(valor)), 2)
      AS porcentaje_ceros,
    APPROX_COUNT_DISTINCT(valor) AS cardinalidad_aproximada,
    MIN(valor) AS minimo,
    APPROX_QUANTILES(valor, 100)[OFFSET(25)] AS q1,
    APPROX_QUANTILES(valor, 100)[OFFSET(50)] AS mediana,
    APPROX_QUANTILES(valor, 100)[OFFSET(75)] AS q3,
    MAX(valor) AS maximo,
    AVG(valor) AS media,
    STDDEV(valor) AS desviacion_tipica

  FROM datos
  GROUP BY variable
  ORDER BY
    SAFE_CAST(REGEXP_EXTRACT(variable, r'[0-9]+') AS INT64)
""", columnas);

EXECUTE IMMEDIATE consulta;