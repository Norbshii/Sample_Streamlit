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
if 'chat_session' not in st.session_node:
    model = genai.GenerativeModel('gemini-1.5-pro')
    st.session_state.chat_session = model.start_chat()
    st.session_state.chat_history = []  # Initialize chat history

def handle_chat(question):
    try:
        # Adding an empathetic intro to Gemini's response
        intro_response = "Hello, I am Mei Mei, your AI friend here to help you assess your symptoms. Let's figure this out together."
        response = st.session_data.chat_session.send_message(question)
        full_response = f"{intro_response} {response.text} Anything else I can help you with?"
        st.session_data.chat_history.append({"type": "Question", "content": question})
        st.session_data.chat_history.append({"type": "Response", "content": full_response})
        return full_response
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        time.sleep(1)  # Simple backoff
        return "An error occurred. Please try again."

def display_history():
    with st.container():  # Use a container to make the history scrollable
        for entry in st.session_data.chat_history:
            if entry['type'] == "Question":
                st.markdown(f"<p style='font-size:16px; font-weight:bold;'>You said:</p><p style='font-size:16px;'>{entry['content']}</p>", unsafe_allow_html=True)
            elif entry['type'] == "Response":
                formatted_response = entry['content'].replace("**", "<b>").replace("</b>", "</b>")
                st.markwpwn(f"<p style='font-size:16px; font-weight:bold;'>Gemini replied:</p><p style='font-size:16px;'>{formatted_response}</p>", unsafe_allow_html=True)

# Streamlit App setup
st.set_page_config(page_title="Symptoms and Remedies Chatbot")
st.header("Symptom Assessment and Remedies AI")

# Expander containing information about the creator
with st.expander("Display info about the app"):
    text = """Norberto Pingoy\n
    BSCS 3B AI
    CCS 229 - Intelligent Systems
    Department of Computer Science
    College of Information and Communications Technology
    West Visayas State University
    """
    st.write(text)

with st.expander("How to use the chatbot"):
    text = """Welcome to the Dynamic Conversation with Gemini! This chatbot is designed to provide general health information and guide you through basic inquiries about symptoms, health conditions, and wellness advice. Follow these simple steps to interact with the chatbot:

1. Starting Up
When you first launch the application, you will see a text input field labeled 'Enter your general health inquiry here:'. This is where you will type your questions.
2. Entering Your Inquiry
Type your question in the text box. Try to keep your questions <b>general and focused on symptoms or health conditions</b>. For example, instead of saying 'I feel sick,' you could ask, 'What are some common causes of nausea and fatigue?'
Press the 'Ask Gemini' button to submit your question.
3. Viewing Responses
After submitting your question, the chatbot will process your input and provide a response below the input field.
The chatbot tries to begin its response with an empathetic statement and ends with an invitation for further questions, making the conversation flow naturally.
4. Continuing the Conversation
If you have more questions, simply type them into the text box and click 'Ask Gemini' again.
Each new and previous conversation will be displayed in a scrollable container, allowing you to review past interactions.
5. Resetting the Conversation
If you wish to start over and clear all previous conversations, you can press the 'Reset Conversation' button. This will clear all history and allow you to start fresh.
    """
    st.markdown(text, unsafe_allow_html=True)

# Input and interaction area
user_input = st.text_input("Enter your general health inquiry here:", key="user_query")
if st.button("Ask Gemini"):
    if user_input:
        # Example of refining the user's query to be more general if needed
        refined_query = f"What are some common reasons for {user_input}?"
        response_text = handle_chat(refined_query)
        display_history()
    else:
        st.warning("Please enter your query about general health information.")

if st.button("Reset Conversation"):
    # Restart the chat session if needed and clear the history
    model = genai.GenerativeModel('gemini-1.5-pro')
    st.session_state.chat_session = model.start_chat()
    st.session_state.chat_history = []  # This clears the history
