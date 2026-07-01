import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------
# 1. Load enriched timeline + overruling cases
# ---------------------------------------------------------
timeline = pd.read_csv("scotus_overruling_timeline_full_enriched.csv")
overrules = pd.read_csv("scotus_overrulings_full_1790_2026.csv")

timeline["term"] = timeline["term"].astype(int)
overrules["term"] = overrules["term"].astype(int)
overrules["dateDecision"] = pd.to_datetime(overrules["dateDecision"], errors="coerce")

# ---------------------------------------------------------
# 2. Presidential party dataset
# ---------------------------------------------------------
presidents = [
    ("George Washington", "Independent", 1789, 1797),
    ("John Adams", "Federalist", 1797, 1801),
    ("Thomas Jefferson", "Democratic-Republican", 1801, 1809),
    ("James Madison", "Democratic-Republican", 1809, 1817),
    ("James Monroe", "Democratic-Republican", 1817, 1825),
    ("John Quincy Adams", "Democratic-Republican", 1825, 1829),
    ("Andrew Jackson", "Democratic", 1829, 1837),
    ("Martin Van Buren", "Democratic", 1837, 1841),
    ("William Henry Harrison", "Whig", 1841, 1841),
    ("John Tyler", "Whig", 1841, 1845),
    ("James K. Polk", "Democratic", 1845, 1849),
    ("Zachary Taylor", "Whig", 1849, 1850),
    ("Millard Fillmore", "Whig", 1850, 1853),
    ("Franklin Pierce", "Democratic", 1853, 1857),
    ("James Buchanan", "Democratic", 1857, 1861),
    ("Abraham Lincoln", "Republican", 1861, 1865),
    ("Andrew Johnson", "Democratic", 1865, 1869),
    ("Ulysses S. Grant", "Republican", 1869, 1877),
    ("Rutherford B. Hayes", "Republican", 1877, 1881),
    ("James A. Garfield", "Republican", 1881, 1881),
    ("Chester A. Arthur", "Republican", 1881, 1885),
    ("Grover Cleveland", "Democratic", 1885, 1889),
    ("Benjamin Harrison", "Republican", 1889, 1893),
    ("Grover Cleveland", "Democratic", 1893, 1897),
    ("William McKinley", "Republican", 1897, 1901),
    ("Theodore Roosevelt", "Republican", 1901, 1909),
    ("William Howard Taft", "Republican", 1909, 1913),
    ("Woodrow Wilson", "Democratic", 1913, 1921),
    ("Warren G. Harding", "Republican", 1921, 1923),
    ("Calvin Coolidge", "Republican", 1923, 1929),
    ("Herbert Hoover", "Republican", 1929, 1933),
    ("Franklin D. Roosevelt", "Democratic", 1933, 1945),
    ("Harry S. Truman", "Democratic", 1945, 1953),
    ("Dwight D. Eisenhower", "Republican", 1953, 1961),
    ("John F. Kennedy", "Democratic", 1961, 1963),
    ("Lyndon B. Johnson", "Democratic", 1963, 1969),
    ("Richard Nixon", "Republican", 1969, 1974),
    ("Gerald Ford", "Republican", 1974, 1977),
    ("Jimmy Carter", "Democratic", 1977, 1981),
    ("Ronald Reagan", "Republican", 1981, 1989),
    ("George H. W. Bush", "Republican", 1989, 1993),
    ("Bill Clinton", "Democratic", 1993, 2001),
    ("George W. Bush", "Republican", 2001, 2009),
    ("Barack Obama", "Democratic", 2009, 2017),
    ("Donald Trump", "Republican", 2017, 2021),
    ("Joe Biden", "Democratic", 2021, 2025),
    ("Donald Trump", "Republican", 2025, 2029),
]

def president_for_term(term):
    year = int(term)
    for name, party, start, end in presidents:
        if start <= year <= end:
            return party
    return "Unknown"

