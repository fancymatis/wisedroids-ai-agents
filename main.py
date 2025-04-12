import streamlit as st
import random
from typing import Dict, Any
from crewai import Agent, Task, Crew
from crewai.tools import tool
from pydantic import BaseModel, Field

class AgentPersonality(BaseModel):
    trait: str = Field(default="Efficient", description="Personality trait of the agent")

@tool
def generate_random_number() -> int:
    return random.randint(1, 100)

def initialize_agent() -> Agent:
    personality = AgentPersonality(trait="Efficient")
    return Agent(
        name="Random Number Generator",
        role="Number generator",
        goal="Generate random numbers between 1 and 100",
        backstory="I am an efficient random number generator.",
        personality=personality.dict(),
        tools=[generate_random_number]
    )

def initialize_task() -> Task:
    return Task(
        description="Generate a random number between 1 and 100",
        expected_output="A single integer between 1 and 100",
        agent=initialize_agent()
    )

def run_crew() -> Dict[str, Any]:
    crew = Crew(
        agents=[initialize_agent()],
        tasks=[initialize_task()],
        verbose=True
    )
    result = crew.kickoff()
    return result

st.title("Random Number Generator")

if st.button("Generate Random Number"):
    try:
        result = run_crew()
        st.success(f"Generated random number: {result}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")