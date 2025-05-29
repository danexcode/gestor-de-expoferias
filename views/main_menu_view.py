# views/main_menu_view.py
import sys
import os

# Asegurar que el directorio del proyecto esté en sys.path para importar 'views'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar funciones de otros módulos de vista
from views.table_management_view import show_table_management_menu
from views.report_view import show_reports_menu
from auth import logout_user, get_logged_in_user # Logout y get_logged_in_user aún de auth.py

# Funciones de utilidad que pueden ser genéricas para todas las vistas CLI
def display_menu(options):
    """
    Muestra un menú numerado en la consola.

    Args:
        options (list): Una lista de cadenas, donde cada cadena es una opción del menú.
    """
    print("\n" + "="*40)
    print("           MENÚ PRINCIPAL           ")
    print("="*40)
    for i, option in enumerate(options):
        print(f"{i + 1}. {option}")
    print("="*40)


def get_menu_choice(num_options):
    """
    Solicita al usuario una elección de menú válida.

    Args:
        num_options (int): El número total de opciones en el menú.

    Returns:
        int: La opción válida elegida por el usuario.
    """
    while True:
        try:
            choice = int(input("Seleccione una opción: "))
            if 1 <= choice <= num_options:
                return choice
            else:
                print("Opción inválida. Por favor, ingrese un número dentro del rango.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número.")


def show_main_menu():
    """
    Muestra el menú principal de la aplicación y maneja la navegación.
    """
    logged_in = True # Ya estamos logueados si llegamos aquí
    while logged_in:
        current_user_data = get_logged_in_user()
        if current_user_data:
            print(f"\nUsuario actual: {current_user_data['nombre_usuario']} ({current_user_data['rol']})")

        main_options = [
            "Administración de Tablas",
            "Reportes",
            "Cerrar Sesión",
            "Salir del Programa"
        ]
        display_menu(main_options)
        main_choice = get_menu_choice(len(main_options))

        if main_choice == 1:
            show_table_management_menu() # Llama a la función de la vista de gestión de tablas
        elif main_choice == 2:
            show_reports_menu() # Llama a la función de la vista de reportes
        elif main_choice == 3:
            logout_user()
            logged_in = False # Cambiar estado para salir del bucle principal y volver al login
        elif main_choice == 4:
            print("Saliendo del programa. ¡Hasta luego!")
            sys.exit()