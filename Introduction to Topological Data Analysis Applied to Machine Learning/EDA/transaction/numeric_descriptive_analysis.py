
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================
# Configuration
# ============================================================

JSON_FILE = "numeric_descriptive_analysis.json"
OUTPUT_FILE = "numeric_descriptive_analysis.png"

DPI = 300

# ============================================================
# Load and prepare data
# ============================================================

with open(JSON_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)

df = pd.DataFrame(data)

numeric_columns = [
    "valores_validos",
    "valores_nulos",
    "minimo",
    "maximo",
    "media",
    "desviacion_tipica",
    "q1",
    "mediana",
    "q3"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

df = df.dropna(subset=["variable", "minimo", "maximo", "q1", "mediana", "q3"])

# Identify variable families
transaction = df[df["variable"] == "TransactionAmt"]

c_family = df[
    df["variable"].str.fullmatch(r"C(?:[1-9]|1[0-4])", na=False)
].copy()

v_family = df[
    df["variable"].str.fullmatch(r"V(?:[1-9]|[1-9][0-9]|[12][0-9]{2}|3[0-3][0-9])", na=False)
].copy()

# Sort variables numerically
c_family["sort_id"] = c_family["variable"].str.extract(r"(\d+)").astype(int)
v_family["sort_id"] = v_family["variable"].str.extract(r"(\d+)").astype(int)

c_family = c_family.sort_values("sort_id")
v_family = v_family.sort_values("sort_id")

# ============================================================
# Figure layout
# ============================================================

fig, axes = plt.subplots(
    2, 2,
    figsize=(19, 15)
)

fig.suptitle(
    "Numerical Variables: Distributions and Outliers",
    fontsize=19,
    fontweight="bold",
    y=0.98
)

# ============================================================
# Panel 1: Transaction Amount
# ============================================================

ax = axes[0, 0]

if not transaction.empty:

    row = transaction.iloc[0]

    stats = [{
        "label": "TransactionAmt",
        "whislo": row["minimo"],
        "q1": row["q1"],
        "med": row["mediana"],
        "q3": row["q3"],
        "whishi": row["maximo"],
        "fliers": []
    }]

    ax.bxp(
        stats,
        vert=False,
        showfliers=False,
        patch_artist=True,
        boxprops=dict(facecolor="#4C78A8", alpha=0.75),
        medianprops=dict(color="#E45756", linewidth=2),
        whiskerprops=dict(color="#555555"),
        capprops=dict(color="#555555")
    )

    ax.set_title(
        "Transaction Amount Distribution",
        fontsize=13,
        fontweight="bold"
    )

    ax.set_xlabel("Transaction Amount")
    ax.set_yticks([])

    ax.text(
        0.02, 0.93,
        f"Mean: {row['media']:,.2f}\n"
        f"Median: {row['mediana']:,.2f}\n"
        f"Maximum: {row['maximo']:,.2f}",
        transform=ax.transAxes,
        fontsize=9,
        verticalalignment="top",
        bbox=dict(
            boxstyle="round,pad=0.4",
            facecolor="white",
            edgecolor="#CCCCCC",
            alpha=0.9
        )
    )

else:
    ax.text(0.5, 0.5, "TransactionAmt not found",
            ha="center", va="center", transform=ax.transAxes)

ax.grid(axis="x", linestyle="--", alpha=0.3)
ax.set_axisbelow(True)

# ============================================================
# Panel 2: C-Family - Mean vs Median
# ============================================================

ax = axes[0, 1]

if not c_family.empty:

    y = np.arange(len(c_family))

    ax.scatter(
        c_family["media"],
        y,
        label="Mean",
        color="#E45756",
        s=55,
        marker="o",
        zorder=3
    )

    ax.scatter(
        c_family["mediana"],
        y,
        label="Median",
        color="#4C78A8",
        s=55,
        marker="s",
        zorder=3
    )

    ax.set_yticks(y)
    ax.set_yticklabels(c_family["variable"])

    ax.set_title(
        "C-Family: Mean vs Median",
        fontsize=13,
        fontweight="bold"
    )

    ax.set_xlabel("Value")
    ax.set_ylabel("Variable")

    ax.legend(frameon=False, loc="lower right")

else:
    ax.text(0.5, 0.5, "C-family variables not found",
            ha="center", va="center", transform=ax.transAxes)

ax.grid(axis="x", linestyle="--", alpha=0.3)
ax.set_axisbelow(True)

# ============================================================
# Panel 3: V-Family - Concentration in Low Values
# ============================================================

ax = axes[1, 0]

if not v_family.empty:

    total_v = len(v_family)

    q3_zero = (v_family["q3"] == 0).sum()

    median_zero_q3_positive = (
        (v_family["mediana"] == 0) &
        (v_family["q3"] > 0)
    ).sum()

    median_positive_q3_le_one = (
        (v_family["mediana"] > 0) &
        (v_family["q3"] <= 1)
    ).sum()

    remaining = (
        total_v
        - q3_zero
        - median_zero_q3_positive
        - median_positive_q3_le_one
    )

    categories = [
        "Q3 = 0",
        "Median = 0, Q3 > 0",
        "Median > 0, Q3 <= 1",
        "Other distributions"
    ]

    counts = [
        q3_zero,
        median_zero_q3_positive,
        median_positive_q3_le_one,
        remaining
    ]

    percentages = [
        count / total_v * 100
        for count in counts
    ]

    bars = ax.bar(
        categories,
        percentages,
        color=["#4C78A8", "#72A0C1", "#F2CF5B", "#9D9DA0"],
        width=0.65
    )

    for bar, count, percentage in zip(bars, counts, percentages):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1,
            f"{count} ({percentage:.1f}%)",
            ha="center",
            va="bottom",
            fontsize=9
        )

    ax.set_title(
        "V-Family: Distribution Concentration",
        fontsize=13,
        fontweight="bold"
    )

    ax.set_ylabel("Percentage of Variables (%)")
    ax.set_ylim(0, max(percentages) * 1.2 if max(percentages) > 0 else 10)

    ax.tick_params(axis="x", rotation=12)

