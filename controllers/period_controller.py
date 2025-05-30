# controllers/period_controller.py
from datetime import date
from models.period_model import (
    create_period,
    get_period_by_id,
    get_period_by_name,
    get_all_periods,
    update_period,
    delete_period
)
from mysql.connector import Error # Para capturar errores específicos de la base de datos

class PeriodController:
    """
    Controlador para la gestión de períodos académicos.
    Centraliza la lógica de negocio, validaciones de fechas y nombres únicos.
    """
    def add_new_period(self, nombre_periodo, fecha_inicio_str, fecha_fin_str, activo=True):
        """
        Añade un nuevo período al sistema.

        Args:
            nombre_periodo (str): Nombre único del período.
            fecha_inicio_str (str): Fecha de inicio del período en formato 'YYYY-MM-DD'.
            fecha_fin_str (str): Fecha de fin del período en formato 'YYYY-MM-DD'.
            activo (bool, optional): Indica si el período está activo. Por defecto es True.

        Returns:
            tuple: (int or None, str or None)
                   - El ID del nuevo período si se añade con éxito.
                   - Un mensaje de error si falla.
        """
        if not all([nombre_periodo, fecha_inicio_str, fecha_fin_str]):
            return None, "Error: Nombre, fecha de inicio y fecha de fin son obligatorios."

        try:
            # Convertir strings de fecha a objetos date
            fecha_inicio = date.fromisoformat(fecha_inicio_str)
            fecha_fin = date.fromisoformat(fecha_fin_str)
        except ValueError:
            return None, "Error: Formato de fecha inválido. Use 'YYYY-MM-DD'."

        if fecha_inicio > fecha_fin:
            return None, "Error: La fecha de inicio no puede ser posterior a la fecha de fin."

        try:
            # Verificar si ya existe un período con el mismo nombre
            if get_period_by_name(nombre_periodo):
                return None, f"Error: Ya existe un período con el nombre '{nombre_periodo}'."
            
            period_id = create_period(nombre_periodo, fecha_inicio, fecha_fin, activo)
            if period_id:
                return period_id, None
            else:
                return None, "Error desconocido al añadir el período. Verifique los logs del modelo."
        except Error as e:
            if "1062" in str(e): # Duplicate entry for unique key
                return None, f"Error de duplicidad: Ya existe un período con el nombre '{nombre_periodo}'."
            return None, f"Error de base de datos al añadir período: {e}"
        except Exception as e:
            return None, f"Error inesperado al añadir período: {e}"

    def get_single_period(self, period_id):
        """
        Obtiene los detalles de un período por su ID.

        Args:
            period_id (int): ID del período.

        Returns:
            tuple: (dict or None, str or None)
                   - Un diccionario con los datos del período si se encuentra.
                   - Un mensaje de error si no se encuentra o falla.
        """
        if not isinstance(period_id, int):
            return None, "Error: El ID del período debe ser un número entero."
        try:
            period = get_period_by_id(period_id)
            if period:
                return period, None
            else:
                return None, f"No se encontró un período con ID {period_id}."
        except Exception as e:
            return None, f"Error al obtener período {period_id}: {e}"

    def get_all_system_periods(self, active_only=False):
        """
        Obtiene una lista de todos los períodos del sistema.

        Args:
            active_only (bool, optional): Si es True, solo retorna períodos activos. Por defecto es False.

        Returns:
            tuple: (list of dict, str or None)
                   - Una lista de diccionarios con los datos de todos los períodos.
                   - Un mensaje de error si falla.
        """
        try:
            periods = get_all_periods(active_only)
            return periods, None
        except Exception as e:
            return [], f"Error al obtener todos los períodos: {e}"

    def update_period_details(self, period_id, **kwargs):
        """
        Actualiza la información de un período existente.

        Args:
            period_id (int): ID del período a actualizar.
            **kwargs: Campos a actualizar (nombre_periodo, fecha_inicio, fecha_fin, activo).
                      Las fechas deben pasarse como strings 'YYYY-MM-DD' si se actualizan.

        Returns:
            tuple: (bool, str or None)
                   - True si la actualización fue exitosa.
                   - Un mensaje de error si falla.
        """
        if not isinstance(period_id, int):
            return False, "Error: El ID del período debe ser un número entero."
        
        if not kwargs:
            return False, "No se proporcionaron datos para actualizar."
        
        # Obtener el período actual para validaciones
        current_period, error_msg = self.get_single_period(period_id)
        if error_msg:
            return False, error_msg # El período no existe para actualizar

        update_data = kwargs.copy() # Trabajar con una copia para no modificar kwargs directamente

        # Validar y convertir fechas si están presentes
        if 'fecha_inicio' in update_data and update_data['fecha_inicio'] is not None:
            try:
                update_data['fecha_inicio'] = date.fromisoformat(update_data['fecha_inicio'])
            except ValueError:
                return False, "Error: Formato de fecha de inicio inválido. Use 'YYYY-MM-DD'."
        
        if 'fecha_fin' in update_data and update_data['fecha_fin'] is not None:
            try:
                update_data['fecha_fin'] = date.fromisoformat(update_data['fecha_fin'])
            except ValueError:
                return False, "Error: Formato de fecha de fin inválido. Use 'YYYY-MM-DD'."

        # Validar que fecha_inicio no sea posterior a fecha_fin
        effective_start_date = update_data.get('fecha_inicio', current_period['fecha_inicio'])
        effective_end_date = update_data.get('fecha_fin', current_period['fecha_fin'])

        if effective_start_date and effective_end_date and effective_start_date > effective_end_date:
            return False, "Error: La fecha de inicio no puede ser posterior a la fecha de fin."

        # Prevenir duplicados si se actualiza el nombre_periodo
        if 'nombre_periodo' in update_data and update_data['nombre_periodo'] is not None:
            existing_period = get_period_by_name(update_data['nombre_periodo'])
            if existing_period and existing_period['id_periodo'] != period_id:
                return False, f"Error: El nombre de período '{update_data['nombre_periodo']}' ya está en uso por otro período."

        try:
            success = update_period(period_id, **update_data)
            if success:
                return True, None
            else:
                return False, "No se pudo actualizar el período. Puede que no exista o no hubo cambios."
        except Error as e:
            if "1062" in str(e): # Duplicate entry for unique key
                return False, f"Error de duplicidad: Ya existe un período con el nombre '{update_data.get('nombre_periodo')}'."
            return False, f"Error de base de datos al actualizar período {period_id}: {e}"
        except Exception as e:
            return False, f"Error inesperado al actualizar período {period_id}: {e}"

    def delete_existing_period(self, period_id):
        """
        Elimina un período del sistema.

        Args:
            period_id (int): ID del período a eliminar.

        Returns:
            tuple: (bool, str or None)
                   - True si la eliminación fue exitosa.
                   - Un mensaje de error si falla.
        """
        if not isinstance(period_id, int):
            return False, "Error: El ID del período debe ser un número entero."
        try:
            success = delete_period(period_id)
            if success:
                return True, None
            else:
                return False, f"No se encontró un período con ID {period_id} para eliminar."
        except Error as e:
            # Captura errores específicos de MySQL, como la restricción de clave foránea
            if "1451" in str(e): # Error 1451: Cannot delete or update a parent row: a foreign key constraint fails
                return False, f"Error: No se puede eliminar el período con ID {period_id} porque está asociado a uno o más proyectos."
            return False, f"Error de base de datos al eliminar período {period_id}: {e}"
        except Exception as e:
            return False, f"Error inesperado al eliminar período {period_id}: {e}"