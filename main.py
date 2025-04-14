import streamlit as st
import random
from crewai import Agent, Task, Crew
from crewai.tools import Tool

@Tool
def pick_random_number(min_value: int = 1, max_value: int = 100) -> int:
    return random.randint(min_value, max_value)

def create_number_picker_agent() -> Agent:
    return Agent(
        name="Number Picker",
        role="Random Number Generator",
        goal="Pick random numbers as requested",
        backstory="I am an AI agent specialized in generating random numbers.",
        verbose=True,
        tools=[pick_random_number]
    )

def create_number_picking_task() -> Task:
    return Task(
        description="Pick a random number between 1 and 100",
        expected_output="A random integer between 1 and 100",
        agent=create_number_picker_agent()
    )

def run_number_picker_crew() -> str:
    crew = Crew(
        agents=[create_number_picker_agent()],
        tasks=[create_number_picking_task()],
        verbose=True
    )
    result = crew.kickoff()
    return result

st.title("Random Number Picker")

if st.button("Pick a Random Number"):
    try:
        result = run_number_picker_crew()
        st.success(f"Random number picked: {result}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")