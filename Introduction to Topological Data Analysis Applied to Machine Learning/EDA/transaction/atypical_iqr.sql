WITH datos AS (
    SELECT variable, valor
    FROM `fraud-detection-eda.fraud_detection.transaction_raw`
    CROSS JOIN UNNEST([
        STRUCT('TransactionAmt' AS variable, TransactionAmt AS valor),
        STRUCT('dist1', dist1),
        STRUCT('dist2', dist2),

        STRUCT('C1', C1), STRUCT('C2', C2),
        STRUCT('C3', C3), STRUCT('C4', C4),
        STRUCT('C5', C5), STRUCT('C6', C6),
        STRUCT('C7', C7), STRUCT('C8', C8),
        STRUCT('C9', C9), STRUCT('C10', C10),
        STRUCT('C11', C11), STRUCT('C12', C12),
        STRUCT('C13', C13), STRUCT('C14', C14),

        STRUCT('D1', D1), STRUCT('D2', D2),
        STRUCT('D3', D3), STRUCT('D4', D4),
        STRUCT('D5', D5), STRUCT('D6', D6),
        STRUCT('D7', D7), STRUCT('D8', D8),
        STRUCT('D9', D9), STRUCT('D10', D10),
        STRUCT('D11', D11), STRUCT('D12', D12),
        STRUCT('D13', D13), STRUCT('D14', D14),
        STRUCT('D15', D15)
    ])
    WHERE valor IS NOT NULL
),
cuartiles AS (
    SELECT
        variable,
        COUNT(*) AS registros_validos,
        MIN(valor) AS minimo,
        MAX(valor) AS maximo,
        APPROX_QUANTILES(valor, 100)[OFFSET(25)] AS q1,
        APPROX_QUANTILES(valor, 100)[OFFSET(75)] AS q3
    FROM datos
    GROUP BY variable
),
limites AS (
    SELECT
        *,
        q3 - q1 AS iqr,
        q1 - 1.5 * (q3 - q1) AS limite_inferior,
        q3 + 1.5 * (q3 - q1) AS limite_superior
    FROM cuartiles
),
resultados AS (
    SELECT
        l.*,
        COUNTIF(
            d.valor < l.limite_inferior
            OR d.valor > l.limite_superior
        ) AS numero_outliers
    FROM limites l
    JOIN datos d USING (variable)
    GROUP BY ALL
)
SELECT
    variable,
    registros_validos,
    minimo,
    q1,
    q3,
    maximo,
    iqr,
    limite_inferior,
    limite_superior,
    numero_outliers,
    ROUND(
        100 * SAFE_DIVIDE(numero_outliers, registros_validos), 2
    ) AS porcentaje_outliers
FROM resultados
ORDER BY porcentaje_outliers DESC;