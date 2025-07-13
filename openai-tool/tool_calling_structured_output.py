import json
from openai import AsyncAzureOpenAI
from agents import (
    Agent, Runner,
    OpenAIChatCompletionsModel,
    function_tool, FunctionTool
)
from dotenv import load_dotenv
import os
import asyncio
from pydantic import BaseModel
from typing import List

load_dotenv()

llm_client = AsyncAzureOpenAI(
    api_key=os.getenv("OPENAI_API_TOKEN"),
    api_version=os.getenv("OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("ENDPOINT"),
)

class OutputFormat(BaseModel):
    team_name: str
    no_of_trophies: int
    years_won: List[int]


@function_tool
def get_trophies(team_name):
    """
    Fetches the no of trophies won by a local club cricket team
    :arg:
    team_name: The requested team name to get information about trophies
    :returns:
    a string description with the team along with trophies won
    """
    trophies_map = {
        "CSK": "7 => 5 in IPL (2010, 2011, 2018, 2021, 2023) and 2 in Champions League (2010 and 2014)",
        "MI": "7 => 5 in IPL (2013, 2015, 2017, 2019, 2020) and 2 in Champions League (2011 and 2013)",
        "RCB": "1 => 1 in IPL (2025)"
    }

    return trophies_map.get(team_name, "Requested local club team not found")


search_agent = Agent(
    name="Cricket Info Agent",
    instructions="Your are an helpful agent who can assist with cricket queries",
    model=OpenAIChatCompletionsModel(
        model=os.getenv("DEPLOYMENT"),
        openai_client=llm_client
    ),
    tools=[get_trophies],
    output_type=OutputFormat
)

for tool in search_agent.tools:
    if isinstance(tool, FunctionTool):
        print("************************")
        print("JSON Tool Schema")
        print("************************")
        print(tool.name)
        print(tool.description)
        print(json.dumps(tool.params_json_schema, indent=4))
        print()


async def main():
    response = await Runner.run(
        search_agent,
        "How many trophies have CSK won in total?"
    )
    print("****** Result *******")
    print(response.final_output)

if __name__ == "__main__":
    asyncio.run(main())
