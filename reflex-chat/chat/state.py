from typing import Any, TypedDict
import asyncio
import reflex as rx
import httpx
import json
import random


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
    flashcard_modal_open: bool = False
    current_flashcard: dict = {}
    
    # Backend integration
    backend_url: str = "http://127.0.0.1:8000"

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

    @rx.event
    def set_flashcard_modal_open(self, is_open: bool):
        """Open or close the flashcard modal."""
        self.flashcard_modal_open = is_open
        
    @rx.event
    def show_random_flashcard(self):
        """Show a random flashcard from the gl-phrases.json file."""
        import json
        import random
        import os
        
        try:
            # Load the phrases from the JSON file
            # Use a hardcoded list for now since file loading might be tricky in Reflex
            phrases = [
                {"gl": "Bo día", "es": "Buenos días"},
                {"gl": "Boas tardes", "es": "Buenas tardes"},
                {"gl": "Boas noites", "es": "Buenas noches"},
                {"gl": "Ata logo", "es": "Hasta luego"},
                {"gl": "Apertas", "es": "Abrazos"},
                {"gl": "Que aproveite", "es": "Que aproveche"},
                {"gl": "Saúdos", "es": "Saludos"},
                {"gl": "Ter morriña", "es": "Sentir nostalgia"},
                {"gl": "Botarlle unha man", "es": "Echar una mano"},
                {"gl": "De balde", "es": "Gratis"},
                {"gl": "Non é doado", "es": "No es fácil"},
                {"gl": "Ir indo", "es": "Ir tirando"},
                {"gl": "Quedar abraiado", "es": "Quedarse asombrado"},
                {"gl": "Ollo!", "es": "¡Cuidado!"},
                {"gl": "Veña", "es": "Venga / anda"},
                {"gl": "Xa veremos", "es": "Ya veremos"},
                {"gl": "Un chisco", "es": "Un poco"},
                {"gl": "Non hai perda", "es": "No tiene pérdida"},
                {"gl": "Estar farto", "es": "Estar harto"},
                {"gl": "Botar en falta", "es": "Echar de menos"}
            ]
                    
            if phrases:
                # Select a random phrase
                selected_phrase = random.choice(phrases)
                self.current_flashcard = selected_phrase
                self.flashcard_modal_open = True
            else:
                # Fallback if list is empty
                self.current_flashcard = {
                    "gl": "Bo día",
                    "es": "Buenos días"
                }
                self.flashcard_modal_open = True
        except Exception:
            # Fallback in case of any error
            self.current_flashcard = {
                "gl": "Bo día",
                "es": "Buenos días"
            }
            self.flashcard_modal_open = True

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
        """Get the response from the Galician tutor API.

        Args:
            question: The question from the user.
        """

        # Add the question to the list of questions.
        qa = QA(question=question, answer="")
        self._chats[self.current_chat].append(qa)

        # Clear the input and start the processing.
        self.processing = True
        yield

        try:
            # Prepare request to backend
            user_id = self.current_user or "anonymous"
            level_index = self.selected_level
            
            request_data = {
                "user_id": user_id,
                "message": question,
                "level_index": level_index,
                "mode": "conversation"
            }

            # Make API call to backend
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.backend_url}/api/chat/message",
                    json=request_data,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    tutor_response = result.get("tutor_response", "Error: No response from tutor")
                    
                    # Show corrections if any
                    if result.get("has_errors", False):
                        corrections_text = "\n**Correccións:**\n"
                        for correction in result.get("corrections", []):
                            corrections_text += f"• '{correction['error']}' → '{correction['correction']}' ({correction['explanation']})\n"
                        tutor_response = corrections_text + "\n" + tutor_response
                    
                else:
                    tutor_response = "Error: Non se puido conectar co titor. Téntao de novo."
                    
        except Exception as e:
            tutor_response = f"Error de conexión: {str(e)}"

        # Stream character by character to simulate realtime typing.
        for i in range(0, len(tutor_response), 8):
            chunk = tutor_response[i:i + 8]
            self._chats[self.current_chat][-1]["answer"] += chunk
            # Trigger reactivity
            self._chats = self._chats
            await asyncio.sleep(0.02)
            yield

        # Toggle the processing flag.
        self.processing = False
