import mysql.connector
from mysql.connector import Error

from database import create_connection, close_connection

# --- Funciones CRUD para la tabla 'participantes' ---

def create_participant(tipo_participante, nombre, apellido, cedula, correo_electronico=None, telefono=None, carrera=None):
    """
    Inserta un nuevo participante (Estudiante o Docente) en la tabla 'participantes'.

    Args:
        tipo_participante (str): Tipo de participante ('Estudiante' o 'Docente').
        nombre (str): Nombre del participante.
        apellido (str): Apellido del participante.
        cedula (str): Cédula de identidad única del participante.
        correo_electronico (str, optional): Correo electrónico único del participante.
        telefono (str, optional): Número de teléfono del participante.
        carrera (str, optional): Carrera del estudiante (solo para 'Estudiante').

    Returns:
        int or None: El ID del nuevo participante si la inserción es exitosa, None en caso de error.
    """
    conn = create_connection()
    if conn is None:
        return None

    participant_id = None
    try:
        cursor = conn.cursor()
        query = """
        INSERT INTO participantes (tipo_participante, nombre, apellido, cedula, correo_electronico, telefono, carrera)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (tipo_participante, nombre, apellido, cedula, correo_electronico, telefono, carrera))
        conn.commit()
        participant_id = cursor.lastrowid
        print(f"Participante '{nombre} {apellido}' ({tipo_participante}) creado con ID: {participant_id}")
    except Error as e:
        print(f"Error al crear participante: {e}")
        conn.rollback()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        close_connection(conn)
    return participant_id

def get_participant_by_id(participant_id):
    """
    Obtiene un participante de la tabla 'participantes' por su ID.

    Args:
        participant_id (int): ID del participante a buscar.

    Returns:
        dict or None: Un diccionario con los datos del participante si se encuentra, None si no.
    """
    conn = create_connection()
    if conn is None:
        return None

    participant_data = None
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM participantes WHERE id_participante = %s"
        cursor.execute(query, (participant_id,))
        participant_data = cursor.fetchone()
    except Error as e:
        print(f"Error al obtener participante por ID: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        close_connection(conn)
    return participant_data

def get_participant_by_cedula(cedula):
    """
    Obtiene un participante de la tabla 'participantes' por su cédula.

    Args:
        cedula (str): Cédula del participante a buscar.

    Returns:
        dict or None: Un diccionario con los datos del participante si se encuentra, None si no.
    """
    conn = create_connection()
    if conn is None:
        return None

    participant_data = None
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM participantes WHERE cedula = %s"
        cursor.execute(query, (cedula,))
        participant_data = cursor.fetchone()
    except Error as e:
        print(f"Error al obtener participante por cédula: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        close_connection(conn)
    return participant_data

def get_all_participants(tipo_participante=None):
    """
    Obtiene todos los participantes o filtra por tipo (Estudiante/Docente).

    Args:
        tipo_participante (str, optional): 'Estudiante' o 'Docente' para filtrar.

    Returns:
        list of dict: Una lista de diccionarios con los datos de los participantes.
    """
    conn = create_connection()
    if conn is None:
        return []

    participants_data = []
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM participantes"
        if tipo_participante:
            query += " WHERE tipo_participante = %s"
            cursor.execute(query, (tipo_participante,))
        else:
            cursor.execute(query)
        participants_data = cursor.fetchall()
    except Error as e:
        print(f"Error al obtener participantes: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        close_connection(conn)
    return participants_data


def update_participant(participant_id, **kwargs):
    """
    Actualiza la información de un participante existente.

    Args:
        participant_id (int): ID del participante a actualizar.
        **kwargs: Argumentos de palabra clave con los campos a actualizar
                  (ej. telefono='555-1234', carrera='Nueva Carrera').

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
        if key in ['tipo_participante', 'nombre', 'apellido', 'cedula', 'correo_electronico', 'telefono', 'carrera']:
            updates.append(f"{key} = %s")
            values.append(value)
        else:
            print(f"Advertencia: El campo '{key}' no es actualizable o es desconocido para participantes.")

    if not updates:
        print("No hay campos válidos para actualizar.")
        close_connection(conn)
        return False

    query = f"UPDATE participantes SET {', '.join(updates)} WHERE id_participante = %s"
    values.append(participant_id)

    success = False
    try:
        cursor = conn.cursor()
        cursor.execute(query, tuple(values))
        conn.commit()
        success = True
        print(f"Participante con ID {participant_id} actualizado exitosamente.")
    except Error as e:
        print(f"Error al actualizar participante: {e}")
        conn.rollback()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        close_connection(conn)
    return success

