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

# Initialize the chat session and history
if 'chat_session' not in st.session_state:
    model = genai.GenerativeModel('gemini-pro')
    st.session_state.chat_session = model.start_chat()
    st.session_state.chat_history = []  # Initialize chat history

def handle_chat(question):
    try:
        response = st.session_state.chat_session.send_message(question)
        st.session_state.chat_history.append({"type": "Question", "content": question})
        st.session_state.chat_history.append({"type": "Response", "content": response.text})
        return response.text
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        time.sleep(1)  # Simple backoff
        return "An error occurred. Please try again."

# Pagination function to handle large outputs
def display_history():
    start_idx = st.session_state.get('start_idx', 0)
    end_idx = start_idx + 5  # Show 5 entries at a time
    paginated_history = st.session_state.chat_history[start_idx:end_idx]

    for entry in paginated_history:
        if entry['type'] == "Question":
            st.markdown(f"<p style='font-weight:bold;'>You said:</p>{entry['content']}", unsafe_allow_html=True)
        elif entry['type'] == "Response":
            st.markdown(f"<p style='font-weight:bold;'>Gemini replied:</p>{entry['content']}", unsafe_allow_html=True)

    if len(st.session_state.chat_history) > end_idx:
        if st.button('Show More'):
            st.session_state['start_idx'] = end_idx

# Streamlit App setup
st.set_page_config(page_title="Dynamic Q&A Demo")
st.header("Dynamic Conversation with Gemini")

user_input = st.text_input("Your Question:", key="user_query")

if st.button("Ask Gemini"):
    if user_input:
        response_text = handle_chat(user_input)
        display_history()
    else:
        st.warning("Please enter a question.")

if st.button("Reset Conversation"):
    # Restart the chat session if needed and clear the history
    model = genai.GenerativeModel('gemini-pro')
    st.session_state.chat_session = model.start_chat()
    st.session_state.chat_history = []
    st.session_state.start_idx = 0  # Reset pagination

