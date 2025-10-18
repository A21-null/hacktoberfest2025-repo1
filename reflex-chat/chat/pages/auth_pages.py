import reflex as rx
from chat.state import State


def login_page() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Breogan", size="6", color="#2563eb"),
            rx.heading("Iniciar sesión", size="4", color="#64748b"),
            rx.cond(
                State.login_error,
                rx.text(
                    State.login_error,
                    color="#ef4444",
                    font_size="sm",
                    text_align="center",
                    padding="8px",
                    background_color="#fef2f2",
                    border="1px solid #fecaca",
                    border_radius="6px",
                    width="100%",
                ),
                rx.fragment(),
            ),
            rx.form(
                rx.vstack(
                    rx.input(
                        placeholder="Usuario",
                        name="username",
                        width="85%",
                        background_color="#f8fafc",
                        border_color="#cbd5e1",
                        _focus={"border_color": "#2563eb"},
                        color="#000000"
                    ),
                    rx.input(
                        placeholder="Contraseña",
                        name="password",
                        width="85%",
                        type="password",
                        background_color="#f8fafc",
                        border_color="#cbd5e1",
                        _focus={"border_color": "#2563eb"},
                        color="#000000"
                    ),
                    rx.button(
                        "Entrar",
                        type="submit",
                        background_color="#2563eb",
                        color="white",
                        _hover={"background_color": "#1d4ed8"},
                        width="100%",
                    ),
                    spacing="4",
                ),
                id="login-form",
                on_submit=State.login,
                reset_on_submit=True,
            ),
            rx.link(
                "¿No tienes cuenta? Regístrate",
                href="/register",
                color="#2563eb",
            ),
            width="100%",
            max_width="30em",
            padding="32px",
            background_color="white",
            border_radius="12px",
            box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1)",
        ),
        background="linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%)",
        height="100vh",
    )


def register_page() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Breogan", size="6", color="#2563eb"),
            rx.heading("Crear cuenta", size="4", color="#64748b"),
            rx.form(
                rx.vstack(
                    rx.input(
                        placeholder="Nombre",
                        name="name",
                        background_color="#f8fafc",
                        border_color="#cbd5e1",
                        _focus={"border_color": "#2563eb"},
                    ),
                    rx.input(
                        placeholder="Usuario",
                        name="username",
                        background_color="#f8fafc",
                        border_color="#cbd5e1",
                        _focus={"border_color": "#2563eb"},
                    ),
                    rx.input(
                        placeholder="Contraseña",
                        name="password",
                        type="password",
                        background_color="#f8fafc",
                        border_color="#cbd5e1",
                        _focus={"border_color": "#2563eb"},
                    ),
                    rx.button(
                        "Crear cuenta",
                        type="submit",
                        background_color="#2563eb",
                        color="white",
                        _hover={"background_color": "#1d4ed8"},
                        width="100%",
                    ),
                    spacing="4",
                ),
                id="register-form",
                on_submit=State.register,
            ),
            rx.link(
                "¿Ya tienes cuenta? Inicia sesión",
                href="/login",
                color="#2563eb",
            ),
            width="100%",
            max_width="30em",
            padding="32px",
            background_color="white",
            border_radius="12px",
            box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1)",
        ),
        background="linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%)",
        height="100vh",
    )
