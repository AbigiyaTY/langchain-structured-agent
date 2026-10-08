import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from tools import search_tool, wiki_tool, save_tool

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]
    
api_key = os.getenv("AZURE_AI_API_KEY")
project_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
model = os.getenv("AZURE_AI_MODEL")

if not api_key:
    raise ValueError("AZURE_AI_API_KEY is missing from .env")

if not project_endpoint:
    raise ValueError("AZURE_AI_PROJECT_ENDPOINT is missing from .env")

if not model:
    raise ValueError("AZURE_AI_MODEL is missing from .env")


llm = ChatOpenAI(
    api_key=api_key,
    base_url=f"{project_endpoint.rstrip('/')}/openai/v1/",
    model=model,
)

tools = [
    search_tool,
    wiki_tool,
    save_tool,
]

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=(
        "You are an expert research assistant. "
        "Provide thorough and accurate research. "
        "Return the final answer using the requested structured format."
    ),
    response_format=ResearchResponse,
)

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What is the latest research on quantum computing?",
            }
        ]
    }
)

research = result["structured_response"]

try:
    research = result["structured_response"]

    print("\n" + "=" * 50)
    print("RESEARCH RESULT")
    print("=" * 50)

    print(f"\nTopic:\n{research.topic}")

    print(f"\nSummary:\n{research.summary}")

    print(f"\nSources:")
    for source in research.sources:
        print(f"- {source}")

    print(f"\nTools used:")
    for tool in research.tools_used:
        print(f"- {tool}")

except KeyError:
    print("Error: structured_response was not returned by the agent.")

except Exception as e:
    print(f"Error processing the response: {e}")