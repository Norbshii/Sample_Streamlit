import streamlit as st
import os
import textwrap
import google.generativeai as genai

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

# First level of input
user_input_level1 = st.text_input("Your initial question:", key="level1")

if st.button("Refine Question"):
    # Store first level input and ask for refinement
    st.session_state['level1_input'] = user_input_level1
    st.session_state['refinement_prompt'] = True

if 'refinement_prompt' in st.session_state and st.session_state['refinement_prompt']:
    st.subheader("Refine your question:")
    user_input_level2 = st.text_input("Your refined question:", key="level2", value=st.session_state['level1_input'])
    if st.button("Submit Final Question"):
        final_question = user_input_level2
        response = get_gemini_response(final_question)
        st.subheader("Gemini's Response:")
        for chunk in response:
            st.write(textwrap.fill(chunk.text))
        # Reset the state after submission
        st.session_state['refinement_prompt'] = False
else:
    st.warning("Please enter your initial question.")

# Print chat history for debugging purposes (optional)
# st.write("Chat History:", chat.history)
