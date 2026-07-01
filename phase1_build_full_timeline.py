import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("scotus_overrulings_full_1790_2026.csv")

df["term"] = df["term"].astype(int)
df["dateDecision"] = pd.to_datetime(df["dateDecision"], errors="coerce")

timeline = (
    df.groupby("term")
    .agg(
        overruling_count=("precedentAlteration", "size"),
        first_case=("caseName", "first"),
        last_case=("caseName", "last"),
    )
    .reset_index()
)

timeline["has_overruling"] = timeline["overruling_count"] > 0

timeline.to_csv("scotus_overruling_timeline_full_1790_2026.csv", index=False)
print("Saved scotus_overruling_timeline_full_1790_2026.csv")

plt.figure(figsize=(14, 6))
plt.plot(timeline["term"], timeline["overruling_count"], marker="o")
plt.title("SCOTUS Overrulings by Term (1790–2026)")
plt.xlabel("Term")
plt.ylabel("Overrulings")
plt.grid(True)
plt.tight_layout()
plt.savefig("scotus_overrulings_full_plot_phase1.png", dpi=300)
print("Saved scotus_overrulings_full_plot_phase1.png")
