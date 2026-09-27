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

INSTRUCTIONS = """
You are a senior researcher tasked with writing a cohesive report for a research query.
You will be provided with the original query, and some research.
Generate a comprehensive report based on the research and the query.
The final output should be in markdown format, and it should be lengthy and detailed. Aim 
for 5-10 pages of content, at least 1000 words.
"""

class ResearchReport(BaseModel):
    short_summary: str = Field(..., description="A concise summary of the research report.")
    detailed_report: str = Field(..., description="A comprehensive and detailed research report in markdown format.")
    follow_up_questions: list[str] = Field(..., description="A list of follow-up questions that arise from the research report.")
    
writer_agent = Agent(
    name="writer-agent",
    model=model,
    instructions=INSTRUCTIONS,
    output_type=ResearchReport,
)    