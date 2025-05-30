import mysql.connector
from mysql.connector import Error
from datetime import date # Para trabajar con fechas

from db.connection import create_connection, close_connection

# --- Funciones CRUD para la tabla 'periodos' ---

def create_period(nombre_periodo, fecha_inicio, fecha_fin, activo=True):
    """
    Inserta un nuevo período en la tabla 'periodos'.

    Args:
        nombre_periodo (str): Nombre único del período (ej. '2025-I', 'Verano 2024').
        fecha_inicio (date): Fecha de inicio del período (objeto datetime.date).
        fecha_fin (date): Fecha de fin del período (objeto datetime.date).
        activo (bool, optional): Indica si el período está activo. Por defecto es True.

    Returns:
        int or None: El ID del nuevo período si la inserción es exitosa, None en caso de error.
    """
    conn = create_connection()
    if conn is None:
        return None

    period_id = None
    try:
        cursor = conn.cursor()
        query = """
        INSERT INTO periodos (nombre_periodo, fecha_inicio, fecha_fin, activo)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (nombre_periodo, fecha_inicio, fecha_fin, activo))
        conn.commit()
        period_id = cursor.lastrowid
        print(f"Período '{nombre_periodo}' creado con ID: {period_id}")
    except Error as e:
        print(f"Error al crear período: {e}")
        conn.rollback()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        close_connection(conn)
    return period_id

def get_period_by_id(period_id):
    """
    Obtiene un período de la tabla 'periodos' por su ID.

    Args:
        period_id (int): ID del período a buscar.

    Returns:
        dict or None: Un diccionario con los datos del período si se encuentra, None si no.
    """
    conn = create_connection()
    if conn is None:
        return None

    period_data = None
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM periodos WHERE id_periodo = %s"
        cursor.execute(query, (period_id,))
        period_data = cursor.fetchone()
    except Error as e:
        print(f"Error al obtener período por ID: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        close_connection(conn)
    return period_data

def get_period_by_name(nombre_periodo):
    """
    Obtiene un período de la tabla 'periodos' por su nombre.

    Args:
        nombre_periodo (str): Nombre del período a buscar.

    Returns:
        dict or None: Un diccionario con los datos del período si se encuentra, None si no.
    """
    conn = create_connection()
    if conn is None:
        return None

    period_data = None
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM periodos WHERE nombre_periodo = %s"
        cursor.execute(query, (nombre_periodo,))
        period_data = cursor.fetchone()
    except Error as e:
        print(f"Error al obtener período por nombre: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        close_connection(conn)
    return period_data

def get_all_periods(active_only=False):
    """
    Obtiene todos los períodos de la tabla 'periodos'.

    Args:
        active_only (bool, optional): Si es True, solo retorna períodos activos. Por defecto es False.

    Returns:
        list of dict: Una lista de diccionarios con los datos de todos los períodos.
    """
    conn = create_connection()
    if conn is None:
        return []

    periods_data = []
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM periodos"
        if active_only:
            query += " WHERE activo = TRUE"
        query += " ORDER BY fecha_inicio DESC" # Ordenar por fecha de inicio descendente
        cursor.execute(query)
        periods_data = cursor.fetchall()
    except Error as e:
        print(f"Error al obtener todos los períodos: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        close_connection(conn)
    return periods_data

def update_period(period_id, **kwargs):
    """
    Actualiza la información de un período existente.

    Args:
        period_id (int): ID del período a actualizar.
        **kwargs: Argumentos de palabra clave con los campos a actualizar
                  (ej. nombre_periodo='2025-II', fecha_fin=date(2025, 12, 31)).

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
        if key in ['nombre_periodo', 'fecha_inicio', 'fecha_fin', 'activo']:
            updates.append(f"{key} = %s")
            values.append(value)
        else:
            print(f"Advertencia: El campo '{key}' no es actualizable o es desconocido para períodos.")

    if not updates:
        print("No hay campos válidos para actualizar.")
        close_connection(conn)
        return False

    query = f"UPDATE periodos SET {', '.join(updates)} WHERE id_periodo = %s"
    values.append(period_id)

    success = False
    try:
        cursor = conn.cursor()
        cursor.execute(query, tuple(values))
        conn.commit()
        success = True
        print(f"Período con ID {period_id} actualizado exitosamente.")
    except Error as e:
        print(f"Error al actualizar período: {e}")
        conn.rollback()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        close_connection(conn)
    return success

