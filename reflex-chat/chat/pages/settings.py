"""Settings page for the Breogan app."""

import reflex as rx
from chat.state import State


def settings_page() -> rx.Component:
    """Settings page layout."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.link(
                    rx.hstack(
                        rx.icon("arrow-left", size=20, color="#2563eb"),
                        rx.text("Volver", color="#2563eb", font_weight="500"),
                        spacing="2",
                    ),
                    href="/",
                    text_decoration="none",
                ),
                rx.spacer(),
                justify_content="space-between",
                align_items="center",
                width="100%",
                margin_bottom="32px",
            ),
            rx.heading(
                "Configuración",
                size="6",
                color="#1e40af",
                margin_bottom="24px",
            ),
            rx.vstack(
                rx.box(
                    rx.heading(
                        "Idioma de origem",
                        size="4",
                        color="#374151",
                        margin_bottom="12px",
                    ),
                    rx.text(
                        "Selecciona o teu idioma nativo para personalizar "
                        "a experiencia de aprendizaxe:",
                        color="#64748b",
                        margin_bottom="16px",
                    ),
                    rx.select(
                        [
                            "Español (España)",
                            "Español (América)",
                            "Português",
                            "English",
                            "Français"
                        ],
                        placeholder="Selecciona idioma...",
                        background_color="white",
                        border="1px solid #d1d5db",
                        padding="12px 16px",
                        border_radius="8px",
                        width="100%",
                        color="#374151",
                        default_value="Español (España)",
                    ),
                    background_color="white",
                    padding="24px",
                    border_radius="12px",
                    border="1px solid #e5e7eb",
                    margin_bottom="24px",
                ),
                rx.box(
                    rx.heading(
                        "Conta",
                        size="4",
                        color="#374151",
                        margin_bottom="12px",
                    ),
                    rx.text(
                        f"Sesión actual: {State.current_user}",
                        color="#64748b",
                        margin_bottom="16px",
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon("log-out", size=16, color="white"),
                            rx.text("Pechar sesión", color="white"),
                            spacing="2",
                        ),
                        background_color="#ef4444",
                        border="none",
                        padding="12px 24px",
                        border_radius="8px",
                        _hover={"background_color": "#dc2626"},
                        on_click=State.logout,
                    ),
                    background_color="white",
                    padding="24px",
                    border_radius="12px",
                    border="1px solid #e5e7eb",
                ),
                spacing="0",
                width="100%",
                max_width="600px",
            ),
            spacing="0",
            align_items="start",
            width="100%",
            max_width="800px",
            margin="0 auto",
        ),
        padding="32px",
        min_height="100vh",
        background="linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)",
    )
