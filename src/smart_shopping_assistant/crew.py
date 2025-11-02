import os

from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	ScrapeWebsiteTool,
	SerpApiGoogleShoppingTool
)






@CrewBase
class SmartShoppingAssistantCrew:
    """SmartShoppingAssistant crew"""

    
    @agent
    def smart_list_manager_agent(self) -> Agent:

        
        return Agent(
            config=self.agents_config["smart_list_manager_agent"],
            
            
            tools=[
				ScrapeWebsiteTool(),
				SerpApiGoogleShoppingTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def deal_hunter_agent(self) -> Agent:

        
        return Agent(
            config=self.agents_config["deal_hunter_agent"],
            
            
            tools=[
				SerpApiGoogleShoppingTool(),
				ScrapeWebsiteTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    

    
    @task
    def smart_list_generation(self) -> Task:
        return Task(
            config=self.tasks_config["smart_list_generation"],
            markdown=False,
            
            
        )
    
    @task
    def deal_hunting(self) -> Task:
        return Task(
            config=self.tasks_config["deal_hunting"],
            markdown=False,
            
            
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the SmartShoppingAssistant crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )

    def _load_response_format(self, name):
        with open(os.path.join(self.base_directory, "config", f"{name}.json")) as f:
            json_schema = json.loads(f.read())

        return SchemaConverter.build(json_schema)
