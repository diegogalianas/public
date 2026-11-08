SELECT 
    CASE 
        WHEN UID_card_addr_fq = 1 THEN '1 Transaction (Single-use)'
        WHEN UID_card_addr_fq BETWEEN 2 AND 5 THEN '2-5 Transactions'
        WHEN UID_card_addr_fq BETWEEN 6 AND 20 THEN '6-20 Transactions'
        ELSE '> 20 Transactions (High Volume)'
    END AS user_activity_bucket,
    COUNT(*) AS total_transactions,
    SUM(CAST(isFraud AS INT64)) AS fraud_count,
    ROUND(AVG(CAST(isFraud AS FLOAT64)) * 100, 2) AS fraud_rate_percentage
FROM `fraud-detection-eda.fraud_detection.02_uid_view`
GROUP BY user_activity_bucket
ORDER BY fraud_rate_percentage DESC;