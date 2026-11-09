import os
import json
import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from ripser import ripser
from persim import plot_diagrams

def main():
    print("=== Running Unified TDA Pipeline (Diagram + Inverse Mapping + Centroids Extraction) ===")

    plt.rcParams.update({
        "font.family": "sans-serif",
        "axes.labelsize": 11,
        "font.size": 10,
        "legend.fontsize": 9,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "savefig.bbox": "tight"
    })

    input_sample_path = "/tmp/tda_run/tda_point_cloud_sample.parquet"
    if not os.path.exists(input_sample_path):
        print("-> Local file not found. Downloading from GCS...")
        os.makedirs("/tmp/tda_run", exist_ok=True)
        subprocess.run(
            ["gcloud", "storage", "cp", "gs://fraud-detection-imf/processed/tda_point_cloud_sample.parquet", input_sample_path], 
            check=True
        )

    print("-> Loading subsampled TDA dataset...")
    df = pd.read_parquet(input_sample_path)

    # Ensure TransactionID is retained as an explicit column
    if 'TransactionID' not in df.columns and df.index.name == 'TransactionID':
        df = df.reset_index()
    elif 'TransactionID' not in df.columns:
        df = df.reset_index().rename(columns={'index': 'TransactionID'})

    metadata_cols = ['TransactionID', 'y_true', 'y_pred', 'y_prob', 'error_type']
    feature_cols = [col for col in df.columns if col not in metadata_cols]
    X_raw = df[feature_cols].fillna(0)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_raw.values)

    max_points = 4000
    np.random.seed(42)
    if X_scaled.shape[0] > max_points:
        indices = np.random.choice(X_scaled.shape[0], max_points, replace=False)
        X_subset = X_scaled[indices]
        df_subset = df.iloc[indices].reset_index(drop=True)
    else:
        X_subset = X_scaled
        df_subset = df.reset_index(drop=True)

    print("-> Computing Persistent Homology and Cocycles ONCE via Ripser...")
    result = ripser(X_subset, maxdim=1, do_cocycles=True)
    diagrams = result['dgms']
    cocycles = result['cocycles']

    print("-> Generating and saving Persistence Diagram plot...")
    plt.figure(figsize=(8, 8))
    plot_diagrams(diagrams, show=False, title="Persistence Diagram - Fraud Decision Boundary")
    plt.tight_layout()
    output_png = 'tda_persistence_diagram.png'
    plt.savefig(output_png, format='png', dpi=300)
    plt.close()
    print(f"-> Saved visualization to: {output_png}")

    print("\n" + "="*60)
    print("=== INVERSE MAPPING: Analyzing most persistent structures ===")
    print("="*60)

    dgm_h0 = diagrams[0]
    finite_h0_idx = np.isfinite(dgm_h0[:, 1])
    h0_persistence = dgm_h0[finite_h0_idx, 1] - dgm_h0[finite_h0_idx, 0]
    top_h0_indices = np.argsort(h0_persistence)[-5:]

    print("\nTop 5 Most Persistent H0 Features (Isolated Clusters):")
    for rank, idx in enumerate(top_h0_indices[::-1]):
        birth = dgm_h0[finite_h0_idx][idx, 0]
        death = dgm_h0[finite_h0_idx][idx, 1]
        pers = h0_persistence[idx]
        print(f"  {rank+1}. Birth: {birth:.3f} | Death: {death:.3f} | Persistence: {pers:.3f}")

    dgm_h1 = diagrams[1]
    cocs_h1 = cocycles[1]
    if len(dgm_h1) > 0:
        h1_persistence = dgm_h1[:, 1] - dgm_h1[:, 0]
        top_h1_indices = np.argsort(h1_persistence)[-5:]

        print("\nTop 5 Most Persistent H1 Features (Topological Loops):")
        for rank, idx in enumerate(top_h1_indices[::-1]):
            birth = dgm_h1[idx, 0]
            death = dgm_h1[idx, 1]
            pers = h1_persistence[idx]
            print(f"  {rank+1}. Birth: {birth:.3f} | Death: {death:.3f} | Persistence: {pers:.3f}")

    print("\n=== Error Type Distribution in TDA Sample ===")
    print(df_subset['error_type'].value_counts())

    print("\n" + "="*60)
    print("=== INVERSE MAPPING: TOPOLOGICAL ERROR ANALYSIS (TOP 3 LOOPS) ===")
    print("="*60)

    if len(dgm_h1) > 0:
        top_3_h1_indices = np.argsort(h1_persistence)[-3:]

        for rank, idx in enumerate(top_3_h1_indices[::-1]):
            birth = dgm_h1[idx, 0]
            death = dgm_h1[idx, 1]
            pers = h1_persistence[idx]
            
            print(f"\n  [Loop #{rank+1}] Birth: {birth:.3f} | Death: {death:.3f} | Persistence: {pers:.3f}")
            
            if idx < len(cocs_h1):
                cocycle = cocs_h1[idx]
                if len(cocycle) > 0:
                    flat_indices = np.unique(cocycle[:, :2].astype(int))
                    loop_transactions = df_subset.iloc[flat_indices]
                    
                    print(f"    -> Points involved in this loop: {len(flat_indices)}")
                    print(f"    -> Error Type breakdown inside this loop:")
                    error_counts = loop_transactions['error_type'].value_counts().to_dict()
                    for err, count in error_counts.items():
                        print(f"       - {err}: {count} transactions")
                else:
                    print("    -> Cocycle contains no active simplex indices.")

    print("\n" + "="*60)
    print("=== EXTRACTING H1 CENTROIDS FOR PYSPARK ===")
    print("="*60)

    local_json_path = "/tmp/tda_run/tda_centroids.json"

    if len(dgm_h1) > 0:
        h1_persistence = dgm_h1[:, 1] - dgm_h1[:, 0]
        sorted_h1_indices = np.argsort(h1_persistence)[::-1]
        top_k = 5
        centroids_dict = {}

        for rank in range(min(top_k, len(dgm_h1))):
            loop_idx = sorted_h1_indices[rank]
            cocycle = cocs_h1[loop_idx]
            
            if len(cocycle) > 0:
                flat_indices = np.unique(cocycle[:, :2].astype(int))
                centroid = np.mean(X_subset[flat_indices], axis=0)
                centroids_dict[f"dist_to_h1_loop_{rank + 1}"] = centroid.tolist()
                print(f"  -> Centroid #{rank + 1} calculated using {len(flat_indices)} points (Persistence: {h1_persistence[loop_idx]:.3f})")

        print("\n-> Exporting centroid and scaler metadata to JSON...")
        metadata_payload = {
            "feature_cols": feature_cols,
            "scaler_mean": scaler.mean_.tolist(),
            "scaler_scale": scaler.scale_.tolist(),
            "centroids": centroids_dict
        }
        with open(local_json_path, "w") as f:
            json.dump(metadata_payload, f)

    print("\n" + "="*60)
    print("=== UPLOADING ARTIFACTS DIRECTLY TO GCS ===")
    print("="*60)
    
    if os.path.exists(local_json_path):
        gcs_json_target = "gs://fraud-detection-imf/processed/tda_centroids.json"
        subprocess.run(["gcloud", "storage", "cp", local_json_path, gcs_json_target], check=True)
        print(f"-> Uploaded Centroids JSON to: {gcs_json_target}")

    print("\n=== Pipeline completed successfully! ===")

if __name__ == "__main__":
    main()