import pandas as pd
import matplotlib.pyplot as plt

timeline = pd.read_csv("scotus_overruling_timeline_full_enriched_ideology_president.csv")
timeline["term"] = timeline["term"].astype(int)
timeline["x"] = range(len(timeline))

# Map ideology to numeric score
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

fig, ax1 = plt.subplots(figsize=(20, 10))

# Left axis: overrulings
ax1.plot(
    timeline["x"],
    timeline["overruling_count"],
    color="blue",
    marker="o",
    label="Overrulings"
)
ax1.set_ylabel("Overrulings", fontsize=14)

# Right axis: ideology score
ax2 = ax1.twinx()
ax2.plot(
    timeline["x"],
    timeline["ideology_score"],
    color="darkred",
    linewidth=2,
    label="Ideology Score"
)
ax2.set_ylabel("Ideology Score", fontsize=14)

plt.title("Dual-Axis Plot: Overrulings vs Ideology Score (1790–2026)", fontsize=18)
plt.tight_layout()
plt.savefig("dual_axis_overrulings_ideology.png", dpi=300)
