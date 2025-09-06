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
            tag_attr = tag_attr + f" {attr}='{value}'"

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


def process_languages(languages_list):
    df_languages_list = []

    for language in languages_list:
       print(f"Processing language: {language}")
       filepath = f"../Languages/{language}.xml"
       df = ReadXML(filepath,f"{language}")
       df_languages_list.append(df)
       output_file = f"./excel/Flattened/Flattened_{language}.xlsx"
       df.to_excel(output_file)
       print(f"Excel files saved as {output_file}")
       
    output_file_merged = "./excel/Compare_Files.xlsx"
    df_merged = pd.concat(df_languages_list, axis=1, join="outer")
    df_merged.to_excel(output_file_merged)
    print(f"Merged all languages in Excel file saved as {output_file_merged}")

    for language in languages_list:
       if language != "English":
           print(f"Processing missing translation for language: {language}")
           filter_missing = (df_merged[f"{language}"].isna() | (df_merged[f"{language}"].str.strip() == "")) & (df_merged["English"].notna() & (df_merged["English"].str.strip() != ""))
           df_missing = df_merged.loc[filter_missing,["English",f"{language}"]]
           output_file_missing = f"./excel/Missing/Missing_{language}.xlsx"
           df_missing.to_excel(output_file_missing)
           print(f"Missing {language} translations Excel file saved as {output_file_missing}")

def main():
   languages_list = ["English","French","German","Italian","Dutch","Spanish","Greek","Portuguese","Japanese","Russian","Chinese (simplified)","Arabic"]

   process_languages(languages_list)


if __name__ == "__main__":
   main()