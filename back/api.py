from pathlib import Path
import json
import ast

from fastapi import FastAPI, HTTPException
from langgraph.graph import StateGraph

from .agent import setup_graph, run_chatbot

#########################################
#                                       #
#       SOME KIND OF TOP NOTCH DB       #
#                                       #
#########################################

messages = {}
org_db = {
  "id": {
    "0": None,
    "1": None
  },
  "name": {
    "0": None,
    "1": None
  },
  "domain": {
    "0": "gatewatcher.com",
    "1": "airfrance.fr"
  },
  "industry": {
    "0": None,
    "1": None
  },
  "phone": {
    "0": None,
    "1": None
  }
}

people_db = {
  "id": {
    "0": None,
    "1": None
  },
  "first_name": {
    "0": None,
    "1": None
  },
  "last_name": {
      "0": None,
      "1": None
  },
  "email": {
      "0": "joshua.garrison@apollo.io",
      "1": None
  },
  "phone": {
    "0": None,
    "1": None
  },
  "linkedin_url": {
      "0": None,
      "1": None,
  }
}

#####################
#                   #
#       MODELS      #
#                   #
#####################

graph: StateGraph = setup_graph()

#####################
#                   #
#       API         #
#                   #
#####################

app = FastAPI()

    #####################
    #                   #
    #       CHAT        #
    #                   #
    #####################

@app.get("/messages/")
async def retrieve_all_messages() -> list:
    if messages and len(messages) > 0:
        parsed_messages = {}
        messages_to_return = []
        for key in messages.keys():
            try:
                parsed_messages[key] = ast.literal_eval(messages[key])
                messages_to_return.append(parsed_messages[key][1])  # Return user message and ai final message
                messages_to_return.append(parsed_messages[key][-1])  # Return user message and ai final message
            except Exception as e:
                print(f"Error while parsing message {key}: {e}")
                continue
        return messages_to_return
    else:
        raise HTTPException(status_code=404, detail="No message could be found")

@app.post("/messages/")
async def add_message(user_input: str):
    try:
        msg_id = 0
        if len(messages) > 0:
            msg_id = len(messages)
        messages[msg_id] = str(run_chatbot(user_input, graph))
        return {
            "sucess":"Sucessfully added message to database",
            "details":messages[msg_id]
            }
    except Exception as e:
        print("Error while adding message:", e)
        raise HTTPException(status_code=500, detail=f"Internal server error : {e}")
    
@app.get("/companies/")
async def get_companies():
    FOLDER_PATH = Path("apollo/organizations")
    combined = {}

    if not FOLDER_PATH.exists() or not FOLDER_PATH.is_dir():
        return {}
    
    json_files = list(FOLDER_PATH.glob("*.json"))

    for file in json_files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                combined[file.stem] = data
        except (json.JSONDecodeError, IOError):
            continue

    return combined

@app.delete("/messages/")
async def reset_messages():
    global messages
    if messages and len(messages) > 0:
        messages = {}
    else:
        raise HTTPException(status_code=404, detail="No message to delete")
    

    ##################
    #                #
    #       DB       #
    #                #
    ##################

@app.get("/org_db")
async def get_org_db():
    global org_db
    return org_db

@app.put("/org_db")
async def update_org_db(org_df: dict):
    global org_db
    org_db = org_df

@app.get("/people_db")
async def get_people_db():
    global people_db
    return people_db

@app.put("/people_db")
async def update_people_db(people_df: dict):
    global people_db
    people_db = people_df
