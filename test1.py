import xml.etree.ElementTree as ET
import csv
import re

# ====== File paths ======
input_file = r"C:\Users\nagen\OneDrive\Documents\job_output.xml"
output_file = r"C:\Users\nagen\OneDrive\Documents\output.csv"

# ====== Parse XML ======
tree = ET.parse(input_file)
root = tree.getroot()

data = []

# ====== Traverse to all <Error> nodes ======
for error in root.findall(".//Error"):
    cdata_text = error.text
    if not cdata_text:
        continue

    # Clean up whitespace
    cdata_text = cdata_text.strip()

    # Split multiple logical keys inside one <Error>
    # Each block starts with 'key: Logical key:'
    blocks = re.split(r"key:\s*Logical key:", cdata_text)
    
    for block in blocks:
        block = block.strip()
        if not block:
            continue

        # Add back 'key: Logical key:' to simplify regex
        block = "key: Logical key:" + block

        # Extract fields
        grgrp_match = re.search(r"grgrp\s*=\s*(\d+)", block)
        proiv_match = re.search(r"proiv\s*=\s*(\d+)", block)
        errmsg_match = re.search(r"Error message:\s*(.*?)\s*Solution:", block, re.DOTALL)
        solution_match = re.search(r"Solution:\s*(.*)", block, re.DOTALL)

        if grgrp_match and proiv_match:
            grgrp = grgrp_match.group(1)
            proiv = proiv_match.group(1)
            errmsg = errmsg_match.group(1).strip() if errmsg_match else ""
            solution = solution_match.group(1).strip() if solution_match else ""

            print(f"Found: grgrp={grgrp}, proiv={proiv}, Error='{errmsg}', Solution='{solution}'")
            data.append([grgrp, proiv, errmsg, solution])

# ====== Write to CSV ======
if data:
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["grgrp", "proiv", "Error message", "Solution"])
        writer.writerows(data)
    print(f"\n✅ Extraction complete! {len(data)} rows saved to: {output_file}")
else:
    print("\n❌ No valid records found.")
