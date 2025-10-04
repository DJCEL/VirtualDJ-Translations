import xml.etree.ElementTree as ET
import pandas as pd
from pathlib import Path
import sys

# Function to add elements recursively
def add_elements(language, parent, df, parent_tag=""):
        for tag in df.index:
            if tag.startswith(parent_tag) or parent_tag == "":
                parts = tag.split("><")
                current_tag = parts[0].replace("<", "").replace(">", "")
                if len(parts) > 1:
                    child_tag = "><".join(parts[1:]).replace("<", "").replace(">", "")
                else:
                    child_tag = ""
                # Check if the current tag already exists under the parent
                existing = parent.find(current_tag)
                if existing is None:
                    elem = ET.SubElement(parent, current_tag)
                else:
                    elem = existing
                
                # If there's a value, set it
                if child_tag and tag in df.index:
                    value = df.at[tag, language]
                    if pd.notna(value):
                        elem.text = str(value)

                # Recurse for children
                parent_tag_new = f"{parent_tag}<{current_tag}>"
                add_elements(language, elem, df, parent_tag_new)


def generate_xml(language: str):
    input_excel = Path(f"./excel/Translated/Translated_{language}.xlsx")
    output_xml = Path(f"./xml/Translated_{language}_v2.xml")

    if not input_excel.exists():
        print(f"Input Excel file does not exist: {input_excel}")
        return

    # Read the Excel file
    df = pd.read_excel(input_excel)
    if df.empty:
      print("input_excel file is empty.")
      return

    df.set_index("Tag", inplace=True)
    
    # Create the root element
    root = ET.Element("language", lang=language, iso="fr", author="ChatGPT")

    # Start adding elements from the root
    add_elements(language, root, df)

    # Create the tree and write to XML file
    tree = ET.ElementTree(root)
    tree.write(output_xml, encoding="UTF-8", xml_declaration=True)

    print(f"Generated XML file: {output_xml}")