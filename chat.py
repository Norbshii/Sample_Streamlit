import streamlit as st
import os
import google.generativeai as genai

# Load API key from environment variable
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    st.error("Please set the GOOGLE_API_KEY environment variable with your Gemini API key.")
    exit()

genai.configure(api_key=API_KEY)

# Initialize the chat session and history
if 'chat_session' not in st.session_state:
    model = genai.GenerativeModel('gemini-pro')
    st.session_state.chat_session = model.start_chat()
    st.session_state.chat_history = []  # Initialize chat history

# Function to handle chat interaction
def handle_chat(question):
    try:
        # Send the user's question to Gemini and fetch the response
        response = st.session_state.chat_session.send_message(question)
        # Store the question and response in the history
        st.session_state.chat_history.append({"type": "Question", "content": question})
        st.session_state.chat_history.append({"type": "Response", "content": response.text})
        return response.text
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def calculate_height(text):
    # Basic calculation: one line per 80 characters, and then some padding
    lines = text.count('\n') + 1
    lines += len(text) // 80  # rough estimate of line breaks for long lines
    return max(3, lines) * 20  # 20 pixels per line as a rough estimate

# Streamlit App setup
st.set_page_config(page_title="Dynamic Q&A Demo")
st.header("Dynamic Conversation with Gemini")

user_input = st.text_input("Your Question:", key="user_query")

if st.button("Ask Gemini"):
    if user_input:
        response_text = handle_chat(user_input)
        if response_text:
            st.subheader("Conversation History:")
            for entry in st.session_state.chat_history:
                height = calculate_height(entry['content'])
                if entry['type'] == "Question":
                    st.text_area("You said:", value=entry['content'], height=height, disabled=True)
                elif entry['type'] == "Response":
                    st.text_area("Gemini replied:", value=entry['content'], height=height, disabled=True)
    else:
        st.warning("Please enter a question.")

if st.button("Reset Conversation"):
    # Restart the chat session if needed and clear the history
    model = genai.GenerativeModel('gemini-pro')
    st.session_state.chat_session = model.start_chat()
    st.session_state.chat_history = []

