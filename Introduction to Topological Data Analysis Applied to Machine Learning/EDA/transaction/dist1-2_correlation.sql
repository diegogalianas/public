SELECT
  CORR(dist1, CAST(isFraud AS FLOAT64)) AS corr_dist1,
  CORR(dist2, CAST(isFraud AS FLOAT64)) AS corr_dist2
FROM `fraud-detection-eda.fraud_detection.transaction_raw`;