from typing import Annotated

from typing_extensions import TypedDict

# Framework
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.graph.state import CompiledStateGraph
from langchain_anthropic import ChatAnthropic

# Tools
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
from .excel_manager import get_companies, update_org_info

# Memory
from langgraph.checkpoint.memory import MemorySaver

# Metrics
from langfuse.callback import CallbackHandler

# Misc
from dotenv import load_dotenv
import os
import requests
import json
from pathlib import Path


#############################
#                           #
#       Util functions      #
#                           #
#############################

def get_anthropic_key():
    load_dotenv()
    return os.getenv("ANTHROPIC_API_KEY")

def get_apollo_key():
    load_dotenv()
    return os.getenv("APOLLO_API_KEY")


#############################
#                           #
#       Initialization      #
#                           #
#############################

#
# Functions
#

def update_company_info_in_CRM(domain:str, data: dict):
    """
    Updates a given company info inside the CRM with the data passed as argument.
    """
    update_org_info(domain=domain, data=data)

#
# Tools
#

@tool
def enrich_company_info(domain:str, update_crm: bool) -> dict:
    """
    Function to properly enrich the company information using the apollo API.
    You can use this tool to get more information about the company you're looking for.
    Only use this function if the company is not in the database.
    Only use this function after using the get_company_info_from_database function.
    This tool is better than web search to retrieve company info.
    The domain needs to be of the following format: 'company.com'.
    Do not add www or http:// or https:// before the domain.
    If the tool returns an error, you can use the web search tool to get more information about the company or tell the user you can't find any information about the company.
    Update_crm boolean variable is set depending on rather or not you want to update the CRM with the info you recovered or not. Defaults to True.
    """
    url = f"https://api.apollo.io/api/v1/organizations/enrich?domain={domain}"

    headers = {
        "accept": "application/json",
        "Cache-Control": "no-cache",
        "Content-Type": "application/json",
        "x-api-key": get_apollo_key(),
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open(f"./apollo/organizations/{domain.split('.')[0]}.json", "w") as f:
            json.dump(json.loads(response.text), f, indent=4)
        
        if update_crm:
            update_company_info_in_CRM(domain=domain, data=json.loads(response.text))

        return response.text
    else:
        return {"error": f"Error: {response.status_code}"}


@tool
def enrich_company_info_from_database(domain:str, update_crm: bool) -> dict:
    """
    Cheaper function than enrich_company_info to get the company information.
    Use this function before using the enrich_company_info function.
    You can use this tool to get more information about the company you're looking for.
    When the user asks you to enrich a company information, you can use this tool to get more information about the company.
    Update_crm boolean variable is set depending on rather or not you want to update the CRM with the info you recovered or not. Defaults to True.
    """
    domain_split = domain.split(".")[0]
    FOLDER_PATH = Path("apollo/organizations")
    file_path = FOLDER_PATH / f"{domain_split}.json"

    if not file_path.exists():
        return {
            "error": f"Company '{domain}' is not in the database."
        }

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if update_crm:
            update_company_info_in_CRM(domain=domain, data=data)

        return data
    except (json.JSONDecodeError, IOError):
        return {
            "error": f"Failed to load data for company '{domain}'."
        }


@tool
def get_companies_in_CRM() -> list[str]:
    """
    To retrieve the list of companies that you have in the user's CRM.
    The function returns a list of domains of companies in your CRM.
    """
    return get_companies()


def create_tools() -> list:
    load_dotenv()
    web_search_tool = TavilySearchResults(max_results=2)
    return [web_search_tool, get_companies_in_CRM, enrich_company_info_from_database, enrich_company_info]


class State(TypedDict):
    messages: Annotated[list, add_messages]

####################
#                  #
#       Start      #
#                  #
####################



def setup_graph():

    available_models = ["claude-3-haiku-20240307","claude-3-5-haiku-20241022"]
    chosen_model = 0
    tools = create_tools()
    # Initialize
    memory = MemorySaver()
    llm = ChatAnthropic(model=available_models[chosen_model], api_key=get_anthropic_key())        # Using cheapest model
    llm = llm.bind_tools(tools)


    # Graph building

    graph_builder = StateGraph(State)
        
        # Nodes
    def chatbot(state: State):
        message = llm.invoke(state["messages"])
        return {"messages": [message]}
    
    graph_builder.add_node("chatbot", chatbot)

    tool_node = ToolNode(tools=tools)
    graph_builder.add_node("tools", tool_node)

        # Edges
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_conditional_edges("chatbot", tools_condition)
    graph_builder.add_edge("tools", "chatbot")

        # Compile
    graph = graph_builder.compile(checkpointer=memory)

    return graph


# Initialize Langfuse CallbackHandler for Langchain (tracing)
def create_handler() -> CallbackHandler:
    load_dotenv()
    return CallbackHandler()


def stream_graph_updates(graph: CompiledStateGraph, user_input: str, config):
    system_message = {
        "role":"system",
        "content": (
            "You are Alfred, an intelligent and professional CRM assistant built to support users with managing customer relationships."
            "You are always courteous, precise, and proactive. You assist with tasks such as updating customer records, retrieving contact info, generating follow-up summaries, and identifying sales opportunities."
            "You speak in a friendly and confident tone, and you are always respectful and efficient."
            "You clarify if you're unsure, and you use tools to fetch or manipulate data when needed."
            "Your goal is to make CRM tasks seamless and effortless for the user. When helpful, suggest ways to improve productivity or customer engagement."
            "Use all the tools at your disposal until you can achieve the task you're asked to do. You can use multiple tools one after the other if relevant."
        )
    }
    
    events = graph.stream(
            {"messages": [{"role": "user", "content": user_input}]},
            config=config,
            stream_mode="values"
        )
    
    messages = []
    # Add system message to the first event
    messages.append(system_message["content"])
    for event in events:
        event["messages"][-1].pretty_print()
        messages.append(event["messages"][-1].text())

    return messages

def run_chatbot(user_input:str, graph: CompiledStateGraph):
    langfuse_handler = create_handler()
    thread_id = 1
    user = "My User"
    thread_config={
        "configurable": {"thread_id": thread_id},
        "callbacks": [langfuse_handler],
        "metadata": {
            "langfuse_session_id": thread_id,
            "langfuse_user_id": user,
            },
        }

    return stream_graph_updates(graph, user_input, thread_config)
