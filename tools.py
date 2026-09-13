# Importing Library

from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print


load_dotenv()

tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY"),
)


# Featch real time Data (Done)
@tool
def web_search(query : str) -> str:
    """
    Search the web for recent and reliable information on a topic . 
    Returns title , URLs and snippets .
    """
    results = tavily.search(query=query,max_results=2)
    out = []
    for r in results['results']:
        out.append(
            f"Title : {r['title']}\nURL: {r['url']} \nSnippets : {r['content'][:300]}\n")

    return "\n ------ \n".join(out)

# Beautiful soup (DONE)
@tool
def scrape_url(url : str ) -> str:
    """
    Scrape and return clean text content from a given URL for deeper reading...
    """

    try:
        response = requests.get(url,timeout=8,headers={"User-Agent" : "Mozilla/5.0"})
        soup = BeautifulSoup(response.text,"html.parser")
        for tag in soup(['script','style','nav','footer']):
            tag.decompose()
        return soup.get_text(separator=" ",strip=True)[:3000]
    except Exception as e:
        return f"Colud not Scrape URL : {str(e)}"
    

# '''
# # Step 3 : Create Agents.py 
# Heart of the Project. we will build 4 things
# 1 -> search agent using create_agent + agent_executor -> used the web_search tool
# 2 -> Reader Agent same pattern with scrape tool.
# 3 -> writer Chain using the LCEL pipline which takes all the researches and writes a full stories.
# 4 -> Critic chain -> used LCEL pipline which reads report and gives a score and feedback.
# LCEL(Langchain Expression Language )
# '''
 
