import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. Load full timeline + full overruling cases
# ---------------------------------------------------------
timeline = pd.read_csv("scotus_overruling_timeline_full_1790_2026.csv")
overrules = pd.read_csv("scotus_overrulings_full_1790_2026.csv")

timeline["term"] = timeline["term"].astype(int)
overrules["term"] = overrules["term"].astype(int)

# ---------------------------------------------------------
# 2. Chief Justice eras
# ---------------------------------------------------------
chief_eras = [
    ("Marshall", 1801, 1835),
    ("Taney", 1836, 1864),
    ("Chase", 1864, 1873),
    ("Waite", 1874, 1888),
    ("Fuller", 1888, 1910),
    ("White", 1910, 1921),
    ("Taft", 1921, 1930),
    ("Hughes", 1930, 1941),
    ("Stone", 1941, 1946),
    ("Vinson", 1946, 1953),
    ("Warren", 1953, 1969),
    ("Burger", 1969, 1986),
    ("Rehnquist", 1986, 2005),
    ("Roberts", 2005, 2026),
]

def assign_chief(term):
    for cj, start, end in chief_eras:
        if start <= term <= end:
            return cj
    return "Unknown"

timeline["chief_justice_era"] = timeline["term"].apply(assign_chief)

# ---------------------------------------------------------
# 3. Major overruling cases (curated list)
# ---------------------------------------------------------
major_cases_list = {
    "Brown v. Board of Education": 1954,
    "Miranda v. Arizona": 1966,
    "Lawrence v. Texas": 2003,
    "Dobbs v. Jackson Women's Health Organization": 2022,
    "West Coast Hotel v. Parrish": 1937,
    "Gideon v. Wainwright": 1963,
    "Obergefell v. Hodges": 2015,
    "Citizens United v. FEC": 2010,
}

overrules["is_major_case"] = overrules["caseName"].apply(
    lambda x: x in major_cases_list
)

major_cases = overrules.loc[overrules["is_major_case"] == True].copy()
major_cases.to_csv("scotus_major_overruling_cases_full.csv", index=False)

major_counts = (
    major_cases.groupby("term")
    .agg(major_overruling_count=("is_major_case", "size"))
    .reset_index()
)

timeline = timeline.merge(major_counts, on="term", how="left")
timeline["major_overruling_count"] = timeline["major_overruling_count"].fillna(0).astype(int)

timeline.to_csv("scotus_overruling_timeline_full_enriched.csv", index=False)
print("Saved scotus_overruling_timeline_full_enriched.csv")
print("Saved scotus_major_overruling_cases_full.csv")

# ---------------------------------------------------------
# 4. Plot enriched timeline
# ---------------------------------------------------------
plt.figure(figsize=(14, 6))
plt.plot(timeline["term"], timeline["overruling_count"], marker="o", label="All Overrulings")
plt.plot(timeline["term"], timeline["major_overruling_count"], marker="s", label="Major Overrulings")
plt.title("SCOTUS Overrulings by Term (1790–2026) — Enriched")
plt.xlabel("Term")
plt.ylabel("Number of Overrulings")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("scotus_overrulings_full_plot_phase2.png", dpi=300)
print("Saved scotus_overrulings_full_plot_phase2.png")
