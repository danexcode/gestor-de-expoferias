#!/usr/bin/env python3
"""
Launcher script for Gestor de Expoferias application.
Handles both development and production environments.
"""
import os
import sys
import subprocess
from pathlib import Path

def ensure_dependencies():
    """Check and install required dependencies if needed."""
    try:
        import mysql.connector
        import customtkinter
        import ttkthemes
        import reportlab
    except ImportError:
        print("Required dependencies not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def setup_environment():
    """Set up the development environment."""
    # Create necessary directories
    Path("db").mkdir(exist_ok=True)
    Path("assets").mkdir(exist_ok=True)
    Path("templates").mkdir(exist_ok=True)
    
    # Create a default .env file if it doesn't exist
    if not Path(".env").exists():
        with open(".env", "w") as f:
            f.write("# Application Environment Variables\n")
            f.write("PYTHONUNBUFFERED=1\n")
            f.write("PYTHONIOENCODING=utf-8\n")

def main():
    """Main entry point for the application."""
    # Check if running in development or production
    is_production = getattr(sys, 'frozen', False)
    
    if not is_production:
        # Development mode
        print("Running in development mode...")
        ensure_dependencies()
        setup_environment()
        
        # Set environment variables for development
        os.environ["PYTHONPATH"] = os.path.abspath(".")
        
        # Import and run the main application
        from gui.main_app import MainApp
        app = MainApp()
        app.mainloop()
    else:
        # Production mode (PyInstaller bundle)
        try:
            # Set up paths for production
            base_path = sys._MEIPASS
            os.environ["PYTHONPATH"] = base_path
            
            # Import and run the main application
            from gui.main_app import MainApp
            app = MainApp()
            app.mainloop()
        except Exception as e:
            print(f"Error in production mode: {e}", file=sys.stderr)
            input("Press Enter to exit...")
            sys.exit(1)

if __name__ == "__main__":
    main()
