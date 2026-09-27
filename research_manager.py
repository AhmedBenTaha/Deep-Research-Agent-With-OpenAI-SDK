from agents import Runner,trace,gen_trace_id
from writer_agent import writer_agent,ResearchReport
from email_agent import email_agent
from search_agent import search_agent
from planner_agent import planner_agent,WebSearchItem,WebSearchPlan
from dotenv import load_dotenv
load_dotenv(override=True)
import asyncio


class ResearchManager:
    async def run(self,query:str):
        """ Run the deep research process, yielding the status updates and the final report"""
        trace_id=gen_trace_id()
        with trace("Research Trace",trace_id=trace_id):
            yield f"Starting research. Trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            search_plan=await self.plan_searches(query)
            yield f"Search plan generated: {len(search_plan.searches)} searches to perform."
            search_results=await self.perform_searches(search_plan)
            yield f"Searches completed. {len(search_results)} results obtained."
            report=await self.generate_report(query,search_results)
            yield f"Report generated. Sending email..."
            await self.send_report(report)
            yield f"Email sent successfully. Research process completed."
            yield report.detailed_report
            
    async def plan_searches(self,query:str)->WebSearchPlan:
        """ Generate a search plan based on the user query """
        result=await Runner.run(planner_agent,f"query: {query}")
        return result.final_output
    
    async def perform_searches(self,search_plan:WebSearchPlan)->list[str]:
        """ Perform the searches to perform for the query """
        tasks=[self.search(item) for item in search_plan.searches]
        return await asyncio.gather(*tasks)
    
    async def search(self,search_item:WebSearchItem)->str:
        """ Perform a single search and return the result """
        # For now, we will just simulate a search by returning the query itself
        input_message=f"Performing search for: {search_item.query}\nReasoning: {search_item.reasoning}"
        result=await Runner.run(search_agent,input_message)
        return result.final_output
    
    async def generate_report(self,query:str,search_results:list[str])->ResearchReport:
        """ Generate a research report based on the query and search results """
        input_message=f"query: {query}\nsearch_results: {search_results}"
        result=await Runner.run(writer_agent,input_message)
        return result.final_output
    
    async def send_report(self,report:ResearchReport)->None:
        await Runner.run(email_agent,report.detailed_report)
        
    
            

