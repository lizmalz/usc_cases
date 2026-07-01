import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

timeline = pd.read_csv("scotus_overruling_timeline_full_enriched_ideology_president.csv")

ideology_map = {
    "Liberal": 1,
    "Moderate-Liberal": 0.5,
    "Nationalist-Liberal": 0.7,
    "Conservative": -1,
    "Moderate-Conservative": -0.5,
    "States' Rights-Conservative": -0.7,
    "Mixed": 0,
    "Moderate": 0,
    "Unknown": 0
}

timeline["ideology_score"] = timeline["ideology_majority_label"].map(ideology_map)

corr = timeline[["overruling_count", "ideology_score"]].corr()

plt.figure(figsize=(6, 5))
sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
plt.title("Heatmap: Overrulings vs Ideology Score")
plt.tight_layout()
plt.savefig("heatmap_overrulings_ideology.png", dpi=300)
