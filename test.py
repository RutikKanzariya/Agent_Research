from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_groq import ChatGroq

import os
# load_dotenv()

# llm = ChatGoogleGenerativeAI(
#     model="gemini-3.5-flash"

# )

# response = llm.invoke("Who is Virat kohli?")
# print(response.content)


load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0,
    max_tokens=500
)

res = llm.invoke("Virat Kohli")
print(res)