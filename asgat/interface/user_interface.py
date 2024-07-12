from PyInquirer import prompt

def choose_language_category(message, language_categories, include_unknown=True):
    choices = list(language_categories.keys())
    if include_unknown:
        choices.append('Распознать текст')

    category_question = [
        {
            'type': 'list',
            'name': 'category',
            'message': message,
            'choices': choices
        }
    ]

    category_answer = prompt(category_question)
    category = category_answer['category']

    if category == 'Распознать текст':
        return 'Распознать текст', None
    else:
        return category, language_categories[category]

def choose_language(languages, message):
    choices = languages + ['Вернуться к типам']

    language_question = [
        {
            'type': 'list',
            'name': 'language',
            'message': message,
            'choices': choices
        }
    ]
    language_answer = prompt(language_question)
    return language_answer['language']

def get_text_input():
    text_question = [
        {
            'type': 'input',
            'name': 'text',
            'message': 'Введите текст для распознавания языка и перевода:',
        }
    ]
    text_answer = prompt(text_question)
    return text_answer['text']
