import streamlit as st
import os
from crewai import Agent, Task, Crew
from langchain.llms import OpenAI

def set_openai_api_key(api_key):
    os.environ["OPENAI_API_KEY"] = api_key

def check_api_key():
    return "OPENAI_API_KEY" in os.environ and os.environ["OPENAI_API_KEY"]

def main():
    st.title("AI Research Assistant")

    # Sidebar for API key input
    st.sidebar.title("Configuration")
    api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")
    
    if api_key:
        set_openai_api_key(api_key)

    if not check_api_key():
        st.warning("Please enter your OpenAI API key in the sidebar to continue.")
        return

    # Main application
    topic = st.text_input("Enter a research topic:", "Artificial Intelligence Trends in 2025")
    
    if st.button("Generate Research Summary"):
        try:
            with st.spinner("Generating research summary..."):
                # Define the agent
                researcher = Agent(
                    role="Researcher",
                    goal="Gather information on a given topic and summarize it",
                    backstory="You are an expert researcher skilled at finding and condensing information.",
                    verbose=True,
                    allow_delegation=False,
                    llm=OpenAI()
                )

                # Define the task
                research_task = Task(
                    description=f"Research the topic '{topic}' and write a short summary.",
                    expected_output="A concise summary of the topic, about 100 words.",
                    agent=researcher
                )

                # Create the crew and assign the task
                crew = Crew(
                    agents=[researcher],
                    tasks=[research_task],
                    verbose=True
                )

                # Execute the crew's task
                result = crew.kickoff()

                # Display the result
                st.subheader("Research Summary:")
                st.write(result)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()