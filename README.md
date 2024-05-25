# SARBOT - Symptom Assessment and Remedies Chatbot

The SARBOT is a Streamlit-based chatbot designed to provide users with general health information and guide them through basic inquiries about symptoms and health conditions. It utilizes Google's Generative AI model, Gemini, to understand and respond to user queries effectively.

## Developer Information
- **Name**: Norberto Pingoy
- **Course & Section**: BSCS 3B AI
- **Project Context**: Final Project for CCS 229 - Intelligent Systems
- **Institution**: College of Information and Communications Technology, West Visayas State University

## Project Setup

### Prerequisites
- Python 3.11
- Streamlit
- Google Generative AI access (requires API key)

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/norbshii/streamlit.git
   cd streamlit
   ```

2. **Install dependencies:**
   ```bash
   pip install streamlit google-generativeai
   ```

3. **Set up the environment variable:**
   Create a `.env` file in the root directory and add your Gemini API key:
   ```plaintext
   GOOGLE_API_KEY='MyAPIisHiddenInTheSecrets'
   ```
### You can also skip the installation and Directly use the streamlit application via this [Link](https://sampleapp-ad7jx2ptscwwg8uspcrqia.streamlit.app/#perform-the-calculation-based-on-the-operator)

### Running the Application
Execute the following command in the terminal:
```bash
streamlit run app.py
```

## Functionalities

- **Symptom Inquiry**: Users can type in their health-related questions or symptoms, and Mei Mei, the AI assistant, will provide relevant information and advice.
- **History Display**: The chat history is displayed in a scrollable container, allowing users to review past interactions.
- **Session Reset**: Users can reset the conversation at any time to clear the history and start a new chat session.

## How to Use

1. **Start the Application**: Open your browser to `(https://sampleapp-ad7jx2ptscwwg8uspcrqia.streamlit.app/#perform-the-calculation-based-on-the-operator)`.
2. **Enter Your Inquiry**: Use the text input field to describe your symptoms or ask health-related questions.
3. **Interact with Mei Mei**: After submitting your inquiry, Mei Mei will process and respond. Continue the conversation by typing more questions if needed.
4. **Reset If Necessary**: Use the 'Reset Conversation' button to clear all previous interactions.

## Support
For support, please contact the developer at `norberto.pingoy@wvsu.edu.ph`.