def delete_period(period_id):
    """
    Elimina un período de la tabla 'periodos' por su ID.
    Ten en cuenta que esto podría afectar la tabla 'proyectos'
    debido a la RESTRICT en la FK.

    Args:
        period_id (int): ID del período a eliminar.

    Returns:
        bool: True si la eliminación fue exitosa, False en caso de error.
    """
    conn = create_connection()
    if conn is None:
        return False

    success = False
    try:
        cursor = conn.cursor()
        query = "DELETE FROM periodos WHERE id_periodo = %s"
        cursor.execute(query, (period_id,))
        conn.commit()
        success = (cursor.rowcount > 0)
        if success:
            print(f"Período con ID {period_id} eliminado exitosamente.")
        else:
            print(f"No se encontró período con ID {period_id} para eliminar.")
    except Error as e:
        print(f"Error al eliminar período: {e}")
        # En caso de RESTRICT, un error como 1451 (Cannot delete or update a parent row)
        # se mostrará si hay proyectos asociados a este período.
        conn.rollback()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        close_connection(conn)
    return success

# --- Bloque de Prueba (uso de ejemplo) ---
if __name__ == "__main__":
    print("--- Probando operaciones CRUD para períodos ---")

    # Importar date para las fechas
    from datetime import date

    # 1. Crear un nuevo período
    print("\n--- Creando un nuevo período (2025-I) ---")
    periodo_id_1 = create_period("2025-I", date(2025, 1, 15), date(2025, 6, 30), activo=True)
    if periodo_id_1:
        print(f"Período de prueba 2025-I creado con ID: {periodo_id_1}")
    else:
        print("Fallo al crear el período 2025-I.")

    print("\n--- Creando otro período (2024-II, inactivo) ---")
    periodo_id_2 = create_period("2024-II", date(2024, 7, 1), date(2024, 12, 15), activo=False)
    if periodo_id_2:
        print(f"Período de prueba 2024-II creado con ID: {periodo_id_2}")
    else:
        print("Fallo al crear el período 2024-II.")

    # 2. Intentar crear período con nombre duplicado (debería fallar por UNIQUE)
    print("\n--- Intentando crear período con nombre duplicado (debería fallar) ---")
    create_period("2025-I", date(2025, 2, 1), date(2025, 7, 31))

    # 3. Obtener período por ID
    if periodo_id_1:
        print(f"\n--- Obteniendo período con ID {periodo_id_1} ---")
        periodo = get_period_by_id(periodo_id_1)
        if periodo:
            print("Período encontrado:", periodo)
        else:
            print("Período no encontrado.")

    # 4. Obtener período por nombre
    print("\n--- Obteniendo período por nombre '2024-II' ---")
    periodo_by_name = get_period_by_name("2024-II")
    if periodo_by_name:
        print("Período encontrado por nombre:", periodo_by_name)
    else:
        print("Período no encontrado por nombre.")

    # 5. Obtener todos los períodos (activos e inactivos)
    print("\n--- Obteniendo todos los períodos ---")
    all_periods = get_all_periods()
    for p in all_periods:
        print(p)

    # 6. Obtener solo períodos activos
    print("\n--- Obteniendo solo períodos activos ---")
    active_periods = get_all_periods(active_only=True)
    for p in active_periods:
        print(p)

    # 7. Actualizar un período
    if periodo_id_1:
        print(f"\n--- Actualizando período con ID {periodo_id_1} ---")
        update_success = update_period(periodo_id_1,
                                       fecha_fin=date(2025, 7, 15),
                                       activo=False) # Ahora lo desactivamos para la prueba
        if update_success:
            print("Período actualizado exitosamente.")
            updated_periodo = get_period_by_id(periodo_id_1)
            print("Período actualizado:", updated_periodo)

    # 8. Eliminar un período (esto puede fallar si ya está referenciado por un proyecto,
    #    debido a ON DELETE RESTRICT en la FK de proyectos)
    if periodo_id_2: # Intentaremos eliminar el periodo 2024-II
        print(f"\n--- Intentando eliminar período con ID {periodo_id_2} ---")
        delete_success = delete_period(periodo_id_2)
        if delete_success:
            print("Período eliminado exitosamente. Verificando si existe:")
            deleted_period_check = get_period_by_id(periodo_id_2)
            if deleted_period_check is None:
                print("El período ya no existe en la base de datos.")
        else:
            print("Fallo al eliminar el período (posiblemente por restricciones de clave foránea).")