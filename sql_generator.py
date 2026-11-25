
import os
from dotenv import load_dotenv
from google import genai

from schema_inspector import get_database_schema

# Load environment variables
load_dotenv()

# Connect to Gemini
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_sql(question):

    # Get actual database schema
    schema = get_database_schema()

    # Instructions for Gemini
    prompt = f"""
    You are an expert MySQL query generator.

    Your task is to convert the user's business question
    into a valid MySQL SELECT query.

    DATABASE SCHEMA:
    {schema}

    RULES:
    1. Generate only SELECT queries.
    2. Use only tables and columns present in the schema.
    3. Use correct JOIN conditions.
    4. Never generate INSERT, UPDATE, DELETE, DROP,
       ALTER, CREATE or TRUNCATE statements.
    5. Do not invent column names.
    6. Return only SQL query text.
    7. Do not use markdown code blocks.

    USER QUESTION:
    {question}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text.strip()


if __name__ == "__main__":

    question = input("Ask your business question: ")

    try:
        sql_query = generate_sql(question)

        print("\nGENERATED SQL:")
        print("====================")
        print(sql_query)

    except Exception as error:
        print("Error generating SQL:", error)
