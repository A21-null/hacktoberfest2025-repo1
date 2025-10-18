from typing import Any, TypedDict
import asyncio
import reflex as rx

# # Checkin Exception("Please set OPENAI_API_KEY environment variable.")


class QA(TypedDict):
    """A question and answer pair."""

    question: str
    answer: str


class State(rx.State):
    """The app state."""

    # A dict from the chat name to the list of questions and answers.
    _chats: dict[str, list[QA]] = {
        "Introducciones": [],
    }

    # The current chat name.
    current_chat = "Introducciones"

    # Whether we are processing the question.
    processing: bool = False

    # Whether the new chat modal is open.
    is_modal_open: bool = False

    # Auth state
    login_modal_open: bool = False
    register_modal_open: bool = False
    current_user: str | None = None
    
    # UI state
    voice_modal_open: bool = False
    profile_modal_open: bool = False
    selected_level: int = 1

    @rx.event
    def create_chat(self, form_data: dict[str, Any]):
        """Create a new chat."""
        # Add the new chat to the list of chats.
        new_chat_name = form_data["new_chat_name"]
        self.current_chat = new_chat_name
        self._chats[new_chat_name] = []
        self.is_modal_open = False

    @rx.event
    def set_is_modal_open(self, is_open: bool):
        """Set the new chat modal open state.

        Args:
            is_open: Whether the modal is open.
        """
        self.is_modal_open = is_open

    @rx.event
    def set_login_modal_open(self, is_open: bool):
        """Open or close the login modal."""
        self.login_modal_open = is_open

    @rx.event
    def set_register_modal_open(self, is_open: bool):
        """Open or close the register modal."""
        self.register_modal_open = is_open

    @rx.event
    def login(self, form_data: dict[str, Any]):
        """Simple login handler (frontend-only).

        Args:
            form_data: dict with 'email' and 'password'
        """
        # Expecting username and password; accept only admin/admin
        username = form_data.get("username")
        password = form_data.get("password")
        if username == "admin" and password == "admin":
            self.current_user = username
        else:
            # invalid credentials; do not set user
            pass
        self.login_modal_open = False

    @rx.event
    def register(self, form_data: dict[str, Any]):
        """Simple register handler (frontend-only).

        Args:
            form_data: dict with 'name','email' and 'password'
        """
        email = form_data.get("email")
        name = form_data.get("name")
        if email:
            # Pretend registration succeeded and set current_user
            self.current_user = name or email
        self.register_modal_open = False

    @rx.event
    def logout(self):
        """Log out the current user."""
        self.current_user = None

    @rx.event
    def set_voice_modal_open(self, is_open: bool):
        """Open or close the voice modal."""
        self.voice_modal_open = is_open

    @rx.event
    def set_profile_modal_open(self, is_open: bool):
        """Open or close the profile modal."""
        self.profile_modal_open = is_open

    @rx.event
    def set_selected_level(self, level: int):
        """Set the selected language level."""
        self.selected_level = level

    @rx.var
    def selected_chat(self) -> list[QA]:
        """Get the list of questions and answers for the current chat.

        Returns:
            The list of questions and answers.
        """
        return (
            self._chats[self.current_chat]
            if self.current_chat in self._chats
            else []
        )

    @rx.event
    def delete_chat(self, chat_name: str):
        """Delete the current chat."""
        if chat_name not in self._chats:
            return
        del self._chats[chat_name]
        if len(self._chats) == 0:
            self._chats = {
                "Introducciones": [],
            }
        if self.current_chat not in self._chats:
            self.current_chat = list(self._chats.keys())[0]

    @rx.event
    def set_chat(self, chat_name: str):
        """Set the name of the current chat.

        Args:
            chat_name: The name of the chat.
        """
        self.current_chat = chat_name

    @rx.event
    def set_new_chat_name(self, new_chat_name: str):
        """Set the name of the new chat.

        Args:
            new_chat_name: The name of the new chat.
        """
        self.new_chat_name = new_chat_name

    @rx.var
    def chat_titles(self) -> list[str]:
        """Get the list of chat titles.

        Returns:
            The list of chat names.
        """
        return list(self._chats.keys())

    @rx.event
    async def process_question(self, form_data: dict[str, Any]):
        # Get the question from the form
        question = form_data["question"]

        # Check if the question is empty
        if not question:
            return

        async for value in self.openai_process_question(question):
            yield value

    @rx.event
    async def openai_process_question(self, question: str):
        """Get the response from the API.

        Args:
            form_data: A dict with the current question.
        """

        # Add the question to the list of questions.
        qa = QA(question=question, answer="")
        self._chats[self.current_chat].append(qa)

        # Clear the input and start the processing.
        self.processing = True
        yield
        # Build a mock Galician tutor response.
    # For frontend-only work, we simulate streaming by yielding
    # after chunks.
        mock_response = (
            "Moi ben! Esto é unha resposta de exemplo en galego. "
            "Vou darte correccións e explicacións breves para axudarche a "
            "aprender.\n\n"
            "1. Saúdos: 'Ola' é equivalente a 'Hola' en español.\n"
            "2. Gramática: 'teño' significa 'tengo'.\n"
            "3. Exercicio: Traduce '¿Cómo estás?' ao galego.\n"
            "Boa sorte e segue practicando!"
        )

    # Stream character by character (or in small chunks) to simulate
    # realtime typing.
        for i in range(0, len(mock_response), 8):
            chunk = mock_response[i:i + 8]
            self._chats[self.current_chat][-1]["answer"] += chunk
            # Trigger reactivity
            self._chats = self._chats
            await asyncio.sleep(0.02)
            yield

        # Toggle the processing flag.
        self.processing = False
