SELECT
  CORR(TransactionAmt, CAST(isFraud AS FLOAT64)) AS corr_TransactionAmt,
  CORR(TransactionDT, CAST(isFraud AS FLOAT64)) AS corr_TransactionDT,

  CORR(C1, CAST(isFraud AS FLOAT64)) AS corr_C1,
  CORR(C2, CAST(isFraud AS FLOAT64)) AS corr_C2,
  CORR(C3, CAST(isFraud AS FLOAT64)) AS corr_C3,
  CORR(C4, CAST(isFraud AS FLOAT64)) AS corr_C4,
  CORR(C5, CAST(isFraud AS FLOAT64)) AS corr_C5,
  CORR(C6, CAST(isFraud AS FLOAT64)) AS corr_C6,
  CORR(C7, CAST(isFraud AS FLOAT64)) AS corr_C7,
  CORR(C8, CAST(isFraud AS FLOAT64)) AS corr_C8,
  CORR(C9, CAST(isFraud AS FLOAT64)) AS corr_C9,
  CORR(C10, CAST(isFraud AS FLOAT64)) AS corr_C10,
  CORR(C11, CAST(isFraud AS FLOAT64)) AS corr_C11,
  CORR(C12, CAST(isFraud AS FLOAT64)) AS corr_C12,
  CORR(C13, CAST(isFraud AS FLOAT64)) AS corr_C13,
  CORR(C14, CAST(isFraud AS FLOAT64)) AS corr_C14

FROM `fraud-detection-eda.fraud_detection.transaction_raw`;