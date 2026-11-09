import sys
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

def main():
    # Initialize PySpark Session
    spark = SparkSession.builder \
        .appName("TFM_ETL_01_TemporalFeatures") \
        .getOrCreate()

    # Define GCS Input and Output Paths
    input_path = "gs://fraud-detection-imf/processed/joined_dataset.parquet"
    output_path = "gs://fraud-detection-imf/processed/step_01_temporal.parquet"

    print(f"Loading joined dataset from: {input_path}")
    df = spark.read.parquet(input_path)

    # -------------------------------------------------------------------------
    # Temporal Transformations on TransactionDT
    # TransactionDT represents a time delta in seconds from an arbitrary reference point.
    # Conversion metrics:
    #   - 1 Hour = 3,600 seconds
    #   - 1 Day  = 86,400 seconds (24 hours)
    #   - 1 Week = 604,800 seconds (7 days)
    # -------------------------------------------------------------------------

    print("Engineering cyclical and continuous temporal features...")
    df_transformed = df \
        .withColumn("DT_hour", (F.col("TransactionDT") / 3600) % 24) \
        .withColumn("DT_day_of_week", (F.col("TransactionDT") / 86400) % 7) \
        .withColumn("DT_day_continuous", (F.col("TransactionDT") / 86400))

    # Cast extracted features to Integer to optimize storage footprint
    df_transformed = df_transformed \
        .withColumn("DT_hour", F.col("DT_hour").cast("integer")) \
        .withColumn("DT_day_of_week", F.col("DT_day_of_week").cast("integer")) \
        .withColumn("DT_day_continuous", F.col("DT_day_continuous").cast("integer"))

    # Save the transformed dataset back to GCS in Parquet format
    print(f"Saving step 01 output to: {output_path}")
    df_transformed.write \
        .mode("overwrite") \
        .parquet(output_path)

    print("Phase 01 (Temporal Features) executed successfully.")
    spark.stop()

if __name__ == "__main__":
    main()