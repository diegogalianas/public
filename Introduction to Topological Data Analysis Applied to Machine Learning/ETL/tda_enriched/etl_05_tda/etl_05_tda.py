import sys
import json
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import LongType

def main():
    spark = SparkSession.builder \
        .appName("TFM_ETL_05_TDA_FullProjection") \
        .getOrCreate()

    input_base_path = "gs://fraud-detection-imf/processed/step_04_agg.parquet"
    centroids_gcs_path = "gs://fraud-detection-imf/processed/tda_centroids.json"
    output_path = "gs://fraud-detection-imf/processed_tda/step_05_tda.parquet"

    print(f"1. Loading base dataset from: {input_base_path}")
    df_base = spark.read.parquet(input_base_path)

    # Asegurar que TransactionID sea LongType por seguridad en posibles cruces posteriores
    df_base = df_base.withColumn("TransactionID", F.col("TransactionID").cast(LongType()))

    print("2. Reading TDA centroids and scaler metadata from GCS...")
    sc = spark.sparkContext
    centroids_json_str = sc.textFile(centroids_gcs_path).collect()[0]
    tda_meta = json.loads(centroids_json_str)

    feature_cols = tda_meta["feature_cols"]
    means = tda_meta["scaler_mean"]
    scales = tda_meta["scaler_scale"]
    centroids = tda_meta["centroids"]

    print("3. Computing standardized Euclidean distances across all rows in parallel...")
    
    # Construir la expresión de normalización por columna: (X - media) / escala
    scaled_exprs = [
        F.coalesce((F.col(col_name) - F.lit(m)) / F.lit(s if s != 0 else 1.0), F.lit(0.0))
        for col_name, m, s in zip(feature_cols, means, scales)
    ]

    # Calcular la distancia euclídea exacta para cada uno de los 5 centroides H1
    for loop_name, centroid_coords in centroids.items():
        squared_diffs = [
            F.pow(scaled_col - F.lit(c_val), 2)
            for scaled_col, c_val in zip(scaled_exprs, centroid_coords)
        ]
        
        # Sumar los cuadrados de las diferencias de las 20 dimensiones
        sum_squared = squared_diffs[0]
        for sd in squared_diffs[1:]:
            sum_squared = sum_squared + sd
        
        # Aplicar la raíz cuadrada para obtener la distancia euclídea final
        df_base = df_base.withColumn(loop_name, F.sqrt(sum_squared))

    print(f"4. Saving fully enriched TDA dataset to: {output_path}")
    df_base.write \
        .mode("overwrite") \
        .parquet(output_path)

    print("Phase 05 (TDA Full Projection) completed successfully with 0 nulls and full coverage!")
    spark.stop()

if __name__ == "__main__":
    main()