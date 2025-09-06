import xml.etree.ElementTree as ET
import pandas as pd

def ReadXML(xml_file:str):
    # Load and parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Recursive function to flatten XML structure
    def flatten_xml(element, parent_path=""):
        rows = []
        tag_path = f"{parent_path}_{element.tag}" if parent_path else element.tag
    
        # If element has text and it's not just whitespace, save it
        if element.text and element.text.strip():
            rows.append((tag_path, element.text.strip()))
    
        # Process attributes (with @ prefix)
        for attr, value in element.attrib.items():
            rows.append((f"{tag_path}_@{attr}", value))
    
        # Recurse into children
        for child in element:
            rows.extend(flatten_xml(child, tag_path))
    
        return rows

    # Flatten the whole XML tree
    flattened_data = flatten_xml(root)

    # Create DataFrame
    df = pd.DataFrame(flattened_data, columns=["Tag", "Value"])
 
    return df

def main():
   filepath1 = "../English.xml"
   filepath2 = "../French.xml"
   output_file1 = "./excel/English_flattened.xlsx"
   output_file2 = "./excel/French_flattened.xlsx"

   df1 = ReadXML(filepath1)
   df2 = ReadXML(filepath2)

   # Save to Excel
   df1.to_excel(output_file1, index=False)
   df2.to_excel(output_file2, index=False)
   print(f"Excel files saved as {output_file1} and {output_file2}")

if __name__ == "__main__":
    main()
