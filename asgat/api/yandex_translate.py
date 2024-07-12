import requests

def detect_language(api_key, text):
    url = 'https://translate.api.cloud.yandex.net/translate/v2/detect'
    headers = {"Authorization": f"Api-Key {api_key}"}

    data = {
        "text": text,
        "languageCodeHints": [
            "ru",
            "en",
        ]
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        detected_language = response.json().get('languageCode')
        return detected_language
    else:
        print("Ошибка при распознавании языка:", response.status_code, response.text)
        return None

def get_translation(api_key, source_language, target_language, text):
    url = 'https://translate.api.cloud.yandex.net/translate/v2/translate'
    headers = {"Authorization": f"Api-Key {api_key}"}

    max_length = 10000
    if len(text) > max_length:
        text = text[:max_length]

    data = {
        "sourceLanguageCode": source_language,
        "targetLanguageCode": target_language,
        "format": "PLAIN_TEXT",
        "texts": [text],
        "speller": True
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        translations = response.json().get('translations')
        for translation in translations:
            translated_text = translation.get('text')
            detected_language = translation.get('detectedLanguageCode')
            return translated_text, detected_language
    else:
        print("Ошибка:", response.status_code, response.text)
        return None, None
