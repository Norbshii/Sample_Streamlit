import streamlit as st
import os
import textwrap
import google.generativeai as genai

# Load API key from environment variable (replace with your actual key)
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    st.error("Please set the GOOGLE_API_KEY environment variable with your Gemini API key.")
    exit()

genai.configure(api_key=API_KEY)

# Initialize or retrieve chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

## Function to interact with Gemini and maintain conversation
def get_gemini_response(question):
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(st.session_state.chat_history)
    response = chat.send_message(question)
    st.session_state.chat_history.append({"user": question})
    for chunk in response:
        st.session_state.chat_history.append({"gemini": chunk.text})
    return response

## Streamlit App
st.set_page_config(page_title="Dynamic Q&A Demo")
st.header("Dynamic Conversation with Gemini")

user_input = st.text_input("Your Question:", key="user_query")

if st.button("Ask Gemini"):
    if user_input:
        responses = get_gemini_response(user_input)
        st.subheader("Conversation:")
        for entry in st.session_state.chat_history:
            if 'user' in entry:
                st.write(f"You: {entry['user']}")
            if 'gemini' in entry:
                st.write(f"Gemini: {entry['gemini']}")
    else:
        st.warning("Please enter a question.")

# Optionally, add a reset conversation button
if st.button("Reset Conversation"):
    st.session_state.chat_history = []

# Debug: Print chat history
# st.write("Chat History:", st.session_state.chat_history)
