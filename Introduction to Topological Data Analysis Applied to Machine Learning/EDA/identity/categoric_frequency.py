
import json
import pandas as pd
import matplotlib.pyplot as plt

# Load categorical frequency data
with open("categoric_frequency.json", "r", encoding="utf-8") as file:
    data = json.load(file)

df = pd.DataFrame(data)

# Convert numerical columns
df["frecuencia"] = pd.to_numeric(df["frecuencia"])
df["porcentaje"] = pd.to_numeric(df["porcentaje"])

# Define variable groups
categorical_variables = [
    "id_12", "id_15", "id_16", "id_23",
    "id_27", "id_28", "id_29"
]

boolean_variables = ["id_35", "id_36", "id_37", "id_38"]

imbalanced_variables = ["id_27", "id_36", "id_37", "id_23"]

# Create figure
fig, axes = plt.subplots(2, 2, figsize=(19, 17))

# Adjust spacing between subplots
fig.subplots_adjust(
    hspace=0.35,
    wspace=0.55,
    top=0.92,
    bottom=0.07
)

axes = axes.flatten()

# --------------------------------------------------
# Plot 1: Categorical Variables
# --------------------------------------------------
ax = axes[0]

plot_df = df[df["variable"].isin(categorical_variables)].copy()

plot_df["variable"] = pd.Categorical(
    plot_df["variable"],
    categories=categorical_variables,
    ordered=True
)

plot_df = plot_df.sort_values(
    ["variable", "porcentaje"],
    ascending=[True, True]
)

labels = [
    f"{row.variable}: {row.valor}"
    for row in plot_df.itertuples()
]

ax.barh(
    labels,
    plot_df["porcentaje"],
    alpha=0.8
)

ax.set_title(
    "Categorical Variables – Category Frequencies",
    fontsize=13,
    fontweight="bold",
    pad=12
)

ax.set_xlabel("Frequency (%)")
ax.set_ylabel("Variable and Category")
ax.grid(axis="x", linestyle="--", alpha=0.4)
ax.set_axisbelow(True)

# --------------------------------------------------
# Plot 2: Boolean Features
# --------------------------------------------------
ax = axes[1]

plot_df = df[df["variable"].isin(boolean_variables)].copy()

pivot_df = plot_df.pivot(
    index="variable",
    columns="valor",
    values="porcentaje"
).fillna(0)

pivot_df = pivot_df.reindex(boolean_variables)

pivot_df.plot(
    kind="barh",
    stacked=True,
    ax=ax,
    alpha=0.85
)

ax.set_title(
    "Boolean Features – True/False Distribution",
    fontsize=13,
    fontweight="bold",
    pad=12
)

ax.set_xlabel("Frequency (%)")
ax.set_ylabel("Variable")
ax.set_xlim(0, 100)
ax.legend(title="Value")
ax.grid(axis="x", linestyle="--", alpha=0.4)
ax.set_axisbelow(True)

# --------------------------------------------------
# Plot 3: Device Type
# --------------------------------------------------
ax = axes[2]

plot_df = df[df["variable"] == "DeviceType"].copy()
plot_df = plot_df.sort_values("porcentaje")

bars = ax.barh(
    plot_df["valor"],
    plot_df["porcentaje"],
    alpha=0.8
)

ax.set_title(
    "Device Type – Distribution",
    fontsize=13,
    fontweight="bold",
    pad=12
)

ax.set_xlabel("Frequency (%)")
ax.set_ylabel("Device Type")
ax.set_xlim(0, 100)
ax.grid(axis="x", linestyle="--", alpha=0.4)
ax.set_axisbelow(True)

for bar, value in zip(bars, plot_df["porcentaje"]):
    ax.text(
        value + 1,
        bar.get_y() + bar.get_height() / 2,
        f"{value:.2f}%",
        va="center",
        fontsize=9
    )

# --------------------------------------------------
# Plot 4: Most Imbalanced Variables
# --------------------------------------------------
ax = axes[3]

plot_df = df[df["variable"].isin(imbalanced_variables)].copy()

plot_df["variable"] = pd.Categorical(
    plot_df["variable"],
    categories=imbalanced_variables,
    ordered=True
)

plot_df = plot_df.sort_values(
    ["variable", "porcentaje"],
    ascending=[True, True]
)

labels = [
    f"{row.variable}: {row.valor}"
    for row in plot_df.itertuples()
]

bars = ax.barh(
    labels,
    plot_df["porcentaje"],
    alpha=0.8
)

ax.set_title(
    "Most Imbalanced Categorical Features",
    fontsize=13,
    fontweight="bold",
    pad=12
)

ax.set_xlabel("Frequency (%)")
ax.set_ylabel("Variable and Category")
ax.grid(axis="x", linestyle="--", alpha=0.4)
ax.set_axisbelow(True)

for bar, value in zip(bars, plot_df["porcentaje"]):
    ax.text(
        value + 1,
        bar.get_y() + bar.get_height() / 2,
        f"{value:.2f}%",
        va="center",
        fontsize=8
    )

# Overall title
fig.suptitle(
    "Categorical and Boolean Variables – Cardinality and Frequencies",
    fontsize=16,
    fontweight="bold"
)

# Save figure
plt.savefig(
    "identity_categorical_frequencies.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
