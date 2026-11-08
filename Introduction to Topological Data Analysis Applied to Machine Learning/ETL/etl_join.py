from pyspark.sql import SparkSession

def main():
    # Initialize Spark session
    spark = SparkSession.builder.appName("TFM_ETL_Join").getOrCreate()

    # Google Cloud Storage paths
    transaction_path = "gs://fraud-detection-imf/raw/transaction.csv"
    identity_path = "gs://fraud-detection-imf/raw/identity.csv"
    output_path = "gs://fraud-detection-imf/processed/joined_dataset.parquet"

    # 1. Load the CSV files
    print("Loading transaction.csv and identity.csv...")
    df_transaction = spark.read.csv(transaction_path, header=True, inferSchema=True)
    df_identity = spark.read.csv(identity_path, header=True, inferSchema=True)

    # 2. Perform the LEFT JOIN
    # Identity columns will be added to transactions matching the TransactionID.
    # Unmatched transactions will have nulls in the identity columns.
    print("Executing LEFT JOIN...")
    df_joined = df_transaction.join(df_identity, on="TransactionID", how="left")

    # 3. Save the result in Parquet format
    print(f"Saving joined dataset to {output_path}...")
    df_joined.write.mode("overwrite").parquet(output_path)
    
    print("ETL finished successfully.")
    spark.stop()

if __name__ == "__main__":
    main()