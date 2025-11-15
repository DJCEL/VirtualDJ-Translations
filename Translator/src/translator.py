import os
from openai import OpenAI
import pandas as pd
from pathlib import Path

def translate_missing(language:str, client, model:str):
    print(f"Processing translation for: {language}\n")

    file_missing = Path(f"./excel/Missing/Missing_{language}.xlsx")
    file_translated = Path(f"./excel/Translated/Translated_{language}.xlsx")

    df = pd.read_excel(file_missing)
    if df.empty:
      print("No missing translations found.")
      return
   
    number_of_rows = df.shape[0]  # len(df.index)

    for row_id in range(number_of_rows):
        print(f"Step {row_id+1}/{number_of_rows}")

        input_text_english = df.loc[row_id, "English"]
        print("<English>" + input_text_english + "</English>")

        df[f"{language}"] = df[f"{language}"].astype("string")
        
        instructions = f"You are a English-{language} translator assistant for a DJ software named VirtualDJ."
        input_text = f"Translate in {language} the following text: {input_text_english}"
        #temperature=
        #top_p=
        #max_output_tokens=

        result = client.responses.create(
            model=model,
            instructions=instructions,
            input=input_text,
            reasoning={ "effort": "low" },
            text={ "verbosity": "low" },
        )

        translation = str(result.output_text)

        print(f"<{language}>" + translation + f"</{language}>")
        df.loc[row_id,f"{language}"] = translation
        
        df.to_excel(file_translated, index=False)
        print(f"Excel file saved as {file_translated}\n")


def translate_missing_list(languagestotranslate_list):
    """ 
    Translates the missing entries in the excel file.

    We use ChatGPT from OpenAI (gpt-5 model).
    Make sure to set the environment variable OPENAI_API_KEY with your API key. 
    """
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("Please set the OPENAI_API_KEY environment variable.")

    openai_model = "gpt-5"

    client = OpenAI(api_key=openai_api_key)

    for language in languagestotranslate_list:
        if language != "English":
            translate_missing(language, client, openai_model)

    print("All translations done.")

def check_current_translation(language:str, explanations_language = "English"):
    """
    Verifies the existing translations in the excel file.
    If you want comments in another language, change explanations_language variable.

    :param language: language to check (e.g. "French")
    :param explanations_language: language for comments if translation is NOK (by default "English")

    We use ChatGPT from OpenAI (gpt-5 model).
    Make sure to set the environment variable OPENAI_API_KEY with your API key.
    """

    print(f"Processing checks of translation for {language} with NOK comments in {explanations_language}\n")

    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("Please set the OPENAI_API_KEY environment variable.")

    openai_model = "gpt-5"

    merged_languages = Path("./excel/All_Translations.xlsx")
    compare_translation = Path(f"./excel/Compare/Compare_{language}.xlsx")
   
    df_all = pd.read_excel(merged_languages)
    df = df_all.loc[~df_all["English"].isna() ,["Tag","English",f"{language}"]]

    df["Compare"] = ""
    df["Commments"] = ""

    number_of_rows = df.shape[0]  # len(df.index)

    client = OpenAI(api_key=openai_api_key)

    for row_id in range(number_of_rows):
        input_text_english = df.loc[row_id, "English"]
        input_text_translated = df.loc[row_id, f"{language}"]
        
        step_id = row_id+1
        print(f"Step {step_id}/{number_of_rows}")
        print(f"<English>{input_text_english}</English>")
        print(f"<{language}>{input_text_translated}</{language}")

        instructions = f"You are a English-{language} translator assistant for a DJ software named VirtualDJ."
        input_text = f"Check if the following {language} translation is correct for the following English text. Answer only 'OK' or 'NOK'. If 'NOK', then explain briefly why in {explanations_language} between xml tag 'Comments'\n\n<English>{input_text_english}</English><{language}>{input_text_translated}</{language}>"

        res1 = client.responses.create(
            model=openai_model,
            instructions=instructions,
            input=input_text,
            reasoning={ "effort": "low" },
            text={ "verbosity": "low" },
        )

        result_translated = str(res1.output_text)
       
        is_NOK = result_translated.startswith("NOK")
        position_comments = result_translated.find("<Comments>")
        if is_NOK == True and position_comments != -1:
            answer_status = result_translated[:position_comments].strip()
            comments_tmp = result_translated[position_comments:].strip()
            comments = comments_tmp.replace("<Comments>","").replace("</Comments>","").strip()
            print(f"<Result>{answer_status}</Result>")
            print(f"<Comments>{comments}</Comments>")
            df.loc[row_id,"Compare"] = answer_status
            df.loc[row_id,"Commments"] = comments
        else:
            answer_status = result_translated
            print(f"<Result>{answer_status}</Result>")
            df.loc[row_id,"Compare"] = answer_status
         

        df.to_excel(compare_translation, index=False)
        print(f"Excel file saved as {compare_translation}\n")

    print("All checks done.")