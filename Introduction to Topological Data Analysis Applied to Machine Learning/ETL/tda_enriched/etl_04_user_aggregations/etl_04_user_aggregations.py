import sys
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

def main():
    spark = SparkSession.builder \
        .appName("TFM_ETL_04_UserAggregations") \
        .getOrCreate()

    # Define GCS Input and Output Paths
    input_path = "gs://fraud-detection-imf/processed/step_03_email.parquet"
    output_path = "gs://fraud-detection-imf/processed/step_04_agg.parquet"

    print(f"Loading input dataset from: {input_path}")
    df = spark.read.parquet(input_path)

    # -------------------------------------------------------------------------
    # Aggregations over Virtual User ID (UID_card_addr)
    # Calculate historical spending patterns per virtual user profile.
    # -------------------------------------------------------------------------
    print("Computing user-level aggregations on TransactionAmt...")

    # Group by Virtual User ID to calculate global stats per user
    user_stats = df.groupBy("UID_card_addr").agg(
        F.avg("TransactionAmt").alias("uid_amt_mean"),
        F.stddev("TransactionAmt").alias("uid_amt_std"),
        F.min("TransactionAmt").alias("uid_amt_min"),
        F.max("TransactionAmt").alias("uid_amt_max")
    )

    # Replace null stddev (users with only 1 transaction) with 0.0
    user_stats = user_stats.fillna({"uid_amt_std": 0.0})

    # Join metrics back to the main DataFrame
    df_transformed = df.join(user_stats, on="UID_card_addr", how="left")

    # -------------------------------------------------------------------------
    # Relative Deviation Features
    # Measure how much current transaction deviates from user's historical average
    # -------------------------------------------------------------------------
    print("Engineering relative amount deviation features...")

    df_transformed = df_transformed \
        .withColumn("uid_amt_diff_mean", F.col("TransactionAmt") - F.col("uid_amt_mean")) \
        .withColumn("uid_amt_ratio_mean", F.col("TransactionAmt") / (F.col("uid_amt_mean") + 1e-5))

    print(f"Saving step 04 output to: {output_path}")
    df_transformed.write \
        .mode("overwrite") \
        .parquet(output_path)

    print("Phase 04 (User Aggregation Features) executed successfully.")
    spark.stop()

if __name__ == "__main__":
    main()