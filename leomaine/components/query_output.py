import reflex as rx

from leomaine.queries import QueryAPI


def create_table_header(title: str):
    return rx.table.column_header_cell(title)


def create_query_rows(data: dict[str, str]):
    def fill_rows_with_data(data_):
        return rx.table.cell(
            f"{data_[1]}",
            on_click=QueryAPI.display_selected_row(data),
            cursor="pointer",
        )

    return rx.table.row(
        rx.foreach(data, fill_rows_with_data),
        _hover={"bg": rx.color(color="gray", shade=4)},
    )


def create_pagination():
    return rx.hstack(
        rx.hstack(
            rx.text("Entries per page", weight="bold"),
            rx.select(
                QueryAPI.limits, default_value="5", on_change=QueryAPI.delta_limit
            ),
            align_items="center",
        ),
        rx.hstack(
            rx.text(
                f"Page {QueryAPI.current_page}/{QueryAPI.total_pages}",
                width="100px",
                weight="bold",
            ),
            rx.chakra.button_group(
                rx.icon(
                    tag="chevron-left", on_click=QueryAPI.previous, cursor="pointer"
                ),
                rx.icon(tag="chevron-right", on_click=QueryAPI.next, cursor="pointer"),
                is_attached=True,
            ),
            align_items="center",
            spacing="1",
        ),
        align_items="center",
        spacing="4",
    )


# def render_output():
#     return rx.center(
#         rx.cond(
#             QueryAPI.get_data,
#             rx.vstack(
#                 create_pagination(),
#                 rx.table.root(
#                     rx.table.header(
#                         rx.table.row(
#                             rx.foreach(QueryAPI.get_table_headers, create_table_header)
#                         ),
#                     ),
#                     rx.table.body(
#                         rx.foreach(QueryAPI.paginated_data, create_query_rows)
#                     ),
#                     width="100%",
#                     variant="surface",
#                     size="1",
#                 ),
#                 width="70%",
#                 overflow="auto",
#             ),
#             rx.spacer(),
#         ),
#         flex="60%",
#         bg=rx.color_mode_cond(
#             "#faf9fb",
#             "#1a181a",
#         ),
#         border_radius="10px",
#         overflow="auto",
#     )
# Chat state for showing/hiding the chat box
class ChatState(QueryAPI):
    show_chat_box: bool = False
    user_query: str = ""

    # Function to toggle the chat box visibility
    def toggle_chat_box(self):
        self.show_chat_box = not self.show_chat_box

    # Function to handle user input and store the query
    def set_user_query(self, value: str):
        self.user_query = value

    # Function to handle submitting the query (e.g., send to OpenAI or other API)
    async def submit_query(self):
        if self.user_query:
            # You can send this query to your backend or OpenAI API here
            print(f"User Query Submitted: {self.user_query}")
            # Reset the input after submission
            self.user_query = ""


# Render the input card for chatting
def render_chat_box():
    return rx.box(
        rx.vstack(
            rx.text("Chat with API", font_weight="bold", font_size="md"),
            rx.input(
                placeholder="Type your query...",
                width="100%",
                on_change=ChatState.set_user_query,  # Store input value
            ),
            rx.button(
                "Send",
                size="sm",
                on_click=ChatState.submit_query,  # Submit the query
                color_scheme="blue",
            ),
        ),
        padding="1em",
        border="1px solid",
        border_color=rx.color_mode_cond("gray.200", "gray.700"),
        border_radius="md",
        bg=rx.color_mode_cond("white", "gray.800"),
        width="100%",
        margin_top="1em",
    )


# Modify the render_output function to include the chat functionality
def render_output():
    return rx.center(
        rx.cond(
            QueryAPI.get_data,
            rx.vstack(
                create_pagination(),
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.foreach(QueryAPI.get_table_headers, create_table_header)
                        ),
                    ),
                    rx.table.body(
                        rx.foreach(QueryAPI.paginated_data, create_query_rows)
                    ),
                    width="100%",
                    variant="surface",
                    size="1",
                ),
                # Add a "Chat" button that toggles the chat box
                rx.button(
                    "Chat",
                    size="md",
                    on_click=ChatState.toggle_chat_box,
                    color_scheme="green",
                ),
                # Conditionally render the chat box if `show_chat_box` is True
                rx.cond(
                    ChatState.show_chat_box,
                    render_chat_box(),  # Show the chat box when button is clicked
                ),
                width="70%",
                overflow="auto",
            ),
            rx.spacer(),
        ),
        flex="60%",
        bg=rx.color_mode_cond(
            "#faf9fb",
            "#1a181a",
        ),
        border_radius="10px",
        overflow="auto",
    )
