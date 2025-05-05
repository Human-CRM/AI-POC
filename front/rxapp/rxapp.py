import reflex as rx
from rxapp.pages.index import index
from rxapp.pages.organizations import organizations
from rxapp.pages.people import people

app = rx.App()

app.add_page(index, route="/")
app.add_page(organizations, route="/organizations")
app.add_page(people, route="/people")
