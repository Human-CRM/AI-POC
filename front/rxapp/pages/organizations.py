import reflex as rx
from rxapp.components.alfred import alfred_sidebar
from rxapp.state import AppState

def organizations():
    return rx.fragment(
        alfred_sidebar(),
        rx.box(
            rx.heading("CRM - Organizations"),
            rx.hstack(
                rx.button("Add Row", on_click=AppState.add_org_row),
                rx.button("Export DB", on_click=AppState.export_org_df),
                rx.button("Refresh DB", on_click=AppState.load_org_data),
            ),
            rx.data_table(
                data=AppState.org_df,
                pagination=True,
                search=True,
            ),
            padding_left="320px",
            padding="2em",
        ),
    )
