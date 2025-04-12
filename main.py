import os
import streamlit as st
from typing import Dict, Any
from crewai import Agent, Task, Crew
from crewai.tools import tool
import requests
from pydantic import BaseModel, Field

LASTFM_API_KEY = "your_lastfm_api_key_here"

class SingerInfo(BaseModel):
    name: str = Field(..., description="The name of the singer")
    bio: str = Field(..., description="A brief biography of the singer")

class MusicResearchTool:
    @tool("Get singer bio by song name")
    def get_singer_bio(self, song_name: str) -> Dict[str, Any]:
        try:
            search_url = f"http://ws.audioscrobbler.com/2.0/?method=track.search&track={song_name}&api_key={LASTFM_API_KEY}&format=json"
            response = requests.get(search_url)
            response.raise_for_status()
            data = response.json()
            
            artist_name = data['results']['trackmatches']['track'][0]['artist']
            
            artist_url = f"http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={artist_name}&api_key={LASTFM_API_KEY}&format=json"
            response = requests.get(artist_url)
            response.raise_for_status()
            artist_data = response.json()
            
            bio = artist_data['artist']['bio']['summary']
            
            return SingerInfo(name=artist_name, bio=bio).dict()
        except requests.RequestException as e:
            st.error(f"Error fetching data from Last.fm API: {e}")
            return SingerInfo(name="Unknown", bio="Unable to fetch biography").dict()
        except (KeyError, IndexError) as e:
            st.error(f"Error parsing API response: {e}")
            return SingerInfo(name="Unknown", bio="Unable to parse biography").dict()

def initialize_agent() -> Agent:
    return Agent(
        role="Music Researcher",
        goal="Find music singer biographies based on song names",
        backstory="I am an AI agent specialized in researching music artists and their backgrounds.",
        verbose=True,
        allow_delegation=False,
        tools=[MusicResearchTool().get_singer_bio]
    )

def create_task(song_name: str) -> Task:
    return Task(
        description=f"Find the biography of the singer who performed the song '{song_name}'",
        expected_output="A dictionary containing the singer's name and a brief biography",
        agent=initialize_agent()
    )

def run_crew(song_name: str) -> Dict[str, Any]:
    crew = Crew(
        agents=[initialize_agent()],
        tasks=[create_task(song_name)],
        verbose=True
    )
    result = crew.kickoff()
    return result

st.title("Music Singer Biography Finder")

song_name = st.text_input("Enter a song name:", "Bohemian Rhapsody")

if st.button("Find Singer Bio"):
    with st.spinner("Searching for singer's biography..."):
        result = run_crew(song_name)
    
    st.subheader(f"Singer Info for '{song_name}':")
    st.write(f"**Name:** {result['name']}")
    st.write(f"**Bio:** {result['bio']}")