
import pandas as pd
from thefuzz import process
import logging
import sys
import re

def sanitize(text):
    text = str(text).strip().lower()
    text = re.sub(r'[^a-z0-9 ]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def normalize_and_key(df, required_cols):
    for col in required_cols:
        df[col] = df[col].fillna("").apply(sanitize)
    df["key"] = df[required_cols[0]] + "|" + df[required_cols[1]] + "|" + df[required_cols[2]]
    return df

def deduplicate(df):
    return df.drop_duplicates(subset="key")

def find_fuzzy_matches(keys, threshold=90):
    fuzzy_matches = []
    for i, key in enumerate(keys):
        results = process.extract(key, keys, limit=5)
        for match_key, score in results:
            if score >= threshold and match_key != key:
                fuzzy_matches.append((key, match_key, score))
    return fuzzy_matches

# Main script logic
INPUT_FILE = "dedup_input.xlsx"
OUTPUT_FILE = "deduped_contacts.xlsx"
NEAR_DUP_FILE = "near_duplicates.xlsx"
REQUIRED_COLS = ["First Name", "Last Name", "Address"]

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def main():
    try:
        df = pd.read_excel(INPUT_FILE)
        logging.info(f"Loaded {len(df)} rows from {INPUT_FILE}")
    except Exception as e:
        logging.error(f"Failed to read input file: {e}")
        sys.exit(1)

    missing_cols = [col for col in REQUIRED_COLS if col not in df.columns]
    if missing_cols:
        logging.error(f"Missing required columns: {missing_cols}")
        sys.exit(1)

    df = normalize_and_key(df, REQUIRED_COLS)
    df_exact = deduplicate(df)
    logging.info(f"Exact deduplication reduced to {len(df_exact)} rows")

    keys = df_exact["key"].tolist()
    fuzzy_matches = find_fuzzy_matches(keys, threshold=90)

    if fuzzy_matches:
        logging.info(f"Found {len(fuzzy_matches)} fuzzy near-duplicate pairs (score >= 90):")
        for k1, k2, score in fuzzy_matches:
            logging.info(f"  '{k1}' <-> '{k2}' (score: {score})")
    else:
        logging.info("No fuzzy near-duplicates found.")

    try:
        df_exact.to_excel(OUTPUT_FILE, index=False)
        logging.info(f"Deduped data exported to {OUTPUT_FILE}")
    except Exception as e:
        logging.error(f"Failed to write output file: {e}")

    if fuzzy_matches:
        df_near_dupes = pd.DataFrame(fuzzy_matches, columns=["Key 1", "Key 2", "Score"])
        try:
            df_near_dupes.to_excel(NEAR_DUP_FILE, index=False)
            logging.info(f"Near-duplicate pairs exported to {NEAR_DUP_FILE}")
        except Exception as e:
            logging.error(f"Failed to write near-duplicates file: {e}")

if __name__ == "__main__":
    main()