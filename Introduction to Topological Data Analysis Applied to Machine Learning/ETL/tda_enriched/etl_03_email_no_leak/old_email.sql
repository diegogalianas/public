SELECT 
    COUNT(*) AS total_records,
    COUNT(DISTINCT P_emaildomain) AS raw_P_email_unique_domains,
    COUNT(DISTINCT R_emaildomain) AS raw_R_email_unique_domains,
    COUNTIF(P_emaildomain IS NULL) AS null_P_email_count,
    COUNTIF(R_emaildomain IS NULL) AS null_R_email_count
FROM `fraud-detection-eda.fraud_detection.02_uid_view`;