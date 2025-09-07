from prepare_files import prepare_process_languages
from translator import translate_missing

def main():
    #languages_list = ["English","French","German","Italian","Dutch","Spanish","Greek","Portuguese","Japanese","Russian","Chinese (simplified)","Arabic"]
    languages_list = ["French"]

    prepare_process_languages(languages_list)

    for language in languages_list:
        if language != "English":
            print(f"Processing language: {language}\n")
            translate_missing(language)


if __name__ == "__main__":
   main()