from prepare_files import prepare_process_languages
from translator import translate_missing_list

def main():
    languages_list = ["English","French","German","Italian","Dutch","Spanish","Greek","Portuguese","Japanese","Russian","Chinese (simplified)","Arabic"]
    languagestotranslate_list = ["French"]

    """ We prepare the missing translations by language (file compared to English.xml) """
    """ We use Excel files to store the data """
    prepare_process_languages(languages_list)

    """ We translate the missing translations with ChatGPT (gpt-5 model) """
    translate_missing_list(languagestotranslate_list)

if __name__ == "__main__":
   main()
