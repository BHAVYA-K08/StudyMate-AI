from dotenv import  load_dotenv
from langchain_groq import ChatGroq

#LOAD THE ENVIRONMENT VARIABLES FROM .env FILE

load_dotenv()


def get_llm():
    """INITIALIZE AND RETURN THE GROQ LLM"""

    llm = ChatGroq(
        model = "openai/gpt-oss-20b",
        temperature = 0.2,
        max_tokens = 2000
    )

    return llm