# ---------------------------------------------------------
# 3. FIX: Add president_party BEFORE plotting
# ---------------------------------------------------------
timeline["president_party"] = timeline["term"].apply(president_for_term)


# ---------------------------------------------------------
# Presidential party shading colors
# ---------------------------------------------------------
party_colors = {
    "Democratic": "#d0e7ff",
    "Republican": "#ffd0d0",
    "Whig": "#e8e8e8",
    "Federalist": "#e8e8e8",
    "Democratic-Republican": "#e8e8e8",
    "Independent": "#f5f5f5",
    "Unknown": "#f5f5f5",
}


# ---------------------------------------------------------
# 4. Ideology model
# ---------------------------------------------------------
historical_ideology = {
    "Marshall": "Nationalist-Liberal",
    "Taney": "States' Rights-Conservative",
    "Chase": "Reconstruction-Liberal",
    "Waite": "Moderate",
    "Fuller": "Conservative",
    "White": "Conservative",
    "Taft": "Conservative",
    "Hughes": "Moderate-Liberal",
    "Stone": "Liberal",
    "Vinson": "Moderate-Conservative",
}

def ideology_label(term, era):
    if term < 1937:
        return historical_ideology.get(era, "Unknown")
    if era in ["Rehnquist", "Roberts"]:
        return "Conservative"
    if era in ["Warren"]:
        return "Liberal"
    return "Mixed"

timeline["ideology_majority_label"] = timeline.apply(
    lambda row: ideology_label(row["term"], row["chief_justice_era"]),
    axis=1,
)

timeline["majority_shift"] = timeline["ideology_majority_label"].ne(
    timeline["ideology_majority_label"].shift(1)
)

timeline.to_csv("scotus_overruling_timeline_full_enriched_ideology_president.csv", index=False)

# ---------------------------------------------------------
# 5. Final plot with presidential party shading + equal spacing
# ---------------------------------------------------------

plt.figure(figsize=(20, 10))

# Background shading by president party
for _, row in timeline.iterrows():
    plt.axvspan(
        row["term"] - 0.5,
        row["term"] + 0.5,
        color=party_colors.get(row["president_party"], "#f5f5f5"),
        alpha=0.3,
    )

# Overruling counts (equal spacing because x = term index)
plt.plot(
    timeline["term"],
    timeline["overruling_count"],
    marker="o",
    linewidth=1.5,
    label="Overrulings per Term",
    color="#1f77b4",
)

# Major overruling terms
major_terms = timeline.loc[timeline["major_overruling_count"] > 0]
plt.scatter(
    major_terms["term"],
    major_terms["overruling_count"],
    color="red",
    s=80,
    label="Major Overruling Terms",
)

plt.title("SCOTUS Overrulings with Ideology & Presidential Context (1790–2026)", fontsize=18)
plt.xlabel("Presidential Transition Years", fontsize=14)
plt.ylabel("Number of Overrulings", fontsize=14)

# ---------------------------------------------------------
# X-axis ticks = presidential transition years
# ---------------------------------------------------------
president_transitions = [start for (_, _, start, _) in presidents]
president_transitions.append(2026)  # current year

plt.xticks(president_transitions, rotation=45)

plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("phase5_overrulings_enriched_timeline_presidential_ticks.png", dpi=300)


# ---------------------------------------------------------
# 6. PDF (Probability Density Function)
# ---------------------------------------------------------
plt.figure(figsize=(14, 6))
sns.histplot(timeline["overruling_count"], bins=20, kde=True, color="darkgreen")
plt.title("Distribution of Overruling Counts per Term (PDF + Histogram)")
plt.xlabel("Overruling Count")
plt.ylabel("Density")
plt.tight_layout()
plt.savefig("phase5_overrulings_pdf.png", dpi=300)

# ---------------------------------------------------------
# 7. CDF
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
plt.savefig("phase5_overrulings_cdf.png", dpi=300)

print("Phase 5 complete.")
