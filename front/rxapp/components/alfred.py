import requests
import json
import ast

import reflex as rx

from rxapp.settings import Settings

settings = Settings()

class AlfredState(rx.State):
    
    messages = ["Send a message to ALFRED :)"]
    debug = ""
    user_input = ""

    def get_messages(self):
        response = requests.get(f"{settings.FAST_API_URL}/messages")
        self.messages = []
        if response.status_code == 200:
            fetched_messages = json.loads(response.text)
            self.debug += f"\n\nFetched messages: {fetched_messages}"
            for message in fetched_messages:
                self.messages.append(message)
        else:
            self.messages = ["No messages found."]

    def send_message(self):
        response = requests.post(f"{settings.FAST_API_URL}/messages/?user_input={self.user_input.strip()}")
        if response.status_code == 200:
            self.debug = f"Message sent: {self.user_input.strip()}"
            self.user_input = ""
        else:
            self.debug = f"Error sending message: {response.text}"
        self.get_messages()

    def send_on_key_down(self, event):
        if event == "Enter" and self.user_input.strip() != "":
            self.send_message()

def alfred_sidebar():
    return rx.container(
        rx.vstack(
            rx.heading("ALFRED - HELPER", mb="4"),
            
            # Message display area with scroll - using index instead of zip
            rx.box(
                rx.foreach(
                    AlfredState.messages,
                    lambda message, index: rx.box(
                        rx.box(
                            rx.text(
                                message,
                                font_size="14px",
                                color=rx.cond(index % 2 == 0, "grey", "black"),
                            ),
                            max_width="75%",
                        ),
                        width="100%",
                        display="flex",
                        justify_content=rx.cond(
                            index % 2 == 0, "flex-end", "flex-start"
                        ),
                    )
                ),
                width="100%",
                overflow_y="auto",
                flex="1",  # Take available space
                min_height="300px",
                p="2",
            ),
            
            # Message input with auto-expand and Enter key functionality
            rx.vstack(
                rx.text_area(
                    placeholder="Type your message here...",
                    value=AlfredState.user_input,
                    on_change=AlfredState.set_user_input,
                    # Handle Enter key press (without shift)
                    on_key_down=AlfredState.send_on_key_down,
                    width="100%",
                    min_height="60px",
                    padding="10px",
                    border_radius="8px",
                    resize="vertical",  # Allow vertical resizing
                    rows=str(3),  # Default rows
                ),
                rx.button(
                    "Send Message", 
                    color_scheme="blue", 
                    on_click=AlfredState.send_message, 
                    width="100%",
                    is_disabled=AlfredState.user_input.strip() == "",  # Disable if empty
                ),
                width="100%",
                spacing="2",
                pt="2",
            ),
            

            rx.box(
                rx.text("Debug Info:", font_weight="bold", color="red"),
                rx.text(AlfredState.debug, font_size="12px", color="red"),
                bg="gray.50",
                p="2",
                border_radius="md",
                width="100%",
            ),
            
            spacing="4",
            height="100%",
            width="100%",
            align_items="stretch",
        ),
        max_width="800px",
        background="white",
        border_right="1px solid #eee",
        padding="20px",
        height="100vh",
        display="flex",
    )