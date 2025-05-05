import reflex as rx
from rxapp.components.alfred import alfred_sidebar

def index():
    return rx.fragment(
        alfred_sidebar(),
        rx.box(
            rx.heading("H/UMAN CRM"),
            rx.text("Welcome to H/UMAN, powered by AI."),
            rx.text("Please choose a page to start!"),
            padding_left="320px",
            padding="2em",
        ),
    )
