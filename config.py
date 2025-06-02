"""
Configuration settings for Gestor de Expoferias application.
Handles both development and production environments.
"""
import os
import sys
from pathlib import Path

# Determine if running as a PyInstaller bundle
IS_BUNDLED = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')

# Base application paths
if IS_BUNDLED:
    # Running in PyInstaller bundle
    BASE_DIR = Path(sys._MEIPASS)
    DB_DIR = Path(sys.executable).parent / 'db'
    ASSETS_DIR = Path(sys.executable).parent / 'assets'
    TEMPLATES_DIR = Path(sys.executable).parent / 'templates'
else:
    # Running in development
    BASE_DIR = Path(__file__).parent
    DB_DIR = BASE_DIR / 'db'
    ASSETS_DIR = BASE_DIR / 'assets'
    TEMPLATES_DIR = BASE_DIR / 'templates'

# Ensure required directories exist
for directory in [DB_DIR, ASSETS_DIR, TEMPLATES_DIR]:
    if not directory.exists():
        directory.mkdir(parents=True, exist_ok=True)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'admin',
    'database': 'gestor_expoferias',
    'raise_on_warnings': True,
    'auth_plugin': 'mysql_native_password',
}

# Application settings
APP_NAME = 'Gestor de Expoferias'
APP_VERSION = '1.0.0'
DEFAULT_ENCODING = 'utf-8'

# UI Settings
THEME = 'arc'  # Default theme for ttkthemes
FONT_FAMILY = 'Segoe UI'
FONT_SIZE = 10

# Email settings (example - configure in production)
EMAIL_CONFIG = {
    'smtp_server': 'smtp.example.com',
    'smtp_port': 587,
    'smtp_username': 'your_email@example.com',
    'smtp_password': 'your_password',
    'from_email': 'noreply@example.com',
    'use_tls': True
}

def get_database_connection_string():
    """Generate a MySQL connection string."""
    return f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"

def get_asset_path(filename):
    """Get the full path to an asset file."""
    return str(ASSETS_DIR / filename)

def get_template_path(filename):
    """Get the full path to a template file."""
    return str(TEMPLATES_DIR / filename)
