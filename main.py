import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from tools import search_tool, wiki_tool, save_tool

load_dotenv()

# Structured response model for the agent's output
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

# Environment variables
api_key = os.getenv("AZURE_AI_API_KEY")
project_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
model = os.getenv("AZURE_AI_MODEL")

# LLM
llm = ChatOpenAI(
    api_key=api_key,
    base_url=f"{project_endpoint.rstrip('/')}/openai/v1/",
    model=model,
)

# Tools
tools = [
    search_tool,
    wiki_tool,
    save_tool,
]

# Agent
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=(
        "You are an expert research assistant. "
        "Use the available search and Wikipedia tools to gather "
        "thorough and accurate information before answering. "
        "After completing the research, you MUST use the save_tool "
        "to save the final research result to research_output.txt. "
        "Only after saving the research should you provide the final answer."
    ),
    response_format=ResearchResponse,
)

# Run agent

try:
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "What is the latest research on quantum computing? "
                        "Research this topic and save the completed research "
                        "to the research_output.txt file."
                    ),
                }
            ]
        }
    )

    research = result["structured_response"]

    print("\n" + "=" * 50)
    print("RESEARCH RESULT")
    print("=" * 50)

    print(f"\nTopic:\n{research.topic}")

    print(f"\nSummary:\n{research.summary}")

    print("\nSources:")
    for source in research.sources:
        print(f"- {source}")

    print("\nTools used:")
    for tool in research.tools_used:
        print(f"- {tool}")

except Exception as e:
    print(f"Error while running agent: {type(e).__name__}: {e}")