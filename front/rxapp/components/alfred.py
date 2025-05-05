import reflex as rx
from rxapp.state import AppState

def alfred_sidebar():
    return rx.box(
        rx.vstack(
            rx.heading("ALFRED - HELPER"),
            rx.box(
                rx.markdown(AppState.info_text),
                height="400px",
                border="1px solid #ccc",
                padding="1em",
                overflow="auto",
            ),
            rx.form(
                rx.text_area(
                    placeholder="Message",
                    value=AppState.user_input,
                    on_change=AppState.set_user_input,
                ),
                rx.button(
                    "Send",
                    type_="submit",
                ),
                on_submit=AppState.send_message,
            ),
            rx.button(
                "RESET",
                color_scheme="red",
                on_click=AppState.reset_messages,
            ),
            width="300px",
            padding="1em",
        ),
        position="fixed",
        height="100vh",
        background="white",
        border_right="1px solid #eee",
    )