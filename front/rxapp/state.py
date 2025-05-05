import reflex as rx
import requests
import json

class AppState(rx.State):
    """Combined application state for H/UMAN CRM."""
    
    # Alfred assistant state
    user_input: str = ""
    info_text: str = ""
    
    # Organization state
    org_df: dict = {}
    
    # People state
    people_df: dict = {}
    
    def load_messages(self):
        """Load messages from the API."""
        try:
            response = requests.get("http://fastapi-app:8000/messages/")
            if response.status_code == 200:
                raw_msg = json.loads(response.text)
                self.info_text = ""
                
                for i in range(0, len(raw_msg)):
                    s = str(raw_msg[f"{i}"])
                    list_msg = eval(s)
                    self.info_text += list_msg[1] + "\n\n----------------------------\n\n" + list_msg[-1] + "\n\n----------------------------\n\n"
        except Exception as e:
            self.info_text = f"Error: {str(e)}"
    
    def send_message(self):
        """Send a message to the API."""
        if not self.user_input:
            return
            
        try:
            response = requests.post(f"http://fastapi-app:8000/messages/?user_input={self.user_input}")
            self.user_input = ""
            self.load_messages()
        except Exception as e:
            self.info_text = f"Error: {str(e)}"
    
    def reset_messages(self):
        """Reset all messages."""
        try:
            requests.delete("http://fastapi-app:8000/messages/")
            self.info_text = ""
        except Exception as e:
            self.info_text = f"Error: {str(e)}"
    
    # Organization methods
    def load_org_data(self):
        """Load organization data from the API."""
        try:
            response = requests.get("http://fastapi-app:8000/org_db")
            if response.status_code == 200:
                self.org_df = json.loads(response.text)
        except Exception as e:
            print(f"Error: {str(e)}")
    
    def add_org_row(self):
        """Add a new row to the organization dataframe."""
        for key in self.org_df:
            keys = list(self.org_df[key].keys())
            if keys:
                new_idx = str(max([int(k) for k in keys]) + 1)
                self.org_df[key][new_idx] = None
            else:
                self.org_df[key]["0"] = None
    
    def export_org_df(self):
        """Export organization data to the API."""
        try:
            requests.put("http://fastapi-app:8000/org_db", json=self.org_df)
        except Exception as e:
            print(f"Error: {str(e)}")
    
    # People methods
    def load_people_data(self):
        """Load people data from the API."""
        try:
            response = requests.get("http://fastapi-app:8000/people_db")
            if response.status_code == 200:
                self.people_df = json.loads(response.text)
        except Exception as e:
            print(f"Error: {str(e)}")
    
    def add_people_row(self):
        """Add a new row to the people dataframe."""
        for key in self.people_df:
            keys = list(self.people_df[key].keys())
            if keys:
                new_idx = str(max([int(k) for k in keys]) + 1)
                self.people_df[key][new_idx] = None
            else:
                self.people_df[key]["0"] = None
    
    def export_people_df(self):
        """Export people data to the API."""
        try:
            requests.put("http://fastapi-app:8000/people_db", json=self.people_df)
        except Exception as e:
            print(f"Error: {str(e)}")