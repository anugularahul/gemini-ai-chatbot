
import streamlit as st
import google.generativeai as genai
import speech_recognition as sr

# Load API Key securely
if "GEMINI_API_KEY" not in st.secrets:
    st.error("API key missing! Please add it to Streamlit secrets.")
    st.stop()

api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# Initialize the Gemini Model
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

# Initialize speech recognition
recognizer = sr.Recognizer()

def recognize_speech():
    """Captures and transcribes speech using Google Speech Recognition."""
    with sr.Microphone() as source:
        st.write("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source)
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError:
            return "Speech recognition service is unavailable"

# Streamlit UI Configuration (Only one call)
st.set_page_config(page_title="Gemini AI Chatbot", page_icon="app_logo.png")

st.title("Gemini AI Chatbot: Your AI-Powered Assistant")
st.write("Ask me anything! I provide fast, accurate, and to-the-point answers tailored to your needs")

# Chat session state
st.session_state.messages = st.session_state.get("messages", [])

# Sidebar - Chatbot Settings
st.sidebar.title("Chatbot Settings")
st.sidebar.write("Customize the chatbot experience here.")

# Response Style Selection
response_style = st.sidebar.radio(
    "Select response type:",
    ("Friendly", "Professional", "Coder-like")
)

if st.sidebar.button("Clear chat"):
    st.session_state.messages = []
    st.rerun()

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input and voice input
col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.chat_input("Type your message here...")

with col2:
    if st.button("🎤"):
        voice_input = recognize_speech()
        if voice_input:
            st.write(f"You said: {voice_input}")
            user_input = voice_input

if user_input:
    # Modify input based on selected response style
    if response_style == "Friendly":
        prompt = f"Respond in a friendly and engaging manner: {user_input}"
    elif response_style == "Professional":
        prompt = f"Provide a professional and well-structured response: {user_input}"
    elif response_style == "Coder-like":
        prompt = f"Explain the answer like a programmer, using technical terms when needed: {user_input}"
    
    # Store user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate AI response
    try:
        response = model.generate_content(prompt)
        response_text = response.text if hasattr(response, 'text') else str(response)
    except Exception as e:
        response_text = f"Error generating response: {e}"

    # Store AI response
    st.session_state.messages.append({"role": "assistant", "content": response_text})

    # Display AI response
    with st.chat_message("assistant"):
        st.markdown(response_text)
