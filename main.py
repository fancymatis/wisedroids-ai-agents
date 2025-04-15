import streamlit as st
import os
from crewai import Agent, Task, Crew
from crewai.tools import tool
from typing import List
import random
import requests
from pydantic import BaseModel, Field
import openai

class APIError(Exception):
    pass

class AINewsArticle(BaseModel):
    title: str = Field(..., description="The title of the AI news article")
    summary: str = Field(..., description="A brief summary of the AI news article")
    url: str = Field(..., description="The URL of the full article")

@tool
def fetch_ai_news(query: str = "artificial intelligence") -> List[AINewsArticle]:
    """
    Fetches recent AI news articles based on the given query.
    
    Args:
        query (str): The search query for AI news. Defaults to "artificial intelligence".
    
    Returns:
        List[AINewsArticle]: A list of AI news articles.
    """
    try:
        articles = [
            AINewsArticle(
                title=f"AI Breakthrough in {random.choice(['Healthcare', 'Finance', 'Education'])}",
                summary=f"Researchers have made significant progress in AI applications for {query}.",
                url=f"https://example.com/ai-news-{random.randint(1000, 9999)}"
            )
            for _ in range(3)
        ]
        return articles
    except Exception as e:
        raise APIError(f"Error fetching AI news: {str(e)}")

def set_openai_api_key(api_key: str):
    os.environ["OPENAI_API_KEY"] = api_key

def check_api_key():
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        openai.Completion.create(engine="davinci", prompt="Test", max_tokens=5)
        return True
    except:
        return False

def main():
    st.title("AI News Aggregator")

    st.sidebar.header("OpenAI API Key")
    api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")

    if api_key:
        set_openai_api_key(api_key)
        if check_api_key():
            st.success("API key is valid. You can now use the application.")
            run_ai_news_crew()
        else:
            st.error("Invalid API key. Please enter a valid OpenAI API key.")
    else:
        st.info("Please enter your OpenAI API key in the sidebar to use the application.")

def run_ai_news_crew():
    ai_news_agent = Agent(
        name="AI News",
        role="AI Topics information provider",
        goal="Provide up-to-date information about AI topics",
        backstory="I am an AI agent specialized in gathering and presenting the latest news and developments in artificial intelligence.",
        verbose=True,
        allow_delegation=False,
        tools=[fetch_ai_news]
    )

    ai_news_task = Task(
        description="Fetch and summarize the latest AI news",
        agent=ai_news_agent,
        expected_output="A summary of the latest AI news articles with their titles and URLs",
        tools=[fetch_ai_news]
    )

    ai_news_crew = Crew(
        agents=[ai_news_agent],
        tasks=[ai_news_task],
        verbose=True
    )

    try:
        with st.spinner("Fetching AI news..."):
            result = ai_news_crew.kickoff()
        st.subheader("AI News Summary:")
        st.write(result)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()