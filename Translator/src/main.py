from prepare_files import prepare_process_languages
from translator import translate_missing_list
from translator import check_current_translation

def main():
    languages_list = ["English","French","German","Italian","Dutch","Spanish","Greek","Portuguese","Japanese","Russian","Chinese (simplified)","Arabic"]
    languagestotranslate_list = ["French"]
    bPrepare_step = True
    bTranslate_step = False
    bCheckTranslation_step = False

    """ We prepare the missing translations by language (file compared to English.xml) """
    """ We use Excel files to store the data """
    if bPrepare_step:
        prepare_process_languages(languages_list)

    """ We translate the missing translations with ChatGPT (gpt-5 model) """
    if bTranslate_step:
        translate_missing_list(languagestotranslate_list)

    """ We check the current translation """
    if bCheckTranslation_step:
        check_current_translation("French")

if __name__ == "__main__":
   main()
