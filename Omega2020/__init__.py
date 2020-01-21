"""Entry Point for Omega2020."""

from .app import create_app

APP = create_app()
APP.run(host="0.0.0.0",debug=False)
