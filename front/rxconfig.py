import reflex as rx

config = rx.Config(
    app_name="rxapp",
    frontend_port=3000,
    backend_port=8001,
    api_url="http://localhost:8001",
    db_url="",
)