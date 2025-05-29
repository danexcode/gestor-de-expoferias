import mysql.connector
from mysql.connector import Error
from database import create_connection, close_connection

def get_filtered_projects_report(period_id=None, student_id=None, teacher_id=None, subject_id=None):
    """
    Obtiene proyectos filtrados dinámicamente por período, tipo de participante (estudiante/profesor)
    y/o materia. Todos los filtros son opcionales.

    Args:
        period_id (int, optional): ID del período.
        student_id (int, optional): ID de un participante (estudiante).
        teacher_id (int, optional): ID de un participante (docente).
        subject_id (int, optional): ID de la materia.

    Returns:
        list of dict: Una lista de diccionarios con detalles de los proyectos y sus asociados.
    """
    conn = create_connection()
    if conn is None:
        return []

    projects_data = []
    try:
        cursor = conn.cursor(dictionary=True)

        # La consulta base para proyectos
        query = """
        SELECT
            p.id_proyecto,
            p.nombre_proyecto,
            p.descripcion,
            p.fecha_registro,
            pe.nombre_periodo,
            pe.fecha_inicio AS periodo_inicio,
            pe.fecha_fin AS periodo_fin,
            m.nombre_materia,
            m.codigo_materia
        FROM proyectos p
        JOIN periodos pe ON p.id_periodo = pe.id_periodo
        JOIN materias m ON p.id_materia = m.id_materia
        """
        params = []
        where_clauses = []

        # Construir dinámicamente las cláusulas WHERE basadas en los filtros
        if period_id:
            where_clauses.append("p.id_periodo = %s")
            params.append(period_id)
        
        if subject_id:
            where_clauses.append("p.id_materia = %s")
            params.append(subject_id)

        # Si hay filtros por participante, necesitamos JOIN con proyectos_participantes y participantes
        participant_join_needed = student_id is not None or teacher_id is not None
        if participant_join_needed:
            query += " JOIN proyectos_participantes pp ON p.id_proyecto = pp.id_proyecto "
            query += " JOIN participantes part ON pp.id_participante = part.id_participante "

            if student_id:
                where_clauses.append("part.id_participante = %s AND part.tipo_participante = 'Estudiante'")
                params.append(student_id)
            if teacher_id:
                where_clauses.append("part.id_participante = %s AND part.tipo_participante = 'Docente'")
                params.append(teacher_id)

        # Unir todas las cláusulas WHERE
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
        
        # Asegurar que los proyectos se muestren una sola vez si hay joins de participantes
        if participant_join_needed:
             query += " GROUP BY p.id_proyecto " # Agrupar para evitar duplicados si hay múltiples participantes

        query += " ORDER BY pe.fecha_inicio DESC, p.nombre_proyecto ASC"
        
        cursor.execute(query, tuple(params))
        projects_data = cursor.fetchall()

        # Para cada proyecto, obtener sus participantes asociados (todos los tipos)
        for project in projects_data:
            participants_query = """
            SELECT part.id_participante, part.tipo_participante, part.nombre, part.apellido, part.cedula
            FROM participantes part
            JOIN proyectos_participantes pp ON part.id_participante = pp.id_participante
            WHERE pp.id_proyecto = %s
            ORDER BY part.tipo_participante ASC, part.apellido ASC
            """
            cursor.execute(participants_query, (project['id_proyecto'],))
            project['participantes'] = cursor.fetchall()

    except Error as e:
        print(f"Error al generar reporte de proyectos: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        close_connection(conn)
    return projects_data

def get_filtered_participants_report(period_id=None, participant_type=None):
    """
    Obtiene participantes que están asociados a proyectos, filtrados opcionalmente
    por período y/o tipo de participante.

    Args:
        period_id (int, optional): ID del período. Si es None, trae participantes de todos los períodos.
        participant_type (str, optional): Tipo de participante ('Estudiante', 'Docente').
                                          Si es None, trae ambos tipos.

    Returns:
        list of dict: Una lista de diccionarios con datos de participantes y los proyectos en los que están.
    """
    conn = create_connection()
    if conn is None:
        return []

    participants_data = []
    try:
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT DISTINCT
            part.id_participante,
            part.nombre,
            part.apellido,
            part.cedula,
            part.correo_electronico,
            part.telefono,
            part.tipo_participante,
            part.carrera,
            GROUP_CONCAT(DISTINCT p.nombre_proyecto SEPARATOR '; ') AS proyectos_asociados
        FROM participantes part
        JOIN proyectos_participantes pp ON part.id_participante = pp.id_participante
        JOIN proyectos p ON pp.id_proyecto = p.id_proyecto
        """
        params = []
        where_clauses = []

        if period_id:
            where_clauses.append("p.id_periodo = %s")
            params.append(period_id)

        if participant_type:
            where_clauses.append("part.tipo_participante = %s")
            params.append(participant_type)
        
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
        
        query += " GROUP BY part.id_participante " # Agrupar para tener una lista de proyectos por participante
        query += " ORDER BY part.tipo_participante ASC, part.apellido ASC, part.nombre ASC"

        cursor.execute(query, tuple(params))
        participants_data = cursor.fetchall()

    except Error as e:
        print(f"Error al generar reporte de participantes: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        close_connection(conn)
    return participants_data

# --- Bloque de Prueba (uso de ejemplo) ---
if __name__ == "__main__":
    print("--- Probando Módulo de Reportes Reestructurado ---")

    # Asegúrate de tener datos en tu DB para probar estos escenarios

    # Reporte de Proyectos: Todos los proyectos
    print("\n--- Reporte de Proyectos: Todos ---")
    all_projects = get_filtered_projects_report()
    if all_projects:
        for proj in all_projects:
            print(f"ID: {proj['id_proyecto']}, Nombre: {proj['nombre_proyecto']}, Periodo: {proj['nombre_periodo']}, Materia: {proj['nombre_materia']}")
            print("  Participantes:")
            for p in proj['participantes']:
                print(f"    - {p['tipo_participante']}: {p['nombre']} {p['apellido']}")
    else:
        print("No hay proyectos para mostrar.")

    # Reporte de Proyectos: Filtrado por Período (ej. ID 1)
    print("\n--- Reporte de Proyectos: Filtrado por Periodo (ID 1) ---")
    period_filtered_projects = get_filtered_projects_report(period_id=1)
    if period_filtered_projects:
        for proj in period_filtered_projects:
            print(f"ID: {proj['id_proyecto']}, Nombre: {proj['nombre_proyecto']}, Periodo: {proj['nombre_periodo']}")
    else:
        print("No hay proyectos para el periodo ID 1.")

    # Reporte de Proyectos: Filtrado por Docente (ej. ID 2, asume que es un docente)
    print("\n--- Reporte de Proyectos: Filtrado por Docente (ID 2) ---")
    teacher_filtered_projects = get_filtered_projects_report(teacher_id=2)
    if teacher_filtered_projects:
        for proj in teacher_filtered_projects:
            print(f"ID: {proj['id_proyecto']}, Nombre: {proj['nombre_proyecto']}, Materia: {proj['nombre_materia']}")
    else:
        print("No hay proyectos asociados al docente ID 2.")
    
    # Reporte de Participantes: Todos
    print("\n--- Reporte de Participantes: Todos ---")
    all_participants_report = get_filtered_participants_report()
    if all_participants_report:
        for part in all_participants_report:
            print(f"ID: {part['id_participante']}, Nombre: {part['nombre']} {part['apellido']}, Tipo: {part['tipo_participante']}")
            print(f"  Proyectos: {part['proyectos_asociados']}")
    else:
        print("No hay participantes asociados a proyectos.")

    # Reporte de Participantes: Filtrado por Estudiante y Periodo 1
    print("\n--- Reporte de Participantes: Estudiantes del Periodo 1 ---")
    filtered_students = get_filtered_participants_report(period_id=1, participant_type='Estudiante')
    if filtered_students:
        for part in filtered_students:
            print(f"ID: {part['id_participante']}, Nombre: {part['nombre']} {part['apellido']}, Carrera: {part['carrera']}")
            print(f"  Proyectos: {part['proyectos_asociados']}")
    else:
        print("No hay estudiantes para el periodo ID 1.")