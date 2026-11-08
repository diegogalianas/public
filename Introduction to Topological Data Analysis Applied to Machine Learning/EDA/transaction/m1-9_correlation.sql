SELECT
  CORR(IF(M1 IS TRUE, 1.0, IF(M1 IS FALSE, 0.0, NULL)), CAST(isFraud AS FLOAT64)) AS corr_M1,
  CORR(IF(M2 IS TRUE, 1.0, IF(M2 IS FALSE, 0.0, NULL)), CAST(isFraud AS FLOAT64)) AS corr_M2,
  CORR(IF(M3 IS TRUE, 1.0, IF(M3 IS FALSE, 0.0, NULL)), CAST(isFraud AS FLOAT64)) AS corr_M3,
  CORR(IF(M4 = 'T', 1.0, IF(M4 = 'F', 0.0, NULL)), CAST(isFraud AS FLOAT64)) AS corr_M4,
  CORR(IF(M5 IS TRUE, 1.0, IF(M5 IS FALSE, 0.0, NULL)), CAST(isFraud AS FLOAT64)) AS corr_M5,
  CORR(IF(M6 IS TRUE, 1.0, IF(M6 IS FALSE, 0.0, NULL)), CAST(isFraud AS FLOAT64)) AS corr_M6,
  CORR(IF(M7 IS TRUE, 1.0, IF(M7 IS FALSE, 0.0, NULL)), CAST(isFraud AS FLOAT64)) AS corr_M7,
  CORR(IF(M8 IS TRUE, 1.0, IF(M8 IS FALSE, 0.0, NULL)), CAST(isFraud AS FLOAT64)) AS corr_M8,
  CORR(IF(M9 IS TRUE, 1.0, IF(M9 IS FALSE, 0.0, NULL)), CAST(isFraud AS FLOAT64)) AS corr_M9
FROM `fraud-detection-eda.fraud_detection.transaction_raw`;