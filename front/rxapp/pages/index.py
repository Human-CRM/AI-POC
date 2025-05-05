import reflex as rx
from rxapp.components.alfred import alfred_sidebar

def index():
    return rx.hstack(
        rx.box(
            alfred_sidebar(),
        ),
        rx.box(
            rx.heading("H/UMAN CRM"),
            rx.text("Welcome to H/UMAN, powered by AI."),
            rx.text("Please choose a page to start!"),
            padding_left="320px",
            padding="2em",
            flex="1",
        ),
        width="100%",
        spacing="0",
        align_items="flex-start"
    )
