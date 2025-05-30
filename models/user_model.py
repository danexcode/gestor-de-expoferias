import mysql.connector
from mysql.connector import Error
import hashlib # Para hashear contraseñas

# Importar la función de conexión desde nuestro módulo database.py
# Asegúrate de que database.py esté en el mismo nivel o en una ruta accesible
from db.connection import create_connection, close_connection

# --- Funciones CRUD para la tabla 'usuarios' ---

def hash_password(password):
    """
    Hashea una contraseña usando SHA256.
    En una aplicación real, se usaría un algoritmo más robusto como bcrypt o Argon2.
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def verify_password(stored_password_hash, provided_password):
    """
    Verifica si una contraseña proporcionada coincide con un hash almacenado.
    """
    return stored_password_hash == hash_password(provided_password)

def create_user(nombre_usuario, contrasena, rol, nombre_completo=None, correo_electronico=None):
    """
    Inserta un nuevo usuario en la tabla 'usuarios'.

    Args:
        nombre_usuario (str): Nombre de usuario único.
        contrasena (str): Contraseña del usuario (se hasheará antes de almacenar).
        rol (str): Rol del usuario (debe ser 'Administrador', 'Coordinador' o 'Profesor').
        nombre_completo (str, optional): Nombre completo del usuario.
        correo_electronico (str, optional): Correo electrónico único del usuario.

    Returns:
        int or None: El ID del nuevo usuario si la inserción es exitosa, None en caso de error.
    """
    conn = create_connection()
    if conn is None:
        return None

    user_id = None
    try:
        cursor = conn.cursor()
        contrasena_hash = hash_password(contrasena) # Hashear la contraseña

        query = """
        INSERT INTO usuarios (nombre_usuario, contrasena_hash, rol, nombre_completo, correo_electronico)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (nombre_usuario, contrasena_hash, rol, nombre_completo, correo_electronico))
        conn.commit()
        user_id = cursor.lastrowid # Obtener el ID del último registro insertado
        print(f"Usuario '{nombre_usuario}' creado con ID: {user_id}")
    except Error as e:
        print(f"Error al crear usuario: {e}")
        conn.rollback() # Revertir la transacción en caso de error
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        close_connection(conn)
    return user_id

