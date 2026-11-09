
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# LOAD ENVIRONMENT VARIABLES FROM .env
load_dotenv()


def get_llm():
    """INITIALIZE AND RETURN THE GROQ LLM"""

    # GET API KEY FROM ENVIRONMENT OR STREAMLIT SECRETS
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        try:
            api_key = st.secrets["GROQ_API_KEY"]
        except (KeyError, FileNotFoundError):
            raise ValueError(
                "GROQ_API_KEY is missing. Configure it in .env "
                "or Streamlit Cloud Secrets."
            )

    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0.2,
        max_tokens=2000,
        api_key=api_key
    )

    return llm
