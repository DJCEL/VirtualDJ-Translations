import os
from openai import OpenAI
import pandas as pd
from pathlib import Path

def translate_missing(language):
    """ 
    We use ChatGPT from OpenAI to translate the missing entries in the excel file.
    Make sure to set the environment variable OPENAI_API_KEY with your API key. 
    """
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    model = "gpt-5"
    #temperature=
    #top_p=
    #max_output_tokens=

    client = OpenAI(api_key=openai_api_key)

    file_missing = Path(f"./excel/Missing/Missing_{language}.xlsx")
    file_translated = Path(f"./excel/Translated/Translated_{language}.xlsx")

    df = pd.read_excel(file_missing)
    if df.empty:
      print("No missing translations found.")
      return
   
    number_of_rows = df.shape[0]  # len(df.index)

    for row_id in range(number_of_rows):
        tag = df.loc[row_id,"Tag"]
        print("Tag =", tag)

        input_text_english = df.loc[row_id, "English"]
        print("English =",input_text_english)

        df[f"{language}"] = df[f"{language}"].astype("string")
        
        instructions = "You are a translator assistant for a DJ software named VirtualDJ."
        input_text = f"Translate in {language} the following text: {input_text_english}"

        result = client.responses.create(
            model=model,
            instructions=instructions,
            input=input_text,
            reasoning={ "effort": "low" },
            text={ "verbosity": "low" },
        )

        translation = str(result.output_text)

        print(f"{language} =", translation)
        print("\n")

        df.loc[row_id,f"{language}"] = translation
    
    df.set_index("Tag", inplace=True)
    df.to_excel(file_translated)
    print(f"Excel files saved as {file_translated}")


def main():
    language = "Italian"
    translate_missing(language)

if __name__ == "__main__":
   main()
