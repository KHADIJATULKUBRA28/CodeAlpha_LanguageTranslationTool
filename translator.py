from deep_translator import GoogleTranslator
from gtts import gTTS
import uuid
import speech_recognition as sr

def translate_text(text, target_lang, source_lang="auto"):
    try:
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        return translator.translate(text)
    except Exception:
        return None

def text_to_speech(text, lang_code):
    try:
        filename = f"audio_{uuid.uuid4().hex}.mp3"
        gTTS(text=text, lang=lang_code).save(filename)
        return filename
    except Exception:
        return None

def speech_file_to_text(audio_file):
    """
    Convert uploaded audio file to text
    """
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)

    try:
        return recognizer.recognize_google(audio)
    except Exception:
        return None
