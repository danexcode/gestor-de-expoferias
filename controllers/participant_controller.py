# controllers/participant_controller.py
from models.participant_model import (
    create_participant,
    get_all_participants,
    get_participant_by_id,
    update_participant,
    delete_participant
    # get_participants_by_type, # Estas se pueden manejar con get_all_participants y filtrar en el controlador
    # get_participants_by_project_id # Esta iría en project_model o report_model si la necesitas
)
from mysql.connector import Error # Importar Error para manejo específico de la base de datos

class ParticipantController:
    """
    Controlador para la gestión de participantes (Estudiantes y Docentes).
    Centraliza la lógica de negocio, validaciones y manejo de errores.
    """
    def add_new_participant(self, tipo_participante, nombre, apellido, cedula, correo_electronico=None, telefono=None, carrera=None):
        """
        Añade un nuevo participante a la base de datos.

        Args:
            tipo_participante (str): 'Estudiante' o 'Docente'.
            nombre (str): Nombre del participante.
            apellido (str): Apellido del participante.
            cedula (str): Cédula única del participante.
            correo_electronico (str, optional): Correo electrónico.
            telefono (str, optional): Número de teléfono.
            carrera (str, optional): Carrera (solo para estudiantes).

        Returns:
            tuple: (int or None, str or None)
                   - El ID del nuevo participante si tiene éxito.
                   - Un mensaje de error si falla.
        """
        if not all([tipo_participante, nombre, apellido, cedula]):
            return None, "Error: Todos los campos obligatorios (tipo, nombre, apellido, cédula) deben ser llenados."

        if tipo_participante not in ['Estudiante', 'Docente']:
            return None, "Error: Tipo de participante inválido. Debe ser 'Estudiante' o 'Docente'."
        
        # Validación de que la cédula sea única
        all_parts, _ = self.get_all_system_participants()
        for p in all_parts:
            if p['cedula'] == cedula:
                return None, f"Error: La cédula '{cedula}' ya está registrada para otro participante."
        
        # Validación de que el correo electrónico sea único (si se proporciona)
        if correo_electronico:
            for p in all_parts:
                if p['correo_electronico'] == correo_electronico:
                    return None, f"Error: El correo electrónico '{correo_electronico}' ya está registrado."

        if tipo_participante == 'Docente' and carrera:
            # print("Advertencia: Se especificó una carrera para un docente. Se ignorará.")
            carrera = None # Asegurarse de que docentes no tengan carrera
        
        try:
            participant_id = create_participant(tipo_participante, nombre, apellido, cedula, correo_electronico, telefono, carrera)
            if participant_id:
                return participant_id, None
            else:
                return None, "Error desconocido al añadir participante. Verifique los logs del modelo."
        except Error as e:
            # Captura errores específicos de MySQL, como duplicados si hay UNIQUE en la DB
            if "1062" in str(e): # MySQL error code for Duplicate entry for key 'PRIMARY' or 'UNIQUE'
                return None, "Error de duplicidad: La cédula o el correo electrónico ya existen."
            return None, f"Error de base de datos al añadir participante: {e}"
        except Exception as e:
            return None, f"Error inesperado al añadir participante: {e}"

    def get_all_system_participants(self):
        """
        Obtiene todos los participantes registrados en el sistema.

        Returns:
            tuple: (list of dict, str or None)
                   - Una lista de diccionarios con los datos de los participantes.
                   - Un mensaje de error si falla.
        """
        try:
            participants = get_all_participants()
            return participants, None
        except Exception as e:
            return [], f"Error al obtener todos los participantes: {e}"

    def get_participant_details(self, participant_id):
        """
        Obtiene los detalles de un participante específico por su ID.

        Args:
            participant_id (int): El ID del participante.

        Returns:
            tuple: (dict or None, str or None)
                   - Los datos del participante si se encuentra.
                   - Un mensaje de error si falla.
        """
        if not isinstance(participant_id, int):
            return None, "Error: El ID del participante debe ser un número entero."
        try:
            participant = get_participant_by_id(participant_id)
            if participant:
                return participant, None
            else:
                return None, f"No se encontró un participante con ID {participant_id}."
        except Exception as e:
            return None, f"Error al obtener detalles del participante {participant_id}: {e}"

    def update_existing_participant(self, participant_id, tipo_participante=None, nombre=None, apellido=None, cedula=None, correo_electronico=None, telefono=None, carrera=None):
        """
        Actualiza los datos de un participante existente.

        Args:
            participant_id (int): El ID del participante a actualizar.
            tipo_participante (str, optional): Nuevo tipo de participante.
            nombre (str, optional): Nuevo nombre.
            apellido (str, optional): Nuevo apellido.
            cedula (str, optional): Nueva cédula.
            correo_electronico (str, optional): Nuevo correo electrónico.
            telefono (str, optional): Nuevo número de teléfono.
            carrera (str, optional): Nueva carrera (si aplica).

        Returns:
            tuple: (bool, str or None)
                   - True si la actualización fue exitosa.
                   - Un mensaje de error si falla.
        """
        if not isinstance(participant_id, int):
            return False, "Error: El ID del participante debe ser un número entero."
        
        if not any(arg is not None for arg in [tipo_participante, nombre, apellido, cedula, correo_electronico, telefono, carrera]):
            return False, "No se proporcionaron campos para actualizar."

        current_participant, error_msg = self.get_participant_details(participant_id)
        if error_msg:
            return False, error_msg # El participante no existe para actualizar

        effective_type = tipo_participante if tipo_participante else current_participant['tipo_participante']

        if effective_type not in ['Estudiante', 'Docente']:
            return False, "Error: Tipo de participante inválido. Debe ser 'Estudiante' o 'Docente'."

        # Lógica para asegurar que si se cambia a Docente, se limpia la carrera
        # O si el participante ya es Docente y se intenta asignar carrera
        if effective_type == 'Docente' and carrera:
            # print("Advertencia: Se intentó asignar carrera a un docente. Se ignorará.")
            carrera = None # Asegurarse de que docentes no tengan carrera
        
        # Validar unicidad de cédula si se está actualizando
        if cedula and cedula != current_participant['cedula']:
            all_parts, _ = self.get_all_system_participants()
            for p in all_parts:
                if p['cedula'] == cedula and p['id_participante'] != participant_id:
                    return False, f"Error: La cédula '{cedula}' ya está registrada para otro participante."

        # Validar unicidad de correo electrónico si se está actualizando
        if correo_electronico and correo_electronico != current_participant['correo_electronico']:
            all_parts, _ = self.get_all_system_participants()
            for p in all_parts:
                if p['correo_electronico'] == correo_electronico and p['id_participante'] != participant_id:
                    return False, f"Error: El correo electrónico '{correo_electronico}' ya está registrado."

        try:
            success = update_participant(participant_id, tipo_participante, nombre, apellido, cedula, correo_electronico, telefono, carrera)
            if success:
                return True, None
            else:
                return False, "No se pudo actualizar el participante. Puede que no exista o no hubo cambios."
        except Error as e:
            if "1062" in str(e): # Duplicate entry
                return False, "Error de duplicidad al actualizar: la cédula o el correo ya existen."
            return False, f"Error de base de datos al actualizar participante {participant_id}: {e}"
        except Exception as e:
            return False, f"Error inesperado al actualizar participante {participant_id}: {e}"

    def delete_existing_participant(self, participant_id):
        """
        Elimina un participante de la base de datos.

        Args:
            participant_id (int): El ID del participante a eliminar.

        Returns:
            tuple: (bool, str or None)
                   - True si la eliminación fue exitosa.
                   - Un mensaje de error si falla.
        """
        if not isinstance(participant_id, int):
            return False, "Error: El ID del participante debe ser un número entero."
        try:
            success = delete_participant(participant_id)
            if success:
                return True, None
            else:
                return False, f"No se encontró un participante con ID {participant_id} para eliminar."
        except Error as e:
            # Aquí es donde podría haber un error de clave foránea si el participante
            # está asociado a un proyecto y la FK de proyectos_participantes es ON DELETE RESTRICT
            if "1451" in str(e): # Cannot delete or update a parent row: a foreign key constraint fails
                return False, "Error: No se puede eliminar el participante porque está asociado a uno o más proyectos."
            return False, f"Error de base de datos al eliminar participante {participant_id}: {e}"
        except Exception as e:
            return False, f"Error inesperado al eliminar participante {participant_id}: {e}"

    def get_students(self):
        """
        Obtiene solo los participantes de tipo 'Estudiante'.

        Returns:
            tuple: (list of dict, str or None)
                   - Una lista de estudiantes.
                   - Un mensaje de error si falla.
        """
        all_parts, error_msg = self.get_all_system_participants()
        if error_msg:
            return [], error_msg
        
        students = [p for p in all_parts if p['tipo_participante'] == 'Estudiante']
        return students, None

    def get_teachers(self):
        """
        Obtiene solo los participantes de tipo 'Docente'.

        Returns:
            tuple: (list of dict, str or None)
                   - Una lista de docentes.
                   - Un mensaje de error si falla.
        """
        all_parts, error_msg = self.get_all_system_participants()
        if error_msg:
            return [], error_msg
        
        teachers = [p for p in all_parts if p['tipo_participante'] == 'Docente']
        return teachers, None