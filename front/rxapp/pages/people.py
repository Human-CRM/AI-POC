import requests
import json

import reflex as rx

from rxapp.components.alfred import alfred_sidebar
from rxapp.settings import Settings


class DatabaseTableState(rx.State):
    people: list[str] = []

    @rx.event
    def fetch_people(self):
        response = requests.get(f"{Settings.FAST_API_URL}/people_db")
        if response.status_code == 200:
            self.people = []
            db_people: dict = json.loads(response.text)
            keys = list(db_people.keys())
            for idx in range(len(db_people[keys[0]])):
                idx_str = str(idx)
                id = db_people[keys[0]][idx_str]
                first_name = db_people[keys[1]][idx_str]
                last_name = db_people[keys[2]][idx_str]
                email = db_people[keys[3]][idx_str]
                phone = db_people[keys[4]][idx_str]
                linkedin_url = db_people[keys[5]][idx_str]
                self.people.append([id, first_name, last_name, email, phone, linkedin_url])


    @rx.event
    def add_person(self, form_data: dict):
        email_to_add = form_data["person_email"]
        params = {"email": email_to_add}
        requests.post(f"{Settings.FAST_API_URL}/people_db", params=params)
        self.fetch_people()


def show_people(person: list):
    return rx.table.row(
        rx.table.cell(person[0]),
        rx.table.cell(person[1]),
        rx.table.cell(person[2]),
        rx.table.cell(person[3]),
        rx.table.cell(person[4]),
        rx.table.cell(person[5]),
    )


def people():
    return rx.hstack(
        rx.box(
            alfred_sidebar(),
            width="25%"
        ),
        rx.vstack(
            rx.box(
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Id"),
                            rx.table.column_header_cell("First Name"),
                            rx.table.column_header_cell("Last Name"),
                            rx.table.column_header_cell("Email"),
                            rx.table.column_header_cell("Phone"),
                            rx.table.column_header_cell("Linkedin"),
                        ),
                    ),
                    rx.table.body(
                        rx.foreach(
                            DatabaseTableState.people, show_people
                        )
                    ),
                    on_mount=DatabaseTableState.fetch_people,
                    width="100%",
                ),
                width="100%"
            ),
            rx.hstack(
                rx.button(
                    "Fetch data",
                    on_click=DatabaseTableState.fetch_people
                ),
                rx.form(
                    rx.hstack(
                        rx.input(
                            name="person_email",
                            placeholder="Person's email...",
                            width="70%"
                        ),
                        rx.button(
                            rx.text("Add person", font_weight="bold", font_size="16", color="white"),
                            type="submit",
                            color_scheme="tomato", 
                            width="30%",
                        ),
                    ),
                    on_submit=DatabaseTableState.add_person,
                    reset_on_submit=True
                ),
                spacing="3",
                height="40px",
                width="60%"
            ),
            flex="1",
        ),
        width="100%",
        spacing="3",
        align_items="flex-start",
        flex="1"
    )
