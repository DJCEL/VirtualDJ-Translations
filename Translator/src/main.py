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
   languages_list = ["English","French","German","Italian","Dutch","Spanish","Greek","Portuguese","Japanese","Russian","Chinese (simplified)","Arabic"]

   filepath_English = "../Languages/English.xml"
   output_file_English = "./excel/English_flattened.xlsx"
   filepath_French = "../Languages/French.xml"
   output_file_French = "./excel/French_flattened.xlsx"
   filepath_German = "../Languages/German.xml"
   output_file_German = "./excel/German_flattened.xlsx"
   filepath_Italian = "../Languages/Italian.xml"
   output_file_Italian = "./excel/Italian_flattened.xlsx"

   df_English = ReadXML(filepath_English,"English")
   df_French = ReadXML(filepath_French,"French")
   df_German = ReadXML(filepath_German,"German")
   df_Italian = ReadXML(filepath_Italian,"Italian")

   # Save to Excel files
   df_English.to_excel(output_file_English)
   print(f"Excel files saved as {output_file_English}")
   df_French.to_excel(output_file_French)
   print(f"Excel files saved as {output_file_French}")
   df_German.to_excel(output_file_German)
   print(f"Excel files saved as {output_file_German}")
   df_Italian.to_excel(output_file_Italian)
   print(f"Excel files saved as {output_file_Italian}")

   output_file_merged = "./excel/Compare_Files.xlsx"
   df100 = pd.concat([df_English, df_French, df_German ,df_Italian], axis=1, join="outer")
   df100.to_excel(output_file_merged)
   print(f"Merged Excel file saved as {output_file_merged}")


   output_file_missing_French = "./excel/Missing_in_French.xlsx"
   output_file_missing_German = "./excel/Missing_in_German.xlsx"
   output_file_missing_Italian = "./excel/Missing_in_Italian.xlsx"

   filter_missing_French = df100["French"].isna() | (df100["French"].str.strip() == "")
   filter_missing_German = df100["German"].isna() | (df100["German"].str.strip() == "")
   filter_missing_Italian = df100["Italian"].isna() | (df100["Italian"].str.strip() == "")

   df102 = df100.loc[filter_missing_French,["English","French"]]
   df102.to_excel(output_file_missing_French)
   print(f"Missing French translations Excel file saved as {output_file_missing_French}")

   df103 = df100.loc[filter_missing_German,["English","German"]]
   df103.to_excel(output_file_missing_German)
   print(f"Missing German translations Excel file saved as {output_file_missing_German}")

   df103 = df100.loc[filter_missing_Italian,["English","Italian"]]
   df103.to_excel(output_file_missing_Italian)
   print(f"Missing Italian translations Excel file saved as {output_file_missing_Italian}")


if __name__ == "__main__":
   main()