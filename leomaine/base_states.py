import reflex as rx


class BaseState(rx.State):
    query_toggle: str = "none"
    is_request: str = "New request"
    is_expanded: bool = False

    def toggle_query(self):
        self.query_toggle = "block" if self.query_toggle == "none" else "none"
        self.is_request = (
            "New request" if self.query_toggle == "none" else "Close request"
        )

    # Toggles the expanded state of the accordion section
    def toggle_expansion(self):
        if self.is_expanded:
            self.is_expanded = False
        else:
            self.is_expanded = not self.is_expanded
