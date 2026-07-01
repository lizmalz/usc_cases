import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------
# 1. Load enriched timeline (with ideology labels)
# ---------------------------------------------------------
timeline = pd.read_csv("scotus_overruling_timeline_full_enriched_ideology_president.csv")
timeline["term"] = timeline["term"].astype(int)

# Equal spacing index
timeline["x"] = range(len(timeline))

# ---------------------------------------------------------
# 2. Court ideology colour scheme
# ---------------------------------------------------------
ideology_colors = {
    "Conservative": "#ffd0d0",
    "Liberal": "#d0e7ff",
    "Mixed": "#e8e8e8",
    "Nationalist-Liberal": "#cfe2ff",
    "States' Rights-Conservative": "#ffcccc",
    "Moderate": "#f0f0f0",
    "Moderate-Liberal": "#d9e8ff",
    "Moderate-Conservative": "#ffe0e0",
    "Unknown": "#f5f5f5",
}

# ---------------------------------------------------------
# 3. Presidential transition years (for labeling only)
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

transition_years = [start for (_, _, start, _) in presidents] + [2026]

transition_positions = [
    timeline.index[timeline["term"] == year][0]
    for year in transition_years
    if year in timeline["term"].values
]

# ---------------------------------------------------------
# 4. Court-leaning timeline plot (equal spacing)
# ---------------------------------------------------------
plt.figure(figsize=(20, 10))

# Background shading by ideology
for _, row in timeline.iterrows():
    plt.axvspan(
        row["x"] - 0.5,
        row["x"] + 0.5,
        color=ideology_colors.get(row["ideology_majority_label"], "#f5f5f5"),
        alpha=0.35,
    )

plt.plot(
    timeline["x"],
    timeline["overruling_count"],
    marker="o",
    linewidth=1.5,
    label="Overrulings per Term",
    color="#1f77b4",
)

major_terms = timeline.loc[timeline["major_overruling_count"] > 0]
plt.scatter(
    major_terms["x"],
    major_terms["overruling_count"],
    color="red",
    s=80,
    label="Major Overruling Terms",
)

plt.title("SCOTUS Overrulings by Court Ideology (1790–2026)", fontsize=18)
plt.xlabel("Year (Presidential Transition Labels Only)", fontsize=14)
plt.ylabel("Overrulings", fontsize=14)


# ---------------------------------------------------------
# Filter transition years to match actual positions
# ---------------------------------------------------------
filtered_years = []
filtered_positions = []

for year in transition_years:
    matches = timeline.index[timeline["term"] == year].tolist()
    if matches:
        filtered_positions.append(matches[0])
        filtered_years.append(year)

plt.xticks(filtered_positions, filtered_years, rotation=45)


plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("court_leaning_overrulings_timeline_equal_spacing.png", dpi=300)

# ---------------------------------------------------------
# 5. PDF (Probability Density Function)
# ---------------------------------------------------------
plt.figure(figsize=(14, 6))
sns.histplot(timeline["overruling_count"], bins=20, kde=True, color="darkgreen")
plt.title("PDF of Overruling Counts per Term")
plt.xlabel("Overruling Count")
plt.ylabel("Density")
plt.tight_layout()
plt.savefig("court_leaning_overrulings_pdf.png", dpi=300)

# ---------------------------------------------------------
# 6. CDF
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
plt.savefig("court_leaning_overrulings_cdf.png", dpi=300)

print("Court-leaning timeline (equal spacing) generated.")
