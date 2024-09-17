import reflex as rx


def navbar():
    return rx.flex(
        rx.hstack(
            rx.image(src="/lemon.svg", height="38px"),
            rx.heading("Leomaine", size="7"),
            rx.badge(
                "0.0.1",
                radius="full",
                align="center",
                color_scheme="orange",
                variant="surface",
            ),
            align="center",
        ),
        rx.spacer(),
        spacing="2",
        flex_direction=["column", "column", "row"],
        align="center",
        width="100%",
        top="0px",
    )
