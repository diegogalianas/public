SELECT 
    COUNT(*) AS total_records,
    ROUND(AVG(uid_amt_mean), 2) AS avg_user_mean_amt,
    ROUND(MAX(uid_amt_diff_mean), 2) AS max_positive_deviation,
    ROUND(MIN(uid_amt_diff_mean), 2) AS max_negative_deviation,
    ROUND(MAX(uid_amt_ratio_mean), 2) AS max_ratio_spike
FROM `fraud-detection-eda.fraud_detection.04_user_aggregations_view`;