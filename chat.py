import streamlit as st
import os
import google.generativeai as genai

# Load API key from environment variable
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    st.error("Please set the GOOGLE_API_KEY environment variable with your Gemini API key.")
    exit()

genai.configure(api_key=API_KEY)

# Initialize the chat session
if 'chat_session' not in st.session_state:
    model = genai.GenerativeModel('gemini-pro')
    st.session_state.chat_session = model.start_chat()

# Function to handle chat interaction
def handle_chat(question):
    try:
        # Send the user's question to Gemini and fetch the response
        response = st.session_state.chat_session.send_message(question)
        return response
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# Streamlit App setup
st.set_page_config(page_title="Dynamic Q&A Demo")
st.header("Dynamic Conversation with Gemini")

user_input = st.text_input("Your Question:", key="user_query")

if st.button("Ask Gemini"):
    if user_input:
        response = handle_chat(user_input)
        if response:
            st.subheader("Gemini's Response:")
            st.write(response.text)  # Assuming 'text' is the correct attribute; adjust as per the actual response structure
    else:
        st.warning("Please enter a question.")

if st.button("Reset Conversation"):
    # Restart the chat session if needed
    model = genai.GenerativeModel('gemini-pro')
    st.session_state.chat_session = model.start_chat()
