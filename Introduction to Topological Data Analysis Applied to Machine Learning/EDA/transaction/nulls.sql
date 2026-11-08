DECLARE columnas STRING;

SET columnas = (
    SELECT STRING_AGG(
        FORMAT(
            """
            SELECT
                '%s' AS variable,
                COUNTIF(`%s` IS NULL) AS valores_nulos,
                COUNTIF(`%s` IS NOT NULL) AS valores_no_nulos,
                ROUND(
                    SAFE_DIVIDE(
                        COUNTIF(`%s` IS NULL),
                        COUNT(*)
                    ) * 100,
                    2
                ) AS porcentaje_nulos
            FROM `fraud-detection-eda.fraud_detection.transaction_raw`
            """,
            column_name,
            column_name,
            column_name,
            column_name
        ),
        ' UNION ALL '
    )
    FROM `fraud-detection-eda.fraud_detection.INFORMATION_SCHEMA.COLUMNS`
    WHERE table_name = 'transaction_raw'
);

EXECUTE IMMEDIATE FORMAT(
    """
    %s
    ORDER BY porcentaje_nulos DESC, variable
    """,
    columnas
);