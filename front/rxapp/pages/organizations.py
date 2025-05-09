import requests
import json
import ast

import reflex as rx

from rxapp.components.alfred import alfred_sidebar
from rxapp.settings import Settings


class DatabaseTableState(rx.State):
    companies: list[str] = []
    log: str = ""
    last_analysis: str = ""

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

    @rx.event
    def enhance(self, domain:str):
        params = {"org_domain":domain}
        response = requests.put(f"{Settings.FAST_API_URL}/org_db", params=params)
        if response.status_code == 200:
            self.log += f"{response.text}"
            self.fetch_companies()
        else:
            self.log += f"[ERROR] API access upon enhancing"

    @rx.event    
    def analysis(self, domain: str):
        self.log += f"\nDOMAIN: {domain}\n"
        query = f"""According to the informations at your disposal regarding company with domain {domain}, please
        conduct an analysis regarding the capacity this company has to be successful. Be brief, straight to the point.
        """
        params = {"user_input": query, "save_db": False}
        response = requests.post(f"{Settings.FAST_API_URL}/messages", params=params)
        if response.status_code == 200:
            self.last_analysis = ast.literal_eval(json.loads(response.text))[-1]
        else:
            self.last_analysis = f"Last analysis for {domain} failed"


def show_company(company: list):
    return rx.table.row(
        rx.table.cell(company[0]),
        rx.table.cell(company[1]),
        rx.table.cell(company[2]),
        rx.table.cell(company[3]),
        rx.table.cell(company[4]),
        rx.table.cell(company[5]),
        rx.table.cell(
            rx.hstack(
                # Using direct event handlers with arguments
                rx.button(
                    "Analysis",
                    on_click=DatabaseTableState.analysis(company[2]),
                    color_scheme="blue",
                ),
                rx.button(
                    "Enhance",
                    on_click=DatabaseTableState.enhance(company[2]),
                    color_scheme="green",
                ),
                spacing="2",
            ),
        ),
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
                            rx.table.column_header_cell("Tools"),
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
            rx.divider(),
            rx.box(
                rx.heading("Last analysis:"),
                rx.text(DatabaseTableState.last_analysis, font_size="14px", color="black")
            ),
            rx.divider(),
            rx.box(
                rx.text("Debug Info:", font_weight="bold", color="red"),
                rx.text(DatabaseTableState.log, font_size="12px", color="red"),
                bg="gray.50",
                p="2",
                border_radius="md",
                width="100%",
            ),
            flex="1",
        ),
        spacing="3",
        align_items="flex-start",
        flex="1"
    )
