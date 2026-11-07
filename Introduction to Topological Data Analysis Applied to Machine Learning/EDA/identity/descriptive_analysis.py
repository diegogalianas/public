import json
import pandas as pd
import matplotlib.pyplot as plt

# Load descriptive analysis data
with open("descriptive_analysis.json", "r", encoding="utf-8") as file:
    data = json.load(file)

df = pd.DataFrame(data)

# Convert numerical columns
numeric_columns = [
    "valores_no_nulos",
    "minimo",
    "q1",
    "mediana",
    "q3",
    "maximo"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# Define variable groups
groups = {
    "Highly Concentrated Variables": [
        "id_03", "id_04", "id_09", "id_10", "id_11"
    ],
    "Low-Range Variables": [
        "id_01", "id_05", "id_06", "id_07",
        "id_08", "id_13", "id_18", "id_24"
    ],
    "Medium and High-Range Variables": [
        "id_14", "id_17", "id_19", "id_20",
        "id_21", "id_22", "id_25", "id_26", "id_32"
    ],
    "High-Scale Variable": [
        "id_02"
    ]
}

# Create figure with four subplots
fig, axes = plt.subplots(2, 2, figsize=(18, 16))

# Increase spacing between rows and columns
fig.subplots_adjust(
    hspace=0.65,
    wspace=0.30,
    top=0.92,
    bottom=0.07
)

axes = axes.flatten()

# Generate boxplots
for ax, (group_name, variables) in zip(axes, groups.items()):

    group_df = df[df["variable"].isin(variables)].copy()

    # Preserve the specified variable order
    group_df["variable"] = pd.Categorical(
        group_df["variable"],
        categories=variables,
        ordered=True
    )

    group_df = group_df.sort_values("variable")

    # Prepare boxplot statistics
    stats = []

    for _, row in group_df.iterrows():
        stats.append({
            "label": f'{row["variable"]} (n={int(row["valores_no_nulos"]):,})',
            "whislo": row["minimo"],
            "q1": row["q1"],
            "med": row["mediana"],
            "q3": row["q3"],
            "whishi": row["maximo"],
            "fliers": []
        })

    # Draw horizontal boxplots
    ax.bxp(
        stats,
        vert=False,
        showfliers=False,
        patch_artist=True,
        boxprops=dict(alpha=0.7),
        medianprops=dict(linewidth=2),
        whiskerprops=dict(linewidth=1.2),
        capprops=dict(linewidth=1.2)
    )

    ax.set_title(group_name, fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Value", fontsize=10)
    ax.set_ylabel("Variable", fontsize=10)

    ax.grid(axis="x", linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)

    ax.tick_params(axis="both", labelsize=9)

# Overall title
fig.suptitle(
    "Numerical Variables – Distribution and Dispersion",
    fontsize=16,
    fontweight="bold"
)

# Save figure
plt.savefig(
    "identity_numerical_boxplots.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()