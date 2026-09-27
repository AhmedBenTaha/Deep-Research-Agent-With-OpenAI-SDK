from pydantic import BaseModel, Field
from agents import Agent,OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from dotenv import load_dotenv
load_dotenv(override=True)
import os


MODEL_NAME = os.getenv("DEFAULT_MODEL_NAME", "openai/gpt-oss-120b")
NUM_SEARCHES = int(os.getenv("NUM_SEARCHES", 4))

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

groq_client = AsyncOpenAI(base_url="https://api.groq.com/openai/v1", api_key=GROQ_API_KEY)
model = OpenAIChatCompletionsModel(
    model=MODEL_NAME,
    client=groq_client,
)

INSTRUCTIONS = f"""
You are a research assistant. Given a user query, come up with a set of web searches
to perform to best answer the query. Output {NUM_SEARCHES} terms to query for.
"""

class WebSearchItem(BaseModel):
    query: str = Field(..., description="The search term to use for the web search.")
    reasoning: str = Field(..., description="The reasoning behind why this search term was chosen.")
    
class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(..., description=f"A list of {NUM_SEARCHES} search terms to use for the web searches.")   
    
planner_agent = Agent(
    name="planner-agent",
    model=model,
    instructions=INSTRUCTIONS,
    output_type=WebSearchPlan,
)     