SELECT 
    COUNT(*) AS total_records,
    COUNT(DISTINCT card1) AS unique_card1,
    COUNT(DISTINCT addr1) AS unique_addr1
FROM `fraud-detection-eda.fraud_detection.01_temporal_view`;