import xml.etree.ElementTree as ET
import pandas as pd

def ReadXML(xml_file:str, colname:str):
    # Load and parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Recursive function to flatten XML structure
    def flatten_xml(element, parent_path=""):
        rows = []
        element_tag = element.tag

        # Process attributes
        tag_attr = ""
        for attr, value in element.attrib.items():
            tag_attr = tag_attr + f' {attr}="{value}"'

        if tag_attr != "":
            element_tag = element_tag + tag_attr

        if parent_path == "":
            tag_path = f"<{element_tag}>"
        elif parent_path.startswith("<language lang="):
            tag_path = f"<{element_tag}>"     
        else:
            tag_path = f"{parent_path}<{element_tag}>"

        # If element has text and it's not just whitespace, save it
        if element.text and element.text.strip():
            tag_value = (tag_path, element.text.strip())
            rows.append(tag_value)
    
        # Recurse into children
        for child in element:
            rows.extend(flatten_xml(child, tag_path))
    
        return rows

    # Flatten the whole XML tree
    flattened_data = flatten_xml(root)

    # Create DataFrame
    df = pd.DataFrame(flattened_data, columns=["Tag", colname])

    df.set_index("Tag", inplace=True)
 
    return df

def main():
   filepath1 = "../English.xml"
   filepath2 = "../French.xml"
   output_file1 = "./excel/English_flattened.xlsx"
   output_file2 = "./excel/French_flattened.xlsx"
   output_file_merged = "./excel/Compare_Files.xlsx"
   output_file_missing = "./excel/Missing_in_French.xlsx"

   df1 = ReadXML(filepath1,"English")
   df2 = ReadXML(filepath2,"French")

   # Save to Excel
   df1.to_excel(output_file1)
   df2.to_excel(output_file2)
   print(f"Excel files saved as {output_file1} and {output_file2}")

   df3 = pd.concat([df1, df2], axis=1, join="outer")
   df3.to_excel(output_file_merged)
   print(f"Merged Excel file saved as {output_file_merged}")

   filter_missing = df3["French"].isna() | (df3["French"].str.strip() == "")

   df4 = df3[filter_missing]
   df4.to_excel(output_file_missing)
   print(f"Missing translations Excel file saved as {output_file_missing}")


if __name__ == "__main__":
   main()