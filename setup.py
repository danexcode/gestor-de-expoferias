#!/usr/bin/env python3
"""
Setup script for Gestor de Expoferias.
Handles environment setup and database initialization.
"""
import os
import sys
import subprocess
import mysql.connector
from pathlib import Path

def print_header():
    """Print the setup header."""
    print("=" * 60)
    print("Gestor de Expoferias - Configuración Inicial")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("Error: Se requiere Python 3.8 o superior.")
        sys.exit(1)
    print(f"✓ Python {sys.version.split()[0]} detectado")

def install_dependencies():
    """Install required Python dependencies."""
    print("\nInstalando dependencias de Python...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencias instaladas correctamente")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error al instalar dependencias: {e}")
        sys.exit(1)

def setup_database():
    """Set up the MySQL database."""
    print("\nConfiguración de la base de datos MySQL")
    print("-" * 40)
    
    # Get database credentials
    db_config = {}
    db_config['host'] = input("Servidor MySQL [localhost]: ") or "localhost"
    db_config['user'] = input("Usuario MySQL [root]: ") or "root"
    db_config['password'] = input("Contraseña MySQL: ")
    
    try:
        # Test connection
        conn = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password']
        )
        cursor = conn.cursor()
        
        # Create database if not exists
        cursor.execute("CREATE DATABASE IF NOT EXISTS gestor_expoferias CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print("✓ Base de datos 'gestor_expoferias' creada o ya existente")
        
        # Import schema
        schema_file = Path("db/database.sql")
        if schema_file.exists():
            with open(schema_file, 'r', encoding='utf-8') as f:
                sql_commands = f.read().split(';')
                for command in sql_commands:
                    if command.strip():
                        cursor.execute(command)
            conn.commit()
            print("✓ Esquema de la base de datos importado correctamente")
        else:
            print("✗ Archivo de esquema no encontrado en db/database.sql")
        
        # Close connection
        cursor.close()
        conn.close()
        
        # Update .env file
        with open(".env", "w") as f:
            f.write(f"DB_HOST={db_config['host']}\n")
            f.write(f"DB_USER={db_config['user']}\n")
            f.write(f"DB_PASSWORD={db_config['password']}\n")
            f.write("DB_NAME=gestor_expoferias\n")
        print("✓ Archivo .env actualizado con las credenciales de la base de datos")
        
    except mysql.connector.Error as err:
        print(f"✗ Error de MySQL: {err}")
        sys.exit(1)

def create_asset_directories():
    """Create necessary asset directories."""
    directories = ["assets", "templates", "logs", "exports"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("✓ Directorios de activos creados")

def main():
    """Main setup function."""
    print_header()
    check_python_version()
    install_dependencies()
    setup_database()
    create_asset_directories()
    
    print("\n¡Configuración completada exitosamente!")
    print("Puedes iniciar la aplicación con: python launch.py\n")

if __name__ == "__main__":
    main()
