# main.py
import sys
import os

# Ajustar sys.path para que pueda encontrar el paquete 'views'
# Es importante que la raíz del proyecto esté en sys.path.
# Esto es para cuando ejecutas 'python3 main.py'
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Importar funciones desde los módulos de vista
from views.auth_view import show_auth_menu
from views.main_menu_view import show_main_menu

def main():
    """
    Función principal de la aplicación.
    Maneja el flujo de registro/login y el menú principal.
    """
    if show_auth_menu(): # Intentar autenticar. Si retorna True, el login fue exitoso.
        show_main_menu() # Mostrar el menú principal si el usuario se autenticó.
    else:
        # El usuario eligió salir desde el menú de autenticación
        pass # La función show_auth_menu ya imprime el mensaje de salida.

if __name__ == "__main__":
    main()