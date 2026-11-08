SELECT
  CORR(IF(M4 = 'M0', 1.0, 0.0), CAST(isFraud AS FLOAT64)) AS corr_M4_M0,
  CORR(IF(M4 = 'M1', 1.0, 0.0), CAST(isFraud AS FLOAT64)) AS corr_M4_M1,
  CORR(IF(M4 = 'M2', 1.0, 0.0), CAST(isFraud AS FLOAT64)) AS corr_M4_M2
FROM `fraud-detection-eda.fraud_detection.transaction_raw`;