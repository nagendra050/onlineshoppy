import xml.etree.ElementTree as ET
import csv
import re

# ====== Update file paths ======
input_file = r"C:\Users\Nagendra\Documents\job_output.xml"
output_file = r"C:\Users\Nagendra\Documents\output.csv"

# ====== Parse XML ======
tree = ET.parse(input_file)
root = tree.getroot()

data = []

# ====== Traverse all <Error> nodes ======
for step in root.findall(".//step"):
    step_number = step.attrib.get("number", "")
    for action in step.findall(".//Action"):
        action_number = action.attrib.get("number", "")
        for engine in action.findall(".//Engine"):
            for error in engine.findall("Error"):
                cdata_text = error.text
                if not cdata_text:
                    continue

                # Normalize whitespace
                cdata_text = cdata_text.strip()

                # Split multiple logical keys inside one <Error>
                blocks = re.split(r'(?=key:\s*Logical key:)', cdata_text, flags=re.IGNORECASE)

                for block in blocks:
                    block = block.strip()
                    if not block:
                        continue

                    # Extract fields
                    grgrp_match = re.search(r"grgrp\s*=\s*(\d+)", block)
                    proiv_match = re.search(r"proiv\s*=\s*(\d+)", block)
                    errmsg_match = re.search(r"Error message:\s*(.*?)(?:Solution:|$)", block, re.DOTALL | re.IGNORECASE)
                    solution_match = re.search(r"Solution:\s*(.*?)(?:\n|$)", block, re.DOTALL | re.IGNORECASE)

                    if grgrp_match and proiv_match:
                        grgrp = grgrp_match.group(1)
                        proiv = proiv_match.group(1)
                        errmsg = errmsg_match.group(1).strip() if errmsg_match else ""
                        solution = solution_match.group(1).strip() if solution_match else ""

                        # Skip empty solution lines like 'Hello'
                        solution = solution.splitlines()[0].strip()

                        data.append([grgrp, proiv, errmsg, solution])

                        print(f"Step={step_number}, Action={action_number}, grgrp={grgrp}, proiv={proiv}, Error='{errmsg}', Solution='{solution}'")

# ====== Write to CSV ======
if data:
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["grgrp", "proiv", "Error message", "Solution"])
        writer.writerows(data)
    print(f"\n✅ Extraction complete! {len(data)} rows saved to: {output_file}")
else:
    print("\n❌ No valid records found.")
