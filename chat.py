# Q&A Chatbot using Gemini API

import streamlit as st
import os
from dotenv 
import load_dotenv
import pathlib
import textwrap

import google.generativeai as genai
load_dotenv()  # This loads the variables from .env into the environment

# Load API key from environment variable (replace with your actual key)
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    st.error("Please set the GOOGLE_API_KEY environment variable with your Gemini API key.")
    exit()

genai.configure(api_key=API_KEY)

## Function to interact with Gemini
def get_gemini_response(question):
  model = genai.GenerativeModel('gemini-pro')
  chat = model.start_chat(history=[])
  response = chat.send_message(question, stream=True)
  return response

## Streamlit App

st.set_page_config(page_title="Q&A Demo")

st.header("Ask Gemini!")

user_input = st.text_input("Your Question:", key="input")

if st.button("Ask"):
  if user_input:
    response = get_gemini_response(user_input)
    st.subheader("Gemini's Response:")
    for chunk in response:
      st.write(textwrap.fill(chunk.text))
  else:
    st.warning("Please enter a question.")

# Print chat history for debugging purposes (optional)
# st.write("Chat History:", chat.history)
