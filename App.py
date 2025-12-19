import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

# ------------------ Load ENV ------------------
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("API key not found. Check .env file")
    st.stop()

# ------------------ Gemini Client ------------------
client = genai.Client(api_key=API_KEY)

# ------------------ UI ------------------
st.title("Simple Chatbot 🤖")

# ------------------ Session State ------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I assist you today?"}
    ]

# ------------------ Display Chat ------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ------------------ User Input (ONLY ONCE) ------------------
user_input = st.chat_input("Type your message...")

if user_input:
    # show user msg
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    # Gemini call
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            f"{m['role']}: {m['content']}"
            for m in st.session_state.messages
        ]
    )

    reply = response.text

    # show assistant msg
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )
    with st.chat_message("assistant"):
        st.markdown(reply)
