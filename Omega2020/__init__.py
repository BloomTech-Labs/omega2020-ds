"""Entry Point for Omega2020."""

from .app import create_app

APP = create_app()
#APP.run(debug=True)

if __name__ == '__main__':
    app.run()