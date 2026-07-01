import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

timeline = pd.read_csv("scotus_overruling_timeline_full_enriched_ideology_president.csv")

groups = timeline.groupby("ideology_majority_label")

# ---------------------------------------------------------
# PDF (KDE or vertical line if variance=0)
# ---------------------------------------------------------
plt.figure(figsize=(14, 6))

for name, group in groups:
    data = group["overruling_count"].dropna()

    if len(data) == 0:
        continue

    if np.var(data) == 0:
        # Plot a vertical line at the constant value
        plt.axvline(data.iloc[0], label=f"{name} (constant)", linestyle="--")
    else:
        sns.kdeplot(data, label=name)

plt.title("PDF of Overruling Counts by Court Ideology")
plt.xlabel("Overruling Count")
plt.ylabel("Density")
plt.legend()
plt.tight_layout()
plt.savefig("pdf_by_ideology.png", dpi=300)

# ---------------------------------------------------------
# CDF (always works)
# ---------------------------------------------------------
plt.figure(figsize=(14, 6))

for name, group in groups:
    data = group["overruling_count"].dropna().sort_values()

    if len(data) == 0:
        continue

    cdf = data.rank(method="first") / len(data)
    plt.plot(data, cdf, marker=".", linestyle="none", label=name)

plt.title("CDF of Overruling Counts by Court Ideology")
plt.xlabel("Overruling Count")
plt.ylabel("Cumulative Probability")
plt.legend()
plt.tight_layout()
plt.savefig("cdf_by_ideology.png", dpi=300)

print("Segmented PDF/CDF generated successfully.")
