from openai import OpenAI
import pandas as pd

def translate_missing(language):
    file_missing = f"./excel/Missing/Missing_{language}.xlsx"

    df = pd.read_excel(file_missing)
    if df.empty:
      print("No missing translations found.")
      return
    
    df.set_index('Tag', inplace=True)

    number_of_rows = df.shape[0]  # len(df.index)

    tag = df.iloc[0]['Tag']
    print("Tag =", tag)

    input_text_english = df.iloc[0]['English']
    print("English =",input_text_english)
  
    client = OpenAI()

    result = client.responses.create(
        model="gpt-5",
        input=f"Translate in {language} the following text: {input_text_english}",
        reasoning={ "effort": "low" },
        text={ "verbosity": "low" },
    )

    translation = result.output_text

    print(f"{language} =", translation)
    print("\n")

    #df.iloc[0]['French'] = translation


def main():
    language = "French"
    translate_missing(language)

if __name__ == "__main__":
   main()