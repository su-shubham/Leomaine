import reflex as rx


# Chat state to manage messages and input
class ChatState(rx.State):
    messages: list[dict[str, str]] = []  # To store the chat history
    current_message: str = ""  # To store the user's current message

    def send_message(self):
        if self.current_message:
            # Add the user's message to the chat history
            self.messages.append({"sender": "User", "message": self.current_message})
            # Simulate bot response for API interaction
            self.simulate_bot_response()
            # Clear the input field after sending the message
            self.set_value("current_message", "")  # Correct way to clear the input

    def simulate_bot_response(self):
        # Simulate an API interaction response based on user's input
        if "GET" in self.current_message.upper():
            response = "Bot: Simulating a GET request to the API..."
        elif "POST" in self.current_message.upper():
            response = "Bot: Simulating a POST request with payload to the API..."
        else:
            response = "Bot: Unknown command. Please use GET or POST."

        # Add bot response to the chat history
        self.messages.append({"sender": "Bot", "message": response})

    def set_value(self, key, value):
        # Helper method to update state values
        setattr(self, key, value)
        self.update()


# Function to render chat messages
def render_chat_messages():
    return rx.box(
        rx.foreach(
            ChatState.messages,  # Iterate through messages
            lambda msg: rx.box(
                rx.text(
                    msg["message"],  # Access message content directly
                    color=rx.cond(
                        msg["sender"].contains(
                            "User"
                        ),  # Check if the sender is the user
                        "blue",
                        "green",
                    ),  # User messages in blue, Bot in green
                ),
                padding="0.5rem",
                margin="0.5rem 0",
                border_radius="5px",
                bg=rx.cond(
                    msg["sender"].contains("User"),  # Check if the sender is the user
                    "gray.100",
                    "gray.200",
                ),  # Different background for user and bot
                max_width="80%",
                align_self=rx.cond(
                    msg["sender"].contains("User"),  # Check if the sender is the user
                    "flex-end",
                    "flex-start",
                ),  # Align messages based on sender
            ),
        ),
        width="100%",
        height="300px",
        overflow_y="auto",  # Scrollable if there are too many messages
        padding="1rem",
        bg="gray.50",
        border_radius="10px",
        border="1px solid #ccc",
    )


# Function to render the chat input section
def render_chat_input():
    return rx.hstack(
        rx.input(
            value=ChatState.current_message,
            placeholder="Type your API command here (e.g., GET / POST)...",
            width="80%",
            on_change=lambda msg: ChatState.set_value(
                "current_message", msg
            ),  # Update state properly
        ),
        rx.button(
            "Chat", on_click=ChatState.send_message, width="20%", color_scheme="orange"
        ),
        width="100%",
        padding="1rem",
    )


# Full chat bot UI component
def chat_bot_ui():
    return rx.vstack(
        render_chat_messages(),
        render_chat_input(),
        width="100%",
        height="400px",
        border="1px solid #ccc",
        border_radius="10px",
        padding="1rem",
    )


# Manage UI Function to integrate chatbot into main interface
def manage_ui():
    return rx.vstack(
        chat_bot_ui(),  # The chatbot UI integrated into the main manage UI
        width="100%",
        padding_bottom="0.75em",
        border_radius="10px",
        bg=rx.color_mode_cond(
            "#faf9fb",  # Light mode background
            "#1a181a",  # Dark mode background
        ),
    )
