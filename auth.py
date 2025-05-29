import sys
import os

# Añadir el directorio padre al sys.path para poder importar 'models'
# Esto es necesario cuando auth.py se ejecuta directamente para las pruebas
# o cuando main.py lo importa desde el mismo nivel
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar funciones desde el modelo de usuarios
from models.user_model import create_user, get_user_by_username, verify_password

# Variable global para almacenar el usuario actualmente logueado
# En una aplicación web, esto sería manejado por sesiones o tokens.
# Para la consola, una variable global es suficiente.
current_user = None

def register_user_cli():
    """
    Función de utilidad para registrar un nuevo usuario desde la línea de comandos.
    """
    print("\n--- Registro de Nuevo Usuario ---")
    while True:
        nombre_usuario = input("Ingrese nombre de usuario (único): ").strip()
        if not nombre_usuario:
            print("El nombre de usuario no puede estar vacío.")
            continue
        existing_user = get_user_by_username(nombre_usuario)
        if existing_user:
            print(f"Error: El nombre de usuario '{nombre_usuario}' ya existe.")
        else:
            break

    while True:
        contrasena = input("Ingrese contraseña: ").strip()
        if not contrasena:
            print("La contraseña no puede estar vacía.")
            continue
        confirm_contrasena = input("Confirme contraseña: ").strip()
        if contrasena != confirm_contrasena:
            print("Las contraseñas no coinciden. Inténtelo de nuevo.")
        else:
            break

    while True:
        rol = input("Ingrese rol (Administrador, Coordinador, Profesor): ").strip()
        if rol not in ['Administrador', 'Coordinador', 'Profesor']:
            print("Rol inválido. Debe ser 'Administrador', 'Coordinador' o 'Profesor'.")
        else:
            break

    nombre_completo = input("Ingrese nombre completo (opcional): ").strip()
    correo_electronico = input("Ingrese correo electrónico (opcional, debe ser único): ").strip()

    if correo_electronico:
        while True:
            existing_user_by_email = get_user_by_username(correo_electronico) # get_user_by_username verifica email también
            if existing_user_by_email and existing_user_by_email['correo_electronico'] == correo_electronico:
                print(f"Error: El correo electrónico '{correo_electronico}' ya está registrado.")
                correo_electronico = input("Ingrese otro correo electrónico o déjelo en blanco: ").strip()
                if not correo_electronico: break # Permitir dejarlo en blanco
            else:
                break


    new_user_id = create_user(nombre_usuario, contrasena, rol, nombre_completo if nombre_completo else None, correo_electronico if correo_electronico else None)

    if new_user_id:
        print(f"Usuario '{nombre_usuario}' registrado exitosamente con ID: {new_user_id}.")
        return True
    else:
        print("Fallo el registro del usuario.")
        return False

def login_user_cli():
    """
    Función de utilidad para iniciar sesión desde la línea de comandos.
    """
    global current_user # Declarar que vamos a modificar la variable global

    print("\n--- Inicio de Sesión ---")
    nombre_usuario = input("Nombre de usuario: ").strip()
    contrasena = input("Contraseña: ").strip()

    user_data = get_user_by_username(nombre_usuario)

    if user_data:
        if verify_password(user_data['contrasena_hash'], contrasena):
            current_user = user_data
            print(f"¡Bienvenido, {current_user['nombre_completo'] if current_user['nombre_completo'] else current_user['nombre_usuario']}!")
            return True
        else:
            print("Contraseña incorrecta.")
    else:
        print("Nombre de usuario no encontrado.")
    return False

def logout_user():
    """
    Cierra la sesión del usuario actual.
    """
    global current_user
    if current_user:
        print(f"Adiós, {current_user['nombre_usuario']}.")
        current_user = None
    else:
        print("No hay ninguna sesión iniciada.")

def get_logged_in_user():
    """
    Retorna los datos del usuario actualmente logueado.
    """
    return current_user

# --- Bloque de Prueba (uso de ejemplo) ---
if __name__ == "__main__":
    print("--- Probando Módulo de Autenticación ---")

    # Prueba de Registro
    print("\n--- Prueba de Registro ---")
    register_user_cli()

    # Prueba de Login
    print("\n--- Prueba de Login ---")
    if login_user_cli():
        print("Usuario logueado:", get_logged_in_user())
        logout_user()
    else:
        print("Fallo el login de prueba.")

    print("\n--- Probando Login con credenciales incorrectas ---")
    if login_user_cli():
        print("ERROR: Login con credenciales incorrectas exitoso.")
    else:
        print("Login con credenciales incorrectas fallido (esperado).")

    print("\n--- Probando si hay usuario logueado después de logout ---")
    if get_logged_in_user():
        print("ERROR: Usuario todavía logueado después de logout.")
    else:
        print("No hay usuario logueado (esperado).")