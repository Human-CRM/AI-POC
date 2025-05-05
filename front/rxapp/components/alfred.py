import reflex as rx

def alfred_sidebar():
    return rx.box(
        rx.vstack(
            rx.heading("ALFRED - HELPER"),
            rx.text("Placeholder for Alfred")
        ),
        height="100vh",
        background="white",
        border_right="1px solid #eee",
    )