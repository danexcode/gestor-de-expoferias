#!/usr/bin/env python3
"""
Build script for Gestor de Expoferias application.
"""
import os
import shutil
import sys
import subprocess
from pathlib import Path

def clean_build():
    """Remove previous build and dist directories."""
    build_dirs = ['build', 'dist']
    for d in build_dirs:
        if os.path.exists(d):
            print(f"Removing {d} directory...")
            shutil.rmtree(d)

def create_assets():
    """Create necessary asset directories if they don't exist."""
    assets_dir = Path('assets')
    assets_dir.mkdir(exist_ok=True)
    
    # Create default icon if not exists
    icon_path = assets_dir / 'icon.ico'
    if not icon_path.exists():
        print("Warning: No icon.ico found in assets directory.")
        print("Please add an icon.ico file to the assets directory for the best results.")

def install_dependencies():
    """Install required dependencies."""
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def build():
    """Build the application using PyInstaller."""
    print("Building application with PyInstaller...")
    subprocess.check_call([
        sys.executable,
        "-m",
        "PyInstaller",
        "--clean",
        "--noconfirm",
        "gestor_expoferias.spec"
    ])

def main():
    """Main build function."""
    try:
        print("Starting build process...")
        clean_build()
        create_assets()
        install_dependencies()
        build()
        print("\nBuild completed successfully!")
        print(f"You can find the built application in the 'dist/GestorExpoferias' directory.")
    except Exception as e:
        print(f"Error during build: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
