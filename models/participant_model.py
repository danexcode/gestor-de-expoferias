# models/participant_model.py
from db.connection import create_connection, close_connection

def create_participant(tipo_participante, nombre, apellido, cedula, correo_electronico, telefono, carrera):
    """Inserta un nuevo participante en la base de datos."""
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
        INSERT INTO participantes (tipo_participante, nombre, apellido, cedula, correo_electronico, telefono, carrera)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (tipo_participante, nombre, apellido, cedula, correo_electronico, telefono, carrera))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        close_connection(conn)

def get_all_participants():
    """Obtiene todos los participantes de la base de datos."""
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM participantes"
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        raise e
    finally:
        close_connection(conn)

def get_participant_by_id(participant_id):
    """Obtiene un participante por su ID."""
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM participantes WHERE id_participante = %s"
        cursor.execute(query, (participant_id,))
        return cursor.fetchone()
    except Exception as e:
        raise e
    finally:
        close_connection(conn)

def update_participant(participant_id, tipo_participante, nombre, apellido, cedula, correo_electronico, telefono, carrera):
    """Actualiza un participante existente."""
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Construir la consulta dinámicamente para actualizar solo los campos proporcionados
        updates = []
        params = []
        if tipo_participante is not None:
            updates.append("tipo_participante = %s")
            params.append(tipo_participante)
        if nombre is not None:
            updates.append("nombre = %s")
            params.append(nombre)
        if apellido is not None:
            updates.append("apellido = %s")
            params.append(apellido)
        if cedula is not None:
            updates.append("cedula = %s")
            params.append(cedula)
        if correo_electronico is not None:
            updates.append("correo_electronico = %s")
            params.append(correo_electronico)
        if telefono is not None:
            updates.append("telefono = %s")
            params.append(telefono)
        # Manejo especial para 'carrera': si se establece a None, se actualizará a NULL
        if carrera is not None:
            updates.append("carrera = %s")
            params.append(carrera)
        
        if not updates:
            return False # No hay campos para actualizar

        query = f"UPDATE participantes SET {', '.join(updates)} WHERE id_participante = %s"
        params.append(participant_id)
        
        cursor.execute(query, tuple(params))
        conn.commit()
        return cursor.rowcount > 0 # Retorna True si se actualizó al menos una fila
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        close_connection(conn)

def delete_participant(participant_id):
    """Elimina un participante de la base de datos."""
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "DELETE FROM participantes WHERE id_participante = %s"
        cursor.execute(query, (participant_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        close_connection(conn)

def get_participants_by_type(participant_type):
    """Obtiene participantes filtrados por tipo (Estudiante o Docente)."""
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM participantes WHERE tipo_participante = %s"
        cursor.execute(query, (participant_type,))
        return cursor.fetchall()
    except Exception as e:
        raise e
    finally:
        close_connection(conn)

def get_participants_by_project_id(project_id):
    """Obtiene los participantes asociados a un proyecto específico."""
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
        SELECT p.* FROM participantes p
        JOIN proyectos_participantes pp ON p.id_participante = pp.id_participante
        WHERE pp.id_proyecto = %s
        """
        cursor.execute(query, (project_id,))
        return cursor.fetchall()
    except Exception as e:
        raise e
    finally:
        close_connection(conn)