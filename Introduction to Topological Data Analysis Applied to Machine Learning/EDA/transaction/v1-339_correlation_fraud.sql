DECLARE columnas STRING;

SET columnas = (
  SELECT STRING_AGG(
    FORMAT('V%d', numero),
    ', ' ORDER BY numero
  )
  FROM UNNEST(GENERATE_ARRAY(1, 339)) AS numero
);

EXECUTE IMMEDIATE FORMAT("""
  SELECT
    variable,
    CORR(valor, CAST(isFraud AS FLOAT64)) AS correlacion
  FROM `fraud-detection-eda.fraud_detection.transaction_raw`
  UNPIVOT (
    valor FOR variable IN (%s)
  )
  GROUP BY variable
  ORDER BY ABS(correlacion) DESC
""", columnas);