
import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# --------------------------------------------------
# 1. Load data
# --------------------------------------------------

with open("nulls.json", "r", encoding="utf-8") as file:
    data = json.load(file)

df = pd.DataFrame(data)

# Convert numeric columns
df["nulos"] = pd.to_numeric(df["nulos"])
df["total"] = pd.to_numeric(df["total"])
df["porcentaje_nulos"] = pd.to_numeric(df["porcentaje_nulos"])

# Exclude transaction identifier
df = df[df["variable"] != "TransactionID"].copy()

# Sort variables by missing value percentage
df = df.sort_values("porcentaje_nulos", ascending=True)

# --------------------------------------------------
# 2. Classify missing value percentages
# --------------------------------------------------

def classify_missingness(percentage):
    if percentage >= 80:
        return "Very high (>=80%)"
    elif percentage >= 50:
        return "High (50-80%)"
    elif percentage >= 10:
        return "Moderate (10-50%)"
    else:
        return "Low (<10%)"

df["category"] = df["porcentaje_nulos"].apply(classify_missingness)

colors = {
    "Very high (>=80%)": "#B23A48",
    "High (50-80%)": "#E07A5F",
    "Moderate (10-50%)": "#F2CC8F",
    "Low (<10%)": "#81B29A"
}

# --------------------------------------------------
# 3. Create horizontal bar chart
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(11, 13))

bars = ax.barh(
    df["variable"],
    df["porcentaje_nulos"],
    color=[colors[category] for category in df["category"]],
    height=0.72
)

# Add percentage labels
for bar, value in zip(bars, df["porcentaje_nulos"]):
    ax.text(
        value + 1,
        bar.get_y() + bar.get_height() / 2,
        f"{value:.2f}%",
        va="center",
        fontsize=8
    )

# Add reference lines
ax.axvline(50, color="gray", linestyle="--", linewidth=0.8, alpha=0.6)
ax.axvline(80, color="gray", linestyle="--", linewidth=0.8, alpha=0.6)

# Chart title and axis labels
ax.set_title(
    "Missing Values by Variable – Identity Dataset",
    fontsize=14,
    fontweight="bold",
    pad=18
)

ax.set_xlabel("Missing Values (%)", fontsize=11)
ax.set_ylabel("Variable", fontsize=11)

# Axis formatting
ax.set_xlim(0, 110)
ax.grid(axis="x", linestyle=":", alpha=0.4)
ax.set_axisbelow(True)

# Add legend
legend_elements = [
    Patch(facecolor=color, label=category)
    for category, color in colors.items()
]

ax.legend(
    handles=legend_elements,
    title="Missingness Level",
    loc="lower right",
    frameon=True
)

plt.tight_layout()

# Save figure
plt.savefig(
    "identity_missing_values.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
