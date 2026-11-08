
import json
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================
# Configuration
# ============================================================

JSON_FILE = "nulls.json"
OUTPUT_FILE = "nulls.png"
TOP_N = 25

# ============================================================
# Load data
# ============================================================

with open(JSON_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)

df = pd.DataFrame(data)

df["valores_nulos"] = pd.to_numeric(
    df["valores_nulos"], errors="coerce"
)

df["valores_no_nulos"] = pd.to_numeric(
    df["valores_no_nulos"], errors="coerce"
)

df["porcentaje_nulos"] = pd.to_numeric(
    df["porcentaje_nulos"], errors="coerce"
)

df = df.dropna(subset=["variable", "porcentaje_nulos"])

# ============================================================
# Select variables with the highest missing-value percentage
# ============================================================

# Select all variables with more than 80% missing values
top_missing = (
    df[df["porcentaje_nulos"] > 80]
    .sort_values("porcentaje_nulos", ascending=True)
)

# ============================================================
# Create horizontal bar chart
# ============================================================

fig, ax = plt.subplots(figsize=(12, 10))

bars = ax.barh(
    top_missing["variable"],
    top_missing["porcentaje_nulos"],
    color="#4C78A8",
    edgecolor="white",
    height=0.72
)

# Add percentage labels
for bar, percentage in zip(bars, top_missing["porcentaje_nulos"]):
    ax.text(
        bar.get_width() + 0.8,
        bar.get_y() + bar.get_height() / 2,
        f"{percentage:.2f}%",
        va="center",
        fontsize=9
    )

# ============================================================
# Formatting
# ============================================================

ax.set_title(
    "Variables with More Than 80% Missing Values",
    fontsize=15,
    fontweight="bold",
    pad=18
)

ax.set_xlabel("Missing Values (%)", fontsize=11)
ax.set_ylabel("Variable", fontsize=11)

ax.set_xlim(0, 108)

ax.grid(
    axis="x",
    linestyle="--",
    alpha=0.35
)

ax.set_axisbelow(True)

plt.tight_layout()

# ============================================================
# Save figure
# ============================================================

plt.savefig(
    OUTPUT_FILE,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print(f"Chart saved to: {Path(OUTPUT_FILE).resolve()}")