def delete_participant(participant_id):
    """
    Elimina un participante de la tabla 'participantes' por su ID.
    Ten en cuenta que esto podría afectar la tabla proyectos_participantes
    debido a la CASCADE en la FK.

    Args:
        participant_id (int): ID del participante a eliminar.

    Returns:
        bool: True si la eliminación fue exitosa, False en caso de error.
    """
    conn = create_connection()
    if conn is None:
        return False

    success = False
    try:
        cursor = conn.cursor()
        query = "DELETE FROM participantes WHERE id_participante = %s"
        cursor.execute(query, (participant_id,))
        conn.commit()
        success = (cursor.rowcount > 0)
        if success:
            print(f"Participante con ID {participant_id} eliminado exitosamente.")
        else:
            print(f"No se encontró participante con ID {participant_id} para eliminar.")
    except Error as e:
        print(f"Error al eliminar participante: {e}")
        conn.rollback()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        close_connection(conn)
    return success

# --- Bloque de Prueba (uso de ejemplo) ---
if __name__ == "__main__":
    print("--- Probando operaciones CRUD para participantes ---")

    # 1. Crear un docente de prueba
    print("\n--- Creando un nuevo docente ---")
    docente_id = create_participant("Docente", "Maria", "Perez", "12345678", "maria.perez@example.com", "0414-1234567")
    if docente_id:
        print(f"Docente de prueba creado con ID: {docente_id}")
    else:
        print("Fallo al crear el docente de prueba.")

    # 2. Crear un estudiante de prueba
    print("\n--- Creando un nuevo estudiante ---")
    estudiante_id = create_participant("Estudiante", "Juan", "Gonzalez", "87654321", "juan.gonzalez@example.com", "0424-9876543", "Ingeniería de Software")
    if estudiante_id:
        print(f"Estudiante de prueba creado con ID: {estudiante_id}")
    else:
        print("Fallo al crear el estudiante de prueba.")

    # 3. Intentar crear participante con cédula duplicada (debería fallar por UNIQUE)
    print("\n--- Intentando crear un participante con cédula duplicada (debería fallar) ---")
    create_participant("Estudiante", "Pedro", "Gomez", "87654321", "pedro.gomez@example.com", "0412-1112233", "Ingeniería Civil")


    # 4. Obtener participante por ID (docente)
    if docente_id:
        print(f"\n--- Obteniendo participante con ID {docente_id} (Docente) ---")
        docente = get_participant_by_id(docente_id)
        if docente:
            print("Docente encontrado:", docente)
        else:
            print("Docente no encontrado.")

    # 5. Obtener participante por cédula (estudiante)
    if estudiante_id:
        print(f"\n--- Obteniendo participante por cédula '87654321' (Estudiante) ---")
        estudiante = get_participant_by_cedula("87654321")
        if estudiante:
            print("Estudiante encontrado:", estudiante)
        else:
            print("Estudiante no encontrado.")

    # 6. Obtener todos los participantes
    print("\n--- Obteniendo todos los participantes ---")
    all_participants = get_all_participants()
    for p in all_participants:
        print(p)

    # 7. Obtener solo estudiantes
    print("\n--- Obteniendo solo estudiantes ---")
    only_students = get_all_participants(tipo_participante='Estudiante')
    for s in only_students:
        print(s)

    # 8. Actualizar un participante (estudiante)
    if estudiante_id:
        print(f"\n--- Actualizando estudiante con ID {estudiante_id} ---")
        update_success = update_participant(estudiante_id,
                                            telefono="0426-5554433",
                                            carrera="Ingeniería de Sistemas")
        if update_success:
            print("Estudiante actualizado exitosamente.")
            updated_estudiante = get_participant_by_id(estudiante_id)
            print("Estudiante actualizado:", updated_estudiante)

    # 9. Eliminar un participante (docente)
    if docente_id:
        print(f"\n--- Eliminando docente con ID {docente_id} ---")
        delete_success = delete_participant(docente_id)
        if delete_success:
            print("Docente eliminado exitosamente. Verificando si existe:")
            deleted_docente_check = get_participant_by_id(docente_id)
            if deleted_docente_check is None:
                print("El docente ya no existe en la base de datos.")
        else:
            print("Fallo al eliminar el docente.")