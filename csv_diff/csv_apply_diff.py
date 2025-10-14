#!/usr/bin/env python3
"""
Apply a csvdiff patch to reconstruct a CSV.
Usage:
    python apply_patch.py old.csv diff.zip --out new.csv
    Decompression is enabled by default; use --nodecompress for plain JSON.
"""

import csv
import json
import argparse
import zipfile
from pathlib import Path

# --- 1️⃣ Load CSV into dict keyed by primary key(s) ---
def load_csv_to_dict(csv_path, keys):
    table = {}
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key_val = tuple(row[k] for k in keys)
            table[key_val] = row
    return table, reader.fieldnames

# --- 2️⃣ Load patch (from ZIP or plain JSON) ---
def load_patch(patch_path, decompress=True, inner_name="diff.json"):
    patch_path = Path(patch_path)
    if decompress:
        with zipfile.ZipFile(patch_path, 'r') as zf:
            with zf.open(inner_name) as f:
                return json.load(f)
    else:
        with open(patch_path, 'r', encoding='utf-8') as f:
            return json.load(f)

# --- 3️⃣ Apply patch ---
def apply_patch(table, patch):
    keys = patch["_index"]  # extract keys from patch
    for row in patch.get("removed", []):
        key_val = tuple(row[k] for k in keys)
        table.pop(key_val, None)
    for row in patch.get("added", []):
        key_val = tuple(row[k] for k in keys)
        table[key_val] = row
    for change in patch.get("changed", []):
        key_val = tuple(change["key"])
        for col, val in change["fields"].items():
            table[key_val][col] = val["to"]

# --- 4️⃣ Write CSV ---
def write_dict_to_csv(table, fieldnames, output_path, keys):
    sorted_rows = sorted(table.values(), key=lambda r: tuple(r[k] for k in keys))
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sorted_rows)

# --- 5️⃣ Main ---
def main():
    parser = argparse.ArgumentParser(description="Apply a csvdiff patch to reconstruct a CSV")
    parser.add_argument("old_csv", help="Original CSV path")
    parser.add_argument("patch_file", help="Patch file path (ZIP or JSON)")
    parser.add_argument("--out", "-o", required=True, help="Output CSV path")
    parser.add_argument("--nodecompress", action="store_true",
                        help="Disable decompression; read plain JSON instead of ZIP")
    args = parser.parse_args()

    # Load patch first to extract keys
    patch = load_patch(args.patch_file, decompress=not args.nodecompress)
    keys = patch["_index"]

    # Load original CSV using patch keys
    table, fieldnames = load_csv_to_dict(args.old_csv, keys)

    # Apply patch
    apply_patch(table, patch)

    # Write new CSV
    write_dict_to_csv(table, fieldnames, args.out, keys)
    print(f"✅ Patch applied. Output written to {args.out}")

if __name__ == "__main__":
    main()
