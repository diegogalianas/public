
import json
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# Configuration
# ============================================================

PRODUCT_FILE = "productCD_fraud.json"
CARD1_SUMMARY_FILE = "card1_fraud.json"
CARD1_FILE = "card1_fraud2.json"
CARD2_FILE = "card2.json"
EMAIL_FILE = "P_emaildomain_R_emaildomain.json"

OUTPUT_FILE = "categorical_variables_fraud.png"

MIN_TRANSACTIONS = 100
TOP_CARD_CODES = 10
TOP_EMAIL_DOMAINS = 8

DPI = 300


# ============================================================
# Data loading
# ============================================================

def load_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def to_dataframe(data):
    if isinstance(data, dict):
        data = [data]

    return pd.DataFrame(data)


product_df = to_dataframe(load_json(PRODUCT_FILE))
card1_summary_df = to_dataframe(load_json(CARD1_SUMMARY_FILE))
card1_df = to_dataframe(load_json(CARD1_FILE))
card2_df = to_dataframe(load_json(CARD2_FILE))
email_df = to_dataframe(load_json(EMAIL_FILE))


# ============================================================
# Data preparation
# ============================================================

# ProductCD
product_df["total_transacciones"] = pd.to_numeric(
    product_df["total_transacciones"]
)
product_df["fraudes"] = pd.to_numeric(product_df["fraudes"])
product_df["porcentaje_fraude"] = pd.to_numeric(
    product_df["porcentaje_fraude"]
)

product_df = product_df.sort_values(
    "total_transacciones", ascending=False
)

product_df["percentage"] = (
    product_df["total_transacciones"]
    / product_df["total_transacciones"].sum()
    * 100
)


# Card 1 and Card 2
for df, column in [
    (card1_df, "card1"),
    (card2_df, "card2")
]:
    df["total_transacciones"] = pd.to_numeric(
        df["total_transacciones"]
    )
    df["fraudes"] = pd.to_numeric(df["fraudes"])
    df["tasa_fraude"] = pd.to_numeric(df["tasa_fraude"])

    df[column] = df[column].astype(str)

    # Exclude categories with insufficient observations
    df.drop(
        df[df["total_transacciones"] < MIN_TRANSACTIONS].index,
        inplace=True
    )


# Email domains
email_df["total_transacciones"] = pd.to_numeric(
    email_df["total_transacciones"]
)
email_df["transacciones_fraudulentas"] = pd.to_numeric(
    email_df["transacciones_fraudulentas"]
)
email_df["tasa_fraude"] = pd.to_numeric(
    email_df["tasa_fraude"]
)

email_df["dominio"] = email_df["dominio"].astype(str)


# ============================================================
# Figure layout
# ============================================================

fig, axes = plt.subplots(2, 2, figsize=(19, 15))

fig.suptitle(
    "Categorical Variables and Fraud Association",
    fontsize=19,
    fontweight="bold",
    y=0.98
)


# ============================================================
# Panel 1: ProductCD
# ============================================================

ax = axes[0, 0]

bars = ax.bar(
    product_df["ProductCD"],
    product_df["porcentaje_fraude"],
    width=0.65
)

ax.set_title(
    "Fraud Rate by Product Category",
    fontsize=13,
    fontweight="bold",
    pad=12
)

ax.set_xlabel("Product Category")
ax.set_ylabel("Fraud Rate (%)")

ax.grid(axis="y", linestyle="--", alpha=0.35)
ax.set_axisbelow(True)

for bar, rate, count, percentage in zip(
    bars,
    product_df["porcentaje_fraude"],
    product_df["total_transacciones"],
    product_df["percentage"]
):
    ax.annotate(
        f"{rate:.2f}%\n({count:,.0f} transactions)",
        xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
        xytext=(0, 5),
        textcoords="offset points",
        ha="center",
        va="bottom",
        fontsize=8
    )

ax.set_ylim(
    0,
    product_df["porcentaje_fraude"].max() * 1.35
)


# ============================================================
# Panel 2: Card1 high-risk codes
# ============================================================

ax = axes[0, 1]

card1_top = (
    card1_df.sort_values("tasa_fraude", ascending=False)
    .head(TOP_CARD_CODES)
    .sort_values("tasa_fraude", ascending=True)
)

bars = ax.barh(
    card1_top["card1"],
    card1_top["tasa_fraude"]
)

ax.set_title(
    f"Highest Fraud Rates by card1 Code\n"
    f"(Minimum {MIN_TRANSACTIONS} transactions)",
    fontsize=13,
    fontweight="bold",
    pad=12
)

ax.set_xlabel("Fraud Rate (%)")
ax.set_ylabel("card1 Code")

ax.grid(axis="x", linestyle="--", alpha=0.35)
ax.set_axisbelow(True)

for bar, rate, count in zip(
    bars,
    card1_top["tasa_fraude"],
    card1_top["total_transacciones"]
):
    ax.annotate(
        f"{rate:.2f}%  (n={count:,.0f})",
        xy=(bar.get_width(), bar.get_y() + bar.get_height() / 2),
        xytext=(5, 0),
        textcoords="offset points",
        ha="left",
        va="center",
        fontsize=8
    )

ax.set_xlim(
    0,
    card1_top["tasa_fraude"].max() * 1.35
)


