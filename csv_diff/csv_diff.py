#!/usr/bin/env python3
"""
Compare two CSV files using csvdiff and output a JSON diff.
Usage:
    python csv_diff_script.py old.csv new.csv --keys id --out diff.json
    Compression is enabled by default; use --no-compress to disable.
"""

import argparse
import json
import csvdiff
import zipfile
from pathlib import Path

def save_json(path, data):
    """Save JSON data to a plain file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def save_json_zip(zip_path, json_data, inner_name="diff.json"):
    """Save JSON data inside a ZIP file."""
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(inner_name, json.dumps(json_data, indent=2, ensure_ascii=False))

def main():
    parser = argparse.ArgumentParser(description="Compute a semantic diff between two CSV files.")
    parser.add_argument("old_csv", help="Path to the old CSV file")
    parser.add_argument("new_csv", help="Path to the new CSV file")
    parser.add_argument("--keys", "-k", required=True, nargs="+", help="Primary key column(s)")
    parser.add_argument("--out", "-o", required=True, help="Output path for diff (JSON or ZIP)")
    parser.add_argument("--no-compress", action="store_false", dest="compress",
                        help="Disable compression (plain JSON output)")
    args = parser.parse_args()
    
    # Compute diff
    diff = csvdiff.diff_files(args.old_csv, args.new_csv, index_columns=args.keys)
    
    output_path = Path(args.out)
    
    if args.compress:
        save_json_zip(output_path, diff)
        print(f"✅ Diff saved and compressed to {output_path}")
    else:
        save_json(output_path, diff)
        print(f"✅ Diff saved to {output_path}")

if __name__ == "__main__":
    main()
