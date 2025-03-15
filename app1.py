import streamlit as st
import google.generativeai as genai

# Load API Key securely
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# Initialize the Gemini Model with the correct model name
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

# Streamlit UI Configuration
st.set_page_config(page_title="Gemini AI Chatbot")

st.title("Gemini AI Chatbot: Your AI-Powered Assistant")
st.write("Ask me anything! I provide fast, accurate, and to-the-point answers tailored to your needs")

# Chat session state
if "messages" not in st.session_state:
    st.session_state.messages = []

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

# Chat input
user_input = st.chat_input("Type your message here...")

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
        response = model.generate_content(prompt).text  # Fetch response from Gemini AI
    except Exception as e:
        response = f"Error generating response: {e}"

    # Store AI response
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Display AI response
    with st.chat_message("assistant"):
        st.markdown(response)
