WITH datos AS (
    SELECT variable, valor
    FROM `fraud-detection-eda.fraud_detection.transaction_raw`
    CROSS JOIN UNNEST([
        STRUCT('card1' AS variable, CAST(card1 AS STRING) AS valor),
        STRUCT('card2', CAST(card2 AS STRING)),
        STRUCT('card3', CAST(card3 AS STRING)),
        STRUCT('card5', CAST(card5 AS STRING)),
        STRUCT('addr1', CAST(addr1 AS STRING)),
        STRUCT('addr2', CAST(addr2 AS STRING))
    ])
),
resumen AS (
    SELECT
        variable,
        COUNT(DISTINCT valor) AS valores_distintos,
        COUNTIF(valor IS NULL) AS valores_nulos,
        ROUND(
            100 * SAFE_DIVIDE(COUNTIF(valor IS NULL), COUNT(*)), 2
        ) AS porcentaje_nulos
    FROM datos
    GROUP BY variable
),
frecuencias AS (
    SELECT
        variable,
        valor,
        COUNT(*) AS frecuencia,
        ROW_NUMBER() OVER (
            PARTITION BY variable
            ORDER BY COUNT(*) DESC
        ) AS posicion
    FROM datos
    WHERE valor IS NOT NULL
    GROUP BY variable, valor
)
SELECT
    f.variable,
    r.valores_distintos,
    r.valores_nulos,
    r.porcentaje_nulos,
    f.valor AS categoria,
    f.frecuencia,
    ROUND(
        100 * SAFE_DIVIDE(f.frecuencia, 590540), 2
    ) AS porcentaje_total
FROM frecuencias f
JOIN resumen r USING (variable)
WHERE f.posicion <= 10
ORDER BY f.variable, f.posicion;