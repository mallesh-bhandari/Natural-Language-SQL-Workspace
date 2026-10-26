import os
import re
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from database import get_db_connection

load_dotenv()

def get_sql_chain():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing from your .env file.")

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        google_api_key=api_key,
        temperature=0
    )
    return llm

def parse_content(content):
    """Helper function to safely extract text whether response is a string or a list of blocks."""
    if isinstance(content, list):
        text = ""
        for block in content:
            if isinstance(block, dict) and "text" in block:
                text += block["text"]
            elif isinstance(block, str):
                text += block
        return text
    return str(content)

def generate_sql_query(user_question: str) -> str:
    _, sql_db = get_db_connection()
    schema_info = sql_db.get_table_info()

    prompt = f"""
    You are an expert SQLite Data Analyst. Given the database schema below, write ONLY a valid executable SQLite query based on the user's question.

    Database Schema:
    {schema_info}

    Rules:
    1. Do NOT include markdown code formatting blocks like ```sql or ```.
    2. Return ONLY the raw SQL statement text.
    3. Use standard SQLite syntax.
    4. Only construct SELECT queries. Never write DELETE, DROP, INSERT, or UPDATE statements.

    User Question: {user_question}
    SQL Query:
    """

    llm = get_sql_chain()
    response = llm.invoke(prompt)
    
    raw_text = parse_content(response.content)
    sql_query = raw_text.strip()
    sql_query = re.sub(r"```sql|```", "", sql_query).strip()
    return sql_query

def generate_insights(user_question: str, sql_query: str, df_data: str) -> str:
    prompt = f"""
    You are a professional Business Intelligence Analyst.
    
    User Question: {user_question}
    Executed SQL Query: {sql_query}
    Query Output Data:
    {df_data}

    Provide a short, 2-3 sentence executive summary explaining the insights from this data.
    """

    llm = get_sql_chain()
    response = llm.invoke(prompt)
    return parse_content(response.content).strip()