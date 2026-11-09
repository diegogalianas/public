WITH stats AS (
  SELECT
    COUNT(*) AS total_rows,
    -- Nulos
    COUNTIF(dist_to_h1_loop_1 IS NULL) AS nulls_loop_1,
    COUNTIF(dist_to_h1_loop_2 IS NULL) AS nulls_loop_2,
    COUNTIF(dist_to_h1_loop_3 IS NULL) AS nulls_loop_3,
    COUNTIF(dist_to_h1_loop_4 IS NULL) AS nulls_loop_4,
    COUNTIF(dist_to_h1_loop_5 IS NULL) AS nulls_loop_5,
    -- Loop 1
    MIN(dist_to_h1_loop_1) AS min_1, AVG(dist_to_h1_loop_1) AS avg_1, MAX(dist_to_h1_loop_1) AS max_1,
    -- Loop 2
    MIN(dist_to_h1_loop_2) AS min_2, AVG(dist_to_h1_loop_2) AS avg_2, MAX(dist_to_h1_loop_2) AS max_2,
    -- Loop 3
    MIN(dist_to_h1_loop_3) AS min_3, AVG(dist_to_h1_loop_3) AS avg_3, MAX(dist_to_h1_loop_3) AS max_3,
    -- Loop 4
    MIN(dist_to_h1_loop_4) AS min_4, AVG(dist_to_h1_loop_4) AS avg_4, MAX(dist_to_h1_loop_4) AS max_4,
    -- Loop 5
    MIN(dist_to_h1_loop_5) AS min_5, AVG(dist_to_h1_loop_5) AS avg_5, MAX(dist_to_h1_loop_5) AS max_5
  FROM `fraud-detection-eda.fraud_detection.05_tda_view`
)
SELECT * FROM stats;