# ============================================================
# Panel 3: Card2 high-risk codes
# ============================================================

ax = axes[1, 0]

card2_top = (
    card2_df.sort_values("tasa_fraude", ascending=False)
    .head(TOP_CARD_CODES)
    .sort_values("tasa_fraude", ascending=True)
)

bars = ax.barh(
    card2_top["card2"],
    card2_top["tasa_fraude"]
)

ax.set_title(
    f"Highest Fraud Rates by card2 Code\n"
    f"(Minimum {MIN_TRANSACTIONS} transactions)",
    fontsize=13,
    fontweight="bold",
    pad=12
)

ax.set_xlabel("Fraud Rate (%)")
ax.set_ylabel("card2 Code")

ax.grid(axis="x", linestyle="--", alpha=0.35)
ax.set_axisbelow(True)

for bar, rate, count in zip(
    bars,
    card2_top["tasa_fraude"],
    card2_top["total_transacciones"]
):
    ax.annotate(
        f"{rate:.2f}%  (n={count:,.0f})",
        xy=(bar.get_width(), bar.get_y() + bar.get_height() / 2),
        xytext=(5, 0),
        textcoords="offset points",
        ha="left",
        va="center",
        fontsize=8
    )

ax.set_xlim(
    0,
    card2_top["tasa_fraude"].max() * 1.35
)


# ============================================================
# Panel 4: Email domain fraud rates
# ============================================================

ax = axes[1, 1]

email_filtered = email_df[
    email_df["total_transacciones"] >= MIN_TRANSACTIONS
].copy()

preferred_domains = [
    "gmail.com",
    "hotmail.com",
    "yahoo.com"
]

selected_domains = []

for variable in ["P_emaildomain", "R_emaildomain"]:

    variable_df = email_filtered[
        email_filtered["variable"] == variable
    ]

    # Select the most frequent domains
    frequent = (
        variable_df.sort_values(
            "total_transacciones", ascending=False
        )
        .head(TOP_EMAIL_DOMAINS)
    )

    # Also include the selected reference domains when available
    preferred = variable_df[
        variable_df["dominio"].isin(preferred_domains)
    ]

    combined = pd.concat(
        [frequent, preferred]
    ).drop_duplicates(subset=["dominio"])

    for _, row in combined.iterrows():
        selected_domains.append({
            "variable": variable,
            "dominio": row["dominio"],
            "total_transacciones": row["total_transacciones"],
            "tasa_fraude": row["tasa_fraude"]
        })


email_plot_df = pd.DataFrame(selected_domains)

if not email_plot_df.empty:

    domain_order = (
        email_plot_df.groupby("dominio")["total_transacciones"]
        .sum()
        .sort_values()
        .index.tolist()
    )

    y_positions = np.arange(len(domain_order))
    bar_height = 0.36

    for variable, offset, label in [
        ("P_emaildomain", -bar_height / 2, "Purchaser domain"),
        ("R_emaildomain", bar_height / 2, "Recipient domain")
    ]:

        variable_df = email_plot_df[
            email_plot_df["variable"] == variable
        ].set_index("dominio")

        rates = [
            variable_df.loc[domain, "tasa_fraude"]
            if domain in variable_df.index else 0
            for domain in domain_order
        ]

        positions = y_positions + offset

        bars = ax.barh(
            positions,
            rates,
            height=bar_height,
            label=label
        )

        for bar, domain in zip(bars, domain_order):

            if domain in variable_df.index:
                count = variable_df.loc[
                    domain, "total_transacciones"
                ]

                rate = variable_df.loc[
                    domain, "tasa_fraude"
                ]

                ax.annotate(
                    f"{rate:.2f}% (n={count:,.0f})",
                    xy=(
                        bar.get_width(),
                        bar.get_y() + bar.get_height() / 2
                    ),
                    xytext=(4, 0),
                    textcoords="offset points",
                    ha="left",
                    va="center",
                    fontsize=7
                )

    ax.set_yticks(y_positions)
    ax.set_yticklabels(domain_order)

    ax.set_title(
        "Fraud Rates Across Email Domains",
        fontsize=13,
        fontweight="bold",
        pad=12
    )

    ax.set_xlabel("Fraud Rate (%)")
    ax.set_ylabel("Email Domain")

    ax.legend(
        loc="lower right",
        fontsize=8,
        frameon=False
    )

    ax.grid(axis="x", linestyle="--", alpha=0.35)
    ax.set_axisbelow(True)

    maximum_rate = email_plot_df["tasa_fraude"].max()
    ax.set_xlim(0, maximum_rate * 1.45 if maximum_rate > 0 else 1)

else:
    ax.text(
        0.5, 0.5,
        "No email domains meet the minimum transaction threshold.",
        ha="center",
        va="center",
        transform=ax.transAxes
    )


# ============================================================
# Final formatting and export
# ============================================================

plt.subplots_adjust(
    left=0.09,
    right=0.97,
    top=0.91,
    bottom=0.08,
    hspace=0.32,
    wspace=0.30
)

plt.savefig(
    OUTPUT_FILE,
    dpi=DPI,
    bbox_inches="tight"
)

plt.show()

print(f"Figure saved as: {OUTPUT_FILE}")
