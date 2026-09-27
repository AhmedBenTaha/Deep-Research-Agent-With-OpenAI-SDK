from agents import Agent,WebSearchTool,ModelSettings
from dotenv import load_dotenv
load_dotenv(override=True)
import os

MODEL_NAME = os.getenv("OPENAI_MODEL_NAME","gpt-4o")
MODEL_SETTINGS = ModelSettings(tool_choice="required")

INSTRUCTIONS = """
You are a research assistant. Given a search term, you search the web for that term and 
produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 words.
Capture the main points and be succinct. Reply only with the summary.
"""

tools = [WebSearchTool()]

search_agent=Agent(
    name="search-agent",
    model=MODEL_NAME,
    model_settings=MODEL_SETTINGS,
    tools=tools,
    instructions=INSTRUCTIONS
)


