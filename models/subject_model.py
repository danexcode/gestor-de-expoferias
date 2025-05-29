import mysql.connector
from mysql.connector import Error

from database import create_connection, close_connection

# --- Funciones CRUD para la tabla 'materias' ---

def create_subject(codigo_materia, nombre_materia, creditos=None):
    """
    Inserta una nueva materia en la tabla 'materias'.

    Args:
        codigo_materia (str): Código alfanumérico único de la materia.
        nombre_materia (str): Nombre completo único de la materia.
        creditos (int, optional): Número de unidades de crédito de la materia.

    Returns:
        int or None: El ID de la nueva materia si la inserción es exitosa, None en caso de error.
    """
    conn = create_connection()
    if conn is None:
        return None

    subject_id = None
    try:
        cursor = conn.cursor()
        query = """
        INSERT INTO materias (codigo_materia, nombre_materia, creditos)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (codigo_materia, nombre_materia, creditos))
        conn.commit()
        subject_id = cursor.lastrowid
        print(f"Materia '{nombre_materia}' ({codigo_materia}) creada con ID: {subject_id}")
    except Error as e:
        print(f"Error al crear materia: {e}")
        conn.rollback()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        close_connection(conn)
    return subject_id

def get_subject_by_id(subject_id):
    """
    Obtiene una materia de la tabla 'materias' por su ID.

    Args:
        subject_id (int): ID de la materia a buscar.

    Returns:
        dict or None: Un diccionario con los datos de la materia si se encuentra, None si no.
    """
    conn = create_connection()
    if conn is None:
        return None

    subject_data = None
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM materias WHERE id_materia = %s"
        cursor.execute(query, (subject_id,))
        subject_data = cursor.fetchone()
    except Error as e:
        print(f"Error al obtener materia por ID: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        close_connection(conn)
    return subject_data

def get_subject_by_code(codigo_materia):
    """
    Obtiene una materia de la tabla 'materias' por su código.

    Args:
        codigo_materia (str): Código de la materia a buscar.

    Returns:
        dict or None: Un diccionario con los datos de la materia si se encuentra, None si no.
    """
    conn = create_connection()
    if conn is None:
        return None

    subject_data = None
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM materias WHERE codigo_materia = %s"
        cursor.execute(query, (codigo_materia,))
        subject_data = cursor.fetchone()
    except Error as e:
        print(f"Error al obtener materia por código: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        close_connection(conn)
    return subject_data

def get_all_subjects():
    """
    Obtiene todas las materias de la tabla 'materias'.

    Returns:
        list of dict: Una lista de diccionarios con los datos de todas las materias.
    """
    conn = create_connection()
    if conn is None:
        return []

    subjects_data = []
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM materias"
        cursor.execute(query)
        subjects_data = cursor.fetchall()
    except Error as e:
        print(f"Error al obtener todas las materias: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        close_connection(conn)
    return subjects_data

def update_subject(subject_id, **kwargs):
    """
    Actualiza la información de una materia existente.

    Args:
        subject_id (int): ID de la materia a actualizar.
        **kwargs: Argumentos de palabra clave con los campos a actualizar
                  (ej. nombre_materia='Nueva Materia', creditos=4).

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
        if key in ['codigo_materia', 'nombre_materia', 'creditos']:
            updates.append(f"{key} = %s")
            values.append(value)
        else:
            print(f"Advertencia: El campo '{key}' no es actualizable o es desconocido para materias.")

    if not updates:
        print("No hay campos válidos para actualizar.")
        close_connection(conn)
        return False

    query = f"UPDATE materias SET {', '.join(updates)} WHERE id_materia = %s"
    values.append(subject_id)

    success = False
    try:
        cursor = conn.cursor()
        cursor.execute(query, tuple(values))
        conn.commit()
        success = True
        print(f"Materia con ID {subject_id} actualizada exitosamente.")
    except Error as e:
        print(f"Error al actualizar materia: {e}")
        conn.rollback()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        close_connection(conn)
    return success

def delete_subject(subject_id):
    """
    Elimina una materia de la tabla 'materias' por su ID.
    Ten en cuenta que esto podría afectar la tabla 'proyectos'
    debido a la RESTRICT en la FK.

    Args:
        subject_id (int): ID de la materia a eliminar.

    Returns:
        bool: True si la eliminación fue exitosa, False en caso de error.
    """
    conn = create_connection()
    if conn is None:
        return False

    success = False
    try:
        cursor = conn.cursor()
        query = "DELETE FROM materias WHERE id_materia = %s"
        cursor.execute(query, (subject_id,))
        conn.commit()
        success = (cursor.rowcount > 0)
        if success:
            print(f"Materia con ID {subject_id} eliminada exitosamente.")
        else:
            print(f"No se encontró materia con ID {subject_id} para eliminar.")
    except Error as e:
        print(f"Error al eliminar materia: {e}")
        # En caso de RESTRICT, un error como 1451 (Cannot delete or update a parent row)
        # se mostrará si hay proyectos asociados a esta materia.
        conn.rollback()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        close_connection(conn)
    return success

# --- Bloque de Prueba (uso de ejemplo) ---
if __name__ == "__main__":
    print("--- Probando operaciones CRUD para materias ---")

    # 1. Crear una nueva materia
    print("\n--- Creando una nueva materia ---")
    materia_id = create_subject("ING401", "Ingeniería de Software I", 4)
    if materia_id:
        print(f"Materia de prueba creada con ID: {materia_id}")
    else:
        print("Fallo al crear la materia de prueba.")

    # 2. Intentar crear materia con código duplicado (debería fallar por UNIQUE)
    print("\n--- Intentando crear materia con código duplicado (debería fallar) ---")
    create_subject("ING401", "Otro Nombre")

    # 3. Obtener materia por ID
    if materia_id:
        print(f"\n--- Obteniendo materia con ID {materia_id} ---")
        materia = get_subject_by_id(materia_id)
        if materia:
            print("Materia encontrada:", materia)
        else:
            print("Materia no encontrada.")

    # 4. Obtener materia por código
    print("\n--- Obteniendo materia por código 'ING401' ---")
    materia_by_code = get_subject_by_code("ING401")
    if materia_by_code:
        print("Materia encontrada por código:", materia_by_code)
    else:
        print("Materia no encontrada por código.")

    # 5. Obtener todas las materias
    print("\n--- Obteniendo todas las materias ---")
    all_subjects = get_all_subjects()
    for s in all_subjects:
        print(s)

    # 6. Actualizar una materia
    if materia_id:
        print(f"\n--- Actualizando materia con ID {materia_id} ---")
        update_success = update_subject(materia_id,
                                        nombre_materia="Ingeniería de Software Avanzada",
                                        creditos=5)
        if update_success:
            print("Materia actualizada exitosamente.")
            updated_materia = get_subject_by_id(materia_id)
            print("Materia actualizada:", updated_materia)

    # 7. Eliminar la materia (esto puede fallar si ya está referenciada por un proyecto,
    #    debido a ON DELETE RESTRICT en la FK de proyectos)
    if materia_id:
        print(f"\n--- Intentando eliminar materia con ID {materia_id} ---")
        delete_success = delete_subject(materia_id)
        if delete_success:
            print("Materia eliminada exitosamente. Verificando si existe:")
            deleted_materia_check = get_subject_by_id(materia_id)
            if deleted_materia_check is None:
                print("La materia ya no existe en la base de datos.")
        else:
            print("Fallo al eliminar la materia (posiblemente por restricciones de clave foránea).")