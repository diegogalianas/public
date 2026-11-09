import sys
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StringType
from pyspark.ml.feature import StringIndexer
from pyspark.ml import Pipeline

def main():
    spark = SparkSession.builder \
        .appName("TFM_ETL_05_EncodingAndSelection") \
        .getOrCreate()

    input_path = "gs://fraud-detection-imf/processed/step_04_agg.parquet"
    output_path = "gs://fraud-detection-imf/processed/step_05_encoding_selection.parquet"

    print(f"Loading input dataset from: {input_path}")
    df = spark.read.parquet(input_path)

    # 1. Dropping raw text fields replaced in previous steps and strict IDs
    cols_to_drop = [
        "TransactionID", 
        "P_emaildomain", 
        "R_emaildomain", 
        "UID_card_addr"  # Dropping string representation; frequency & agg metrics are retained
    ]
    
    existing_cols_to_drop = [c for c in cols_to_drop if c in df.columns]
    df = df.drop(*existing_cols_to_drop)
    print(f"Dropped identifier & raw text columns: {existing_cols_to_drop}")

    # 2. Categorical String Indexing (Label Encoding preserving NULLs for XGBoost)
    print("Applying StringIndexer to remaining categorical string columns...")
    string_cols = [f.name for f in df.schema.fields if isinstance(f.dataType, StringType)]
    
    indexers = [
        StringIndexer(inputCol=c, outputCol=f"{c}_idx", handleInvalid="keep")
        for c in string_cols
    ]
    
    pipeline = Pipeline(stages=indexers)
    df_indexed = pipeline.fit(df).transform(df)

    # Drop original string columns and rename index columns back to original names
    df_final = df_indexed.drop(*string_cols)
    for c in string_cols:
        df_final = df_final.withColumnRenamed(f"{c}_idx", c)

    # 3. Cast Boolean columns to Integer for strict XGBoost compatibility
    print("Formatting schema types...")
    for col_name, dtype in df_final.dtypes:
        if dtype == "boolean":
            df_final = df_final.withColumn(col_name, F.col(col_name).cast("integer"))

    print(f"Encoded matrix: {len(df_final.columns)} total features/columns.")
    print(f"Saving step 05 output to: {output_path}")

    df_final.write \
        .mode("overwrite") \
        .parquet(output_path)

    print("Phase 05 (Categorical Encoding & Selection) completed successfully.")
    spark.stop()

if __name__ == "__main__":
    main()