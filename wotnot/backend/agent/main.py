import json
from fastapi import FastAPI, Request
from langchain_community.llms import Bedrock
from langchain.agents import initialize_agent, AgentType
# from langchain_community.tools.openapi.utils.openapi_utils import OpenAPISpec
from langchain_community.agent_toolkits.openapi.toolkit import RequestsToolkit

import json
from fastapi import FastAPI, Request
from langchain_community.llms import Bedrock
from langchain.agents import initialize_agent, AgentType
from langchain_community.utilities.openapi import OpenAPISpec

# Load OpenAPI spec from file as raw text
with open("wotnot_openapi.json", "r") as f:
    openapi_raw = f.read()

# Use correct OpenAPISpec method
spec = OpenAPISpec.from_text(openapi_raw)
spec.base_url = "https://api.wotnot.io"



# Get tools
toolkit = RequestsToolkit(spec=spec)
tools = toolkit.get_tools()

# LLM
llm = Bedrock(
    model_id="anthropic.claude-v2",
    region_name="us-east-1",
    model_kwargs={"temperature": 0.2}
)

# Agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

# FastAPI app
app = FastAPI()

@app.post("/run-agent/")
async def run_agent(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "Find content for template, create it, and send to today's contacts.")
    try:
        result = agent.run(prompt)
        return {"response": result}
    except Exception as e:
        return {"error": str(e)}