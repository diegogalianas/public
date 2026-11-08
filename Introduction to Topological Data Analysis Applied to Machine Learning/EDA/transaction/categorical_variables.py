
import json
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================
# 1. Load JSON data
# ============================================================

JSON_FILE = "categorical_variables.json"
OUTPUT_FILE = "categorical_variables.png"

with open(JSON_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)

# Extract isFraud records
fraud_data = [
    item for item in data
    if item["variable"] == "isFraud"
]

if not fraud_data:
    raise ValueError("No records found for the isFraud variable.")

# Sort classes to ensure 0 (Legitimate) appears before 1 (Fraudulent)
fraud_data.sort(key=lambda item: int(item["valor"]))

labels = []
counts = []
percentages = []

for item in fraud_data:
    value = int(item["valor"])

    labels.append(
        "Legitimate" if value == 0 else "Fraudulent"
    )

    counts.append(int(item["frecuencia"]))
    percentages.append(float(item["porcentaje"]))

# ============================================================
# 2. Create figure
# ============================================================

fig, ax = plt.subplots(figsize=(10, 6))

colors = ["#4C78A8", "#E45756"]

bars = ax.bar(
    labels,
    percentages,
    color=colors,
    width=0.55,
    edgecolor="black",
    linewidth=0.7
)

# ============================================================
# 3. Add annotations
# ============================================================

for bar, count, percentage in zip(
    bars, counts, percentages
):
    height = bar.get_height()

    annotation = (
        f"{count:,} transactions\n"
        f"({percentage:.2f}%)"
    )

    ax.annotate(
        annotation,
        xy=(bar.get_x() + bar.get_width() / 2, height),
        xytext=(0, 8),
        textcoords="offset points",
        ha="center",
        va="bottom",
        fontsize=10,
        fontweight="bold"
    )

# ============================================================
# 4. Formatting
# ============================================================

ax.set_title(
    "Target Variable Distribution (isFraud)",
    fontsize=15,
    fontweight="bold",
    pad=18
)

ax.set_xlabel(
    "Transaction Class",
    fontsize=11,
    labelpad=10
)

ax.set_ylabel(
    "Percentage of Transactions (%)",
    fontsize=11,
    labelpad=10
)

ax.set_ylim(0, max(percentages) * 1.17)

ax.grid(
    axis="y",
    linestyle="--",
    alpha=0.35
)

ax.set_axisbelow(True)

ax.tick_params(
    axis="both",
    labelsize=10
)

# Remove unnecessary borders
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()

# ============================================================
# 5. Save figure
# ============================================================

plt.savefig(
    OUTPUT_FILE,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print(f"Figure saved as: {Path(OUTPUT_FILE).resolve()}")
