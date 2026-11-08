SELECT
  COUNT(*) AS total_registros,

  COUNTIF(card1 IS NULL) AS card1_nulos,
  COUNT(DISTINCT card1) AS card1_distintos,

  COUNTIF(card2 IS NULL) AS card2_nulos,
  COUNT(DISTINCT card2) AS card2_distintos,

  COUNTIF(card3 IS NULL) AS card3_nulos,
  COUNT(DISTINCT card3) AS card3_distintos,

  COUNTIF(card4 IS NULL) AS card4_nulos,
  COUNT(DISTINCT card4) AS card4_distintos,

  COUNTIF(card5 IS NULL) AS card5_nulos,
  COUNT(DISTINCT card5) AS card5_distintos,

  COUNTIF(card6 IS NULL) AS card6_nulos,
  COUNT(DISTINCT card6) AS card6_distintos

FROM `fraud-detection-eda.fraud_detection.transaction_raw`;