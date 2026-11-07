
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --------------------------------------------------
# Load correlation data
# --------------------------------------------------

with open("correlations.json", "r", encoding="utf-8") as file:
    data = json.load(file)

df = pd.DataFrame(data)

df["correlacion"] = pd.to_numeric(df["correlacion"])
df["observaciones"] = pd.to_numeric(df["observaciones"])

# Load id_03 and id_09 specific analysis
with open("correlation_id03-09.json", "r", encoding="utf-8") as file:
    specific_data = json.load(file)[0]

# Convert specific analysis values
specific_data = {
    key: float(value)
    for key, value in specific_data.items()
}

# --------------------------------------------------
# Prepare correlation matrix
# --------------------------------------------------

variables = sorted(
    set(df["variable_1"]).union(set(df["variable_2"]))
)

correlation_matrix = pd.DataFrame(
    np.nan,
    index=variables,
    columns=variables
)

np.fill_diagonal(correlation_matrix.values, 1.0)

for row in df.itertuples():
    correlation_matrix.loc[
        row.variable_1, row.variable_2
    ] = row.correlacion

    correlation_matrix.loc[
        row.variable_2, row.variable_1
    ] = row.correlacion

# --------------------------------------------------
# Select strongest correlations
# --------------------------------------------------

positive_correlations = (
    df[df["correlacion"] > 0]
    .sort_values("correlacion", ascending=False)
    .head(10)
)

negative_correlations = (
    df[df["correlacion"] < 0]
    .sort_values("correlacion", ascending=True)
    .head(10)
)

# --------------------------------------------------
# Create figure
# --------------------------------------------------

fig, axes = plt.subplots(2, 2, figsize=(22, 18))

fig.subplots_adjust(
    hspace=0.40,
    wspace=0.55,
    top=0.92,
    bottom=0.07
)

axes = axes.flatten()

# --------------------------------------------------
# Plot 1: Correlation Heatmap
# --------------------------------------------------

ax = axes[0]

sns.heatmap(
    correlation_matrix,
    cmap="coolwarm",
    vmin=-1,
    vmax=1,
    center=0,
    square=True,
    linewidths=0.15,
    cbar_kws={"label": "Pearson Correlation"},
    ax=ax
)

ax.set_title(
    "Correlation Matrix – Numerical Variables",
    fontsize=13,
    fontweight="bold",
    pad=12
)

ax.tick_params(axis="both", labelsize=7)

# --------------------------------------------------
# Plot 2: Strongest Positive Correlations
# --------------------------------------------------

ax = axes[1]

positive_labels = [
    f"{row.variable_1} – {row.variable_2}"
    for row in positive_correlations.itertuples()
]

bars = ax.barh(
    positive_labels[::-1],
    positive_correlations["correlacion"].values[::-1],
    alpha=0.85
)

ax.set_title(
    "Strongest Positive Correlations",
    fontsize=13,
    fontweight="bold",
    pad=12
)

ax.set_xlabel("Pearson Correlation")
ax.set_xlim(0, 1)
ax.grid(axis="x", linestyle="--", alpha=0.4)
ax.set_axisbelow(True)

for bar, value in zip(
    bars,
    positive_correlations["correlacion"].values[::-1]
):
    ax.text(
        value + 0.015,
        bar.get_y() + bar.get_height() / 2,
        f"{value:.3f}",
        va="center",
        fontsize=8
    )

# --------------------------------------------------
# Plot 3: Strongest Negative Correlations
# --------------------------------------------------

ax = axes[2]

negative_labels = [
    f"{row.variable_1} – {row.variable_2}"
    for row in negative_correlations.itertuples()
]

bars = ax.barh(
    negative_labels[::-1],
    negative_correlations["correlacion"].values[::-1],
    alpha=0.85
)

ax.set_title(
    "Strongest Negative Correlations",
    fontsize=13,
    fontweight="bold",
    pad=12
)

ax.set_xlabel("Pearson Correlation")
ax.set_xlim(-1, 0)
ax.grid(axis="x", linestyle="--", alpha=0.4)
ax.set_axisbelow(True)

for bar, value in zip(
    bars,
    negative_correlations["correlacion"].values[::-1]
):
    ax.text(
        value - 0.02,
        bar.get_y() + bar.get_height() / 2,
        f"{value:.3f}",
        va="center",
        ha="right",
        fontsize=8
    )

# --------------------------------------------------
# Plot 4: id_03 and id_09 Analysis
# --------------------------------------------------

ax = axes[3]

correlation_values = [
    specific_data["correlacion_total"],
    specific_data["correlacion_sin_ceros"]
]

correlation_labels = [
    "All observations",
    "Excluding zero values"
]

bars = ax.barh(
    correlation_labels,
    correlation_values,
    alpha=0.85
)

ax.set_title(
    "id_03 and id_09 – Effect of Zero Values",
    fontsize=13,
    fontweight="bold",
    pad=12
)

ax.set_xlabel("Pearson Correlation")
ax.set_xlim(0, 1)
ax.grid(axis="x", linestyle="--", alpha=0.4)
ax.set_axisbelow(True)

for bar, value in zip(bars, correlation_values):
    ax.text(
        value + 0.015,
        bar.get_y() + bar.get_height() / 2,
        f"{value:.4f}",
        va="center",
        fontsize=9
    )

# Add observation counts
zero_counts = [
    specific_data["ambos_cero"],
    specific_data["solo_id_03_cero"],
    specific_data["solo_id_09_cero"],
    specific_data["ninguno_cero"]
]

zero_labels = [
    "Both zero",
    "Only id_03 zero",
    "Only id_09 zero",
    "Neither zero"
]

count_text = "\n".join(
    f"{label}: {int(count):,}"
    for label, count in zip(zero_labels, zero_counts)
)

ax.text(
    0.02,
    -0.48,
    count_text,
    transform=ax.transAxes,
    fontsize=8,
    verticalalignment="top"
)

# --------------------------------------------------
# Overall title and export
# --------------------------------------------------

fig.suptitle(
    "Correlation Analysis – Numerical Variables",
    fontsize=16,
    fontweight="bold"
)

plt.savefig(
    "identity_correlation_analysis.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
