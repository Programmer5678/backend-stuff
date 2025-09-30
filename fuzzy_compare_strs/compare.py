#!/usr/bin/env python3
"""
Compare two strings from files using python-Levenshtein and show edit operations.
"""

import argparse
import Levenshtein
import pandas as pd

def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        s = f.read()
        return "".join(s.split()) # strip optional whitespace/newlines


def print_char_read_success_rates(ops, a, b):
    chars = {}
    fails = {"replace": {}, "delete": {}, "insert": {}, "replaced_by": {}}

    # Count total occurrences in `a`
    for c in a:
        chars[c] = chars.get(c, 0) + 1

    # Count failures per operation type
    for op, i, j in ops:
        if op == "replace":
            fails["replace"][a[i]] = fails["replace"].get(a[i], 0) + 1
            fails["replaced_by"][b[j]] = fails["replace"].get(b[j], 0) + 1
            
            if b[j] not in chars:
                chars[b[j]] = 0  # new character from replace
                
        elif op == "delete":
            fails["delete"][a[i]] = fails["delete"].get(a[i], 0) + 1
        elif op == "insert":
            fails["insert"][b[j]] = fails["insert"].get(b[j], 0) + 1
            if b[j] not in chars:
                chars[b[j]] = 0  # new character from insert



    result_rows = []

    for c, total_count in chars.items():
        delete_fail = fails["delete"].get(c, 0)
        replace_fail = fails["replace"].get(c, 0)
        insert_fail = fails["insert"].get(c, 0)
        total_without_replaced_by_fail = delete_fail + replace_fail + insert_fail
        replaced_by_fail = fails["replaced_by"].get(c, 0)

        delete_rate = (total_count - delete_fail) / total_count * 100 if total_count > 0 else 0
        replace_rate = (total_count - replace_fail) / total_count * 100 if total_count > 0 else 0
        insert_rate = (total_count - insert_fail) / total_count * 100 if total_count > 0 else 0
        total_rate = (total_count - total_without_replaced_by_fail) / total_count * 100 if total_count > 0 else 0
        replaced_by_fail_rate = (total_count - replaced_by_fail) / total_count * 100 if total_count > 0 else 0
        
        result_rows.append({
            "Character": c,
            
            "delete_fail": delete_fail,
            "delete_rate": delete_rate,
            
            "replace_fail": replace_fail,
            "replace_rate": replace_rate,
            
            "insert_fail": insert_fail,
            "insert_rate": insert_rate,
            
            "total_without_replaced_by_fail": total_without_replaced_by_fail,
            "total_rate": total_rate,
            
            "replaced_by_fail": replaced_by_fail,
            "replaced_by_fail_rate": replaced_by_fail_rate,
            
            "total_count": total_count,
        })

    results=pd.DataFrame(result_rows)    
    results = results.sort_values(by="total_rate")    
    results.to_csv("compare_output.csv", index=False)


    # print(results.to_string(index=False))

    # print with reverse indexing
    n = len(results)
    for idx, row in enumerate(results.itertuples()):
        reverse_idx = n - idx
        print(
            f"{reverse_idx}: Character '{row.Character}': "
            f"{row.delete_fail}/{row.total_count} deletes ({row.delete_rate:.2f}%), "
            f"{row.insert_fail}/{row.total_count} inserts ({row.insert_rate:.2f}%), "
            f"{row.replace_fail}/{row.total_count} replaces ({row.replace_rate:.2f}%), "
            f"{row.total_without_replaced_by_fail}/{row.total_count} total ({row.total_rate:.2f}%), "
            f"{row.replaced_by_fail}/{row.total_count} replaced_by ({row.replaced_by_fail_rate:.2f}%)"
        )

            
    

def print_stats(ops, len_a):
    # total_ops = len(ops)
    replace_ops = sum(1 for op, _, _ in ops if op == "replace")
    delete_ops = sum(1 for op, _, _ in ops if op == "delete")
    insert_ops = sum(1 for op, _, _ in ops if op == "insert")

    print("\nSuccess Rates:")
    if len_a > 0:
        print(f"Replace operations: {replace_ops} ({(replace_ops / len_a) * 100:.2f}%)")
        print(f"Delete operations:  {delete_ops} ({(delete_ops / len_a) * 100:.2f}%)")
        print(f"Insert operations:  {insert_ops} ({(insert_ops / len_a) * 100:.2f}%)")
    else:
        print("No edit operations found.")

def print_edit_operations(ops, a, b):
    for op, i, j in ops:
        if op == "replace":
            print(f"[REPLACE] a[{i}] '{a[i]}' -> b[{j}] '{b[j]}'")
        elif op == "delete":
            print(f"[DELETE]  a[{i}] '{a[i]}' (deleted in b)")
        elif op == "insert":
            print(f"[INSERT]  b[{j}] '{b[j]}' (inserted in b)")

def print_summary(ops):
    print("\nSummary:")
    a_indices = [i for op, i, _ in ops if op in ("replace", "delete")]
    b_indices = [j for op, _, j in ops if op in ("replace", "insert")]
    if a_indices:
        print(f"Edits start around a[{min(a_indices)}]")
    if b_indices:
        print(f"Edits start around b[{min(b_indices)}]")

def compare_strings(a, b):
    ops = Levenshtein.editops(a, b)
    if not ops:
        print("The strings are identical!")
        return

    print(f"Found {len(ops)} edit operations:\n")
    print_edit_operations(ops, a, b)
    print_summary(ops)
    print_stats(ops, len(a) )
    print_char_read_success_rates(ops, a, b)

        
        

def main():
    parser = argparse.ArgumentParser(
        description="Compare two strings from files using python-Levenshtein."
    )
    parser.add_argument("file1", help="Path to first string file")
    parser.add_argument("file2", help="Path to second string file")
    args = parser.parse_args()

    a = read_file(args.file1)
    b = read_file(args.file2)

    compare_strings(a, b)


main()
