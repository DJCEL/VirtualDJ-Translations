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
   filepath1 = "../Languages/English.xml"
   filepath2 = "../Languages/French.xml"
   filepath3 = "../Languages/German.xml"
   filepath4 = "../Languages/Italian.xml"
   output_file1 = "./excel/English_flattened.xlsx"
   output_file2 = "./excel/French_flattened.xlsx"
   output_file3 = "./excel/German_flattened.xlsx"
   output_file4 = "./excel/Italian_flattened.xlsx"
   output_file_merged = "./excel/Compare_Files.xlsx"
   output_file_french_missing = "./excel/Missing_in_French.xlsx"
   output_file_german_missing = "./excel/Missing_in_German.xlsx"
   output_file_italian_missing = "./excel/Missing_in_Italian.xlsx"

   df1 = ReadXML(filepath1,"English")
   df2 = ReadXML(filepath2,"French")
   df3 = ReadXML(filepath3,"German")
   df4 = ReadXML(filepath4,"Italian")

   # Save to Excel files
   df1.to_excel(output_file1)
   print(f"Excel files saved as {output_file1}")
   df2.to_excel(output_file2)
   print(f"Excel files saved as {output_file2}")
   df3.to_excel(output_file3)
   print(f"Excel files saved as {output_file3}")
   df4.to_excel(output_file4)
   print(f"Excel files saved as {output_file4}")

   df100 = pd.concat([df1, df2, df3 ,df4], axis=1, join="outer")
   df100.to_excel(output_file_merged)
   print(f"Merged Excel file saved as {output_file_merged}")

   filter_french_missing = df100["French"].isna() | (df100["French"].str.strip() == "")
   filter_german_missing = df100["German"].isna() | (df100["German"].str.strip() == "")
   filter_italian_missing = df100["Italian"].isna() | (df100["Italian"].str.strip() == "")

   df102 = df100.loc[filter_french_missing,["English","French"]]
   df102.to_excel(output_file_french_missing)
   print(f"Missing French translations Excel file saved as {output_file_french_missing}")

   df103 = df100.loc[filter_german_missing,["English","German"]]
   df103.to_excel(output_file_german_missing)
   print(f"Missing German translations Excel file saved as {output_file_german_missing}")

   df103 = df100.loc[filter_italian_missing,["English","Italian"]]
   df103.to_excel(output_file_italian_missing)
   print(f"Missing Italian translations Excel file saved as {output_file_italian_missing}")


if __name__ == "__main__":
   main()