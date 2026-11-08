WITH datos AS (
    SELECT variable, valor
    FROM `fraud-detection-eda.fraud_detection.transaction_raw`
    CROSS JOIN UNNEST([
        STRUCT('ProductCD' AS variable, IFNULL(CAST(ProductCD AS STRING), 'NULL') AS valor),
        STRUCT('card4', IFNULL(CAST(card4 AS STRING), 'NULL')),
        STRUCT('card6', IFNULL(CAST(card6 AS STRING), 'NULL')),
        STRUCT('P_emaildomain', IFNULL(CAST(P_emaildomain AS STRING), 'NULL')),
        STRUCT('R_emaildomain', IFNULL(CAST(R_emaildomain AS STRING), 'NULL')),
        STRUCT('M1', IFNULL(CAST(M1 AS STRING), 'NULL')),
        STRUCT('M2', IFNULL(CAST(M2 AS STRING), 'NULL')),
        STRUCT('M3', IFNULL(CAST(M3 AS STRING), 'NULL')),
        STRUCT('M4', IFNULL(CAST(M4 AS STRING), 'NULL')),
        STRUCT('M5', IFNULL(CAST(M5 AS STRING), 'NULL')),
        STRUCT('M6', IFNULL(CAST(M6 AS STRING), 'NULL')),
        STRUCT('M7', IFNULL(CAST(M7 AS STRING), 'NULL')),
        STRUCT('M8', IFNULL(CAST(M8 AS STRING), 'NULL')),
        STRUCT('M9', IFNULL(CAST(M9 AS STRING), 'NULL')),
        STRUCT('isFraud', CAST(isFraud AS STRING))
    ])
),
frecuencias AS (
    SELECT
        variable,
        valor,
        COUNT(*) AS frecuencia
    FROM datos
    GROUP BY variable, valor
)
SELECT
    variable,
    valor,
    frecuencia,
    ROUND(
        100 * SAFE_DIVIDE(
            frecuencia,
            SUM(frecuencia) OVER (PARTITION BY variable)
        ), 2
    ) AS porcentaje
FROM frecuencias
ORDER BY variable, frecuencia DESC;