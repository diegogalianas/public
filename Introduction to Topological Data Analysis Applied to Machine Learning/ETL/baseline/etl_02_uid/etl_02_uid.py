import sys
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

def main():
    # Initialize PySpark Session
    spark = SparkSession.builder \
        .appName("TFM_ETL_02_UIDFeatures") \
        .getOrCreate()

    # Define GCS Input and Output Paths
    input_path = "gs://fraud-detection-imf/processed/step_01_temporal.parquet"
    output_path = "gs://fraud-detection-imf/processed/step_02_uid.parquet"

    print(f"Loading input dataset from: {input_path}")
    df = spark.read.parquet(input_path)

    # -------------------------------------------------------------------------
    # 1. Virtual User ID Construction
    # Concatenate static card features (card1 through card6) and billing address (addr1).
    # Handle NULL values explicitly using coalesce to prevent string truncation.
    # -------------------------------------------------------------------------
    print("Synthesizing Virtual User IDs (UID_card_addr)...")

    def clean_col(c):
        return F.coalesce(F.col(c).cast("string"), F.lit("NA"))

    df_transformed = df.withColumn(
        "UID_card_addr",
        F.concat_ws(
            "_",
            clean_col("card1"),
            clean_col("card2"),
            clean_col("card3"),
            clean_col("card4"),
            clean_col("card5"),
            clean_col("card6"),
            clean_col("addr1")
        )
    )

    # -------------------------------------------------------------------------
    # 2. Frequency Encoding for the Virtual User ID
    # Count the total number of transactions associated with each synthetic user.
    # -------------------------------------------------------------------------
    print("Calculating Virtual User ID frequency encoding...")
    uid_counts = df_transformed.groupBy("UID_card_addr") \
        .count() \
        .withColumnRenamed("count", "UID_card_addr_fq")

    # Join the frequency count back to the main DataFrame
    df_transformed = df_transformed.join(uid_counts, on="UID_card_addr", how="left")

    # -------------------------------------------------------------------------
    # 3. Save Output Data
    # -------------------------------------------------------------------------
    print(f"Saving step 02 output to: {output_path}")
    df_transformed.write \
        .mode("overwrite") \
        .parquet(output_path)

    print("Phase 02 (Virtual User ID Features) executed successfully.")
    spark.stop()

if __name__ == "__main__":
    main()