from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

class RouteQuery(BaseModel):
    """Route a user query to the appropriate agent."""
    destination: str = Field(
        description="The destination agent, must be one of 'data' or 'research'.",
        enum=["data", "research"]
    )

class OrchestrationAgent:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0, 
            model_name="llama-3.1-8b-instant",
            groq_api_key=os.getenv("GROQ_API_KEY")
        )

        structured_llm = self.llm.with_structured_output(RouteQuery)

        system_prompt = """You are an expert at routing a user query to a 'data' agent or a 'research' agent based on the query.

- The 'data' agent handles queries about analyzing numerical or categorical data from tables (like CSVs). This includes calculations, trends, plotting, sales figures, revenue, etc.
- The 'research' agent handles queries about understanding, summarizing, or finding information within text documents (like PDFs).

You must route the user's query to either the 'data' or 'research' agent.
"""

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "Route the following user query: {query}"),
            ]
        )

        self.chain = prompt | structured_llm

    def route_query(self, query: str) -> str:
        """
        Routes the user's query to the appropriate agent.
        """
        try:
            response = self.chain.invoke({"query": query})
            
            print(f"[OrchestrationAgent] Query: {query}")
            print(f"[OrchestrationAgent] Routed to: {response.destination}")
            
            return response.destination
        except Exception as e:
            print(f"Error routing query: {e}")
            return "research"

