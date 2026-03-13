import csv
import json
import re
import argparse

def convert_csv_to_json(input_file, output_file):
    data_list = []

    with open(input_file, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        # Clean headers (strip spaces)
        reader.fieldnames = [h.strip() for h in reader.fieldnames]

        for row in reader:
            print(row)  # debug: see each row
            national_id = row['id'].strip()
            phone_raw = row['phone'].strip()

            # Keep only digits
            phone_digits = re.sub(r'\D', '', phone_raw)

            # Remove first digit and add 972
            if len(phone_digits) >= 1:
                phone_digits = "972" + phone_digits[1:]

            data_list.append({
                "id": national_id,
                "phone_number": phone_digits
            })

    # Write to JSON
    with open(output_file, "w", encoding="utf-8") as jsonfile:
        json.dump(data_list, jsonfile, ensure_ascii=False, indent=2)

    print(f"Converted {len(data_list)} entries to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert CSV of IDs and phones to JSON")
    parser.add_argument("-i", "--input", required=True, help="Input CSV file")
    parser.add_argument("-o", "--output", required=True, help="Output JSON file")
    args = parser.parse_args()

    convert_csv_to_json(args.input, args.output)
