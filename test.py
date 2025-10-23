import re
import csv
import xml.etree.ElementTree as ET

# ====== Update these paths according to your system ======
input_file = r"C:\Users\nagen\OneDrive\Documents\job_output.xml"  # Your input XML file
output_file = r"C:\Users\nagen\OneDrive\Documents\output.csv"     # Desired CSV output path

# Parse the XML file
tree = ET.parse(input_file)
root = tree.getroot()

# Regex patterns to extract values
grgrp_pattern = re.compile(r"grgrp=(\d+)")
proiv_pattern = re.compile(r"proiv=(\d+)")
error_pattern = re.compile(r"Error message:\s*(.*)")
solution_pattern = re.compile(r"Solution:\s*(.*)")

rows = []

# Traverse each Error node inside step -> Action -> Engine
for error_node in root.findall(".//step/Action/Engine/Error"):
    text = error_node.text
    if not text:
        continue

    # Extract values using regex
    grgrp_match = grgrp_pattern.search(text)
    proiv_match = proiv_pattern.search(text)
    error_msg_match = error_pattern.search(text)
    solution_match = solution_pattern.search(text)

    # Only include rows if both grgrp and proiv exist
    if grgrp_match and proiv_match:
        rows.append({
            "grgrp": grgrp_match.group(1),
            "proiv": proiv_match.group(1),
            "Error message": error_msg_match.group(1).strip() if error_msg_match else "",
            "Solution": solution_match.group(1).strip() if solution_match else ""
        })

# Write extracted data to CSV
with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["grgrp", "proiv", "Error message", "Solution"])
    writer.writeheader()
    writer.writerows(rows)

print(f"✅ Extraction complete! Data written to {output_file}")
