from prepare_files import prepare_process_languages
from translator import translate_missing

def main():
    languages_list = ["English","French","German","Italian","Dutch","Spanish","Greek","Portuguese","Japanese","Russian","Chinese (simplified)","Arabic"]
    languagestotranslate_list = ["French"]

    prepare_process_languages(languages_list)

    for language in languagestotranslate_list:
        translate_missing(language)

if __name__ == "__main__":
   main()