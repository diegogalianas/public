
import json
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm


# ============================================================
# Configuration
# ============================================================

V_FILE = "v1-339_correlation_fraud.json"
C_FILE = "c1-14_correlation.json"
D_FILE = "d1-15_correlation.json"
M_FILE = "m1-9_correlation.json"
M4_FILE = "m1-9_correlation2.json"

OUTPUT_FILE = "correlation_analysis.png"

TOP_V_VARIABLES = 20
DPI = 300

VMIN = -0.40
VMAX = 0.40


# ============================================================
# JSON loading
# ============================================================

def load_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def load_single_record(filename):
    data = load_json(filename)

    if isinstance(data, list):
        if not data:
            return {}
        return data[0]

    return data


def to_numeric(value):
    if value is None:
        return np.nan

    try:
        return float(value)
    except (ValueError, TypeError):
        return np.nan


# ============================================================
# Load data
# ============================================================

v_data = load_json(V_FILE)
c_data = load_single_record(C_FILE)
d_data = load_single_record(D_FILE)
m_data = load_single_record(M_FILE)
m4_data = load_single_record(M4_FILE)


# ============================================================
# Prepare V-family correlations
# ============================================================

v_df = pd.DataFrame(v_data)

v_df["correlacion"] = v_df["correlacion"].apply(to_numeric)

v_df = v_df.dropna(subset=["correlacion"])

v_df["variable"] = v_df["variable"].astype(str)

v_top = (
    v_df.assign(
        absolute_correlation=v_df["correlacion"].abs()
    )
    .sort_values(
        "absolute_correlation",
        ascending=False
    )
    .head(TOP_V_VARIABLES)
    .sort_values("correlacion", ascending=True)
)

v_labels = v_top["variable"].tolist()
v_values = v_top["correlacion"].tolist()


# ============================================================
# Prepare C-family correlations
# ============================================================

c_values = {}

for key, value in c_data.items():

    if key.startswith("corr_C"):
        variable = key.replace("corr_", "")
        correlation = to_numeric(value)

        if not np.isnan(correlation):
            c_values[variable] = correlation

c_labels = sorted(
    c_values.keys(),
    key=lambda x: int(x.replace("C", ""))
)

c_correlations = [c_values[x] for x in c_labels]


# ============================================================
# Prepare D-family correlations
# ============================================================

d_values = {}

for key, value in d_data.items():

    if key.startswith("corr_D"):
        variable = key.replace("corr_", "")
        correlation = to_numeric(value)

        if not np.isnan(correlation):
            d_values[variable] = correlation

d_labels = sorted(
    d_values.keys(),
    key=lambda x: int(x.replace("D", ""))
)

d_correlations = [d_values[x] for x in d_labels]


# ============================================================
# Prepare M-family correlations
# ============================================================

m_values = {}

for key, value in m_data.items():

    if key.startswith("corr_M"):
        variable = key.replace("corr_", "")
        correlation = to_numeric(value)

        if not np.isnan(correlation):
            m_values[variable] = correlation


# Add available M4 category correlations
for key, value in m4_data.items():

    if key.startswith("corr_M4_"):
        variable = key.replace("corr_", "")
        correlation = to_numeric(value)

        if not np.isnan(correlation):
            m_values[variable] = correlation


# Sort M variables correctly, including M4_M0, M4_M1 and M4_M2
def sort_m_variables(variable):
    numbers = re.findall(r"\d+", variable)
    return tuple(int(number) for number in numbers)


m_labels = sorted(
    m_values.keys(),
    key=sort_m_variables
)

m_correlations = [m_values[x] for x in m_labels]


# ============================================================
# Heatmap plotting function
# ============================================================

def plot_correlation_heatmap(
    ax,
    labels,
    values,
    title,
    norm,
    cmap,
    show_colorbar=False
):

    matrix = np.array(values).reshape(-1, 1)

    image = ax.imshow(
        matrix,
        cmap=cmap,
        norm=norm,
        aspect="auto"
    )

    ax.set_title(
        title,
        fontsize=13,
        fontweight="bold",
        pad=12
    )

    ax.set_yticks(np.arange(len(labels)))
    ax.set_yticklabels(labels, fontsize=8)

    ax.set_xticks([0])
    ax.set_xticklabels(["isFraud"], fontsize=9)

    ax.set_xticks(
        np.arange(-0.5, 1, 1),
        minor=True
    )

    ax.set_yticks(
        np.arange(-0.5, len(labels), 1),
        minor=True
    )

    ax.grid(
        which="minor",
        color="white",
        linestyle="-",
        linewidth=1.5
    )

    ax.tick_params(
        which="minor",
        bottom=False,
        left=False
    )

    # Correlation values inside the cells
    for i, value in enumerate(values):

        text_color = (
            "white"
            if abs(value) > 0.23
            else "black"
        )

        ax.text(
            0,
            i,
            f"{value:.3f}",
            ha="center",
            va="center",
            fontsize=8,
            color=text_color,
            fontweight="bold"
        )

    if show_colorbar:

        colorbar = plt.colorbar(
            image,
            ax=ax,
            fraction=0.045,
            pad=0.04
        )

        colorbar.set_label(
            "Pearson Correlation",
            fontsize=9
        )

        colorbar.ax.tick_params(labelsize=8)


# ============================================================
# Figure creation
# ============================================================

fig, axes = plt.subplots(
    2,
    2,
    figsize=(17, 17)
)

fig.suptitle(
    "Pearson Correlation with Fraud Target",
    fontsize=19,
    fontweight="bold",
    y=0.98
)

norm = TwoSlopeNorm(
    vmin=VMIN,
    vcenter=0,
    vmax=VMAX
)

cmap = plt.get_cmap("RdBu_r")


# ============================================================
# Panel 1: V-family
# ============================================================

plot_correlation_heatmap(
    axes[0, 0],
    v_labels,
    v_values,
    f"V-Family: Top {len(v_labels)} Correlations",
    norm,
    cmap,
    show_colorbar=True
)


# ============================================================
# Panel 2: C-family
# ============================================================

plot_correlation_heatmap(
    axes[0, 1],
    c_labels,
    c_correlations,
    "C-Family Correlations",
    norm,
    cmap
)


# ============================================================
# Panel 3: D-family
# ============================================================

plot_correlation_heatmap(
    axes[1, 0],
    d_labels,
    d_correlations,
    "D-Family Correlations",
    norm,
    cmap
)


# ============================================================
# Panel 4: M-family
# ============================================================

plot_correlation_heatmap(
    axes[1, 1],
    m_labels,
    m_correlations,
    "M-Family Correlations",
    norm,
    cmap
)


# ============================================================
# Final formatting
# ============================================================

plt.subplots_adjust(
    left=0.10,
    right=0.91,
    top=0.92,
    bottom=0.06,
    hspace=0.38,
    wspace=0.45
)

plt.savefig(
    OUTPUT_FILE,
    dpi=DPI,
    bbox_inches="tight"
)

plt.show()

print(f"Figure saved as: {OUTPUT_FILE}")
