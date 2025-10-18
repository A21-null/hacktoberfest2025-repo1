"""The main Chat app."""

import reflex as rx

from chat.components import chat, sidebar
from chat.pages.auth_pages import login_page, register_page
from chat.pages.settings import settings_page
from chat.state import State


def index() -> rx.Component:
    """The main app."""
    unauth = rx.center(
        rx.vstack(
            rx.heading("Breogan", size="6", color="#2563eb"),
            rx.heading("Acceso requerido", size="4", color="#64748b"),
            rx.text(
                "Debes iniciar sesión para acceder a Breogan.",
                color="#64748b",
            ),
            rx.link(
                "Ir a iniciar sesión",
                href="/login",
                background_color="#2563eb",
                color="white",
                padding="12px 24px",
                border_radius="8px",
                text_decoration="none",
                _hover={"background_color": "#1d4ed8"},
            ),
            spacing="4",
            text_align="center",
        ),
        background="linear-gradient(135deg, #fff5f9 1%, #e2e8f0 100%)",
        height="100vh",
    )

    auth_view = rx.box(
        sidebar.sidebar(),
        rx.box(
            sidebar.top_navbar(),
            rx.box(
                chat.chat(),
                padding_top="80px",
                padding_left="280px",
                padding_right="32px",
                padding_bottom="120px",
                height="100vh",
                overflow_y="auto",
            ),
            chat.action_bar(),
            position="relative",
            width="100%",
            height="100vh",
        ),
        sidebar.voice_modal(),
        sidebar.profile_modal(),
        sidebar.flashcard_modal(),
        sidebar.create_flashcard_modal(),
        position="relative",
        width="100%",
        height="100vh",
        background=(
            "linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #60a5fa 100%)"
        ),
    )

    return rx.cond(State.current_user, auth_view, unauth)


# Add state and page to the app.
app = rx.App()
app.add_page(index)
app.add_page(login_page, "/login")
app.add_page(register_page, "/register")
app.add_page(settings_page, "/settings")
