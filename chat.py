import streamlit as st
import os
import google.generativeai as genai
import time

# Load API key from environment variable
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    st.error("Please set the GOOGLE_API_KEY environment variable with your Gemini API key.")
    exit()

genai.configure(api_key=API_KEY)

# Initialize the chat session and history if not already done
if 'chat_session' not in st.session_state:
    model = genai.GenerativeModel('gemini-1.5-pro')
    st.session_state.chat_session = model.start_chat()
    st.session_state.chat_history = []  # Initialize chat history

def handle_chat(question, cause):
    try:
        intro_response = "Hello, I am Mei Mei, your AI friend here to help you assess your symptoms."
        question_cause = f"Based on your description and the possible cause you provided: '{cause}', let's explore what might be happening."
        response = st.session_state.chat_session.send_message(question)
        full_response = f"{intro_response} {question_cause} {response.text} Anything else I can help you with?"
        
        st.session_state.chat_history.append({"type": "Question", "content": question})
        st.session_state.chat_history.append({"type": "Response", "content": full_response})
        return full_response
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        time.sleep(1)  # Simple backoff
        return "An error occurred. Please try again."

def display_history():
    with st.container():  # Use a container to make the history scrollable
        for entry in st.session_state.chat_history:
            if entry['type'] == "Question":
                st.markdown(f"<p style='font-size:16px; font-weight:bold;'>You said:</p><p style='font-size:16px;'>{entry['content']}</p>", unsafe_allow_html=True)
            elif entry['type'] == "Response":
                formatted_response = entry['content'].replace("**", "<b>").replace("</b>", "</b>")
                st.markdown(f"<p style='font-size:16px; font-weight:bold;'>Gemini replied:</p><p style='font-size:16px;'>{formatted_response}</p>", unsafe_allow_html=True)

# Streamlit App setup
st.set_page_config(page_title="Symptoms and Remedies Chatbot")
st.header("Symptom Assessment and Remedies AI")

# Additional input fields for symptoms and possible causes
st.write("Please describe your symptoms and any recent activities or experiences you think might be related.")
symptoms_input = st.text_area("Describe your symptoms:", height=150)
cause_input = st.text_area("What do you think might be the cause of these symptoms based on your recent activities or experiences?", height=150)

if st.button("Analyze Symptoms"):
    if symptoms_input and cause_input:
        response_text = handle_chat(symptoms_input, cause_input)
        display_history()
    else:
        st.warning("Please fill in both fields to proceed with the symptom analysis.")

# Resetting the conversation
if st.button("Reset Conversation"):
    model = genai.GenerativeModel('gemini-1.5-pro')
    st.session_state.chat_session = model.start_chat()
    st.session_state.chat_history = []  # This clears the history
