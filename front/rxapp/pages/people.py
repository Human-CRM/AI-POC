import reflex as rx
from rxapp.components.alfred import alfred_sidebar
from rxapp.state import AppState

def people():
    return rx.fragment(
        alfred_sidebar(),
        rx.box(
            rx.heading("CRM - People"),
            rx.hstack(
                rx.button("Add Row", on_click=AppState.add_people_row),
                rx.button("Export DB", on_click=AppState.export_people_df),
                rx.button("Refresh DB", on_click=AppState.load_people_data),
            ),
            rx.data_table(
                data=AppState.people_df,
                pagination=True,
                search=True,
            ),
            padding_left="320px",
            padding="2em",
        ),
    )
