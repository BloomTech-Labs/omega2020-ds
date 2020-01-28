"""Entry Point for Omega2020."""

from .app import create_app

application = create_app()
application.run(host="0.0.0.0")