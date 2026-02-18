from color import header 
header("Prompt Template example", "yellow")

import sys
import os
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")

from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI 
from dotenv import load_dotenv

load_dotenv()

llm = AzureChatOpenAI(
    azure_deployment = os.getenv("AZURE_OPENAI_API_DEPLOYMENT"),
    api_version      = os.getenv("AZURE_OPENAI_API_VERSION"),
    api_key          = os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint   = os.getenv("AZURE_OPENAI_ENDPOINT"),
    max_tokens       = 1000,
    temperature      = 0,
    verbose          = False,
    seed             = 1234
)

template = """
"Tell me about {topic} in the style of {style}."
"""
header("Template")
print(template.strip())

prompt_template = PromptTemplate(
    input_variables=["topic", "style"],  
    template=template
)

topic = "the history of pirates"
style = "a pirate"

header("Prompt variables")
print(f"Topic: {topic}")
print(f"Style: {style}")

prompt = prompt_template.format(
    topic=topic, 
    style=style)
header("Query")
print(prompt)

response = llm.invoke(prompt)

header("Response")
print(response)

header("Demonstration completed!")
