import sys
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

def main():
    spark = SparkSession.builder \
        .appName("TFM_ETL_03_EmailFeatures") \
        .getOrCreate()

    # Define GCS Input and Output Paths
    input_path = "gs://fraud-detection-imf/processed/step_02_uid.parquet"
    output_path = "gs://fraud-detection-imf/processed/step_03_email.parquet"

    print(f"Loading input dataset from: {input_path}")
    df = spark.read.parquet(input_path)

    # -------------------------------------------------------------------------
    # Email Domain Cleaning and Parent Grouping
    # Map fragmented domain suffixes to parent corporate providers.
    # -------------------------------------------------------------------------
    print("Grouping email domains into parent providers...")

    def map_email_provider(col_name, new_col_name):
        return F.when(F.col(col_name).rlike("(?i)gmail|google"), "google") \
                .when(F.col(col_name).rlike("(?i)hotmail|outlook|live|msn"), "microsoft") \
                .when(F.col(col_name).rlike("(?i)yahoo|ymail"), "yahoo") \
                .when(F.col(col_name).rlike("(?i)icloud|me.com|mac.com"), "apple") \
                .when(F.col(col_name).rlike("(?i)aol|aim"), "aol") \
                .when(F.col(col_name).rlike("(?i)anonymous"), "anonymous") \
                .when(F.col(col_name).isNull(), "missing") \
                .otherwise("other")

    df_transformed = df \
        .withColumn("P_emaildomain_bin", map_email_provider("P_emaildomain", "P_emaildomain_bin")) \
        .withColumn("R_emaildomain_bin", map_email_provider("R_emaildomain", "R_emaildomain_bin"))

    # Flag domain matches (whether Purchaser and Recipient use the exact same domain)
    df_transformed = df_transformed.withColumn(
        "email_domain_match",
        F.when(
            (F.col("P_emaildomain").isNotNull()) & 
            (F.col("P_emaildomain") == F.col("R_emaildomain")), 
            1
        ).otherwise(0)
    )

    print(f"Saving step 03 output to: {output_path}")
    df_transformed.write \
        .mode("overwrite") \
        .parquet(output_path)

    print("Phase 03 (Email Domain Features) executed successfully.")
    spark.stop()

if __name__ == "__main__":
    main()