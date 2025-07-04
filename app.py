import streamlit as st
import openai
import json
import datetime
import os
from encryptor import load_key, encrypt_message, decrypt_message
from breathing import breathing_exercise 
from certificate import generate_certificate
from deep_translator import GoogleTranslator
import matplotlib.pyplot as plt

# Load OpenAI API Key
openai.api_key = st.secrets.get("OPENAI_API_KEY", "")

# Create journaling folder and file if not exists
if not os.path.exists("journaling_data"):
    os.makedirs("journaling_data")
if not os.path.exists("journaling_data/entries.json"):
    with open("journaling_data/entries.json", "w") as f:
        json.dump([], f)
entries_path = "journaling_data/entries.json"
key = load_key()

def load_entries():
    with open(entries_path, "r") as f:
        return json.load(f)

def save_entry(entry):
    data = load_entries()
    data.append(entry)
    with open(entries_path, "w") as f:
        json.dump(data, f, indent=2)
def translate_prompt(prompt, target_lang):
    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(prompt)
        return translated
    except Exception as e:
        return f"Translation failed: {str(e)}"
def generate_journal(emotion, language):
    default_prompt = f"📝 Journaling Prompt: Reflect on a time you felt '{emotion}'. What led to that feeling? How did you handle it, and what did you learn?"

    if language == "en":
        return default_prompt
    else:
        # Simulate multilingual version without translation API
        return f"[{language.upper()}] {default_prompt}"

def plot_mood_chart():
    entries = load_entries()
    dates = [e["date"] for e in entries]
    moods = [e["emotion"] for e in entries]

    fig, ax = plt.subplots()
    ax.plot(dates, moods, marker="o", color="purple")
    ax.set_title("Your Mood Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Emotion")
    plt.xticks(rotation=45)
    st.pyplot(fig)
st.set_page_config(page_title="MindMate AI+", layout="centered")

st.title("🧠 MindMate AI+")
st.write("Your personal AI-powered mental health journaling companion.")

menu = st.sidebar.radio("Choose a feature:", [
    "Emotion-Based Journaling", 
    "Mood Tracker 📈", 
    "Breathing Coach 🧘", 
    "Download Certificate 🏅"
])
if menu == "Emotion-Based Journaling":
    emotion = st.selectbox("How are you feeling today?", [
        "happy", "sad", "anxious", "angry", "calm", "excited", "lonely", "overwhelmed"
    ])
    language = st.selectbox("Select your preferred language", [
        ("English", "en"),
        ("Hindi", "hi"),
        ("Tamil", "ta"),
        ("Telugu", "te"),
        ("Spanish", "es"),
        ("French", "fr")
    ], format_func=lambda x: x[0])

    if st.button("Generate Journaling Prompt"):
        with st.spinner("Generating..."):
            prompt = generate_journal(emotion, language[1])
        st.success("Here’s your journaling prompt:")
        st.write(prompt)

        entry = st.text_area("Write your journal entry here:")
        if st.button("Save Entry"):
            encrypted = encrypt_message(entry, key)
            save_entry({
                "date": datetime.date.today().isoformat(),
                "entry": encrypted,
                "emotion": emotion
            })
            st.success("Journal entry saved securely!")
elif menu == "Mood Tracker 📈":
    st.subheader("📊 Your Mood Over Time")
    if os.path.exists(entries_path) and load_entries():
        plot_mood_chart()
    else:
        st.warning("No entries yet to show the chart.")
elif menu == "Breathing Coach 🧘":
    breathing_exercise()
elif menu == "Download Certificate 🏅":
    entries = load_entries()
    if len(entries) >= 7:
        name = st.text_input("Enter your name for the certificate:")
        if st.button("Generate Certificate"):
            generate_certificate(name)
            with open("MindMate_Certificate.pdf", "rb") as f:
                st.download_button("Download PDF", f, file_name="MindMate_Certificate.pdf")
    else:
        st.info("Journal at least 7 days to unlock your certificate!")
if "OPENAI_API_KEY" in st.secrets:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    ai_enabled = True
else:
    ai_enabled = False

