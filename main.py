import streamlit as st
from crewai import Agent, Task, Crew
from crewai.tools import tool
from typing import List
import random
from pydantic import BaseModel, Field

class AITopic(BaseModel):
    title: str = Field(..., description="Title of the AI topic")
    description: str = Field(..., description="Brief description of the AI topic")

@tool
def get_ai_topics(num_topics: int = 5) -> List[AITopic]:
    """
    Retrieves a random selection of AI topics with their titles and descriptions.
    
    Args:
        num_topics: The number of AI topics to retrieve (default: 5)
        
    Returns:
        A list of AITopic objects containing titles and descriptions
    """
    ai_topics = [
        AITopic(title="Machine Learning", description="Algorithms that improve through experience"),
        AITopic(title="Natural Language Processing", description="AI for understanding and generating human language"),
        AITopic(title="Computer Vision", description="AI systems that can interpret and analyze visual information"),
        AITopic(title="Robotics", description="AI-powered machines that can perform tasks autonomously"),
        AITopic(title="Deep Learning", description="Neural networks with multiple layers for complex pattern recognition"),
        AITopic(title="Reinforcement Learning", description="AI agents learning through interaction with an environment"),
        AITopic(title="Expert Systems", description="AI systems that emulate human expert decision-making"),
    ]
    return random.sample(ai_topics, min(num_topics, len(ai_topics)))

def create_ai_news_agent():
    return Agent(
        name="AI News",
        role="AI Topics information provider",
        goal="Provide detailed information about AI topics",
        backstory="I am an AI agent specialized in delivering the latest news and information about artificial intelligence topics.",
        verbose=True,
        allow_delegation=False,
        tools=[get_ai_topics]
    )

def create_task(agent, num_topics):
    return Task(
        description=f"Retrieve and summarize information about {num_topics} AI topics",
        agent=agent,
        expected_output=f"A summary of {num_topics} AI topics with their titles and descriptions",
    )

def run_crew(agent, task):
    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True
    )
    return crew.kickoff()

st.title("AI Topics Summarizer")
st.sidebar.header("Configuration")
num_topics = st.sidebar.slider("Number of AI Topics", min_value=1, max_value=7, value=3)

if st.sidebar.button("Generate Summary"):
    with st.spinner("Generating AI topics summary..."):
        ai_news_agent = create_ai_news_agent()
        task = create_task(ai_news_agent, num_topics)
        result = run_crew(ai_news_agent, task)
        
        st.subheader("AI Topics Summary")
        st.write(result)

st.sidebar.info("This app uses CrewAI to generate summaries of AI topics.")
