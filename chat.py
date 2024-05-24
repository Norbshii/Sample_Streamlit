# Q&A Chatbot using Gemini API

import streamlit as st
import os
import pathlib
import textwrap

import google.generativeai as genai

# Load API key from environment variable (replace with your actual key)
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    st.error("Please set the GOOGLE_API_KEY environment variable with your Gemini API key.")
    exit()

genai.configure(api_key=API_KEY)

## Function to interact with Gemini
def get_gemini_response(question, chat):
    response = chat.send_message(question, stream=True)
    return response

## Streamlit App

st.set_page_config(page_title="Q&A Demo")
st.header("Ask Gemini!")

# Initialize or retrieve the existing chat session from Streamlit's session state
if 'chat' not in st.session_state or st.session_state.chat is None:
    st.session_state.chat = genai.GenerativeModel('gemini-pro').start_chat(history=[])

user_input = st.text_input("Your Question:", key="input")

if st.button("Ask"):
    if user_input:
        response = get_gemini_response(user_input, st.session_state.chat)
        st.subheader("Gemini's Response:")
        for chunk in response:
            st.write(dir(chunk))  # Debug: print all available properties of the chunk
            # Attempt to find and display the correct content field
            st.write(textwrap.fill(str(chunk)))  # Display the raw response structure
        # Debugging chat history
        if hasattr(st.session_state.chat, 'history'):
            for message in st.session_state.chat.history:
                st.write(dir(message))  # Print all properties of a message
