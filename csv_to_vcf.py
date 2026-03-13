import csv

csv_file = 'contacts.csv'   # your CSV file
vcf_file = 'contacts.vcf'   # output vCard file

with open(csv_file, newline='', encoding='utf-8') as f_csv, open(vcf_file, 'w', encoding='utf-8') as f_vcf:
    reader = csv.DictReader(f_csv)
    for row in reader:
        name = row['Name']
        given = row.get('Given Name', '')
        family = row.get('Family Name', '')
        phone = row['Phone']

        # Normalize Israeli mobile numbers starting with 05
        if phone.startswith('05'):
            phone = phone.replace('-', '')          # remove dashes
            phone = '+972' + phone[1:]              # replace leading 0 with +972

        f_vcf.write('BEGIN:VCARD\n')
        f_vcf.write('VERSION:3.0\n')
        f_vcf.write(f'FN:{name}\n')
        f_vcf.write(f'N:{family};{given};;;\n')
        f_vcf.write(f'TEL;TYPE=CELL:{phone}\n')
        f_vcf.write('END:VCARD\n\n')

print(f"vCard saved to {vcf_file}")
