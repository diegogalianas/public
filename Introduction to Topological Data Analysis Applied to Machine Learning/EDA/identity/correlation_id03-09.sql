SELECT
  COUNT(*) AS observaciones_totales,

  COUNTIF(id_03 = 0 AND id_09 = 0)
    AS ambos_cero,

  COUNTIF(id_03 = 0 AND id_09 != 0)
    AS solo_id_03_cero,

  COUNTIF(id_03 != 0 AND id_09 = 0)
    AS solo_id_09_cero,

  COUNTIF(id_03 != 0 AND id_09 != 0)
    AS ninguno_cero,

  ROUND(CORR(id_03, id_09), 4)
    AS correlacion_total,

  ROUND(
    CORR(
      IF(id_03 != 0 AND id_09 != 0, id_03, NULL),
      IF(id_03 != 0 AND id_09 != 0, id_09, NULL)
    ), 4
  ) AS correlacion_sin_ceros

FROM `fraud-detection-eda.fraud_detection.identity_raw`
WHERE id_03 IS NOT NULL
  AND id_09 IS NOT NULL;