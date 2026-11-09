SELECT 
    COUNT(*) AS total_records,
    COUNT(DISTINCT UID_card_addr) AS total_unique_virtual_users,
    MIN(UID_card_addr_fq) AS min_user_transactions,
    MAX(UID_card_addr_fq) AS max_user_transactions,
    ROUND(AVG(UID_card_addr_fq), 2) AS avg_transactions_per_user
FROM `fraud-detection-eda.fraud_detection.02_uid_view`;