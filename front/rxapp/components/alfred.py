import requests
import json
import ast

import reflex as rx

from rxapp.settings import Settings

settings = Settings()

class AlfredState(rx.State):
    
    messages = ["Send a message to ALFRED :)"]
    debug = ""

    def get_messages(self):
        response = requests.get(f"{settings.FAST_API_URL}/messages")
        self.messages = []
        if response.status_code == 200:
            fetched_messages = json.loads(response.text)
            self.debug = f"Fetched messages: {fetched_messages}"
            for key in fetched_messages.keys():
                self.messages.append(ast.literal_eval(fetched_messages[key])[-2])
                self.messages.append(ast.literal_eval(fetched_messages[key])[-1])
        else:
            self.messages = ["No messages found."]


def alfred_sidebar():
    return rx.container(
        rx.vstack(
            rx.heading("ALFRED - HELPER"),
            rx.foreach(AlfredState.messages, lambda message: rx.text(message, font_size="14px")),
            rx.input(
                placeholder="Type your message here...",
                size="2",
                width="90%",
                height="200px",
                border_radius="8px",
                padding="10px",
            ),
            rx.hstack(
                rx.button("Send Message", color_scheme="blue", on_click=AlfredState.get_messages),
            ),
            rx.text(AlfredState.debug, font_size="14px", color="red"),
        ),
        max_width="400px",
        background="white",
        border_right="1px solid #eee",
        center_content=True,
        padding="20px",
    )