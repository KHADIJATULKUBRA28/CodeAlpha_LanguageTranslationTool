import streamlit as st
import pyperclip
from translator import (
    translate_text,
    text_to_speech,
    speech_file_to_text
)

st.set_page_config(page_title="Language Translation Tool", layout="centered")
st.title("🌍 Language Translation Tool")

language_codes = {
    "English": "en",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Korean": "ko",
    "Bangla (Bengali)": "bn",
    "Hindi": "hi",
    "Tamil": "ta",
    "Telugu": "te",
    "Malayalam": "ml"
}

languages = list(language_codes.keys())

# ---------- SESSION STATE ----------
if "original_text" not in st.session_state:
    st.session_state.original_text = ""
if "translated_text" not in st.session_state:
    st.session_state.translated_text = None
if "orig_audio" not in st.session_state:
    st.session_state.orig_audio = None
if "trans_audio" not in st.session_state:
    st.session_state.trans_audio = None

# ---------- CALLBACK ----------
def clear_translated_output():
    st.session_state.translated_text = None
    st.session_state.trans_audio = None

# ---------- SPEECH → TEXT (UPLOAD) ----------
st.subheader("🎙️ Speech to Translation")

uploaded_audio = st.file_uploader(
    "Upload an audio file (wav or mp3)",
    type=["wav", "mp3"]
)

if uploaded_audio:
    recognized_text = speech_file_to_text(uploaded_audio)
    if recognized_text:
        st.session_state.original_text = recognized_text
        st.success(f"Recognized Speech: {recognized_text}")
    else:
        st.error("Could not recognize speech from audio.")

# ---------- ORIGINAL TEXT ----------
col1, col2 = st.columns([8, 2])

with col1:
    original_text = st.text_area(
        "Original Text (auto-detected)",
        value=st.session_state.original_text,
        height=150
    )
    st.session_state.original_text = original_text

with col2:
    st.write("")
    if original_text.strip():
        if st.button("🔊", key="orig_sound"):
            st.session_state.orig_audio = text_to_speech(original_text, "en")

        if st.button("📋", key="copy_orig"):
            pyperclip.copy(original_text)
            st.toast("Original text copied")

if st.session_state.orig_audio:
    st.audio(st.session_state.orig_audio)

# ---------- TARGET LANGUAGE ----------
target_language = st.selectbox(
    "Target Language",
    languages,
    on_change=clear_translated_output
)

# ---------- TRANSLATE ----------
if st.button("Translate"):
    if original_text.strip():
        translated = translate_text(
            original_text,
            language_codes[target_language]
        )
        st.session_state.translated_text = translated
        st.session_state.trans_audio = None
    else:
        st.warning("Please enter or upload speech.")

# ---------- TRANSLATED TEXT ----------
if st.session_state.translated_text:
    col3, col4 = st.columns([8, 2])

    with col3:
        st.text_area(
            "Translated Text",
            st.session_state.translated_text,
            height=150,
            disabled=True
        )

    with col4:
        st.write("")
        if st.button("🔊", key="trans_sound"):
            st.session_state.trans_audio = text_to_speech(
                st.session_state.translated_text,
                language_codes[target_language]
            )

        if st.button("📋", key="copy_trans"):
            pyperclip.copy(st.session_state.translated_text)
            st.toast("Translated text copied")

    if st.session_state.trans_audio:
        st.audio(st.session_state.trans_audio)
