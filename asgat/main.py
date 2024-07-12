from PyInquirer import prompt
from api.yandex_translate import detect_language, get_translation
from interface.user_interface import choose_language_category, choose_language, get_text_input
from utils.file_operations import get_text_from_file, save_translation_to_file
from models import save_translation_to_db

def main():
    api_key = '<API-ключ>'  # Замените <API-ключ> на ваш реальный API-ключ

    language_categories = {
        "Европейские языки": ['en', 'es', 'de', 'fr', 'it', 'pt', 'nl', 'el', 'sv', 'da', 'no', 'fi', 'is', 'ga', 'cy'],
        "Славянские языки": ['ru', 'uk', 'be', 'pl', 'cs', 'sk', 'bg', 'sr', 'sr-Latn', 'mk', 'sl', 'bs', 'hr'],
        "Азиатские языки": ['zh', 'ja', 'ko', 'vi', 'th', 'id', 'ms', 'tl', 'hi', 'bn', 'ta', 'te', 'kn', 'ml'],
        "Африканские языки": ['af', 'zu', 'xh', 'sw', 'am', 'ht'],
        "Кавказские и Среднеазиатские языки": ['ka', 'hy', 'az', 'uz', 'uzbcyr', 'kk', 'kazlat', 'tg', 'ky'],
        "Ближневосточные языки": ['ar', 'fa', 'tr', 'he', 'ur', 'pa', 'pap'],
        "Другие языки": ['eo', 'la', 'ceb', 'eu', 'et', 'lv', 'lt', 'mi', 'mn', 'ne', 'my', 'tl', 'si'],
        "Языки, редко используемые": ['ba', 'cv', 'mrj', 'mhr', 'udm', 'sah', 'os', 'lb', 'lo', 'mg', 'tt', 'yi']
    }

    while True:
        category, languages = choose_language_category('Выберите категорию исходного языка:', language_categories, include_unknown=True)

        if category == 'Распознать текст':
            source_language = 'Распознать текст'
        else:
            while True:
                source_language = choose_language(languages, 'Выберите исходный язык:')
                if source_language != 'Вернуться к типам':
                    break
                category, languages = choose_language_category('Выберите категорию исходного языка:', language_categories, include_unknown=True)

        category, languages = choose_language_category('Выберите категорию целевого языка:', language_categories, include_unknown=False)
        while True:
            target_language = choose_language(languages, 'Выберите целевой язык:')
            if target_language != 'Вернуться к типам':
                break
            category, languages = choose_language_category('Выберите категорию целевого языка:', language_categories, include_unknown=False)

        input_method_question = [
            {
                'type': 'list',
                'name': 'input_method',
                'message': 'Выберите метод ввода текста:',
                'choices': ['Ввести текст в консоли', 'Читать текст из файла']
            }
        ]

        input_method_answer = prompt(input_method_question)
        input_method = input_method_answer['input_method']

        if input_method == 'Ввести текст в консоли':
            if source_language == 'Распознать текст':
                text = get_text_input()
                detected_language = detect_language(api_key, text)
                if detected_language:
                    print(f"Распознанный язык: {detected_language}")
                    source_language = detected_language
                else:
                    print("Не удалось распознать язык. Пожалуйста, попробуйте снова.")
                    continue
            else:
                text = get_text_input()
            translated_text, _ = get_translation(api_key, source_language, target_language, text)
            print("Переведенный текст:", translated_text)
            save_translation_to_db(source_language, target_language, text, translated_text)
        else:
            text, input_file_path = get_text_from_file()
            if source_language == 'Распознать текст':
                detected_language = detect_language(api_key, text)
                if detected_language:
                    print(f"Распознанный язык: {detected_language}")
                    source_language = detected_language
                else:
                    print("Не удалось распознать язык. Пожалуйста, попробуйте снова.")
                    continue
            translated_text, _ = get_translation(api_key, source_language, target_language, text)
            save_translation_to_file(translated_text, source_language, target_language, input_file_path)
            save_translation_to_db(source_language, target_language, text, translated_text)

        again = prompt([{
            'type': 'list',
            'name': 'continue',
            'message': 'Хотите продолжить?',
            'choices': ['да', 'нет']
        }])

        if again['continue'] == 'нет':
            break

if __name__ == "__main__":
    main()


