import os
from PyInquirer import prompt

def get_text_from_file():
    file_question = [
        {
            'type': 'input',
            'name': 'file_path',
            'message': 'Введите путь к файлу с текстом для перевода:',
        }
    ]
    file_answer = prompt(file_question)
    file_path = file_answer['file_path']

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text, file_path
    else:
        print("Файл не найден. Пожалуйста, попробуйте снова.")
        return None, None


def save_translation_to_file(translated_text, source_language, target_language, input_file_path):
    output_file_path = f"{input_file_path}_translated_{source_language}_to_{target_language}.txt"
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(translated_text)
    print(f"Перевод сохранен в файл: {output_file_path}")
