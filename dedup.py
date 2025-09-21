
import pandas as pd
from thefuzz import process  # pip install pandas thefuzz
import openpyxl
import logging
import sys

# Configurable file paths
INPUT_FILE = "dedup_input.xlsx"
OUTPUT_FILE = "deduped_contacts.xlsx"

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

REQUIRED_COLS = ["First Name", "Last Name", "Address"]

try:
    df = pd.read_excel(INPUT_FILE)
    logging.info(f"Loaded {len(df)} rows from {INPUT_FILE}")
except Exception as e:
    logging.error(f"Failed to read input file: {e}")
    sys.exit(1)

# Validate columns
missing_cols = [col for col in REQUIRED_COLS if col not in df.columns]
if missing_cols:
    logging.error(f"Missing required columns: {missing_cols}")
    sys.exit(1)

# Normalize key fields and handle missing values
for col in REQUIRED_COLS:
    df[col] = df[col].fillna("").astype(str).str.strip().str.lower()

# Create unique key
df["key"] = df["First Name"] + "|" + df["Last Name"] + "|" + df["Address"]

# Drop exact duplicates
df_exact = df.drop_duplicates(subset="key")
logging.info(f"Exact deduplication reduced to {len(df_exact)} rows")

# Fuzzy near-duplicates (optional)
keys = df_exact["key"].tolist()
fuzzy_matches = []
for i, key in enumerate(keys):
    # Find near-duplicates for each key
    results = process.extract(key, keys, limit=5)
    for match_key, score in results:
        if score >= 90 and match_key != key:
            fuzzy_matches.append((key, match_key, score))

if fuzzy_matches:
    logging.info(f"Found {len(fuzzy_matches)} fuzzy near-duplicate pairs (score >= 90):")
    for k1, k2, score in fuzzy_matches:
        logging.info(f"  '{k1}' <-> '{k2}' (score: {score})")
else:
    logging.info("No fuzzy near-duplicates found.")



# Export deduped data
try:
    df_exact.to_excel(OUTPUT_FILE, index=False)
    logging.info(f"Deduped data exported to {OUTPUT_FILE}")
except Exception as e:
    logging.error(f"Failed to write output file: {e}")

# Export fuzzy near-duplicates to a separate file
NEAR_DUP_FILE = "near_duplicates.xlsx"
if fuzzy_matches:
    df_near_dupes = pd.DataFrame(fuzzy_matches, columns=["Key 1", "Key 2", "Score"])
    try:
        df_near_dupes.to_excel(NEAR_DUP_FILE, index=False)
        logging.info(f"Near-duplicate pairs exported to {NEAR_DUP_FILE}")
    except Exception as e:
        logging.error(f"Failed to write near-duplicates file: {e}")