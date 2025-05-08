import requests
import json
from sqlmodel import select, Field

import reflex as rx

from rxapp.components.alfred import alfred_sidebar
from rxapp.settings import Settings


class DatabaseTableState(rx.State):
    companies: list[str] = []

    @rx.event
    def fetch_companies(self):
        response = requests.get(f"{Settings.FAST_API_URL}/org_db")
        if response.status_code == 200:
            self.companies = []
            db_companies: dict = json.loads(response.text)
            keys = list(db_companies.keys())
            for idx in range(len(db_companies[keys[0]])):
                idx_str = str(idx)
                id = db_companies[keys[0]][idx_str]
                name = db_companies[keys[1]][idx_str]
                domain = db_companies[keys[2]][idx_str]
                description = db_companies[keys[3]][idx_str]
                self.companies.append([id, name, domain, description])


def show_customer(company: list):
    return rx.table.row(
        rx.table.cell(company[0]),
        rx.table.cell(company[1]),
        rx.table.cell(company[2]),
        rx.table.cell(company[3]),
    )


def organizations():
    return rx.hstack(
        rx.box(
            alfred_sidebar(),
        ),
        rx.box(
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Id"),
                        rx.table.column_header_cell("Name"),
                        rx.table.column_header_cell("Domain"),
                        rx.table.column_header_cell("Description"),
                    ),
                ),
                rx.table.body(
                    rx.foreach(
                        DatabaseTableState.companies, show_customer
                    )
                ),
                on_mount=DatabaseTableState.fetch_companies,
                width="100%",
            ),
        ),
        rx.button(
            "Fetch data",
            on_click=DatabaseTableState.fetch_companies
        ),
        width="100%",
        spacing="0",
        align_items="flex-start"
    )
