import reflex as rx
from chat.state import State


def level_item(level: int, title: str) -> rx.Component:
    """A single level item in the sidebar."""
    return rx.button(
        rx.hstack(
            rx.box(
                rx.icon("book-open", size=20, color="white"),
                background_color=rx.cond(
                    State.selected_level == level,
                    "rgba(255, 255, 255, 0.2)",
                    "rgba(255, 255, 255, 0.1)",
                ),
                padding="12px",
                border_radius="8px",
                display="flex",
                align_items="center",
                justify_content="center",
            ),
            rx.vstack(
                rx.text(
                    f"Nivel {level}",
                    color="white",
                    font_weight="600",
                    font_size="sm",
                    margin="0",
                ),
                rx.text(
                    title,
                    color="rgba(255, 255, 255, 0.8)",
                    font_size="xs",
                    margin="0",
                ),
                align_items="flex-start",
                justify_content="center",
                spacing="1",
                flex="1",
            ),
            align_items="center",
            justify_content="flex-start",
            spacing="3",
            width="100%",
        ),
        background_color=rx.cond(
            State.selected_level == level,
            "rgba(255, 255, 255, 0.1)",
            "transparent",
        ),
        padding="12px 16px",
        border_radius="12px",
        border="none",
        width="100%",
        cursor="pointer",
        _hover={"background_color": "rgba(255, 255, 255, 0.15)"},
        margin_bottom="8px",
        on_click=State.set_selected_level(level),
        display="flex",
        align_items="center",
        justify_content="flex-start",
        text_align="left",
    )


def sidebar() -> rx.Component:
    """Left sidebar with language learning levels."""
    return rx.box(
        rx.vstack(
            # Header section - properly centered
            rx.vstack(
                rx.text(
                    "Progreso de Aprendizaxe",
                    color="white",
                    font_weight="700",
                    font_size="lg",
                    margin="0",
                    text_align="center",
                ),
                rx.text(
                    "Segue a túa ruta",
                    color="rgba(255, 255, 255, 0.7)",
                    font_size="sm",
                    margin="0",
                    text_align="center",
                ),
                align_items="center",
                justify_content="center",
                spacing="2",
                margin_bottom="32px",
                width="100%",
            ),
            # Level items - left aligned within centered container
            rx.vstack(
                level_item(1, "Iniciación"),
                level_item(2, "Básico"),
                level_item(3, "Intermedio"),
                level_item(4, "Avanzado"),
                level_item(5, "Experto"),
                align_items="stretch",
                justify_content="flex-start",
                spacing="0",
                width="100%",
            ),
            align_items="center",
            justify_content="flex-start",
            spacing="0",
            width="100%",
            height="100%",
        ),
        width="280px",
        height="100vh",
        background=(
            "linear-gradient(180deg, #1e40af 0%, #1e3a8a 50%, #1e293b 100%)"
        ),
        padding="24px",
        position="fixed",
        left="0",
        top="0",
        overflow_y="auto",
        display="flex",
        align_items="flex-start",
        justify_content="flex-start",
    )


def top_navbar() -> rx.Component:
    """Top navigation bar matching the reference design."""
    return rx.box(
        rx.hstack(
            rx.text(
                "Breogan",
                color="white",
                font_weight="700",
                font_size="xl",
            ),
            rx.spacer(),
            rx.hstack(
                rx.button(
                    rx.hstack(
                        rx.icon("book", size=16, color="white"),
                        rx.text(
                            "Flashcards", 
                            color="white", 
                            font_size="sm"
                        ),
                        spacing="2",
                        align_items="center",
                    ),
                    background_color="rgba(255, 255, 255, 0.1)",
                    border="none",
                    padding="8px 16px",
                    border_radius="8px",
                    _hover={"background_color": "rgba(255, 255, 255, 0.2)"},
                    on_click=State.show_random_flashcard,
                    display="flex",
                    align_items="center",
                ),
                rx.button(
                    rx.hstack(
                        rx.icon("mic", size=16, color="white"),
                        rx.text(
                            "Modo conversación", 
                            color="white", 
                            font_size="sm"
                        ),
                        spacing="2",
                        align_items="center",
                    ),
                    background_color="rgba(255, 255, 255, 0.1)",
                    border="none",
                    padding="8px 16px",
                    border_radius="8px",
                    _hover={"background_color": "rgba(255, 255, 255, 0.2)"},
                    on_click=State.set_voice_modal_open(True),
                    display="flex",
                    align_items="center",
                ),
                rx.button(
                    rx.hstack(
                        rx.icon("user", size=16, color="white"),
                        rx.text("Perfil", color="white", font_size="sm"),
                        spacing="2",
                        align_items="center",
                    ),
                    background_color="rgba(255, 255, 255, 0.1)",
                    border="none",
                    padding="8px 16px",
                    border_radius="8px",
                    _hover={"background_color": "rgba(255, 255, 255, 0.2)"},
                    on_click=State.set_profile_modal_open(True),
                    display="flex",
                    align_items="center",
                ),
                spacing="3",
                align_items="center",
            ),
            justify_content="space-between",
            align_items="center",
            width="100%",
        ),
        background="linear-gradient(90deg, #1e40af 0%, #3b82f6 100%)",
        padding="16px 24px",
        position="fixed",
        top="0",
        left="280px",
        right="0",
        z_index="100",
        display="flex",
        align_items="center",
    )


