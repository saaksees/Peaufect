import os
import streamlit.web.bootstrap

def main():
    """Main entry point for the application."""
    app_path = os.path.join(os.path.dirname(__file__), "app.py")
    streamlit.web.bootstrap.run(app_path, "")

if __name__ == "__main__":
    main()