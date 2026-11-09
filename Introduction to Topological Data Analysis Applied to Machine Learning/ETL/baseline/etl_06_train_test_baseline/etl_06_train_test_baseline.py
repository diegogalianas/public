import sys
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

def main():
    spark = SparkSession.builder \
        .appName("TFM_ETL_06_TrainTestSplit") \
        .getOrCreate()

    input_path = "gs://fraud-detection-imf/processed/step_05_encoding_selection.parquet"
    train_output_path = "gs://fraud-detection-imf/processed/baseline_train_dataset.parquet"
    test_output_path = "gs://fraud-detection-imf/processed/baseline_test_dataset.parquet"

    print(f"Loading step 05 output dataset from: {input_path}")
    df = spark.read.parquet(input_path)

    # -------------------------------------------------------------------------
    # Time-Based Partitioning
    # DT_day_continuous ranges from 1 to 182 days.
    # Split point: Day 145 (~80% historical split boundary)
    #   - Baseline Train: Days 1 to 145
    #   - Baseline Test: Days 146 to 182 (Out-Of-Time validation)
    # -------------------------------------------------------------------------
    split_day_boundary = 145
    print(f"Executing temporal partition split at Day {split_day_boundary}...")

    train_df = df.filter(F.col("DT_day_continuous") <= split_day_boundary)
    test_df = df.filter(F.col("DT_day_continuous") > split_day_boundary)

    print(f"Writing Baseline Train dataset to: {train_output_path}")
    train_df.write \
        .mode("overwrite") \
        .parquet(train_output_path)

    print(f"Writing Baseline Test dataset to: {test_output_path}")
    test_df.write \
        .mode("overwrite") \
        .parquet(test_output_path)

    print("Phase 06 (Time-Based Train/Test Split) completed successfully.")
    spark.stop()

if __name__ == "__main__":
    main()