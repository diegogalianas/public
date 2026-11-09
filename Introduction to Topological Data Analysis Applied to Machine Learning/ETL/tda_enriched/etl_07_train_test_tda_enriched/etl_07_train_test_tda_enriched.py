import sys
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

def main():
    spark = SparkSession.builder \
        .appName("TFM_ETL_07_TrainTestSplit_TDA") \
        .getOrCreate()

    # Pointing to the output of the previous step (Step 06)
    input_path = "gs://fraud-detection-imf/processed_tda/step_06_encoding_selection.parquet"
    
    # New output paths for the TDA datasets (avoiding overwriting baseline datasets)
    train_output_path = "gs://fraud-detection-imf/processed_tda/tda_train_dataset.parquet"
    test_output_path = "gs://fraud-detection-imf/processed_tda/tda_test_dataset.parquet"

    print(f"Loading step 06 encoded dataset from: {input_path}")
    df = spark.read.parquet(input_path)

    # -------------------------------------------------------------------------
    # Time-Based Partitioning
    # DT_day_continuous ranges from 1 to 182 days.
    # Split point: Day 145 (~80% historical split boundary)
    #   - TDA Train: Days 1 to 145
    #   - TDA Test: Days 146 to 182 (Out-Of-Time validation)
    # -------------------------------------------------------------------------
    split_day_boundary = 145
    print(f"Executing temporal partition split at Day {split_day_boundary}...")

    train_df = df.filter(F.col("DT_day_continuous") <= split_day_boundary)
    test_df = df.filter(F.col("DT_day_continuous") > split_day_boundary)

    print(f"Writing TDA Train dataset to: {train_output_path}")
    train_df.write \
        .mode("overwrite") \
        .parquet(train_output_path)

    print(f"Writing TDA Test dataset to: {test_output_path}")
    test_df.write \
        .mode("overwrite") \
        .parquet(test_output_path)

    print("Phase (Time-Based Train/Test Split with TDA) completed successfully.")
    spark.stop()

if __name__ == "__main__":
    main()