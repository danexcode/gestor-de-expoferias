# views/auth_view.py
import sys
import os

# Ajustar sys.path para importar auth (si es necesario cuando este archivo se ejecuta independientemente para pruebas)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar funciones de autenticación del módulo auth
from auth import register_user_cli, login_user_cli, logout_user, get_logged_in_user

# Importar funciones de utilidad de vistas (si display_menu y get_menu_choice están en otro archivo)
# Por ahora, asumimos que main_menu_view.py contendrá estas o las duplicaremos en cada vista que las necesite.
# Para evitar duplicidad, podemos hacer una función display_menu y get_menu_choice aquí o en un cli_utils.py
# Por simplicidad, las mantendré aquí hasta que decidamos un archivo global de utilidades de CLI.
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


def show_auth_menu():
    """
    Muestra el menú de autenticación (Login/Registro) y maneja la elección del usuario.
    Retorna True si el login fue exitoso, False si el usuario elige salir.
    """
    logged_in = False
    while not logged_in:
        print("\n=== Sistema de Gestión de Expoferia ===")
        print("1. Iniciar Sesión")
        print("2. Registrar Nuevo Usuario")
        print("3. Salir")
        choice = get_menu_choice(3)

        if choice == 1:
            logged_in = login_user_cli()
        elif choice == 2:
            register_user_cli()
        elif choice == 3:
            print("Saliendo del sistema. ¡Hasta luego!")
            return False # Indicar que el usuario quiere salir
    return True # Login exitoso