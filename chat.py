import streamlit as st
import os
import time
import google.generativeai as genai

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    st.error("Please set the GOOGLE_API_KEY environment variable with your Gemini API key.")
    exit()

genai.configure(api_key=API_KEY)

def handle_chat(question):
    model = genai.GenerativeModel('gemini-pro')
    session = model.start_chat()
    retry_count = 0
    while retry_count < 3:
        try:
            response = session.send_message(question)
            return response.text
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            time.sleep(1)  # Wait for a second before retrying
            retry_count += 1
    return None

user_input = st.text_input("Your Question:", key="user_query")
if st.button("Ask Gemini") and user_input:
    response_text = handle_chat(user_input)
    if response_text:
        st.write(response_text)
    else:
        st.write("Failed to get a response after several attempts.")
