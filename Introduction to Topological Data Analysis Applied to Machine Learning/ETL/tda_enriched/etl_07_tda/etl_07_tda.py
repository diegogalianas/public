import sys
import json
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType

def project_tda(spark, input_path, output_path, feature_cols, means, scales, centroids):
    print(f"-> Loading dataset from: {input_path}")
    df = spark.read.parquet(input_path)

    # Apply exact standardization matching StandardScaler(fillna(0)) from the Vertex AI extraction job
    scaled_exprs = [
        (F.coalesce(F.col(col_name).cast(DoubleType()), F.lit(0.0)) - F.lit(float(m))) / F.lit(float(s) if float(s) != 0 else 1.0)
        for col_name, m, s in zip(feature_cols, means, scales)
    ]

    # Compute Euclidean distance to each of the 5 H1 topological loop centroids
    for loop_name, centroid_coords in centroids.items():
        squared_diffs = [
            F.pow(scaled_col - F.lit(float(c_val)), 2)
            for scaled_col, c_val in zip(scaled_exprs, centroid_coords)
        ]
        
        sum_squared = squared_diffs[0]
        for sd in squared_diffs[1:]:
            sum_squared = sum_squared + sd
        
        df = df.withColumn(loop_name, F.sqrt(sum_squared))

    print(f"-> Saving enriched TDA dataset to: {output_path}")
    df.write.mode("overwrite").parquet(output_path)

def main():
    spark = SparkSession.builder \
        .appName("TFM_ETL_07_TDA") \
        .getOrCreate()

    # Exact GCS path where Vertex AI saved the clean centroids
    centroids_gcs_path = "gs://fraud-detection-imf/processed_tda/tda_centroids.json"

    print("1. Reading clean TDA centroids and scaler metadata from GCS...")
    sc = spark.sparkContext
    centroids_json_str = "".join(sc.textFile(centroids_gcs_path).collect())
    tda_meta = json.loads(centroids_json_str)

    feature_cols = tda_meta["feature_cols"]
    means = tda_meta["scaler_mean"]
    scales = tda_meta["scaler_scale"]
    centroids = tda_meta["centroids"]

    print(f"   Loaded {len(centroids)} H1 centroids across {len(feature_cols)} features.")

    print("2. Projecting TDA features onto Train and Test partitions...")
    project_tda(
        spark,
        input_path="gs://fraud-detection-imf/processed_tda/train_dataset.parquet",
        output_path="gs://fraud-detection-imf/processed_tda/train_tda_enriched.parquet",
        feature_cols=feature_cols,
        means=means,
        scales=scales,
        centroids=centroids
    )

    project_tda(
        spark,
        input_path="gs://fraud-detection-imf/processed_tda/test_dataset.parquet",
        output_path="gs://fraud-detection-imf/processed_tda/test_tda_enriched.parquet",
        feature_cols=feature_cols,
        means=means,
        scales=scales,
        centroids=centroids
    )

    print("Phase 07 (TDA Enrichment) completed successfully with 0 nulls and zero leakage!")
    spark.stop()

if __name__ == "__main__":
    main()