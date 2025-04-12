from crewai import Agent, Task, Crew
from crewai.tools import tool
from pydantic import BaseModel, Field
import random
import requests

# API key for joke API (embedded directly in the script)
JOKE_API_KEY = "your_joke_api_key_here"

class JokeResponse(BaseModel):
    setup: str = Field(..., description="The setup of the joke")
    punchline: str = Field(..., description="The punchline of the joke")

@tool
def generate_joke() -> JokeResponse:
    """Generate a unique joke using an external API."""
    try:
        response = requests.get(
            "https://official-joke-api.appspot.com/random_joke",
            headers={"Authorization": f"Bearer {JOKE_API_KEY}"}
        )
        response.raise_for_status()
        joke_data = response.json()
        return JokeResponse(setup=joke_data['setup'], punchline=joke_data['punchline'])
    except requests.RequestException as e:
        print(f"Error fetching joke: {e}")
        # Fallback to a local joke if API fails
        fallback_jokes = [
            JokeResponse(setup="Why don't scientists trust atoms?", punchline="Because they make up everything!"),
            JokeResponse(setup="Why did the scarecrow win an award?", punchline="He was outstanding in his field!"),
        ]
        return random.choice(fallback_jokes)

def initialize_agent():
    """Initialize and return the Jokens Generator agent."""
    return Agent(
        name="Jokens Generator",
        role="Joke Generator",
        goal="Generate unique and funny jokes",
        backstory="I am an AI specialized in creating humorous content.",
        verbose=True,
        allow_delegation=False,
        tools=[generate_joke]
    )

def create_joke_task(agent):
    """Create and return a task for generating a joke."""
    return Task(
        description="Generate a unique joke",
        agent=agent,
        expected_output="A setup and punchline for a unique joke",
        tools=[generate_joke]
    )

def run_crew():
    """Initialize the crew, add the task, and execute."""
    agent = initialize_agent()
    task = create_joke_task(agent)
    
    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True
    )

    result = crew.kickoff()
    print("Generated Joke:")
    print(result)

if __name__ == "__main__":
    run_crew()
