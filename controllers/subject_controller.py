# controllers/subject_controller.py
from models.subject_model import (
    create_subject,
    get_subject_by_id,
    get_subject_by_code,
    get_all_subjects,
    update_subject,
    delete_subject
)
from mysql.connector import Error # Para capturar errores específicos de la base de datos

class SubjectController:
    """
    Controlador para la gestión de materias.
    Centraliza la lógica de negocio, validaciones y manejo de errores.
    """
    def add_new_subject(self, codigo_materia, nombre_materia, creditos=None):
        """
        Añade una nueva materia al sistema.

        Args:
            codigo_materia (str): Código alfanumérico único de la materia.
            nombre_materia (str): Nombre completo único de la materia.
            creditos (int, optional): Número de unidades de crédito de la materia.

        Returns:
            tuple: (int or None, str or None)
                   - El ID de la nueva materia si se añade con éxito.
                   - Un mensaje de error si falla.
        """
        if not all([codigo_materia, nombre_materia]):
            return None, "Error: El código y el nombre de la materia son obligatorios."
        
        if creditos is not None and not isinstance(creditos, int):
            return None, "Error: Los créditos deben ser un número entero."

        # Validar unicidad del código de materia
        if get_subject_by_code(codigo_materia):
            return None, f"Error: Ya existe una materia con el código '{codigo_materia}'."
        
        # Validar unicidad del nombre de materia (asumiendo que get_all_subjects puede ayudar)
        # Nota: Idealmente, tendrías get_subject_by_name en el modelo para una búsqueda eficiente.
        # Por ahora, simulamos buscando en todos los nombres.
        all_subjects, _ = self.get_all_system_subjects()
        for sub in all_subjects:
            if sub['nombre_materia'].lower() == nombre_materia.lower():
                return None, f"Error: Ya existe una materia con el nombre '{nombre_materia}'."

        try:
            subject_id = create_subject(codigo_materia, nombre_materia, creditos)
            if subject_id:
                return subject_id, None
            else:
                return None, "Error desconocido al crear la materia. Verifique los logs del modelo."
        except Error as e:
            if "1062" in str(e): # Duplicate entry for unique key (could be code or name if unique)
                return None, f"Error de duplicidad: El código o nombre de la materia ya existen."
            return None, f"Error de base de datos al crear materia: {e}"
        except Exception as e:
            return None, f"Error inesperado al crear materia: {e}"

    def get_single_subject(self, subject_id):
        """
        Obtiene los detalles de una materia por su ID.

        Args:
            subject_id (int): ID de la materia.

        Returns:
            tuple: (dict or None, str or None)
                   - Un diccionario con los datos de la materia si se encuentra.
                   - Un mensaje de error si no se encuentra o falla.
        """
        if not isinstance(subject_id, int):
            return None, "Error: El ID de la materia debe ser un número entero."
        try:
            subject = get_subject_by_id(subject_id)
            if subject:
                return subject, None
            else:
                return None, f"No se encontró una materia con ID {subject_id}."
        except Exception as e:
            return None, f"Error al obtener materia {subject_id}: {e}"

    def get_all_system_subjects(self):
        """
        Obtiene una lista de todas las materias del sistema.

        Returns:
            tuple: (list of dict, str or None)
                   - Una lista de diccionarios con los datos de todas las materias.
                   - Un mensaje de error si falla.
        """
        try:
            subjects = get_all_subjects()
            return subjects, None
        except Exception as e:
            return [], f"Error al obtener todas las materias: {e}"

    def update_existing_subject(self, subject_id, **kwargs):
        """
        Actualiza la información de una materia existente.

        Args:
            subject_id (int): ID de la materia a actualizar.
            **kwargs: Campos a actualizar (codigo_materia, nombre_materia, creditos).

        Returns:
            tuple: (bool, str or None)
                   - True si la actualización fue exitosa.
                   - Un mensaje de error si falla.
        """
        if not isinstance(subject_id, int):
            return False, "Error: El ID de la materia debe ser un número entero."
        
        if not kwargs:
            return False, "No se proporcionaron datos para actualizar."
        
        current_subject, error_msg = self.get_single_subject(subject_id)
        if error_msg:
            return False, error_msg # La materia no existe para actualizar

        # Validar y prevenir duplicidad si se actualiza el código de materia
        if 'codigo_materia' in kwargs and kwargs['codigo_materia'] is not None:
            new_code = kwargs['codigo_materia']
            if new_code != current_subject['codigo_materia']: # Solo verificar si el código realmente cambió
                existing_subject_by_code = get_subject_by_code(new_code)
                if existing_subject_by_code and existing_subject_by_code['id_materia'] != subject_id:
                    return False, f"Error: El código de materia '{new_code}' ya está en uso por otra materia."
        
        # Validar y prevenir duplicidad si se actualiza el nombre de materia
        if 'nombre_materia' in kwargs and kwargs['nombre_materia'] is not None:
            new_name = kwargs['nombre_materia']
            if new_name.lower() != current_subject['nombre_materia'].lower(): # Solo verificar si el nombre cambió
                all_subjects, _ = self.get_all_system_subjects()
                for sub in all_subjects:
                    if sub['nombre_materia'].lower() == new_name.lower() and sub['id_materia'] != subject_id:
                        return False, f"Error: El nombre de materia '{new_name}' ya está en uso por otra materia."

        if 'creditos' in kwargs and kwargs['creditos'] is not None:
            if not isinstance(kwargs['creditos'], int):
                return False, "Error: Los créditos deben ser un número entero."

        try:
            success = update_subject(subject_id, **kwargs)
            if success:
                return True, None
            else:
                return False, "No se pudo actualizar la materia. Puede que no exista o no hubo cambios."
        except Error as e:
            if "1062" in str(e): # Duplicate entry for unique key
                return False, f"Error de duplicidad al actualizar: El código o nombre de la materia ya existen."
            return False, f"Error de base de datos al actualizar materia {subject_id}: {e}"
        except Exception as e:
            return False, f"Error inesperado al actualizar materia {subject_id}: {e}"

    def delete_existing_subject(self, subject_id):
        """
        Elimina una materia del sistema.

        Args:
            subject_id (int): ID de la materia a eliminar.

        Returns:
            tuple: (bool, str or None)
                   - True si la eliminación fue exitosa.
                   - Un mensaje de error si falla.
        """
        if not isinstance(subject_id, int):
            return False, "Error: El ID de la materia debe ser un número entero."
        try:
            success = delete_subject(subject_id)
            if success:
                return True, None
            else:
                return False, f"No se encontró una materia con ID {subject_id} para eliminar."
        except Error as e:
            # Captura errores específicos de MySQL, como la restricción de clave foránea
            if "1451" in str(e): # Error 1451: Cannot delete or update a parent row: a foreign key constraint fails
                return False, f"Error: No se puede eliminar la materia con ID {subject_id} porque está asociada a uno o más proyectos."
            return False, f"Error de base de datos al eliminar materia {subject_id}: {e}"
        except Exception as e:
            return False, f"Error inesperado al eliminar materia {subject_id}: {e}"