def get_user_by_id(user_id):
    """
    Obtiene un usuario de la tabla 'usuarios' por su ID.

    Args:
        user_id (int): ID del usuario a buscar.

    Returns:
        dict or None: Un diccionario con los datos del usuario si se encuentra, None si no.
    """
    conn = create_connection()
    if conn is None:
        return None

    user_data = None
    try:
        cursor = conn.cursor(dictionary=True) # Retorna resultados como diccionarios
        query = "SELECT id_usuario, nombre_usuario, contrasena_hash, rol, nombre_completo, correo_electronico, activo, fecha_creacion, ultima_sesion FROM usuarios WHERE id_usuario = %s"
        cursor.execute(query, (user_id,))
        user_data = cursor.fetchone()
    except Error as e:
        print(f"Error al obtener usuario por ID: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        close_connection(conn)
    return user_data

# Dentro de models/user_model.py, añade esta función:

def get_all_users():
    """
    Obtiene todos los usuarios de la tabla 'usuarios'.

    Returns:
        list of dict: Una lista de diccionarios con los datos de todos los usuarios.
    """
    conn = create_connection()
    if conn is None:
        return []

    users_data = []
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT id_usuario, nombre_usuario, rol, nombre_completo, correo_electronico, activo, fecha_creacion, ultima_sesion FROM usuarios"
        cursor.execute(query)
        users_data = cursor.fetchall()
    except Error as e:
        print(f"Error al obtener todos los usuarios: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        close_connection(conn)
    return users_data

def get_user_by_username(nombre_usuario):
    """
    Obtiene un usuario de la tabla 'usuarios' por su nombre de usuario.

    Args:
        nombre_usuario (str): Nombre de usuario a buscar.

    Returns:
        dict or None: Un diccionario con los datos del usuario si se encuentra, None si no.
    """
    conn = create_connection()
    if conn is None:
        return None

    user_data = None
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT id_usuario, nombre_usuario, contrasena_hash, rol, nombre_completo, correo_electronico, activo, fecha_creacion, ultima_sesion FROM usuarios WHERE nombre_usuario = %s"
        cursor.execute(query, (nombre_usuario,))
        user_data = cursor.fetchone()
    except Error as e:
        print(f"Error al obtener usuario por nombre de usuario: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        close_connection(conn)
    return user_data

def update_user(user_id, **kwargs):
    """
    Actualiza la información de un usuario existente en la tabla 'usuarios'.

    Args:
        user_id (int): ID del usuario a actualizar.
        **kwargs: Argumentos de palabra clave con los campos a actualizar
                  (ej. nombre_completo='Nuevo Nombre', activo=False).
                  La contraseña se debe pasar como 'contrasena' y se hasheará.

    Returns:
        bool: True si la actualización fue exitosa, False en caso de error.
    """
    conn = create_connection()
    if conn is None:
        return False

    if not kwargs:
        print("No se proporcionaron campos para actualizar.")
        close_connection(conn)
        return False

    updates = []
    values = []
    for key, value in kwargs.items():
        if key == 'contrasena':
            # Hashear la nueva contraseña antes de añadirla a los updates
            updates.append("contrasena_hash = %s")
            values.append(hash_password(value))
        elif key in ['nombre_usuario', 'rol', 'nombre_completo', 'correo_electronico', 'activo', 'ultima_sesion']:
            updates.append(f"{key} = %s")
            values.append(value)
        else:
            print(f"Advertencia: El campo '{key}' no es actualizable o es desconocido.")

    if not updates:
        print("No hay campos válidos para actualizar.")
        close_connection(conn)
        return False

    query = f"UPDATE usuarios SET {', '.join(updates)} WHERE id_usuario = %s"
    values.append(user_id) # Añadir el ID del usuario al final de los valores

    success = False
    try:
        cursor = conn.cursor()
        cursor.execute(query, tuple(values))
        conn.commit()
        success = True
        print(f"Usuario con ID {user_id} actualizado exitosamente.")
    except Error as e:
        print(f"Error al actualizar usuario: {e}")
        conn.rollback()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        close_connection(conn)
    return success

def delete_user(user_id):
    """
    Elimina un usuario de la tabla 'usuarios' por su ID.

    Args:
        user_id (int): ID del usuario a eliminar.

    Returns:
        bool: True si la eliminación fue exitosa, False en caso de error.
    """
    conn = create_connection()
    if conn is None:
        return False

    success = False
    try:
        cursor = conn.cursor()
        query = "DELETE FROM usuarios WHERE id_usuario = %s"
        cursor.execute(query, (user_id,))
        conn.commit()
        success = (cursor.rowcount > 0) # True si se eliminó al menos una fila
        if success:
            print(f"Usuario con ID {user_id} eliminado exitosamente.")
        else:
            print(f"No se encontró usuario con ID {user_id} para eliminar.")
    except Error as e:
        print(f"Error al eliminar usuario: {e}")
        conn.rollback()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        close_connection(conn)
    return success

# --- Bloque de Prueba (uso de ejemplo) ---
if __name__ == "__main__":
    print("--- Probando operaciones CRUD para usuarios ---")

    # 1. Crear un usuario de prueba
    print("\n--- Creando un nuevo usuario (Administrador) ---")
    new_user_id = create_user("admin_test", "admin123", "Administrador", "Admin de Prueba", "admin@example.com")
    if new_user_id:
        print(f"Usuario de prueba creado con ID: {new_user_id}")
    else:
        print("Fallo al crear el usuario de prueba.")

    # 2. Intentar crear el mismo usuario (debería fallar por UNIQUE)
    print("\n--- Intentando crear el mismo usuario (debería fallar) ---")
    create_user("admin_test", "otro_pass", "Coordinador")

    # 3. Obtener el usuario por ID
    if new_user_id:
        print(f"\n--- Obteniendo usuario con ID {new_user_id} ---")
        user = get_user_by_id(new_user_id)
        if user:
            print("Usuario encontrado:", user)
            # Verificar la contraseña (solo para fines de prueba, no en producción de esta forma)
            if verify_password(user['contrasena_hash'], "admin123"):
                print("Verificación de contraseña exitosa.")
            else:
                print("Verificación de contraseña fallida.")
        else:
            print("Usuario no encontrado.")

    # 4. Obtener el usuario por nombre de usuario
    print("\n--- Obteniendo usuario por nombre de usuario 'admin_test' ---")
    user_by_username = get_user_by_username("admin_test")
    if user_by_username:
        print("Usuario encontrado por nombre:", user_by_username)
    else:
        print("Usuario no encontrado por nombre.")


    # 5. Actualizar el usuario
    if new_user_id:
        print(f"\n--- Actualizando usuario con ID {new_user_id} ---")
        update_success = update_user(new_user_id,
                                     nombre_completo="Administrador Actualizado",
                                     correo_electronico="updated_admin@example.com",
                                     rol="Coordinador",
                                     contrasena="new_pass_admin")
        if update_success:
            print("Usuario actualizado exitosamente.")
            # Verificar la actualización
            updated_user = get_user_by_id(new_user_id)
            if updated_user:
                print("Usuario actualizado:", updated_user)
                if verify_password(updated_user['contrasena_hash'], "new_pass_admin"):
                    print("Nueva contraseña verificada exitosamente.")

    # 6. Eliminar el usuario
    if new_user_id:
        print(f"\n--- Eliminando usuario con ID {new_user_id} ---")
        delete_success = delete_user(new_user_id)
        if delete_success:
            print("Usuario eliminado exitosamente. Verificando si existe:")
            deleted_user_check = get_user_by_id(new_user_id)
            if deleted_user_check is None:
                print("El usuario ya no existe en la base de datos.")
        else:
            print("Fallo al eliminar el usuario.")