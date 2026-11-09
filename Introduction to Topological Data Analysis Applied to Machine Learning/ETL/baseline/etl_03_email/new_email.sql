SELECT 
    COUNT(*) AS total_records,
    COUNT(DISTINCT P_emaildomain_bin) AS mapped_P_email_providers,
    COUNT(DISTINCT R_emaildomain_bin) AS mapped_R_email_providers,
    SUM(email_domain_match) AS exact_domain_matches_count
FROM `fraud-detection-eda.fraud_detection.03_email_view`;