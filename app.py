import streamlit as st
import google.generativeai as genai
import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt

# 🎨 Dark Mode Styling
GEN_API_KEY = "AIzaSyBj1BzzNCg6FOUeic8DTtU3uYNVMaDErQw"
genai.configure(api_key=GEN_API_KEY)
st.set_page_config(page_title="MindEase 🧘‍♂️", layout="wide")
dark_theme = """
    <style>
    body {
        background-color: #121212;
        color: white;
        font-family: 'Arial', sans-serif;
    }
    .stApp {
        background-color: #121212;
    }
    .stTextInput, .stButton, .stSelectbox, .stTextArea {
        background-color: #1E1E1E !important;
        color: white !important;
        border-radius: 10px;
    }
    .stChatMessage {
        background-color: #2C2C2C;
        color: white;
        border-radius: 10px;
        padding: 12px;
        margin: 5px 0;
    }
    .stSidebar {
        background-color: #181818 !important;
        color: white !important;
    }
    </style>
"""
st.markdown(dark_theme, unsafe_allow_html=True)

# 📌 Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'moods' not in st.session_state:
    st.session_state.moods = []
if 'journals' not in st.session_state:
    st.session_state.journals = []

# 🤖 Chatbot Function
def get_gemini_response(user_input):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(user_input)
    return response.text

# 📊 Mood Tracker
def log_mood(mood):
    today = datetime.date.today().strftime("%Y-%m-%d")
    st.session_state.moods.append({"date": today, "mood": mood})

def show_mood_chart():
    if st.session_state.moods:
        df = pd.DataFrame(st.session_state.moods)
        mood_counts = df["mood"].value_counts()
        st.bar_chart(mood_counts, use_container_width=True)

# 🎵 Meditation Music
def play_music():
    music_files = [f for f in os.listdir("music") if f.endswith(".mp3")]
    if music_files:
        selected_music = st.selectbox("Choose meditation music:", music_files)
        st.audio(os.path.join("music", selected_music), format="audio/mp3")
    else:
        st.warning("No music files found.")

# 🌟 Sidebar Navigation
st.sidebar.title("MindEase 🧘‍♂️")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", ["Chatbot", "Mood Tracker", "Journal", "Meditation Music", "Breathing Exercise", "Affirmations", "Help & Resources"], index=0)

# 🤖 Chatbot UI
if page == "Chatbot":
    st.title("Mental Health Chatbot 🤖")
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.write(chat["text"])
    user_input = st.chat_input("How are you feeling today?")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "text": user_input})
        response = get_gemini_response(user_input)
        st.session_state.chat_history.append({"role": "ai", "text": response})
        st.rerun()

# 📊 Mood Tracker
elif page == "Mood Tracker":
    st.title("Mood Tracker 📊")
    mood = st.selectbox("How do you feel today?", ["Happy", "Sad", "Anxious", "Angry", "Calm"], index=0)
    if st.button("Log Mood", use_container_width=True):
        log_mood(mood)
        st.success("Mood Logged Successfully!")
    show_mood_chart()

# 📖 Daily Journal
elif page == "Journal":
    st.title("Daily Journal 📖")
    entry = st.text_area("Write your thoughts here:", height=150)
    if st.button("Save Journal", use_container_width=True):
        today = datetime.date.today().strftime("%Y-%m-%d")
        st.session_state.journals.append({"date": today, "entry": entry})
        st.success("Journal entry saved!")
    st.write("### Past Entries")
    for journal in st.session_state.journals:
        st.markdown(f"**{journal['date']}**: {journal['entry']}")

# 🎵 Meditation Music
elif page == "Meditation Music":
    st.title("Meditation & Relaxation 🎵")
    play_music()

# 🌬️ Breathing Exercise
elif page == "Breathing Exercise":
    st.title("Breathing Exercise 🌬️")
    st.write("Inhale deeply for 4 seconds... Hold for 4 seconds... Exhale slowly for 6 seconds... Repeat.")
    st.image("https://i.imgur.com/2PbnHUJ.gif")

# ✨ Daily Affirmations
elif page == "Affirmations":
    st.title("Daily Affirmations ✨")
    affirmations = [
        "You are strong and capable.",
        "Every day is a new opportunity.",
        "You are enough just as you are.",
        "You have the power to create change.",
    ]
    st.subheader(f"{affirmations[datetime.datetime.now().day % len(affirmations)]}")

# 📞 Help & Resources
elif page == "Help & Resources":
    st.title("Help & Resources 📞")
    st.write("If you need urgent mental health support, consider reaching out to these resources:")
    st.markdown("📞 **National Helpline:** 1-800-662-HELP")
    st.markdown("🌍 **Online Support:** Visit [BetterHelp](https://www.betterhelp.com/) or [TalkSpace](https://www.talkspace.com/)")
    st.markdown("📚 **Mental Health Articles:** Read helpful guides on stress, anxiety, and mindfulness.")