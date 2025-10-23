import re
import csv

# ====== Update file paths ======
input_file = r"C:\Users\Nagendra\Documents\job_output.xml"
output_file = r"C:\Users\Nagendra\Documents\output.csv"

# Read the XML file as text
with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
    xml_text = f.read()

# Extract all <Error> ... </Error> blocks (even multiline)
error_blocks = re.findall(r"<Error.*?>(.*?)</Error>", xml_text, flags=re.DOTALL | re.IGNORECASE)

rows = []

for block in error_blocks:
    # Clean up CDATA and unnecessary characters
    text = re.sub(r"<!\[CDATA\[|\]\]>", "", block, flags=re.IGNORECASE).strip()

    # Find all individual error entries (there might be multiple inside same <Error>)
    entries = re.split(r"(?=key:)", text)  # split wherever "key:" starts
    for entry in entries:
        grgrp_match = re.search(r"grgrp\s*=\s*(\d+)", entry)
        proiv_match = re.search(r"proiv\s*=\s*(\d+)", entry)
        error_msg_match = re.search(r"Error message:\s*(.*)", entry)
        solution_match = re.search(r"Solution:\s*(.*)", entry)

        # Only add if both grgrp and proiv exist
        if grgrp_match and proiv_match:
            rows.append({
                "grgrp": grgrp_match.group(1).strip(),
                "proiv": proiv_match.group(1).strip(),
                "Error message": (error_msg_match.group(1).strip() if error_msg_match else ""),
                "Solution": (solution_match.group(1).strip() if solution_match else "")
            })

# Write output to CSV
with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["grgrp", "proiv", "Error message", "Solution"])
    writer.writeheader()
    writer.writerows(rows)

print(f"✅ Extraction complete! {len(rows)} record(s) written to {output_file}")
