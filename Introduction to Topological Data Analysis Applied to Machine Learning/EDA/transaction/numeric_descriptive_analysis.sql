DECLARE columnas STRING;

SET columnas = (
    SELECT STRING_AGG(
        FORMAT(
            """
            SELECT
                '%s' AS variable,
                COUNT(`%s`) AS valores_validos,
                COUNTIF(`%s` IS NULL) AS valores_nulos,
                MIN(`%s`) AS minimo,
                MAX(`%s`) AS maximo,
                AVG(`%s`) AS media,
                STDDEV(`%s`) AS desviacion_tipica,
                APPROX_QUANTILES(`%s`, 100)[OFFSET(25)] AS q1,
                APPROX_QUANTILES(`%s`, 100)[OFFSET(50)] AS mediana,
                APPROX_QUANTILES(`%s`, 100)[OFFSET(75)] AS q3
            FROM `fraud-detection-eda.fraud_detection.transaction_raw`
            """,
            column_name,
            column_name,
            column_name,
            column_name,
            column_name,
            column_name,
            column_name,
            column_name,
            column_name,
            column_name
        ),
        ' UNION ALL '
    )
    FROM `fraud-detection-eda.fraud_detection.INFORMATION_SCHEMA.COLUMNS`
    WHERE table_name = 'transaction_raw'
      AND data_type IN ('FLOAT64', 'INT64')
      AND column_name NOT IN (
          'TransactionID',
          'isFraud',
          'card1',
          'card2',
          'card3',
          'card5',
          'addr1',
          'addr2'
      )
);

EXECUTE IMMEDIATE FORMAT(
    """
    %s
    ORDER BY variable
    """,
    columnas
);