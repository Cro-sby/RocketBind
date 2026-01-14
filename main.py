"""
RocketBind - Rocket League Preset Manager
Main entry point for the application.
"""
from ui.main_window import RocketBindApp


def main():
    """Launch the application."""
    app = RocketBindApp()
    app.mainloop()


if __name__ == "__main__":
    main()
