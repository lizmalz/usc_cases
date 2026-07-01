import pandas as pd

# ---------------------------------------------------------
# 1. Load Legacy (1790–1945) and Modern (1946–2026) datasets
# ---------------------------------------------------------
legacy_file = "SCDB_Legacy_07_caseCentered_Citation.csv"
modern_file = "SCDB_2025_01_caseCentered_Citation.csv"

print("Loading Legacy dataset:", legacy_file)
df_legacy = pd.read_csv(legacy_file, encoding="latin1")

print("Loading Modern dataset:", modern_file)
df_modern = pd.read_csv(modern_file, encoding="latin1")

# Ensure common key columns exist in both
common_cols = [
    "term",
    "caseName",
    "dateDecision",
    "precedentAlteration",
    "majVotes",
    "minVotes",
    "chief",
    "issueArea",
]

missing_legacy = [c for c in common_cols if c not in df_legacy.columns]
missing_modern = [c for c in common_cols if c not in df_modern.columns]

if missing_legacy:
    print("Warning: Legacy missing columns:", missing_legacy)
if missing_modern:
    print("Warning: Modern missing columns:", missing_modern)

# ---------------------------------------------------------
# 2. Extract explicit overrulings from each dataset
# ---------------------------------------------------------
legacy_overrules = df_legacy.loc[df_legacy["precedentAlteration"] == 1].copy()
modern_overrules = df_modern.loc[df_modern["precedentAlteration"] == 1].copy()

print("Legacy overrulings:", len(legacy_overrules))
print("Modern overrulings:", len(modern_overrules))

# Normalize types
for df in (legacy_overrules, modern_overrules):
    df["term"] = df["term"].astype(int)
    df["dateDecision"] = pd.to_datetime(df["dateDecision"], errors="coerce")

# ---------------------------------------------------------
# 3. Select harmonized columns and concatenate
# ---------------------------------------------------------
cols_to_keep = [
    "term",
    "caseName",
    "dateDecision",
    "majVotes",
    "minVotes",
    "chief",
    "issueArea",
    "precedentAlteration",
]

legacy_overrules = legacy_overrules[cols_to_keep]
modern_overrules = modern_overrules[cols_to_keep]

full_overrules = pd.concat([legacy_overrules, modern_overrules], ignore_index=True)

# Sort chronologically
full_overrules = full_overrules.sort_values(by=["term", "dateDecision"])

print("Total overrulings (1790–2026):", len(full_overrules))

# ---------------------------------------------------------
# 4. Save unified overruling dataset
# ---------------------------------------------------------
full_overrules.to_csv("scotus_overrulings_full_1790_2026.csv", index=False)
print("Saved scotus_overrulings_full_1790_2026.csv")

# ---------------------------------------------------------
# 5. Build unified term-level timeline
# ---------------------------------------------------------
timeline = (
    full_overrules.groupby("term")
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