else:
    ax.text(0.5, 0.5, "V-family variables not found",
            ha="center", va="center", transform=ax.transAxes)

ax.grid(axis="y", linestyle="--", alpha=0.3)
ax.set_axisbelow(True)

# ============================================================
# Panel 4: V-Family - Maximum Values and Scale
# ============================================================

ax = axes[1, 1]

if not v_family.empty:

    max_values = v_family["maximo"].dropna()

    # Logarithmic transformation to handle different magnitudes
    transformed_max = np.log10(1 + max_values.clip(lower=0))

    ax.hist(
        transformed_max,
        bins=30,
        color="#4C78A8",
        edgecolor="white",
        alpha=0.85
    )

    ax.set_title(
        "V-Family: Distribution of Maximum Values",
        fontsize=13,
        fontweight="bold"
    )

    ax.set_xlabel(r"$\log_{10}(1 + Maximum)$")
    ax.set_ylabel("Number of Variables")

    ax.text(
        0.97, 0.95,
        f"Variables: {len(max_values)}\n"
        f"Maximum observed: {max_values.max():,.2f}",
        transform=ax.transAxes,
        fontsize=9,
        ha="right",
        va="top",
        bbox=dict(
            boxstyle="round,pad=0.4",
            facecolor="white",
            edgecolor="#CCCCCC",
            alpha=0.9
        )
    )

else:
    ax.text(0.5, 0.5, "V-family variables not found",
            ha="center", va="center", transform=ax.transAxes)

ax.grid(axis="y", linestyle="--", alpha=0.3)
ax.set_axisbelow(True)

# ============================================================
# Final layout and export
# ============================================================

plt.subplots_adjust(
    left=0.08,
    right=0.97,
    top=0.91,
    bottom=0.09,
    hspace=0.35,
    wspace=0.30
)

plt.savefig(
    OUTPUT_FILE,
    dpi=DPI,
    bbox_inches="tight"
)

plt.show()

print(f"Chart saved to: {Path(OUTPUT_FILE).resolve()}")
