from fastapi import FastAPI, HTTPException

from langgraph.graph import StateGraph

from .agent import setup_graph, run_chatbot

from pathlib import Path
import json

#########################################
#                                       #
#       SOME KIND OF TOP NOTCH DB       #
#                                       #
#########################################

messages = {}

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


@app.get("/messages/")
async def retrieve_all_messages():
    if messages and len(messages) > 0:
        return messages
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
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
    
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