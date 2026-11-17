import sys
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

def main():
    spark = SparkSession.builder \
        .appName("TFM_ETL_04_UserAggregations") \
        .getOrCreate()

    # Define GCS Input and Output Paths
    input_path = "gs://fraud-detection-imf/processed_tda/step_03_email.parquet"
    output_path = "gs://fraud-detection-imf/processed_tda/step_04_agg.parquet"

    print(f"Loading input dataset from: {input_path}")
    df = spark.read.parquet(input_path)

    # -------------------------------------------------------------------------
    # Aggregations over Virtual User ID (UID_card_addr) - Zero Leakage Window
    # Calculate historical rolling spending patterns per virtual user profile,
    # strictly restricting the window to past transactions (-1 row max).
    # -------------------------------------------------------------------------
    print("Computing historical rolling user-level aggregations on TransactionAmt...")

    past_window = (
        Window.partitionBy("UID_card_addr")
        .orderBy("TransactionDT")
        .rowsBetween(Window.unboundedPreceding, -1)
    )

    df_transformed = df \
        .withColumn("uid_amt_mean", F.avg("TransactionAmt").over(past_window)) \
        .withColumn("uid_amt_std", F.stddev("TransactionAmt").over(past_window)) \
        .withColumn("uid_amt_min", F.min("TransactionAmt").over(past_window)) \
        .withColumn("uid_amt_max", F.max("TransactionAmt").over(past_window))

    # Replace null stddev and stats (e.g., first transaction of a user with no prior history) with 0.0 or safe defaults
    df_transformed = df_transformed.fillna({
        "uid_amt_std": 0.0,
        "uid_amt_mean": 0.0,
        "uid_amt_min": 0.0,
        "uid_amt_max": 0.0
    })

    # -------------------------------------------------------------------------
    # Relative Deviation Features
    # Measure how much current transaction deviates from user's historical past average
    # -------------------------------------------------------------------------
    print("Engineering relative amount deviation features...")

    df_transformed = df_transformed \
        .withColumn("uid_amt_diff_mean", F.col("TransactionAmt") - F.col("uid_amt_mean")) \
        .withColumn("uid_amt_ratio_mean", F.col("TransactionAmt") / (F.col("uid_amt_mean") + 1e-5))

    print(f"Saving step 04 output to: {output_path}")
    df_transformed.write \
        .mode("overwrite") \
        .parquet(output_path)

    print("Phase 04 (User Aggregation Features - Zero Leakage) executed successfully.")
    spark.stop()

if __name__ == "__main__":
    main()