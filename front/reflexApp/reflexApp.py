"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config


def index() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading("H/UMAN CRM - Frontend"),
            rx.text("Welcome to the H/UMAN CRM Frontend!"),
            rx.text("This is a simple web application built with Reflex."),
        ),
    )


app = rx.App()
app.add_page(index)
