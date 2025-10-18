import reflex as rx

# Reflex requires app_name to match the python package that exposes the app
# (the directory containing the Reflex app). The project package is `chat`,
# so keep app_name='chat' to avoid import errors. The user-visible product
# name can still be "Breogan" in README and metadata.
config = rx.Config(
    app_name="chat",
    plugins=[rx.plugins.SitemapPlugin()],
)
