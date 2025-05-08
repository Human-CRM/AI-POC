import requests
import json
import ast

import reflex as rx

from rxapp.settings import Settings

settings = Settings()

class AlfredState(rx.State):
    
    base_message = "Send a message to ALFRED :)"
    messages = [base_message]
    debug = ""

    # Those need async !

    @rx.event
    def get_messages(self):
        if self.messages[0] == self.base_message:
            self.messages.pop(0)

        response = requests.get(f"{settings.FAST_API_URL}/messages")
        if response.status_code == 200:
            fetched_messages = json.loads(response.text)
            self.debug += f"\n\nFetched messages: {fetched_messages}"
            self.messages.append(fetched_messages[-1])
        else:
            self.messages = ["No messages found."]

    @rx.event
    def send_message(self, form_data: dict):
        user_input = str(form_data["user_input"])
        self.messages.append(user_input.strip())
        response = requests.post(f"{settings.FAST_API_URL}/messages/?user_input={user_input.strip()}")
        if response.status_code == 200:
            self.debug = f"Message sent: {user_input.strip()}"
        else:
            self.debug = f"Error sending message: {response.text}"
        self.get_messages()


def alfred_sidebar():
    return rx.container(
        rx.vstack(
            rx.heading("ALFRED - HELPER"),
            
            # Message display area with scroll
            rx.box(
                rx.foreach(
                    AlfredState.messages,
                    lambda message, index: rx.box(
                        rx.box(
                            rx.text(
                                message,
                                font_size="22px",
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
            rx.form(
                rx.vstack(
                    rx.text_area(
                        placeholder="Type your message here...",
                        name="user_input",
                        
                        size="3",
                        width="100%",
                        min_height="60px",
                        padding="10px",
                        radius="large",
                        resize="vertical",  # Allow vertical resizing
                        rows="2",  # Default rows
                    ),
                    rx.button(
                        rx.text("Send", font_weight="bold", font_size="16", color="white"),
                        type="submit",
                        color_scheme="tomato", 
                        width="100%",
                    ),
                    width="100%",  
                ),
                on_submit=AlfredState.send_message,
                reset_on_submit=True, 
            ),

            rx.divider(),
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
        width="600px",
        background="white",
        border_right="1px solid #eee",
        padding="20px",
        height="100vh",
        display="flex",
    )