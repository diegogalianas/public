WITH all_tda AS (
  SELECT 'TRAIN' AS split, isFraud, dist_to_h1_loop_1, dist_to_h1_loop_2, dist_to_h1_loop_3, dist_to_h1_loop_4, dist_to_h1_loop_5
  FROM `fraud-detection-eda.fraud_detection.05_tda_train_view`
  UNION ALL
  SELECT 'TEST' AS split, isFraud, dist_to_h1_loop_1, dist_to_h1_loop_2, dist_to_h1_loop_3, dist_to_h1_loop_4, dist_to_h1_loop_5
  FROM `fraud-detection-eda.fraud_detection.05_tda_test_view`
)
SELECT
  split,
  isFraud,
  COUNT(*) AS total_rows,
  COUNTIF(dist_to_h1_loop_1 IS NULL) +
  COUNTIF(dist_to_h1_loop_2 IS NULL) +
  COUNTIF(dist_to_h1_loop_3 IS NULL) +
  COUNTIF(dist_to_h1_loop_4 IS NULL) +
  COUNTIF(dist_to_h1_loop_5 IS NULL) AS total_nulls,
  ROUND(MIN(dist_to_h1_loop_1), 3) AS min_1, ROUND(AVG(dist_to_h1_loop_1), 3) AS avg_1, ROUND(MAX(dist_to_h1_loop_1), 3) AS max_1,
  ROUND(MIN(dist_to_h1_loop_2), 3) AS min_2, ROUND(AVG(dist_to_h1_loop_2), 3) AS avg_2, ROUND(MAX(dist_to_h1_loop_2), 3) AS max_2,
  ROUND(MIN(dist_to_h1_loop_3), 3) AS min_3, ROUND(AVG(dist_to_h1_loop_3), 3) AS avg_3, ROUND(MAX(dist_to_h1_loop_3), 3) AS max_3,
  ROUND(MIN(dist_to_h1_loop_4), 3) AS min_4, ROUND(AVG(dist_to_h1_loop_4), 3) AS avg_4, ROUND(MAX(dist_to_h1_loop_4), 3) AS max_4,
  ROUND(MIN(dist_to_h1_loop_5), 3) AS min_5, ROUND(AVG(dist_to_h1_loop_5), 3) AS avg_5, ROUND(MAX(dist_to_h1_loop_5), 3) AS max_5
FROM all_tda
GROUP BY split, isFraud
ORDER BY split DESC, isFraud ASC;