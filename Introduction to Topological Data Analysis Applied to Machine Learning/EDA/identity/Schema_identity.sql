SELECT
  ordinal_position,
  column_name,
  data_type,
  is_nullable
FROM
  `TU_PROYECTO.fraud_detection.INFORMATION_SCHEMA.COLUMNS`
WHERE
  table_name = 'identity_raw'
ORDER BY
  ordinal_position;