from .views.navbar import navbar
from .views.manage import manage_ui
import reflex as rx


def _tabs_trigger(text: str, icon: str, value: str):
    return rx.tabs.trigger(
        rx.hstack(
            rx.icon(icon, size=24),
            rx.heading(text, size="5"),
            spacing="2",
            align="center",
            width="100%",
        ),
        value=value,
    )


def index() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.tabs.root(
            rx.tabs.list(
                _tabs_trigger("API", "waypoints", value="manage"),
            ),
            rx.tabs.content(
                manage_ui(),
                margin_top="1em",
                value="manage",
            ),
            default_value="manage",
            width="100%",
        ),
        width="100%",
        spacing="6",
        padding_x=["1.5em", "1.5em", "3em", "5em"],
        padding_y=["1.25em", "1.25em", "2em"],
    )


base_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
    "grid.css",
]

base_style = {
    "font_family": "Inter",
}

app = rx.App(
    style=base_style,
    stylesheets=base_stylesheets,
    theme=rx.theme(
        appearance="light", has_background=True, radius="large", accent_color="orange"
    ),
)
app.add_page(
    index,
    title="Leomaine",
    description="True AI generated API management.",
)
