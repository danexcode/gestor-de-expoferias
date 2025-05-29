# views/table_management_view.py
import sys
import os

# Ajustar sys.path para importar modelos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar modelos (TODAS las funciones CRUD de cada uno)
from models.user_model import *
from models.participant_model import *
from models.subject_model import *
from models.period_model import *
from models.project_model import *

# Importar utilidades de CLI (se asume que estas están en main_menu_view o un archivo común)
# Por ahora, para que este archivo funcione de forma independiente, las duplicamos.
# Idealmente, tendríamos un views/cli_utils.py que las contenga y luego importarlas.
def display_menu(options):
    """Muestra un menú numerado en la consola."""
    print("\n" + "="*40)
    print("           MENÚ PRINCIPAL           ")
    print("="*40)
    for i, option in enumerate(options):
        print(f"{i + 1}. {option}")
    print("="*40)

def get_menu_choice(num_options):
    """Solicita al usuario una elección de menú válida."""
    while True:
        try:
            choice = int(input("Seleccione una opción: "))
            if 1 <= choice <= num_options:
                return choice
            else:
                print("Opción inválida. Por favor, ingrese un número dentro del rango.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número.")

# --- Mueve TODAS las funciones manage_X() aquí ---
# manage_users(), manage_participants(), manage_subjects(), manage_periods(), manage_projects()
# (El contenido completo de estas funciones, tal como las tienes en main.py, iría aquí)

# Por ejemplo, solo el esqueleto para no repetir todo el código:
def manage_users():
    # ... todo el código de manage_users de tu main.py actual ...
    pass

def manage_participants():
    # ... todo el código de manage_participants de tu main.py actual ...
    pass

def manage_subjects():
    # ... todo el código de manage_subjects de tu main.py actual ...
    pass

def manage_periods():
    # ... todo el código de manage_periods de tu main.py actual ...
    pass

def manage_projects():
    # ... todo el código de manage_projects de tu main.py actual ...
    pass


def show_table_management_menu():
    """
    Muestra el menú de administración de tablas y maneja la navegación.
    """
    print("\n--- Administración de Tablas ---")
    table_management_options = [
        "Gestionar Usuarios",
        "Gestionar Participantes",
        "Gestionar Materias",
        "Gestionar Períodos",
        "Gestionar Proyectos",
        "Volver al Menú Principal"
    ]
    while True:
        display_menu(table_management_options)
        table_choice = get_menu_choice(len(table_management_options))

        if table_choice == 1:
            manage_users()
        elif table_choice == 2:
            manage_participants()
        elif table_choice == 3:
            manage_subjects()
        elif table_choice == 4:
            manage_periods()
        elif table_choice == 5:
            manage_projects()
        elif table_choice == 6:
            break