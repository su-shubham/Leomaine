import reflex as rx
from leomaine.queries import QueryState, QueryAPI, BaseState
from typing import Optional
from leomaine.views import chat


# Helper for the title or head of sections
def head(title: str):
    return rx.hstack(
        rx.text(title, font_size=22),
        width="100%",
        justify="center",
    )


# Add event button for adding entries (e.g., headers, cookies)
def item_add_event(event_trigger: callable):
    return rx.button(
        rx.hstack(
            rx.text("+"),
            rx.text("Add", font_weight="bold"),
            width="100%",
            justify="space-between",
        ),
        size="sm",
        on_click=event_trigger,
        padding="0.35em 0.75em",
        cursor="pointer",
        color_scheme="gray",
    )


# Function to handle form entries (key-value pairs)
def form_entry(data: dict[str, list[str, str]]):
    def create_entry(title: str, function: callable):
        return rx.input(
            placeholder=title,
            width="100%",
            on_change=function,
            variant="soft",
        )

    return rx.hstack(
        create_entry("key", lambda key: QueryState.update_keys(key, data)),
        create_entry("value", lambda value: QueryState.update_values(value, data)),
        rx.button(
            "DEL",
            on_click=lambda: QueryState.remove_entry(),
            color_scheme="red",
            cursor="pointer",
            variant="soft",
        ),
        width="100%",
        spacing="2",
    )


# Accordion form item
def form_item(
    title: Optional[str],  # Optional title argument
    state: list[dict[str, str]],
    func: callable,
    event_trigger: callable,
):
    return rx.accordion.item(
        header=title,  # Title for each accordion section
        content=rx.box(
            head(title),  # Use the title in the head
            rx.foreach(state, func),
            item_add_event(event_trigger),
            width="100%",
            padding="0.5rem 0",
            spacing="1rem",  # Adjusting the spacing between items
        ),
    )


# Accordion for handling body params with GET and POST differentiation
def form_body_param_item(
    state: list[dict[str, str]], func: callable, event_trigger: callable
):
    return rx.accordion.item(
        header="Body",  # Title for the body section
        content=rx.box(
            rx.match(
                QueryState.current_req_method,  # Matching the current request method (GET/POST)
                (
                    "GET",
                    rx.select(
                        items=QueryState.get_params_body,
                        default_value="None",
                        width="100%",
                    ),
                ),
                (
                    "POST",
                    rx.vstack(
                        rx.hstack(
                            item_add_event(event_trigger),
                            width="100%",
                            justify="flex-end",
                        ),
                        rx.select(
                            items=QueryState.post_params_body,
                            default_value="JSON",
                            width="100%",
                        ),
                        rx.vstack(rx.foreach(state, func), width="100%", spacing="1"),
                        width="100%",
                    ),
                ),
            ),
        ),
    )


# Accordion for handling request methods, headers, body, and cookies
def form_request_item():
    return rx.accordion.item(
        header="Requests",
        content=rx.box(
            rx.hstack(
                rx.select(
                    items=QueryState.req_methods,
                    width="120px",
                    default_value="GET",
                    on_change=QueryState.get_request,
                ),
                rx.input(
                    value=QueryState.req_url,
                    width="100%",
                    on_change=QueryState.set_req_url,
                    placeholder="https://example_site.com/api/v2/endpoint.json",
                ),
                width="100%",
            )
        ),
    )


# Function to render the entire query form (Headers, Body, Cookies)
def render_query_form():
    return rx.vstack(
        form_item(QueryState.headers, form_entry, QueryState.add_header),
        form_body_param_item(QueryState.body, form_entry, QueryState.add_body),
        form_item(QueryState.cookies, form_entry, QueryState.add_cookie),
        width="100%",  # Set full width for a better layout
        spacing="2",
        padding="0em 0.75em",
    )


# Header section for selecting methods and URL input
def render_query_header():
    return rx.hstack(
        rx.hstack(
            rx.select(
                items=QueryState.req_methods,
                width="100px",
                default_value="GET",
                on_change=QueryState.get_request,
                size="3",
            ),
            rx.input(
                value=QueryState.req_url,
                width="100%",
                on_change=QueryState.set_req_url,
                placeholder="https://example_site.com/api/v2/endpoint.json",
                size="3",
            ),
            rx.button(
                "↓", size="3", on_click=BaseState.toggle_expansion, cursor="pointer"
            ),
            width="100%",
            spacing="1",
        ),
        rx.button(
            "Send", size="3", on_click=QueryAPI.run_get_request, cursor="pointer"
        ),
        width="100%",
        border_bottom=rx.color_mode_cond(
            "1px solid rgba(45, 45, 45, 0.05)", "1px solid rgba(45, 45, 45, 0.51)"
        ),
        padding="1em 0.75em",
        justify="space-between",
    )


# Expandable accordion section for Headers, Body, and Cookies
def render_expandable_section():
    return rx.cond(
        BaseState.is_expanded,  # Conditionally render based on expansion state
        rx.accordion.root(
            form_item("Headers", QueryState.headers, form_entry, QueryState.add_header),
            form_body_param_item(QueryState.body, form_entry, QueryState.add_body),
            form_item("Cookies", QueryState.cookies, form_entry, QueryState.add_cookie),
            collapsible=True,
            variant="surface",
            width="100%",
            border="none",
        ),
    )


# Main UI function that brings everything together
def manage_ui():
    return rx.vstack(
        render_query_header(),
        render_expandable_section(),
        chat.chat_bot_ui(),
        width="100%",
        padding_bottom="0.75em",
        border_radius="10px",
        bg=rx.color_mode_cond(
            "#faf9fb",  # Light mode background
            "#1a181a",  # Dark mode background
        ),
    )
