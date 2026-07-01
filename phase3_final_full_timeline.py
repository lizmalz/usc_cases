import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------
# 1. Load enriched full timeline
# ---------------------------------------------------------
timeline = pd.read_csv("scotus_overruling_timeline_full_enriched.csv")
timeline["term"] = timeline["term"].astype(int)

# ---------------------------------------------------------
# 2. Final timeline plot (years on x-axis)
# ---------------------------------------------------------
plt.figure(figsize=(18, 8))
plt.plot(
    timeline["term"],
    timeline["overruling_count"],
    marker="o",
    linewidth=1.5,
    label="Overrulings per Term",
    color="#1f77b4",
)
plt.title("SCOTUS Overrulings Timeline (1790–2026)", fontsize=18)
plt.xlabel("Year (Term)", fontsize=14)
plt.ylabel("Number of Overrulings", fontsize=14)
plt.xticks(timeline["term"][::10])
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("phase3_overrulings_timeline.png", dpi=300)

# ---------------------------------------------------------
# 3. Histogram + PDF (KDE)
# ---------------------------------------------------------
plt.figure(figsize=(14, 6))
sns.histplot(timeline["overruling_count"], bins=20, kde=True, color="steelblue")
plt.title("Distribution of Overruling Counts per Term (PDF + Histogram)")
plt.xlabel("Overruling Count")
plt.ylabel("Density")
plt.tight_layout()
plt.savefig("phase3_overrulings_pdf.png", dpi=300)

# ---------------------------------------------------------
# 4. CDF
# ---------------------------------------------------------
sorted_counts = timeline["overruling_count"].sort_values()
cdf = sorted_counts.rank(method="first") / len(sorted_counts)

plt.figure(figsize=(14, 6))
plt.plot(sorted_counts, cdf, marker=".", linestyle="none")
plt.title("CDF of Overruling Counts per Term")
plt.xlabel("Overruling Count")
plt.ylabel("Cumulative Probability")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("phase3_overrulings_cdf.png", dpi=300)

print("Phase 3 complete: timeline, PDF, CDF generated.")
