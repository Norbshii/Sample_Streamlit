# NAME: NORBERTO PINGOY            COURSE & SECTION: BSCS 3B AI        FINAL PROJECT FOR CCS 229 - INTELLIGENT SYSTEMS
import streamlit as st
import os
import google.generativeai as genai
import time

# Load API key from environment variable
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    # Displays an error on the Streamlit interface if the API key is not set.
    st.error("Please set the GOOGLE_API_KEY environment variable with your Gemini API key.")
    exit()

# Configures the Gemini API with the obtained API key.
genai.configure(api_key=API_KEY)

# Check if a chat session exists, if not, initialize a new one.
if 'chat_session' not in st.session_state:
    model = genai.GenerativeModel('gemini-1.5-pro')
    st.session_state.chat_session = model.start_chat()
    st.session_state.chat_history = []  # Initialize chat history

def handle_chat(question):
    try:
         # An introduction to the response to make it more engaging and user friendly.
        intro_response = "Hello I am Mei Mei, your chatbot AI Friend to help you assess your symptoms. Let's figure this out together."
        # Sends the user's question to the chat API and gets a response.
        response = st.session_state.chat_session.send_message(question)
        # Formulates the complete response by combining the introduction, API response, and a follow-up prompt.
        full_response = f"{intro_response} {response.text} Anything else I can help you with?"

        # Appends the question and response to the session's history for display.
        st.session_state.chat_history.append({"type": "Question", "content": question})
        st.session_state.chat_history.append({"type": "Response", "content": full_response})
        return full_response
    except Exception as e:
        # Handles exceptions by displaying an error message and returning a fallback message.
        st.error(f"An error occurred: {str(e)}")
        time.sleep(1)  # Introduces a slight delay before responding, simulating thought.
        return "An error occurred. Please try again."

def display_history():
    with st.container():  # Creates a scrollable container to display the chat history.
        for entry in st.session_state.chat_history:
                # Formats and Displays user inquiries.
            if entry['type'] == "Question":
                st.markdown(f"<p style='font-size:16px; font-weight:bold;'>Your Inquiry:</p><p style='font-size:16px;'>{entry['content']}</p>", unsafe_allow_html=True)
            elif entry['type'] == "Response":
                # Formats and Displays responses from the chatbot.
                formatted_response = entry['content'].replace("**", "<b>").replace("<b>", "</b>")
                st.markdown(f"<p style='font-size:16px; font-weight:bold;'>Response from Mei Mei:</p><p style='font-size:16px;'>{formatted_response}</p>", unsafe_allow_html=True)

# Streamlit App setup
st.set_page_config(page_title="SARBOT - Symptoms and Remedies Chatbot")
st.header("SARBOT - Symptom Assessment and Remedies Bot")

# Expander containing information about the creator
with st.expander("Display info about the creator"):
    text = """Norberto Pingoy\n
    BSCS 3B AI
    Final Project for CCS 229 - Intelligent Systems
    Bachelor of Science in Computer Science
    College of Information and Communications Technology
    West Visayas State University
    """
    st.write(text)
# Detailed guide on how to interact with the SARBOT - Mei Mei
with st.expander("How to use the SARBOT"):
    text = """Welcome to the SARBOT - Symptoms and Remedies Chatbot, Mei Mei will be your AI friend while using this chat! This chatbot is designed to provide general health information and guide you through basic inquiries about symptoms, health conditions, and wellness advice. Follow these simple steps to interact with the chatbot:

1. **Starting Up**\n
When you first launch the application, you will see a text input field labeled "Enter your general health inquiry here:". This is where you will type your questions.\n
2. **Entering Your Inquiry**\n
Type your question in the text box. Try to keep your questions **"General and Focused on Symptoms or Health Conditions."**\n For example, instead of saying **"I feel sick,"** you could ask, "What are some common causes of nausea and fatigue?" or you can just say directly your symptom like Headache and Dizziness.\n
You can also add something like the **"Cause"** that you think might be the reason for that symptom to get a more accurate answer.\n
Press the **"Ask Mei Mei"** button to submit your question.\n
3. **Viewing Responses**\n
After submitting your question, the your AI assistant Mei Mei will process your input and provide a response below the input field.\n
4. **Continuing the Conversation**\n
If you have more questions to Mei Mei, simply type them into the text box and click **"Ask Mei Mei"** again.
Each new and previous conversation will be displayed in a scrollable container, allowing you to review past interactions.\n
5. **Resetting the Conversation**\n
If you wish to start over and clear all previous conversations, you can press the "Reset Conversation" button. This will clear all history and allow you to start fresh.
    """
    st.markdown(text, unsafe_allow_html=True)

# Main interaction area where users can input their queries.
user_input = st.text_input("Enter your general health inquiry here:", key="user_query")
if st.button("Ask Mei Mei"):
    if user_input:
        # Check if the query already includes certain keywords
        if 'reasons' in user_input.lower() or 'remedies' in user_input.lower():
            response_text = handle_chat(user_input)  # Use the original user input
        else:
            # Refine the user's query to be more specific
            refined_query = f"What are some common reasons/remedies for {user_input}?"
            response_text = handle_chat(refined_query)
        display_history()
    else:
        st.warning("Please enter your query about general health information.")

# Button to reset the conversation, clearing all history and starting a new session.
if st.button("Reset Conversation"):
    model = genai.GenerativeModel('gemini-1.5-pro')
    st.session_state.chat_session = model.start_chat()
    st.session_state.chat_history = []  # This clears the history
