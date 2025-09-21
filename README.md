# Deduplication Script

This project provides a Python script to deduplicate contact records in an Excel file using both exact and fuzzy matching.

## Features
- Removes exact duplicates based on normalized name and address fields
- Identifies fuzzy near-duplicates using string similarity
- Exports deduped contacts and near-duplicate pairs to separate Excel files
- Logs progress and errors

## Requirements
- Python 3.12+
- See `requirements.txt` for required packages

## Installation
1. Create and activate a virtual environment (recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```


## Usage
1. Place your input Excel file in the project directory and name it `dedup_input.xlsx` (or update the `INPUT_FILE` variable in the script to match your filename).
2. Run the script:
   ```bash
   python dedup.py
   ```
3. Output files:
   - `deduped_contacts.xlsx`: deduplicated contacts
   - `near_duplicates.xlsx`: fuzzy near-duplicate pairs

> **Note:** The script requires the `openpyxl` engine for reading/writing `.xlsx` files. This is included in `requirements.txt`.

## Customization
- To change input/output file names, edit the variables at the top of the script.
- Adjust the fuzzy match threshold in the script if needed.

## Troubleshooting
- Ensure your input file has the columns: `First Name`, `Last Name`, `Address`.
- The script sanitizes these columns by removing non-alphanumeric characters (except spaces), collapsing whitespace, and converting to lowercase for reliable matching.
- If you see import errors, make sure all packages from `requirements.txt` are installed in your environment.

## License
MIT
