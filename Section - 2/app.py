import streamlit as st
from dotenv import load_dotenv
import os
from src.agents.chatbot import FitnessChatbot
from src.data_loaders.data_loader import initialize_data
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables and initialize data (only once at startup)
logger.info("Loading environment variables...")
load_dotenv()

# Initialize data only if not already done
if 'data_initialized' not in st.session_state:
    logger.info("Performing one-time data initialization...")
    initialize_data()
    st.session_state.data_initialized = True
    logger.info("Data initialization completed")

def initialize_session_state():
    """Initialize session state variables."""
    logger.info("Initializing session state...")
    if 'chat_history' not in st.session_state:
        logger.info("Creating new chat history")
        st.session_state.chat_history = []
    if 'chatbot' not in st.session_state:
        try:
            logger.info("Initializing chatbot...")
            st.session_state.chatbot = FitnessChatbot()
            logger.info("Chatbot initialized successfully")
            return True
        except Exception as e:
            st.error(f"Error initializing chatbot: {str(e)}")
            logger.error(f"Error initializing chatbot: {e}", exc_info=True)
            return False
    return True

def main():
    logger.info("Starting Kahunas Fitness Coach application...")
    
    st.set_page_config(
        page_title="Kahunas Fitness Coach",
        page_icon="💪",
        layout="wide"
    )

    # Load Kahunas logo
    logo_path = os.path.join(os.path.dirname(__file__), "kahunas-logo.png")
    
    st.image(logo_path, width=200)
    st.title("Fitness Advisor")
    st.markdown("""
    Welcome to your AI Fitness Coach! Ask me anything about:
    - Workout plans and exercises
    - Nutrition advice
    - Progress tracking
    - Fitness goals
    """)

    # Initialize session state and check for errors
    if not initialize_session_state():
        st.error("Failed to initialize the chatbot. Please refresh the page or contact support.")
        logger.error("Failed to initialize session state")
        return

    # Chat interface
    logger.info("Setting up chat interface...")
    for message in st.session_state.chat_history:
        if message["role"] == "assistant":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        else:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("Ask your fitness-related question..."):
        logger.info(f"Received user input: {prompt}")
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get chatbot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    logger.info("Generating chatbot response...")
                    response = st.session_state.chatbot.get_response(prompt)
                    st.markdown(response)
                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": response}
                    )
                    logger.info("Response generated and displayed successfully")
                except Exception as e:
                    error_message = f"An error occurred: {str(e)}"
                    st.error(error_message)
                    logger.error(f"Error generating response: {e}", exc_info=True)

    # Sidebar with additional options
    with st.sidebar:
        st.header("Settings")
        if st.button("Clear Chat History"):
            logger.info("Clearing chat history...")
            st.session_state.chat_history = []
            st.rerun()

        st.header("About")
        st.markdown("""
        This AI-powered fitness coach uses advanced technology to provide 
        personalized fitness advice and insights based on your data and questions.
        Powered by Kahunas - Your Trusted Health & Fitness Partner.
        """)

if __name__ == "__main__":
    main() 