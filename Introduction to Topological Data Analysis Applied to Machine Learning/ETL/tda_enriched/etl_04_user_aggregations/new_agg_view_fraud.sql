SELECT 
    CASE 
        WHEN uid_amt_ratio_mean > 3.0 THEN '> 3x User Average (Extreme Spike)'
        WHEN uid_amt_ratio_mean BETWEEN 1.5 AND 3.0 THEN '1.5x - 3x User Average (Moderate Spike)'
        WHEN uid_amt_ratio_mean BETWEEN 0.8 AND 1.5 THEN 'Normal Range (~1x User Average)'
        ELSE '< 0.8x User Average (Below Usual)'
    END AS amount_deviation_bucket,
    COUNT(*) AS total_transactions,
    SUM(CAST(isFraud AS INT64)) AS fraud_count,
    ROUND(AVG(CAST(isFraud AS FLOAT64)) * 100, 2) AS fraud_rate_percentage
FROM `fraud-detection-eda.fraud_detection.04_user_aggregations_view`
GROUP BY amount_deviation_bucket
ORDER BY fraud_rate_percentage DESC;