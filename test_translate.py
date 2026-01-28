from deep_translator import GoogleTranslator

translated = GoogleTranslator(source='en', target='fr').translate("Hello")
print(translated)