def create_flashcard_modal() -> rx.Component:
    """Modal for creating flashcards from selected text."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                "Crear Nova Flashcard",
                color="#1e40af",
                font_weight="700",
                text_align="center",
            ),
            rx.vstack(
                rx.text(
                    "Texto seleccionado:",
                    color="#64748b",
                    font_weight="500",
                    font_size="sm",
                    margin_bottom="8px",
                ),
                rx.box(
                    rx.text(
                        State.selected_text,
                        color="#1e40af",
                        font_weight="600",
                        font_size="lg",
                        text_align="center",
                    ),
                    background_color="#f8fafc",
                    padding="16px",
                    border_radius="8px",
                    border="1px solid #e2e8f0",
                    margin_bottom="24px",
                    width="100%",
                ),
                rx.text(
                    "Xerarase unha explicación automática usando Gemini AI",
                    color="#64748b",
                    font_size="sm",
                    text_align="center",
                    margin_bottom="16px",
                ),
                rx.hstack(
                    rx.button(
                        "Crear Flashcard",
                        background_color="#2563eb",
                        color="white",
                        border="none",
                        padding="8px 24px",
                        border_radius="8px",
                        _hover={"background_color": "#1d4ed8"},
                        on_click=State.create_flashcard_from_selection,
                    ),
                    rx.dialog.close(
                        rx.button(
                            "Cancelar",
                            background_color="#f1f5f9",
                            color="#64748b",
                            border="none",
                            padding="8px 24px",
                            border_radius="8px",
                            _hover={"background_color": "#e2e8f0"},
                        ),
                    ),
                    spacing="3",
                    justify_content="center",
                    align_items="center",
                ),
                spacing="4",
                align_items="center",
                width="100%",
            ),
            max_width="450px",
            padding="32px",
            background_color="white",
            border_radius="12px",
        ),
        open=State.create_flashcard_modal_open,
        on_open_change=State.set_create_flashcard_modal_open,
    )


def flashcard_modal() -> rx.Component:
    """Modal for displaying Galician flashcards."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                "Flashcard Galego",
                color="#1e40af",
                font_weight="700",
                text_align="center",
            ),
            rx.vstack(
                rx.box(
                    rx.text(
                        State.current_flashcard["gl"],
                        color="#1e40af",
                        font_weight="600",
                        font_size="xl",
                        text_align="center",
                        margin_bottom="12px",
                    ),
                    rx.text(
                        State.current_flashcard["es"],
                        color="#64748b",
                        font_size="lg",
                        text_align="center",
                        font_style="italic",
                    ),
                    background_color="#f8fafc",
                    padding="24px",
                    border_radius="12px",
                    border="2px solid #e2e8f0",
                    margin_bottom="24px",
                    width="100%",
                    text_align="center",
                ),
                rx.hstack(
                    rx.button(
                        "Nova frase",
                        background_color="#2563eb",
                        color="white",
                        border="none",
                        padding="8px 24px",
                        border_radius="8px",
                        _hover={"background_color": "#1d4ed8"},
                        on_click=State.show_random_flashcard,
                    ),
                    rx.dialog.close(
                        rx.button(
                            "Pechar",
                            background_color="#f1f5f9",
                            color="#64748b",
                            border="none",
                            padding="8px 24px",
                            border_radius="8px",
                            _hover={"background_color": "#e2e8f0"},
                        ),
                    ),
                    spacing="3",
                    justify_content="center",
                    align_items="center",
                ),
                spacing="4",
                align_items="center",
                width="100%",
            ),
            max_width="400px",
            padding="32px",
            background_color="white",
            border_radius="12px",
        ),
        open=State.flashcard_modal_open,
        on_open_change=State.set_flashcard_modal_open,
    )


