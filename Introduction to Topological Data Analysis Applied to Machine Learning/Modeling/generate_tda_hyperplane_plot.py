import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from ripser import ripser

print("-> Script started successfully!")
print("-> Loading dataset and preparing 2D projection for visualization...")

df = pd.read_parquet("/tmp/tda_run/tda_point_cloud_sample.parquet")

metadata_cols = ['y_true', 'y_pred', 'y_prob', 'error_type']
feature_cols = [col for col in df.columns if col not in metadata_cols]
X_raw = df[feature_cols].fillna(0)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_raw.values)

max_points = 4000
np.random.seed(42)
indices = np.random.choice(X_scaled.shape[0], max_points, replace=False)
X_subset = X_scaled[indices]
df_subset = df.iloc[indices].reset_index(drop=True)

print("-> Running Ripser to locate the most persistent loop...")
result = ripser(X_subset, maxdim=1, do_cocycles=True)
dgm_h1 = result['dgms'][1]
cocs_h1 = result['cocycles'][1]

best_loop_idx = np.argmax(dgm_h1[:, 1] - dgm_h1[:, 0])
cocycle = cocs_h1[best_loop_idx]
loop_point_indices = np.unique(cocycle[:, :2].astype(int))

pca = PCA(n_components=2, random_state=42)
X_2d = pca.fit_transform(X_subset)

print("-> Generating explanatory geometric plot...")
plt.figure(figsize=(10, 8))

colors = {'TN': '#1f77b4', 'FP': '#d62728', 'FN': '#ff7f0e', 'TP': '#2ca02c'}
for err_type, color in colors.items():
    mask = df_subset['error_type'] == err_type
    plt.scatter(
        X_2d[mask, 0], X_2d[mask, 1],
        c=color, label=f'{err_type} ({mask.sum()})',
        alpha=0.6, s=25, edgecolors='none'
    )

loop_coords = X_2d[loop_point_indices]
plt.scatter(
    loop_coords[:, 0], loop_coords[:, 1],
    facecolors='none', edgecolors='black', s=80, linewidths=1.2,
    label='Topological Loop ($H_1$) - FP Focus'
)

centroid_2d = np.mean(loop_coords, axis=0)
plt.scatter(
    centroid_2d[0], centroid_2d[1],
    c='black', marker='X', s=150, label='Loop Centroid'
)

split_x = centroid_2d[0] + 0.2
plt.axvline(
    x=split_x, color='purple', linestyle='--', linewidth=2.5,
    label="XGBoost Decision Split (Hyperplane)"
)

ymin, ymax = plt.ylim()
xmin, xmax = plt.xlim()
plt.fill_between(
    [split_x, xmax], ymin, ymax, color='purple', alpha=0.1,
    hatch="//", label="Classification Error Zone (FPs)"
)

plt.title("Geometric Failure of XGBoost: Orthogonal Split vs. Topological Loop ($H_1$)", fontsize=13, fontweight='bold', pad=15)
plt.xlabel("Principal Component 1 (PCA)", fontsize=11)
plt.ylabel("Principal Component 2 (PCA)", fontsize=11)
plt.legend(loc='upper right', frameon=True, framealpha=0.9)
plt.grid(True, linestyle=':', alpha=0.5)

output_plot = 'tda_hyperplane_failure.png'
plt.savefig(output_plot, format='png', dpi=300)
plt.close()
print(f"-> Plot successfully saved locally as {output_plot}")