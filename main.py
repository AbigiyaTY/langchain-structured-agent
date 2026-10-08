import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

api_key = os.getenv("AZURE_AI_API_KEY")
project_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
model = os.getenv("AZURE_AI_MODEL")

client = OpenAI(
    api_key=api_key,
    base_url=f"{project_endpoint.rstrip('/')}/openai/v1/"
)

# response = client.responses.create(
#     model=model,
#     input="What is the current status of the world peace?"
# )

# print(f"Answer: {response.output_text}")
