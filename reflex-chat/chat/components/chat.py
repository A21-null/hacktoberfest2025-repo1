import reflex as rx

from chat.state import QA, State
from reflex.constants.colors import ColorType


def tutor_message_content(text: str, qa_index: int = 0) -> rx.Component:
    """Create a tutor message content component with flashcard creation.

    Args:
        text: The text to display.
        qa_index: Index of the QA pair for identification.

    Returns:
        A component displaying the tutor message with flashcard creation.
    """
    return rx.box(
        rx.markdown(
            text,
            background_color="rgba(59, 130, 246, 0.9)",
            color="white",
            display="inline-block",
            padding="16px 20px",
            border_radius="16px",
            max_width="80%",
            font_size="16px",
            line_height="1.5",
            box_shadow="0 2px 8px rgba(0, 0, 0, 0.1)",
            user_select="text",
        ),
        # Simple button to create flashcard
        rx.button(
            rx.icon("plus", size=12),
            rx.text("Crear flashcard", font_size="xs"),
            background_color="rgba(255, 255, 255, 0.2)",
            border="none",
            padding="4px 8px",
            border_radius="6px",
            color="white",
            font_size="xs",
            margin_top="4px",
            _hover={"background_color": "rgba(255, 255, 255, 0.3)"},
            display="flex",
            align_items="center",
            gap="4px",
            on_click=lambda: State.create_flashcard_from_text("Exemplo"),
        ),
    )


def message_content(text: str, color: ColorType) -> rx.Component:
    """Create a message content component.

    Args:
        text: The text to display.
        color: The color of the message.

    Returns:
        A component displaying the message.
    """
    return rx.markdown(
        text,
        background_color=(
            "rgba(255, 255, 255, 0.95)"
            if color == "mauve"
            else "rgba(59, 130, 246, 0.9)"
        ),
        color="#1e293b" if color == "mauve" else "white",
        display="inline-block",
        padding="16px 20px",
        border_radius="16px",
        max_width="80%",
        font_size="16px",
        line_height="1.5",
        box_shadow="0 2px 8px rgba(0, 0, 0, 0.1)",
    )


def message(qa: QA, index: int = 0) -> rx.Component:
    """A single question/answer message.

    Args:
        qa: The question/answer pair.
        index: Index of the message for identification.

    Returns:
        A component displaying the question/answer pair.
    """
    return rx.box(
        rx.box(
            message_content(qa["question"], "mauve"),
            text_align="right",
            margin_bottom="12px",
        ),
        rx.box(
            # Use special tutor message for answers (from Gemini)
            tutor_message_content(qa["answer"], index),
            text_align="left",
            margin_bottom="20px",
        ),
        width="100%",
        max_width="800px",
        margin_bottom="24px",
    )


def welcome_screen() -> rx.Component:
    """Welcome screen when no chat is selected."""
    return rx.center(
        rx.vstack(
            rx.heading(
                "¡Ola meu!",
                size="8",
                color="white",
                text_align="center",
                margin_bottom="6",
                font_weight="700",
                text_shadow="0 2px 4px rgba(0, 0, 0, 0.3)",
            ),
            rx.text(
                "Benvido a Breogan, o teu titor de galego",
                font_size="24px",
                color="rgba(255, 255, 255, 0.95)",
                text_align="center",
                margin_bottom="8",
                font_weight="500",
                text_shadow="0 1px 2px rgba(0, 0, 0, 0.2)",
            ),
            rx.text(
                "Escribe unha mensaxe para comezar a aprender galego",
                font_size="18px",
                color="rgba(255, 255, 255, 0.8)",
                text_align="center",
                font_weight="400",
                text_shadow="0 1px 2px rgba(0, 0, 0, 0.2)",
            ),
            spacing="6",
            align_items="center",
            max_width="600px",
            padding="40px",
        ),
        height="100%",
        width="100%",
    )


def chat() -> rx.Component:
    """Main chat component."""
    return rx.box(
        rx.cond(
            State.selected_chat.length() > 0,
            rx.vstack(
                rx.foreach(
                    State.selected_chat,
                    lambda qa, index: message(qa, index),
                ),
                spacing="0",
                width="100%",
                max_width="800px",
                margin="0 auto",
                padding="32px",
                align_items="stretch",
            ),
            welcome_screen(),
        ),
        width="100%",
        height="100%",
        overflow_y="auto",
    )


def action_bar() -> rx.Component:
    """Action bar with input and send button."""
    return rx.box(
        rx.form(
            rx.hstack(
                rx.input(
                    placeholder="Escribe a túa pregunta en galego...",
                    id="question",
                    name="question",
                    background_color="rgba(255, 255, 255, 0.95)",
                    border="1px solid rgba(255, 255, 255, 0.2)",
                    border_radius="12px",
                    font_size="16px",     # ← CHANGE THIS TO MAKE TEXT LARGER
                    line_height="1.4",    # ← ADD THIS FOR BETTER READABILITY
                    color="#1e293b",
                    flex="1",
                    _focus={
                        "border_color": "rgba(255, 255, 255, 0.4)",
                        "box_shadow": "0 0 0 3px rgba(255, 255, 255, 0.1)",
                    },
                ),
                rx.button(
                    rx.icon("mic", size=20, color="white"),
                    type="button",
                    background_color="rgba(255, 255, 255, 0.1)",
                    border="1px solid rgba(255, 255, 255, 0.2)",
                    padding="16px",
                    border_radius="50%",
                    width="56px",
                    height="56px",
                    _hover={"background_color": "rgba(255, 255, 255, 0.2)"},
                    on_click=State.set_voice_modal_open(True),
                ),
                rx.button(
                    rx.icon("send", size=20, color="white"),
                    type="submit",
                    background_color="#3b82f6",
                    padding="16px",
                    border_radius="50%",
                    width="56px",
                    height="56px",
                    _hover={"background_color": "#2563eb"},
                    loading=State.processing,
                    disabled=State.processing,
                ),
                spacing="4",
                align_items="center",
                max_width="800px",
                margin="0 auto",
            ),
            reset_on_submit=True,
            on_submit=State.process_question,
        ),
        position="fixed",
        bottom="32px",
        left="280px",
        right="32px",
        padding="0 32px",
        z_index="50",
    )
