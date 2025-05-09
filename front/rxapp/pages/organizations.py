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
                industry = db_companies[keys[3]][idx_str]
                phone = db_companies[keys[4]][idx_str]
                description = db_companies[keys[5]][idx_str]
                self.companies.append([id, name, domain, industry, phone, description])


    @rx.event
    def add_company(self, form_data: dict):
        domain_to_add = form_data["company_domain"]
        params = {"org_domain": domain_to_add}
        requests.post(f"{Settings.FAST_API_URL}/org_db", params=params)
        self.fetch_companies()


def show_company(company: list):
    return rx.table.row(
        rx.table.cell(company[0]),
        rx.table.cell(company[1]),
        rx.table.cell(company[2]),
        rx.table.cell(company[3]),
        rx.table.cell(company[4]),
        rx.table.cell(company[5]),
    )


def organizations():
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
                            rx.table.column_header_cell("Name"),
                            rx.table.column_header_cell("Domain"),
                            rx.table.column_header_cell("Industry"),
                            rx.table.column_header_cell("Phone"),
                            rx.table.column_header_cell("Description"),
                        ),
                    ),
                    rx.table.body(
                        rx.foreach(
                            DatabaseTableState.companies, show_company
                        )
                    ),
                    on_mount=DatabaseTableState.fetch_companies,
                    width="100%",
                ),
                width="100%"
            ),
            rx.hstack(
                rx.button(
                    "Fetch data",
                    on_click=DatabaseTableState.fetch_companies
                ),
                rx.form(
                    rx.hstack(
                        rx.input(
                            name="company_domain",
                            placeholder="Company domain",
                            width="70%"
                        ),
                        rx.button(
                            rx.text("Add company", font_weight="bold", font_size="16", color="white"),
                            type="submit",
                            color_scheme="tomato", 
                            width="30%",
                        ),
                    ),
                    on_submit=DatabaseTableState.add_company,
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
