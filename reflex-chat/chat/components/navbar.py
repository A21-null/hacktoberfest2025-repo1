import reflex as rx
from chat.state import State


def sidebar_chat(chat: str) -> rx.Component:
    """A sidebar chat item.

    Args:
        chat: The chat item.
    """
    return rx.drawer.close(
        rx.hstack(
            rx.button(
                chat,
                on_click=lambda: State.set_chat(chat),
                width="80%",
                variant="surface",
            ),
            rx.button(
                rx.icon(tag="trash", stroke_width=1),
                on_click=lambda: State.delete_chat(chat),
                width="20%",
                variant="surface",
                color_scheme="red",
            ),
            width="100%",
        ),
        key=chat,
    )


def sidebar(trigger) -> rx.Component:
    """The sidebar component."""
    return rx.drawer.root(
        rx.drawer.trigger(trigger),
        rx.drawer.overlay(),
        rx.drawer.portal(
            rx.drawer.content(
                rx.vstack(
                    rx.heading(
                        "Conversaciones",
                        color=rx.color("mauve", 11),
                    ),
                    rx.divider(),
                    rx.foreach(
                        State.chat_titles,
                        lambda chat: sidebar_chat(chat),
                    ),
                    align_items="stretch",
                    width="100%",
                ),
                top="auto",
                right="auto",
                height="100%",
                width="20em",
                padding="2em",
                background_color=rx.color("mauve", 2),
                outline="none",
            )
        ),
        direction="left",
    )


def modal(trigger) -> rx.Component:
    """A modal to create a new chat."""
    return rx.dialog.root(
        rx.dialog.trigger(trigger),
        rx.dialog.content(
            rx.form(
                rx.hstack(
                    rx.input(
                        placeholder="Nombre de la conversación",
                        name="new_chat_name",
                        flex="1",
                        min_width="20ch",
                    ),
                    rx.button("Crear conversación"),
                    spacing="2",
                    wrap="wrap",
                    width="100%",
                ),
                on_submit=State.create_chat,
            ),
            background_color=rx.color("mauve", 1),
        ),
        open=State.is_modal_open,
        on_open_change=State.set_is_modal_open,
    )


def navbar():
    return rx.hstack(
        rx.box(
            rx.heading("Breogan", size="4", color="#2563eb"),
            margin_inline_end="auto",
        ),
        rx.hstack(
            rx.button(
                "Iniciar sesión",
                background_color="#f8fafc",
                color="#2563eb",
                border="1px solid #cbd5e1",
                _hover={"background_color": "#e2e8f0"},
                on_click=lambda: State.set_login_modal_open(True),
            ),
            rx.button(
                "Registrarse",
                background_color="#2563eb",
                color="white",
                _hover={"background_color": "#1d4ed8"},
                on_click=lambda: State.set_register_modal_open(True),
            ),
            spacing="3",
        ),
        sidebar(
            rx.icon_button(
                "messages-square",
                background_color="#f1f5f9",
                color="#64748b",
                _hover={"background_color": "#e2e8f0"},
            )
        ),
        justify_content="space-between",
        align_items="center",
        padding="16px 24px",
        background_color="white",
        border_bottom="1px solid #e2e8f0",
    )
