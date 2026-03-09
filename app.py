import streamlit as st
import os

from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("GOOGLE_API_KEY not found. Please set it as an environment variable.")
    st.stop()

os.environ["GOOGLE_API_KEY"] = api_key


# Page Setup
st.set_page_config(page_title="Text-to-SQL App", layout="centered")
st.title("Talk to Your Database")
st.write("Ask questions about the sales database in plain English.")

# Database Connection
db = SQLDatabase.from_uri("sqlite:///sales.db")

# Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite-preview",
    temperature=0
)

# Prompt
prompt = ChatPromptTemplate.from_template("""
You are a senior data analyst and SQL expert.

Given the database schema below, write a correct SQL query
that answers the user's question.

Rules:
- Use only the tables and columns in the schema
- Do NOT explain anything
- Return ONLY the SQL query
- Return ONLY the raw SQL query.
- Do NOT use markdown formatting.
- Do NOT include ```sql or ``` blocks.

Schema:
{schema}

Question:
{question}
""")

# LCEL Chain
sql_chain = (
    prompt
    | llm
    | StrOutputParser()
)

# Get schema
schema = db.get_table_info()

# UI Input
question = st.text_input(
    "Enter your question:",
    placeholder="e.g., What is the highest price in order?"
)

# Execution
if question:
    try:
        sql_query = sql_chain.invoke(
            {"schema": schema, "question": question}
        ).strip()

        st.subheader("Generated SQL")
        st.code(sql_query, language="sql")

        st.subheader("Result")
        result = db.run(sql_query)
        st.write(result)

    except Exception as e:
        st.error(f"Error: {e}")

# Footer
st.markdown("---")
st.caption("Powered by LangChain 1.x • Gemini • Streamlit")