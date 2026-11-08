SELECT
  CORR(D1, CAST(isFraud AS FLOAT64)) AS corr_D1,
  CORR(D2, CAST(isFraud AS FLOAT64)) AS corr_D2,
  CORR(D3, CAST(isFraud AS FLOAT64)) AS corr_D3,
  CORR(D4, CAST(isFraud AS FLOAT64)) AS corr_D4,
  CORR(D5, CAST(isFraud AS FLOAT64)) AS corr_D5,
  CORR(D6, CAST(isFraud AS FLOAT64)) AS corr_D6,
  CORR(D7, CAST(isFraud AS FLOAT64)) AS corr_D7,
  CORR(D8, CAST(isFraud AS FLOAT64)) AS corr_D8,
  CORR(D9, CAST(isFraud AS FLOAT64)) AS corr_D9,
  CORR(D10, CAST(isFraud AS FLOAT64)) AS corr_D10,
  CORR(D11, CAST(isFraud AS FLOAT64)) AS corr_D11,
  CORR(D12, CAST(isFraud AS FLOAT64)) AS corr_D12,
  CORR(D13, CAST(isFraud AS FLOAT64)) AS corr_D13,
  CORR(D14, CAST(isFraud AS FLOAT64)) AS corr_D14,
  CORR(D15, CAST(isFraud AS FLOAT64)) AS corr_D15
FROM `fraud-detection-eda.fraud_detection.transaction_raw`;