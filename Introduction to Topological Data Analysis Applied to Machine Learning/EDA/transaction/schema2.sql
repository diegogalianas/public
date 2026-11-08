SELECT
  data_type,
  COUNT(*) AS total_variables,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS percentage
FROM
  `fraud-detection-eda.fraud_detection.INFORMATION_SCHEMA.COLUMNS`
WHERE
  table_name = 'transaction_raw'
GROUP BY
  data_type
ORDER BY
  total_variables DESC;