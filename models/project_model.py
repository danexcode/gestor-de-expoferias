import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Importar las funciones de conexión
from db.connection import create_connection, close_connection
# También importaremos los modelos para verificar IDs si es necesario en las pruebas
# Estos imports no son estrictamente necesarios para el modelo en sí, solo para el bloque __main__ de prueba.
# from models.period_model import get_period_by_id
# from models.subject_model import get_subject_by_id
# from models.participant_model import get_participant_by_id

# --- Funciones CRUD para la tabla 'proyectos' y 'proyectos_participantes' ---

def create_project(id_periodo, id_materia, nombre_proyecto, descripcion, participantes_ids):
    """
    Inserta un nuevo proyecto en la tabla 'proyectos' y asocia participantes.

    Args:
        id_periodo (int): ID del período al que pertenece el proyecto.
        id_materia (int): ID de la materia a la que está asociado el proyecto.
        nombre_proyecto (str): Nombre del proyecto.
        descripcion (str): Descripción detallada del proyecto.
        participantes_ids (list): Lista de IDs de los participantes a asociar al proyecto.

    Returns:
        int or None: El ID del nuevo proyecto si la inserción es exitosa, None en caso de error.
    """
    conn = create_connection()
    if conn is None:
        return None

    project_id = None
    try:
        cursor = conn.cursor()

        # 1. Insertar el proyecto principal
        project_query = """
        INSERT INTO proyectos (id_periodo, id_materia, nombre_proyecto, descripcion, fecha_registro)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(project_query, (id_periodo, id_materia, nombre_proyecto, descripcion, datetime.now()))
        project_id = cursor.lastrowid

        # 2. Asociar participantes al proyecto
        if project_id and participantes_ids:
            participant_project_query = """
            INSERT IGNORE INTO proyectos_participantes (id_proyecto, id_participante)
            VALUES (%s, %s)
            """
            # Usamos executemany para mayor eficiencia
            values = [(project_id, p_id) for p_id in participantes_ids]
            cursor.executemany(participant_project_query, values)
            
        conn.commit()
        print(f"Proyecto '{nombre_proyecto}' creado con ID: {project_id}")

    except Error as e:
        print(f"Error al crear proyecto o asociar participantes: {e}")
        conn.rollback() # Revertir toda la transacción
        project_id = None # Asegurarse de retornar None si hubo error
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        close_connection(conn)
    return project_id

def get_project_by_id(project_id):
    """
    Obtiene un proyecto y sus participantes asociados.

    Args:
        project_id (int): ID del proyecto a buscar.

    Returns:
        dict or None: Un diccionario con los datos del proyecto y una lista de participantes,
                      o None si el proyecto no se encuentra.
    """
    conn = create_connection()
    if conn is None:
        return None

    project_data = None
    try:
        cursor = conn.cursor(dictionary=True)

        # 1. Obtener datos del proyecto, INCLUYENDO id_periodo e id_materia
        project_query = """
        SELECT p.id_proyecto, p.nombre_proyecto, p.descripcion, p.fecha_registro,
               p.id_periodo, pe.nombre_periodo, pe.fecha_inicio AS periodo_inicio, pe.fecha_fin AS periodo_fin,
               p.id_materia, m.nombre_materia, m.codigo_materia
        FROM proyectos p
        JOIN periodos pe ON p.id_periodo = pe.id_periodo
        JOIN materias m ON p.id_materia = m.id_materia
        WHERE p.id_proyecto = %s
        """
        cursor.execute(project_query, (project_id,))
        project_data = cursor.fetchone()

        if project_data:
            # 2. Obtener los participantes asociados a este proyecto
            participants_query = """
            SELECT part.id_participante, part.tipo_participante, part.nombre, part.apellido, part.cedula, part.correo_electronico, part.telefono
            FROM participantes part
            JOIN proyectos_participantes pp ON part.id_participante = pp.id_participante
            WHERE pp.id_proyecto = %s
            """
            cursor.execute(participants_query, (project_id,))
            project_data['participantes'] = cursor.fetchall()

    except Error as e:
        print(f"Error al obtener proyecto por ID: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        close_connection(conn)
    return project_data

def get_all_projects():
    """
    Obtiene todos los proyectos con sus detalles básicos (sin participantes completos).
    Para obtener detalles completos de participantes por proyecto, usar get_project_by_id.

    Returns:
        list of dict: Una lista de diccionarios con los datos de todos los proyectos.
    """
    conn = create_connection()
    if conn is None:
        return []

    projects_data = []
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT p.id_proyecto, p.nombre_proyecto, p.descripcion, p.fecha_registro,
               p.id_periodo, pe.nombre_periodo,
               p.id_materia, m.nombre_materia
        FROM proyectos p
        JOIN periodos pe ON p.id_periodo = pe.id_periodo
        JOIN materias m ON p.id_materia = m.id_materia
        ORDER BY p.fecha_registro DESC
        """
        cursor.execute(query)
        projects_data = cursor.fetchall()
    except Error as e:
        print(f"Error al obtener todos los proyectos: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        close_connection(conn)
    return projects_data

def add_participants_to_project(project_id, new_participant_ids):
    """
    Añade nuevos participantes a un proyecto existente.

    Args:
        project_id (int): ID del proyecto.
        new_participant_ids (list): Lista de IDs de participantes a añadir.

    Returns:
        bool: True si la operación es exitosa, False en caso de error.
    """
    conn = create_connection()
    if conn is None:
        return False

    if not new_participant_ids:
        print("No se proporcionaron participantes para añadir.")
        close_connection(conn)
        return False

    success = False
    try:
        cursor = conn.cursor()
        query = "INSERT IGNORE INTO proyectos_participantes (id_proyecto, id_participante) VALUES (%s, %s)"
        values = [(project_id, p_id) for p_id in new_participant_ids]
        cursor.executemany(query, values)
        conn.commit()
        success = True # Consideramos éxito si la operación se completó sin errores de DB
    except Error as e:
        print(f"Error general al añadir participantes al proyecto: {e}")
        conn.rollback()
        success = False
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        close_connection(conn)
    return success

def remove_participants_from_project(project_id, participant_ids_to_remove):
    """
    Elimina participantes de un proyecto existente.

    Args:
        project_id (int): ID del proyecto.
        participant_ids_to_remove (list): Lista de IDs de participantes a remover.

    Returns:
        bool: True si la operación es exitosa, False en caso de error.
    """
    conn = create_connection()
    if conn is None:
        return False

    if not participant_ids_to_remove:
        print("No se proporcionaron participantes para remover.")
        close_connection(conn)
        return False

    success = False
    try:
        cursor = conn.cursor()
        # Construir la parte IN del WHERE para múltiples IDs
        placeholders = ', '.join(['%s'] * len(participant_ids_to_remove))
        query = f"DELETE FROM proyectos_participantes WHERE id_proyecto = %s AND id_participante IN ({placeholders})"
        cursor.execute(query, (project_id, *participant_ids_to_remove))
        conn.commit()
        success = True # Consideramos éxito si el proceso se completa
    except Error as e:
        print(f"Error al remover participantes del proyecto: {e}")
        conn.rollback()
        success = False
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        close_connection(conn)
    return success

def update_project(project_id, **kwargs):
    """
    Actualiza la información de un proyecto existente.
    No se usa para actualizar participantes; usar add_participants_to_project
    y remove_participants_from_project para eso.

    Args:
        project_id (int): ID del proyecto a actualizar.
        **kwargs: Argumentos de palabra clave con los campos a actualizar
                  (ej. nombre_proyecto='Nuevo Nombre', descripcion='Nueva descripción').

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
        if key in ['id_periodo', 'id_materia', 'nombre_proyecto', 'descripcion']:
            updates.append(f"{key} = %s")
            values.append(value)
        else:
            print(f"Advertencia: El campo '{key}' no es actualizable o es desconocido para proyectos.")

    if not updates:
        print("No hay campos válidos para actualizar.")
        close_connection(conn)
        return False

    query = f"UPDATE proyectos SET {', '.join(updates)} WHERE id_proyecto = %s"
    values.append(project_id)

    success = False
    try:
        cursor = conn.cursor()
        cursor.execute(query, tuple(values))
        conn.commit()
        success = (cursor.rowcount > 0) # True si se afectó al menos una fila
        if success:
            print(f"Proyecto con ID {project_id} actualizado exitosamente.")
        else:
            print(f"No se encontró proyecto con ID {project_id} o no hubo cambios para actualizar.")
    except Error as e:
        print(f"Error al actualizar proyecto: {e}")
        conn.rollback()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        close_connection(conn)
    return success

def delete_project(project_id):
    """
    Elimina un proyecto de la tabla 'proyectos' por su ID.
    Debido a ON DELETE CASCADE en proyectos_participantes,
    todas las asociaciones de participantes se eliminarán automáticamente.

    Args:
        project_id (int): ID del proyecto a eliminar.

    Returns:
        bool: True si la eliminación fue exitosa, False en caso de error.
    """
    conn = create_connection()
    if conn is None:
        return False

    success = False
    try:
        cursor = conn.cursor()
        # La FK en proyectos_participantes está en CASCADE, por lo que MySQL
        # se encargará de eliminar las entradas de esa tabla automáticamente.
        query = "DELETE FROM proyectos WHERE id_proyecto = %s"
        cursor.execute(query, (project_id,))
        conn.commit()
        success = (cursor.rowcount > 0)
        if success:
            print(f"Proyecto con ID {project_id} eliminado exitosamente.")
        else:
            print(f"No se encontró proyecto con ID {project_id} para eliminar.")
    except Error as e:
        print(f"Error al eliminar proyecto: {e}")
        conn.rollback()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        close_connection(conn)
    return success

# --- Bloque de Prueba (uso de ejemplo) ---
if __name__ == "__main__":
    print("--- Probando operaciones CRUD para proyectos ---")

    # Asegúrate de tener datos de prueba en otras tablas para que las FKs funcionen
    # Si no tienes, crea algunos:
    # 1. Crear un periodo (si no existe '2025-I')
    print("\n--- Preparando datos de prueba (Periodo, Materia, Participantes) ---")
    # Es importante que estos modelos estén accesibles o definidos
    from models.period_model import create_period, get_period_by_name, get_period_by_id
    from models.subject_model import create_subject, get_subject_by_code, get_subject_by_id
    from models.participant_model import create_participant, get_participant_by_cedula, get_participant_by_id

    periodo_ejemplo = get_period_by_name("2025-I")
    if not periodo_ejemplo:
        id_periodo_ejemplo = create_period("2025-I", datetime(2025, 1, 15).date(), datetime(2025, 6, 30).date(), True)
        if id_periodo_ejemplo:
            periodo_ejemplo = get_period_by_id(id_periodo_ejemplo)
    else:
        id_periodo_ejemplo = periodo_ejemplo['id_periodo']
    print(f"ID Periodo de ejemplo: {id_periodo_ejemplo}")


    materia_ejemplo = get_subject_by_code("ING401")
    if not materia_ejemplo:
        id_materia_ejemplo = create_subject("ING401", "Ingeniería de Software I", 4)
        if id_materia_ejemplo:
            materia_ejemplo = get_subject_by_id(id_materia_ejemplo)
    else:
        id_materia_ejemplo = materia_ejemplo['id_materia']
    print(f"ID Materia de ejemplo: {id_materia_ejemplo}")


    estudiante_ejemplo = get_participant_by_cedula("11111111")
    if not estudiante_ejemplo:
        id_estudiante_ejemplo = create_participant("Estudiante", "Ana", "Torres", "11111111", "ana.t@example.com", carrera="Sistemas")
        if id_estudiante_ejemplo:
            estudiante_ejemplo = get_participant_by_id(id_estudiante_ejemplo)
    else:
        id_estudiante_ejemplo = estudiante_ejemplo['id_participante']
    print(f"ID Estudiante de ejemplo: {id_estudiante_ejemplo}")


    docente_ejemplo = get_participant_by_cedula("99999999")
    if not docente_ejemplo:
        id_docente_ejemplo = create_participant("Docente", "Carlos", "Reyes", "99999999", "carlos.r@example.com")
        if id_docente_ejemplo:
            docente_ejemplo = get_participant_by_id(id_docente_ejemplo)
    else:
        id_docente_ejemplo = docente_ejemplo['id_participante']
    print(f"ID Docente de ejemplo: {id_docente_ejemplo}")

    if not all([id_periodo_ejemplo, id_materia_ejemplo, id_estudiante_ejemplo, id_docente_ejemplo]):
        print("No se pudieron preparar todos los datos de prueba. Saliendo de las pruebas de proyecto.")
        exit()

    # 1. Crear un nuevo proyecto
    print("\n--- Creando un nuevo proyecto con participantes ---")
    proyecto_id = create_project(
        id_periodo=id_periodo_ejemplo,
        id_materia=id_materia_ejemplo,
        nombre_proyecto="Sistema de Gestión de Exposiciones",
        descripcion="Un sistema para administrar los proyectos de la expoferia de ingeniería.",
        participantes_ids=[id_estudiante_ejemplo, id_docente_ejemplo]
    )
    if proyecto_id:
        print(f"Proyecto creado con ID: {proyecto_id}")
    else:
        print("Fallo al crear el proyecto.")

    # 2. Obtener el proyecto por ID
    if proyecto_id:
        print(f"\n--- Obteniendo proyecto con ID {proyecto_id} ---")
        project_details = get_project_by_id(proyecto_id)
        if project_details:
            print("Proyecto encontrado:", project_details)
            print("Participantes del proyecto:", project_details.get('participantes'))
        else:
            print("Proyecto no encontrado.")

    # 3. Obtener todos los proyectos
    print("\n--- Obteniendo todos los proyectos ---")
    all_projects = get_all_projects()
    for proj in all_projects:
        print(proj)

    # 4. Añadir otro participante al proyecto
    estudiante_extra_ejemplo = get_participant_by_cedula("22222222")
    if not estudiante_extra_ejemplo:
        id_estudiante_extra_ejemplo = create_participant("Estudiante", "Roberto", "Morales", "22222222", "roberto.m@example.com", carrera="Industrial")
        if id_estudiante_extra_ejemplo:
            estudiante_extra_ejemplo = get_participant_by_id(id_estudiante_extra_ejemplo)
    else:
        id_estudiante_extra_ejemplo = estudiante_extra_ejemplo['id_participante']
    print(f"ID Estudiante extra de ejemplo: {id_estudiante_extra_ejemplo}")

    if proyecto_id and id_estudiante_extra_ejemplo:
        print(f"\n--- Añadiendo un participante adicional al proyecto {proyecto_id} ---")
        add_success = add_participants_to_project(proyecto_id, [id_estudiante_extra_ejemplo])
        if add_success:
            print("Participantes adicionales añadidos exitosamente.")
            updated_project_details = get_project_by_id(proyecto_id)
            print("Proyecto con nuevos participantes:", updated_project_details.get('participantes'))

    # 5. Actualizar el proyecto (solo campos de proyecto, no participantes)
    if proyecto_id:
        print(f"\n--- Actualizando descripción del proyecto con ID {proyecto_id} ---")
        update_success = update_project(proyecto_id,
                                        descripcion="Descripción actualizada: Nuevo sistema de gestión de proyectos para la universidad.")
        if update_success:
            print("Descripción del proyecto actualizada exitosamente.")
            updated_project = get_project_by_id(proyecto_id)
            print("Proyecto actualizado:", updated_project['descripcion'])

    # 6. Eliminar un participante del proyecto (pero no el participante de la DB)
    if proyecto_id and id_estudiante_extra_ejemplo:
        print(f"\n--- Removiendo participante {id_estudiante_extra_ejemplo} del proyecto {proyecto_id} ---")
        remove_success = remove_participants_from_project(proyecto_id, [id_estudiante_extra_ejemplo])
        if remove_success:
            print("Participante removido exitosamente del proyecto.")
            updated_project_details = get_project_by_id(proyecto_id)
            print("Proyecto sin participante removido:", updated_project_details.get('participantes'))

    # 7. Eliminar el proyecto
    if proyecto_id:
        print(f"\n--- Eliminando proyecto con ID {proyecto_id} ---")
        delete_success = delete_project(proyecto_id)
        if delete_success:
            print("Proyecto eliminado exitosamente. Verificando si existe:")
            deleted_project_check = get_project_by_id(proyecto_id)
            if deleted_project_check is None:
                print("El proyecto ya no existe en la base de datos.")
            else:
                print("Error: El proyecto todavía existe.")
        else:
            print("Fallo al eliminar el proyecto.")