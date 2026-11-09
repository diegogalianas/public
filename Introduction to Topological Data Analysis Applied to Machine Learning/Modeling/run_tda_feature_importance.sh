cat << 'EOF' > run_tda_feature_importance.sh
#!/usr/bin/env bash
set -euo pipefail

echo "=== 1. Checking and installing dependencies ==="
python3 -m pip install --quiet xgboost scikit-learn pandas numpy matplotlib seaborn pyarrow fastparquet

echo "=== 2. Creating working directory and downloading artifacts ==="
mkdir -p /tmp/tda_eval/test_sample/
gcloud storage cp gs://fraud-detection-imf/models/tda/xgboost_tda.json /tmp/tda_eval/
gcloud storage cp "gs://fraud-detection-imf/processed_tda/tda_test_dataset.parquet/*.parquet" /tmp/tda_eval/test_sample/

echo "=== 3. Running Python script to map real feature names and generate PNG ==="
python3 - << 'PYTHON_SCRIPT'
import os
import xgboost as xgb
import pandas as pd
import pyarrow.parquet as pq
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams.update({
    "font.family": "sans-serif",
    "axes.labelsize": 11,
    "font.size": 10,
    "legend.fontsize": 9,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "savefig.bbox": "tight"
})

print("-> Reading feature names from TDA parquet schema...")
dataset = pq.ParquetDataset("/tmp/tda_eval/test_sample/")
feature_names = dataset.schema.names

if 'isFraud' in feature_names:
    feature_names.remove('isFraud')

print(f"-> Total TDA-enriched features detected: {len(feature_names)}")

print("-> Loading XGBoost TDA booster model...")
model_path = "/tmp/tda_eval/xgboost_tda.json"
booster = xgb.Booster()
booster.load_model(model_path)

# Map real column names to the booster
booster.feature_names = feature_names

# Extract feature importances by Gain
score_gain = booster.get_score(importance_type='gain')

df_importance = pd.DataFrame({
    'feature': list(score_gain.keys()),
    'importance_gain': list(score_gain.values())
}).sort_values('importance_gain', ascending=False)

print("\n=== TOP 20 MOST IMPORTANT FEATURES (TDA-ENHANCED) ===")
print(df_importance.head(20).to_string(index=False))

print("\n-> Generating PNG plot...")
plt.figure(figsize=(10, 6))
sns.barplot(
    data=df_importance.head(20),
    x='importance_gain',
    y='feature',
    palette='Greens_r'
)
plt.title('Top 20 Feature Importance (XGBoost + TDA - Real Names)', pad=12)
plt.xlabel('Average Gain')
plt.ylabel('Feature Name')
plt.grid(True, linestyle=':', alpha=0.5)
plt.tight_layout()

output_png = 'tda_enriched_feature_importance.png'
plt.savefig(output_png, format='png', dpi=300)
plt.close()

print(f"-> Plot saved locally as {output_png}")
PYTHON_SCRIPT

echo "=== 4. Uploading PNG plot to Google Cloud Storage ==="
gcloud storage cp tda_enriched_feature_importance.png gs://fraud-detection-imf/reports/figures/

echo "=== Process completed successfully! ==="
EOF

chmod +x run_tda_feature_importance.sh
./run_tda_feature_importance.sh