import reflex as rx
from rxapp.components.alfred import alfred_sidebar

def people():
    return rx.hstack(
        rx.box(
            alfred_sidebar(),
        ),
        rx.box(
            rx.text("Placeholder for PEOPLE"),
            flex="1",
        ),
        width="100%",
        spacing="0",
        align_items="flex-start"
    )