import streamlit as st
import os
import textwrap
import google.generativeai as genai

# Load API key from environment variable
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    st.error("Please set the GOOGLE_API_KEY environment variable with your Gemini API key.")
    exit()

genai.configure(api_key=API_KEY)

# Function to interact with Gemini
def get_gemini_response(question):
    model = genai.GenerativeModel('gemini-pro')
    
    # Ensure chat_history is structured correctly
    if 'chat_history' not in st.session_state or not st.session_state['chat_history']:
        st.session_state['chat_history'] = model.start_chat()

    try:
        # Update the history with the user's question
        st.session_state['chat_history'].send_message({"text": question})
        
        # Get the response from Gemini
        response = st.session_state['chat_history'].get_next_response()
        
        # Display the response and update the history
        st.session_state['chat_history'].append({"gemini": response.text})
        return response
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return []

# Streamlit App setup
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

if st.button("Reset Conversation"):
    st.session_state.chat_history = []

