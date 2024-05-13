from langdetect import detect

def detect_language(text):
    try:
        # La función 'detect' devuelve el código de idioma en formato ISO 639-1
        return detect(text)
    except Exception as e:
        return f"Error detecting language: {str(e)}"

# Ejemplo de uso
text = "Bonjour le monde"
language = detect_language(text)
print(f"Detected language: {language}")


from translate import Translator

def translate_text(text, dest_language):
    try:
        translator = Translator(to_lang=dest_language)
        translation = translator.translate(text)
        return translation
    except Exception as e:
        return f"Error in translation: {str(e)}"