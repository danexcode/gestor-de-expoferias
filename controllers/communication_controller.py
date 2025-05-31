# controllers/communication_controller.py

# De tu db/connection.py
from db.connection import create_connection as get_db_connection 
from mysql.connector import Error

# Importamos la función de reporte que ya tienes para obtener participantes filtrados
from models.report_model import get_filtered_participants_report 

class CommunicationController:
    def __init__(self):
        # No se necesitan credenciales de email aquí
        pass

    def get_all_eligible_recipients(self):
        """
        Obtiene todos los usuarios y participantes con correos electrónicos válidos.
        Retorna una lista de diccionarios con id, nombre, email, y tipo.
        """
        recipients = []
        conn = None
        try:
            conn = get_db_connection()
            if conn is None:
                return [], "Error: No se pudo establecer conexión con la base de datos."
            cursor = conn.cursor(dictionary=True)

            # Obtener usuarios (solo si tienen email)
            cursor.execute("SELECT id_usuario AS id, nombre_usuario AS nombre_completo, correo_electronico AS email, 'Usuario' AS tipo FROM usuarios WHERE correo_electronico IS NOT NULL AND correo_electronico != ''")
            users = cursor.fetchall()
            for u in users:
                recipients.append({
                    'id': f"user_{u['id']}", 
                    'nombre_completo': u['nombre_completo'],
                    'email': u['email'],
                    'tipo': u['tipo']
                })

            # Obtener participantes (solo si tienen email)
            # Usamos get_filtered_participants_report para esto y los filtros.
            # Aquí obtenemos todos los participantes elegibles (sin filtro de periodo inicial)
            # NOTA: get_filtered_participants_report ya filtra por correo_electronico no nulo/vacío
            all_participants = get_filtered_participants_report() 
            for p in all_participants:
                recipients.append({
                    'id': f"part_{p['id_participante']}", 
                    'nombre_completo': f"{p['nombre']} {p['apellido']}",
                    'email': p['correo_electronico'],
                    'tipo': p['tipo_participante']
                })
            
            return recipients, None
        except Error as e:
            return [], f"Error al obtener destinatarios: {e}"
        except Exception as e:
            return [], f"Error inesperado al obtener destinatarios: {e}"
        finally:
            if conn:
                conn.close()

    def get_periods(self):
        """
        Obtiene una lista de todos los períodos disponibles desde la base de datos.
        Retorna una lista de diccionarios con 'id_periodo' y 'nombre_periodo'.
        """
        periods = []
        conn = None
        try:
            conn = get_db_connection()
            if conn is None:
                return [], "Error: No se pudo establecer conexión con la base de datos."
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id_periodo, nombre_periodo FROM periodos ORDER BY fecha_inicio DESC")
            periods = cursor.fetchall()
            return periods, None
        except Error as e:
            return [], f"Error al obtener períodos: {e}"
        finally:
            if conn:
                conn.close()

    def get_participants_by_period(self, period_id):
        """
        Obtiene participantes con correos válidos asociados a proyectos en un período específico.
        Utiliza la función existente en report_model.
        """
        # get_filtered_participants_report ya nos da los participantes asociados a proyectos en un periodo
        participants_raw = get_filtered_participants_report(period_id=period_id)
        
        filtered_participants = []
        for p in participants_raw:
            # Asegurarse de que el correo no sea nulo o vacío
            if p.get('correo_electronico') and p['correo_electronico'] != '':
                filtered_participants.append({
                    'id': f"part_{p['id_participante']}", 
                    'nombre_completo': f"{p['nombre']} {p['apellido']}",
                    'email': p['correo_electronico'],
                    'tipo': p['tipo_participante']
                })
        return filtered_participants, None