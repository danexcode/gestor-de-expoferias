# controllers/report_controller.py
from models.report_model import (
    get_filtered_projects_report,
    get_filtered_participants_report
)

# Importar modelos para validación de IDs.
# NOTA: En un sistema más grande, podrías inyectar los controladores de Periodo, Sujeto, Participante
#       en el ReportController para que este use sus métodos de validación, en lugar de importar los modelos directamente.
#       Por ahora, usar los modelos directamente es más simple para este ejemplo.
from models.period_model import get_period_by_id
from models.subject_model import get_subject_by_id
from models.participant_model import get_participant_by_id
from mysql.connector import Error

class ReportController:
    """
    Controlador para la generación de reportes del sistema.
    Coordina la obtención de datos para proyectos y participantes con filtros.
    """
    def generate_projects_report(self, period_id=None, student_id=None, teacher_id=None, subject_id=None):
        """
        Genera un reporte de proyectos aplicando los filtros especificados.
        Realiza validaciones de los IDs de filtro.

        Args:
            period_id (int, optional): ID del período.
            student_id (int, optional): ID de un participante (estudiante).
            teacher_id (int, optional): ID de un participante (docente).
            subject_id (int, optional): ID de la materia.

        Returns:
            tuple: (list of dict, str or None) - Una lista de proyectos si tiene éxito,
                   o una lista vacía y un mensaje de error en caso de fallo.
        """
        # Validaciones de entrada para los filtros
        if period_id is not None:
            try:
                period_id = int(period_id)
                if not get_period_by_id(period_id):
                    return [], f"Error: El ID de período '{period_id}' no existe."
            except ValueError:
                return [], "Error: El ID de período debe ser un número entero válido."
        
        if student_id is not None:
            try:
                student_id = int(student_id)
                participant_data = get_participant_by_id(student_id)
                if not participant_data:
                    return [], f"Error: El ID de estudiante '{student_id}' no existe."
                if participant_data['tipo_participante'] != 'Estudiante':
                    return [], f"Error: El participante con ID '{student_id}' no es un estudiante."
            except ValueError:
                return [], "Error: El ID de estudiante debe ser un número entero válido."

        if teacher_id is not None:
            try:
                teacher_id = int(teacher_id)
                participant_data = get_participant_by_id(teacher_id)
                if not participant_data:
                    return [], f"Error: El ID de docente '{teacher_id}' no existe."
                if participant_data['tipo_participante'] != 'Docente':
                    return [], f"Error: El participante con ID '{teacher_id}' no es un docente."
            except ValueError:
                return [], "Error: El ID de docente debe ser un número entero válido."

        if subject_id is not None:
            try:
                subject_id = int(subject_id)
                if not get_subject_by_id(subject_id):
                    return [], f"Error: El ID de materia '{subject_id}' no existe."
            except ValueError:
                return [], "Error: El ID de materia debe ser un número entero válido."

        try:
            projects = get_filtered_projects_report(period_id, student_id, teacher_id, subject_id)
            if not projects:
                return [], "No se encontraron proyectos con los filtros aplicados."
            return projects, None
        except Error as e: # Captura errores específicos de MySQL si el modelo los propaga
            return [], f"Error de base de datos al generar el reporte de proyectos: {e}"
        except Exception as e:
            return [], f"Error inesperado al generar el reporte de proyectos: {e}"

    def generate_participants_report(self, period_id=None, participant_type=None):
        """
        Genera un reporte de participantes asociados a proyectos, aplicando los filtros especificados.
        Realiza validaciones básicas de los IDs y el tipo de participante.

        Args:
            period_id (int, optional): ID del período.
            participant_type (str, optional): Tipo de participante ('Estudiante', 'Docente').

        Returns:
            tuple: (list of dict, str or None) - Una lista de participantes si tiene éxito,
                   o una lista vacía y un mensaje de error en caso de fallo.
        """
        # Validaciones de entrada para los filtros
        if period_id is not None:
            try:
                period_id = int(period_id)
                if not get_period_by_id(period_id):
                    return [], f"Error: El ID de período '{period_id}' no existe."
            except ValueError:
                return [], "Error: El ID de período debe ser un número entero válido."

        if participant_type is not None:
            if participant_type not in ['Estudiante', 'Docente']:
                return [], "Error: El tipo de participante debe ser 'Estudiante' o 'Docente'."
        
        try:
            participants = get_filtered_participants_report(period_id, participant_type)
            if not participants:
                return [], "No se encontraron participantes con los filtros aplicados."
            return participants, None
        except Error as e: # Captura errores específicos de MySQL si el modelo los propaga
            return [], f"Error de base de datos al generar el reporte de participantes: {e}"
        except Exception as e:
            return [], f"Error inesperado al generar el reporte de participantes: {e}"