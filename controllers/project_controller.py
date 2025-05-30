# controllers/project_controller.py
from datetime import datetime
from models.project_model import (
    create_project,
    get_project_by_id,
    get_all_projects,
    update_project,
    delete_project,
    add_participants_to_project,
    remove_participants_from_project
)
# Importar modelos para validación de IDs.
# NOTA: En una arquitectura más estricta, podrías inyectar los controladores de Periodo, Sujeto, Participante
#       en el ProjectController para usar sus métodos de validación, en lugar de importar los modelos directamente.
#       Por ahora, usar los modelos directamente es más simple para este ejemplo.
from models.period_model import get_period_by_id
from models.subject_model import get_subject_by_id
from models.participant_model import get_participant_by_id
from mysql.connector import Error # Para capturar errores específicos de la base de datos

class ProjectController:
    """
    Controlador para la gestión de proyectos.
    Centraliza la lógica de negocio, validaciones de claves foráneas y la
    asociación/desasociación de participantes.
    """
    def create_new_project(self, id_periodo, id_materia, nombre_proyecto, descripcion, participantes_ids=None):
        """
        Crea un nuevo proyecto en el sistema, validando las claves foráneas
        y asociando participantes.

        Args:
            id_periodo (int): ID del período al que pertenece el proyecto.
            id_materia (int): ID de la materia a la que está asociado el proyecto.
            nombre_proyecto (str): Nombre del proyecto.
            descripcion (str): Descripción detallada del proyecto.
            participantes_ids (list, optional): Lista de IDs de los participantes a asociar.

        Returns:
            tuple: (int or None, str or None)
                   - El ID del nuevo proyecto si se crea con éxito.
                   - Un mensaje de error si ocurre un problema.
        """
        if not all([id_periodo, id_materia, nombre_proyecto, descripcion]):
            return None, "Error: Todos los campos obligatorios (período, materia, nombre, descripción) deben ser llenados."

        try:
            id_periodo = int(id_periodo)
            id_materia = int(id_materia)
        except ValueError:
            return None, "Error: Los IDs de período y materia deben ser números enteros."

        # Validar IDs de claves foráneas
        if not get_period_by_id(id_periodo):
            return None, f"Error: El período con ID {id_periodo} no existe."
        if not get_subject_by_id(id_materia):
            return None, f"Error: La materia con ID {id_materia} no existe."
        
        # Validar que los IDs de participantes sean válidos
        processed_participants_ids = []
        if participantes_ids:
            if not isinstance(participantes_ids, list):
                return None, "Error: La lista de participantes debe ser una lista de IDs."
            
            unique_participant_ids = set() # Usar un set para evitar duplicados y validar
            for p_id_raw in participantes_ids:
                try:
                    p_id = int(p_id_raw)
                except ValueError:
                    return None, f"Error: El ID de participante '{p_id_raw}' no es un número entero válido."

                if not get_participant_by_id(p_id):
                    return None, f"Error: El participante con ID {p_id} no existe."
                unique_participant_ids.add(p_id)
            processed_participants_ids = list(unique_participant_ids)

        # Validar unicidad del nombre del proyecto
        all_projects, _ = self.get_all_system_projects()
        for proj in all_projects:
            if proj['nombre_proyecto'].lower() == nombre_proyecto.lower():
                return None, f"Error: Ya existe un proyecto con el nombre '{nombre_proyecto}'."

        try:
            project_id = create_project(id_periodo, id_materia, nombre_proyecto, descripcion, processed_participants_ids)
            if project_id:
                return project_id, None
            else:
                return None, "Error desconocido al crear el proyecto. No se recibió un ID de proyecto."
        except Error as e:
            if "1062" in str(e): # Duplicate entry for UNIQUE constraint (e.g., nombre_proyecto si es único en DB)
                return None, f"Error de duplicidad: Ya existe un proyecto con el nombre '{nombre_proyecto}'."
            elif "1452" in str(e): # Foreign key constraint fails (aunque ya validamos arriba, es un respaldo)
                return None, "Error de clave foránea. Asegúrese de que el período y la materia existan y sean correctos."
            else:
                return None, f"Error de base de datos al crear el proyecto: {e}"
        except Exception as e:
            return None, f"Error inesperado al crear el proyecto: {e}"

    def get_project_details(self, project_id):
        """
        Obtiene los detalles completos de un proyecto, incluyendo sus participantes.

        Args:
            project_id (int): ID del proyecto.

        Returns:
            tuple: (dict or None, str or None)
                   - Un diccionario con los datos del proyecto y sus participantes.
                   - Un mensaje de error si el proyecto no se encuentra o falla.
        """
        if not isinstance(project_id, int):
            return None, "Error: El ID del proyecto debe ser un número entero."
        try:
            project = get_project_by_id(project_id)
            if project:
                return project, None
            else:
                return None, f"No se encontró un proyecto con ID {project_id}."
        except Exception as e:
            return None, f"Error al obtener detalles del proyecto: {e}"

    def get_all_system_projects(self):
        """
        Obtiene una lista de todos los proyectos registrados en el sistema.

        Returns:
            tuple: (list of dict, str or None)
                   - Una lista de diccionarios con los datos básicos de los proyectos.
                   - Un mensaje de error si falla.
        """
        try:
            projects = get_all_projects()
            return projects, None
        except Exception as e:
            return [], f"Error al obtener todos los proyectos: {e}"

    def update_existing_project(self, project_id, **kwargs):
        """
        Actualiza la información de un proyecto existente.
        Permite actualizar id_periodo, id_materia, nombre_proyecto, descripcion.
        Para actualizar participantes, usar los métodos específicos de añadir/remover participantes.

        Args:
            project_id (int): ID del proyecto a actualizar.
            **kwargs: Campos a actualizar.

        Returns:
            tuple: (bool, str or None)
                   - True si la actualización fue exitosa.
                   - Un mensaje de error si ocurre un problema.
        """
        if not isinstance(project_id, int):
            return False, "Error: El ID del proyecto debe ser un número entero."
        if not kwargs:
            return False, "Error: No se proporcionaron campos para actualizar."

        current_project, error_msg = self.get_project_details(project_id)
        if error_msg:
            return False, error_msg # El proyecto no existe para actualizar

        # Validar IDs de claves foráneas si se están actualizando
        if 'id_periodo' in kwargs and kwargs['id_periodo'] is not None:
            try:
                new_period_id = int(kwargs['id_periodo'])
                if not get_period_by_id(new_period_id):
                    return False, f"Error: El período con ID {new_period_id} no existe."
                kwargs['id_periodo'] = new_period_id # Actualizar con el entero validado
            except ValueError:
                return False, "Error: El ID de período debe ser un número entero válido."

        if 'id_materia' in kwargs and kwargs['id_materia'] is not None:
            try:
                new_subject_id = int(kwargs['id_materia'])
                if not get_subject_by_id(new_subject_id):
                    return False, f"Error: La materia con ID {new_subject_id} no existe."
                kwargs['id_materia'] = new_subject_id # Actualizar con el entero validado
            except ValueError:
                return False, "Error: El ID de materia debe ser un número entero válido."

        # Validar unicidad del nombre del proyecto si se está actualizando
        if 'nombre_proyecto' in kwargs and kwargs['nombre_proyecto'] is not None:
            new_name = kwargs['nombre_proyecto']
            if new_name.lower() != current_project['nombre_proyecto'].lower(): # Solo verificar si el nombre realmente cambió
                all_projects, _ = self.get_all_system_projects()
                for p in all_projects:
                    if p['nombre_proyecto'].lower() == new_name.lower() and p['id_proyecto'] != project_id:
                        return False, f"Error: Ya existe un proyecto con el nombre '{new_name}'."

        try:
            success = update_project(project_id, **kwargs)
            if success:
                return True, None
            else:
                return False, "No se pudo actualizar el proyecto. Puede que el proyecto no exista o no hubo cambios."
        except Error as e:
            if "1062" in str(e): # Duplicate entry for UNIQUE constraint
                return False, f"Error de duplicidad al actualizar: Ya existe un proyecto con el nombre '{kwargs.get('nombre_proyecto', current_project['nombre_proyecto'])}'."
            elif "1452" in str(e): # Foreign key constraint fails
                return False, "Error de clave foránea al actualizar. Asegúrese de que el período y la materia existan."
            return False, f"Error de base de datos al actualizar el proyecto: {e}"
        except Exception as e:
            return False, f"Error inesperado al actualizar el proyecto: {e}"

    def delete_single_project(self, project_id):
        """
        Elimina un proyecto del sistema.

        Args:
            project_id (int): ID del proyecto a eliminar.

        Returns:
            tuple: (bool, str or None)
                   - True si la eliminación fue exitosa.
                   - Un mensaje de error si ocurre un problema.
        """
        if not isinstance(project_id, int):
            return False, "Error: El ID del proyecto debe ser un número entero."
        try:
            success = delete_project(project_id)
            if success:
                return True, None
            else:
                return False, f"No se encontró un proyecto con ID {project_id} para eliminar."
        except Error as e:
            # Puedes añadir manejo de errores específicos si tu DB tiene ON DELETE RESTRICT
            # para otras tablas relacionadas con proyectos (ej. reportes).
            if "1451" in str(e): # Cannot delete or update a parent row: a foreign key constraint fails
                return False, f"Error: No se puede eliminar el proyecto con ID {project_id} porque está asociado a otros registros (ej. reportes)."
            return False, f"Error de base de datos al eliminar el proyecto: {e}"
        except Exception as e:
            return False, f"Error inesperado al eliminar el proyecto: {e}"

    def add_participants_to_project_controller(self, project_id, new_participant_ids):
        """
        Añade nuevos participantes a un proyecto existente, validando su existencia.

        Args:
            project_id (int): ID del proyecto.
            new_participant_ids (list): Lista de IDs de participantes a añadir.

        Returns:
            tuple: (bool, str or None)
                   - True si la operación es exitosa.
                   - Un mensaje de error si ocurre un problema.
        """
        if not isinstance(project_id, int):
            return False, "Error: El ID del proyecto debe ser un número entero."
        if not self.get_project_details(project_id)[0]: # Check if project exists using the controller's method
            return False, f"Error: El proyecto con ID {project_id} no existe."
        
        if not new_participant_ids:
            return True, None # No hay participantes para añadir, se considera éxito
        
        if not isinstance(new_participant_ids, list):
            return False, "Error: La lista de IDs de participantes a añadir debe ser una lista."

        # Validar que los IDs de participantes sean válidos y únicos
        validated_ids = set()
        for p_id_raw in new_participant_ids:
            try:
                p_id = int(p_id_raw)
            except ValueError:
                return False, f"Error: El ID de participante '{p_id_raw}' no es un número entero válido."
            if not get_participant_by_id(p_id):
                return False, f"Error: El participante con ID {p_id} no existe."
            validated_ids.add(p_id)
        
        try:
            success = add_participants_to_project(project_id, list(validated_ids))
            if success:
                return True, None
            else:
                return False, "No se pudieron añadir los participantes al proyecto. Es posible que algunos ya estén asociados."
        except Error as e:
            # Error 1062 puede ocurrir si se intenta añadir un participante que ya está asociado
            if "1062" in str(e):
                 return False, f"Error de duplicidad: Uno o más participantes ya están asociados a este proyecto."
            return False, f"Error de base de datos al añadir participantes: {e}"
        except Exception as e:
            return False, f"Error inesperado al añadir participantes: {e}"

    def remove_participants_from_project_controller(self, project_id, participant_ids_to_remove):
        """
        Elimina participantes de un proyecto existente.

        Args:
            project_id (int): ID del proyecto.
            participant_ids_to_remove (list): Lista de IDs de participantes a remover.

        Returns:
            tuple: (bool, str or None)
                   - True si la operación es exitosa.
                   - Un mensaje de error si ocurre un problema.
        """
        if not isinstance(project_id, int):
            return False, "Error: El ID del proyecto debe ser un número entero."
        if not self.get_project_details(project_id)[0]: # Check if project exists
            return False, f"Error: El proyecto con ID {project_id} no existe."
        
        if not participant_ids_to_remove:
            return True, None # No hay participantes para remover, se considera éxito

        if not isinstance(participant_ids_to_remove, list):
            return False, "Error: La lista de IDs de participantes a remover debe ser una lista."

        # Validar que los IDs de participantes a remover sean enteros
        processed_remove_ids = set()
        for p_id_raw in participant_ids_to_remove:
            try:
                p_id = int(p_id_raw)
            except ValueError:
                return False, f"Error: El ID de participante '{p_id_raw}' no es un número entero válido."
            processed_remove_ids.add(p_id) # Usar set para unicidad
            
        try:
            success = remove_participants_from_project(project_id, list(processed_remove_ids))
            if success:
                return True, None
            else:
                return False, "No se pudieron remover los participantes del proyecto. Verifique si están asociados."
        except Error as e:
            return False, f"Error de base de datos al remover participantes: {e}"
        except Exception as e:
            return False, f"Error inesperado al remover participantes: {e}"