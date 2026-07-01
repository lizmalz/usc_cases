import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# Load timeline
# ---------------------------------------------------------
timeline = pd.read_csv("scotus_overruling_timeline_full_enriched_ideology_president.csv")
timeline["term"] = timeline["term"].astype(int)
timeline["x"] = range(len(timeline))

# ---------------------------------------------------------
# Chief Justice eras
# ---------------------------------------------------------
chief_eras = [
    ("Marshall", 1801, 1835, "#cfe2ff"),
    ("Taney", 1836, 1864, "#ffcccc"),
    ("Chase", 1864, 1873, "#e8e8e8"),
    ("Waite", 1874, 1888, "#f0f0f0"),
    ("Fuller", 1888, 1910, "#ffe0e0"),
    ("White", 1910, 1921, "#ffd0d0"),
    ("Taft", 1921, 1930, "#e0f0ff"),
    ("Hughes", 1930, 1941, "#d0e7ff"),
    ("Stone", 1941, 1946, "#cfe2ff"),
    ("Vinson", 1946, 1953, "#ffe0e0"),
    ("Warren", 1953, 1969, "#d0e7ff"),
    ("Burger", 1969, 1986, "#ffd0d0"),
    ("Rehnquist", 1986, 2005, "#ffcccc"),
    ("Roberts", 2005, 2026, "#e8e8e8"),
]

# ---------------------------------------------------------
# Map CJ boundaries to nearest SCDB x positions
# ---------------------------------------------------------
def nearest_x(year):
    diffs = abs(timeline["term"] - year)
    idx = diffs.idxmin()
    return timeline.loc[idx, "x"]

cj_labels = []
cj_positions = []

for cj, start, end, color in chief_eras:
    start_x = nearest_x(start)
    cj_labels.append(cj)
    cj_positions.append(start_x)

# ---------------------------------------------------------
# Plot
# ---------------------------------------------------------
plt.figure(figsize=(22, 10))

# CJ era shading
for cj, start, end, color in chief_eras:
    start_x = nearest_x(start)
    end_x = nearest_x(end)
    plt.axvspan(start_x, end_x, color=color, alpha=0.3)

# Overrulings
plt.plot(
    timeline["x"],
    timeline["overruling_count"],
    marker="o",
    color="blue",
    linewidth=1.5,
    label="Overrulings"
)

plt.title("SCOTUS Overrulings by Chief Justice Era", fontsize=18)
plt.xlabel("Chief Justice Era Boundaries", fontsize=14)
plt.ylabel("Overrulings", fontsize=14)

# CJ era boundaries on x-axis
plt.xticks(cj_positions, cj_labels, rotation=45)

plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("chief_justice_era_boundaries_xaxis.png", dpi=300)

print("CJ era plot with CJ boundaries on x-axis generated.")