def voice_modal() -> rx.Component:
    """Modal for voice input mode."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                "Modo Conversación",
                color="#1e40af",
                font_weight="700",
                text_align="center",
            ),
            rx.vstack(
                rx.text(
                    "Prepárate para practicar galego por voz",
                    color="#64748b",
                    text_align="center",
                    margin_bottom="16px",
                ),
                rx.box(
                    rx.icon(
                        "mic",
                        size=64,
                        color=rx.cond(
                            State.voice_modal_open,
                            "#ef4444",
                            "#64748b",
                        ),
                    ),
                    text_align="center",
                    padding="24px",
                    background_color="#f8fafc",
                    border_radius="12px",
                    margin_bottom="16px",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                ),
                rx.text(
                    "Esta funcionalidade estará dispoñible pronto.",
                    color="#64748b",
                    font_size="sm",
                    text_align="center",
                    margin_bottom="24px",
                ),
                rx.hstack(
                    rx.dialog.close(
                        rx.button(
                            "Cancelar",
                            background_color="#f1f5f9",
                            color="#64748b",
                            border="none",
                            padding="8px 24px",
                        ),
                    ),
                    rx.button(
                        "Comezar",
                        background_color="#2563eb",
                        color="white",
                        border="none",
                        padding="8px 24px",
                        _hover={"background_color": "#1d4ed8"},
                    ),
                    spacing="3",
                    justify_content="center",
                    align_items="center",
                ),
                spacing="4",
                align_items="center",
                width="100%",
            ),
            max_width="400px",
            padding="32px",
            background_color="white",
            border_radius="12px",
        ),
        open=State.voice_modal_open,
        on_open_change=State.set_voice_modal_open,
    )


def profile_modal() -> rx.Component:
    """Modal for profile options."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                "Perfil",
                color="#1e40af",
                font_weight="700",
                text_align="center",
            ),
            rx.vstack(
                rx.text(
                    f"Conectado como: {State.current_user}",
                    color="#64748b",
                    margin_bottom="16px",
                    text_align="center",
                ),
                rx.vstack(
                    rx.link(
                        rx.hstack(
                            rx.icon("settings", size=16, color="#2563eb"),
                            rx.text(
                                "Configuración",
                                color="#2563eb",
                                font_weight="500",
                            ),
                            spacing="2",
                            align_items="center",
                        ),
                        href="/settings",
                        text_decoration="none",
                        padding="12px 16px",
                        border_radius="8px",
                        width="100%",
                        _hover={"background_color": "#f1f5f9"},
                        display="flex",
                        align_items="center",
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon("log-out", size=16, color="#ef4444"),
                            rx.text(
                                "Pechar sesión",
                                color="#ef4444",
                                font_weight="500",
                            ),
                            spacing="2",
                            align_items="center",
                        ),
                        background_color="transparent",
                        border="none",
                        padding="12px 16px",
                        border_radius="8px",
                        width="100%",
                        _hover={"background_color": "#fef2f2"},
                        on_click=[
                            State.logout,
                            State.set_profile_modal_open(False)
                        ],
                        display="flex",
                        align_items="center",
                    ),
                    spacing="2",
                    width="100%",
                    align_items="stretch",
                ),
                rx.dialog.close(
                    rx.button(
                        "Pechar",
                        background_color="#f1f5f9",
                        color="#64748b",
                        border="none",
                        padding="8px 24px",
                        margin_top="16px",
                    ),
                ),
                spacing="4",
                align_items="center",
                width="100%",
            ),
            max_width="300px",
            padding="24px",
            background_color="white",
            border_radius="12px",
        ),
        open=State.profile_modal_open,
        on_open_change=State.set_profile_modal_open,
    )