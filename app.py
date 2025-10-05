import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="AI Q&A Bot",
    page_icon="🤖",
    layout="centered"
)

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Initialize Gemini
@st.cache_resource
def initialize_model():
    """Initialize Gemini model (cached to avoid reinitialization)"""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        st.error("❌ GEMINI_API_KEY not found in .env file!")
        st.stop()
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.5-flash')

model = initialize_model()

# App Header
st.title("🤖 AI Question & Answer Bot")
st.markdown("**Powered by Google Gemini**")
st.markdown("---")

# Sidebar with info
with st.sidebar:
    st.header("ℹ️ About")
    st.write("This is an AI-powered Q&A bot using Google's Gemini API.")
    st.write("Ask any question and get instant answers!")
    
    st.markdown("---")
    
    st.header("📊 Statistics")
    st.metric("Total Questions", len(st.session_state.chat_history))
    
    st.markdown("---")
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()
    
    st.markdown("---")
    st.caption("Built as part of Intern Assignment")

# Display chat history
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(chat['question'])
    with st.chat_message("assistant"):
        st.write(chat['answer'])

# User input
user_question = st.chat_input("Ask me anything...")

if user_question:
    # Display user message
    with st.chat_message("user"):
        st.write(user_question)
    
    # Generate and display AI response
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            try:
                response = model.generate_content(user_question)
                answer = response.text
                st.write(answer)
                
                # Save to chat history
                st.session_state.chat_history.append({
                    'question': user_question,
                    'answer': answer
                })
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Example questions
if len(st.session_state.chat_history) == 0:
    st.markdown("### 💡 Try asking:")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🌍 What is climate change?"):
            st.session_state.example_q = "What is climate change?"
            st.rerun()
        if st.button("💻 Explain Python"):
            st.session_state.example_q = "Explain Python programming in simple terms"
            st.rerun()
    
    with col2:
        if st.button("🚀 Facts about space"):
            st.session_state.example_q = "Tell me interesting facts about space"
            st.rerun()
        if st.button("🧠 What is AI?"):
            st.session_state.example_q = "What is artificial intelligence?"
            st.rerun()

# Handle example questions
if 'example_q' in st.session_state:
    user_question = st.session_state.example_q
    del st.session_state.example_q
    
    with st.chat_message("user"):
        st.write(user_question)
    
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            try:
                response = model.generate_content(user_question)
                answer = response.text
                st.write(answer)
                
                st.session_state.chat_history.append({
                    'question': user_question,
                    'answer': answer
                })
            except Exception as e:
                st.error(f"Error: {str(e)}")