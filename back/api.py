from pathlib import Path
import json
import ast
import requests

from fastapi import FastAPI, HTTPException
from langgraph.graph import StateGraph

from .agent import setup_graph, run_chatbot, get_apollo_key
from .excel_manager import update_org_info

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
  },
  "short_description": {
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
      "1": "hugo.bonnell@gatewatcher.com"
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
async def add_message(user_input: str, save_db: bool = True):
    try:
        msg_id = 0
        if len(messages) > 0:
            msg_id = len(messages)
        if save_db:
            messages[msg_id] = str(run_chatbot(user_input, graph))
        else:
            return str(run_chatbot(user_input, graph))
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


@app.post("/org_db")
async def add_org_to_db(org_domain: str):
    global org_db
    keys = list(org_db.keys())
    id = len(org_db[keys[0]])
    for key in keys:
        if key == "domain":
            org_db[key][str(id)] = org_domain
        else:
            org_db[key][str(id)] = None


def enrich_company_info_from_database(domain:str) -> dict:
    domain_split = domain.split(".")[0]
    FOLDER_PATH = Path("apollo/organizations")
    file_path = FOLDER_PATH / f"{domain_split}.json"

    if not file_path.exists():
        return {"error": f"Company '{domain}' is not in the database."}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        update_org_info(domain=domain, data=data)
        return data
    except (json.JSONDecodeError, IOError):
        return {"error": f"Failed to load data for company '{domain}'."}

def enrich_company_info(domain:str) -> dict:
    url = f"https://api.apollo.io/api/v1/organizations/enrich?domain={domain}"
    headers = {
        "accept": "application/json",
        "Cache-Control": "no-cache",
        "Content-Type": "application/json",
        "x-api-key": get_apollo_key(),
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        if "organization" in json.loads(response.text):
            with open(f"./apollo/organizations/{domain.split('.')[0]}.json", "w") as f:
                json.dump(json.loads(response.text), f, indent=4)
            update_org_info(domain=domain, data=json.loads(response.text))
            return json.loads(response.text)    
    return {"error": f"Error: {response.status_code} | {response.text}"}

@app.put("/org_db")
async def enhance_db(org_domain: str):
    database_enrich = enrich_company_info_from_database(org_domain)
    if "error" in database_enrich.keys():
        enrich = enrich_company_info(org_domain)
        if "organization" in enrich.keys():
            return f"Success enhancing {org_domain} via APOLLO"
        else:
            return f"Failed to enhance {org_domain}"
    return f"Sucess enhancing {org_domain} via DATABASE"

@app.get("/people_db")
async def get_people_db():
    global people_db
    return people_db


@app.post("/people_db")
async def add_person_to_db(email: str):
    global people_db
    keys = list(people_db.keys())
    id = len(people_db[keys[0]])
    for key in keys:
        if key == "email":
            people_db[key][str(id)] = email
        else:
            people_db[key][str(id)] = None
