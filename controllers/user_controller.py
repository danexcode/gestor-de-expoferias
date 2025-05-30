# controllers/user_controller.py
import hashlib # No es estrictamente necesario aquí si el hashing está en el modelo, pero se mantiene si se necesita para algo más.
from mysql.connector import Error # Importar Error para manejo específico

# Importar todas las funciones CRUD y de hashing/verificación desde user_model.py
from models.user_model import (
    create_user, get_user_by_username, get_user_by_id,
    get_all_users, update_user, delete_user,
    hash_password, verify_password # Importar las funciones de hashing y verificación
)

class UserController:
    """
    Controlador para la gestión de usuarios.
    Centraliza la lógica de negocio relacionada con la autenticación y la administración de usuarios.
    """
    _logged_in_user = None # Variable de clase para el usuario actualmente logueado

    def get_logged_in_user(self):
        """Retorna los datos del usuario actualmente logueado."""
        return UserController._logged_in_user

    def logout_user(self):
        """Cierra la sesión del usuario actual."""
        UserController._logged_in_user = None
        return True # Indica que la sesión se cerró correctamente

    def login_user(self, username, password):
        """
        Intenta iniciar sesión con el nombre de usuario y contraseña proporcionados.
        
        Args:
            username (str): Nombre de usuario.
            password (str): Contraseña en texto plano.

        Returns:
            tuple: (dict or None, str or None)
                   - Un diccionario con los datos del usuario si el login es exitoso y activo.
                   - Un mensaje de error si falla (ej. credenciales incorrectas, cuenta inactiva).
        """
        if not username or not password:
            return None, "Por favor, ingrese el nombre de usuario y la contraseña."

        user = get_user_by_username(username)
        if user:
            # Usar la función verify_password del modelo para comparar la contraseña
            if verify_password(user['contrasena_hash'], password):
                if user['activo']:
                    UserController._logged_in_user = user
                    return user, None # Login exitoso
                else:
                    return None, "Su cuenta está inactiva. Por favor, contacte al administrador."
            else:
                return None, "Credenciales incorrectas. Verifique su nombre de usuario o contraseña."
        return None, "Credenciales incorrectas. Verifique su nombre de usuario o contraseña."

    def register_new_user(self, username, password, role, full_name=None, email=None):
        """
        Registra un nuevo usuario en el sistema.

        Args:
            username (str): Nombre de usuario único.
            password (str): Contraseña en texto plano.
            role (str): Rol del usuario ('Administrador', 'Coordinador', 'Profesor').
            full_name (str, optional): Nombre completo del usuario.
            email (str, optional): Correo electrónico único.

        Returns:
            tuple: (int or None, str or None)
                   - El ID del nuevo usuario si el registro es exitoso.
                   - Un mensaje de error si falla.
        """
        if not all([username, password, role]):
            return None, "Nombre de usuario, contraseña y rol son obligatorios."
        if len(password) < 6: # Ejemplo de validación de contraseña simple
            return None, "La contraseña debe tener al menos 6 caracteres."
        if role not in ['Administrador', 'Coordinador', 'Profesor']:
            return None, "Rol inválido. Los roles permitidos son 'Administrador', 'Coordinador', 'Profesor'."

        # Verificar si el nombre de usuario ya existe
        if get_user_by_username(username):
            return None, f"El nombre de usuario '{username}' ya está en uso."
        
        # Verificar si el correo electrónico ya existe (si se proporciona)
        if email:
            all_users = get_all_users() # Obtener todos los usuarios para buscar si el email ya está registrado
            for u in all_users:
                if u['correo_electronico'] == email: # Asumiendo que 'correo_electronico' es la clave
                    return None, f"El correo electrónico '{email}' ya está registrado."

        try:
            # Llamar a create_user del modelo. El modelo se encarga del hashing.
            user_id = create_user(username, password, role, full_name, email)
            if user_id:
                return user_id, None
            else:
                return None, "Error desconocido al registrar el usuario. Verifique los logs del modelo."
        except Error as e:
            # Captura errores específicos de MySQL (ej. 1062 para duplicados)
            if "1062" in str(e): 
                return None, "Error de duplicidad. El usuario o correo ya existen."
            return None, f"Error de base de datos al registrar el usuario: {e}"
        except Exception as e:
            return None, f"Error inesperado al registrar el usuario: {e}"

    def get_all_system_users(self):
        """
        Obtiene una lista de todos los usuarios del sistema.

        Returns:
            tuple: (list of dict, str or None)
                   - Una lista de diccionarios con los datos de los usuarios.
                   - Un mensaje de error si falla.
        """
        try:
            users = get_all_users()
            return users, None
        except Exception as e:
            return [], f"Error al obtener todos los usuarios: {e}"

    def get_single_user_by_id(self, user_id):
        """
        Obtiene un usuario por su ID.

        Args:
            user_id (int): ID del usuario.

        Returns:
            tuple: (dict or None, str or None)
                   - Un diccionario con los datos del usuario si se encuentra.
                   - Un mensaje de error si falla.
        """
        if not isinstance(user_id, int):
            return None, "El ID de usuario debe ser un número entero."
        try:
            user = get_user_by_id(user_id)
            if user:
                return user, None
            else:
                return None, f"No se encontró un usuario con ID {user_id}."
        except Exception as e:
            return None, f"Error al obtener el usuario por ID: {e}"

    def update_existing_user(self, user_id, username=None, password=None, role=None, full_name=None, email=None, activo=None):
        """
        Actualiza los datos de un usuario existente.
        
        Args:
            user_id (int): El ID del usuario a actualizar.
            username (str, optional): Nuevo nombre de usuario.
            password (str, optional): Nueva contraseña (si se proporciona, se hashea en el modelo).
            role (str, optional): Nuevo rol.
            full_name (str, optional): Nuevo nombre completo.
            email (str, optional): Nuevo correo electrónico.
            activo (bool, optional): Nuevo estado de actividad.

        Returns:
            tuple: (bool, str or None)
                   - True si la actualización fue exitosa.
                   - Un mensaje de error si falla.
        """
        if not isinstance(user_id, int):
            return False, "El ID de usuario debe ser un número entero."
        
        # Verificar que se proporcionen campos para actualizar
        # Se verifica si al menos uno de los argumentos opcionales no es None
        if not any(arg is not None for arg in [username, password, role, full_name, email, activo]):
            return False, "No se proporcionaron campos para actualizar."

        if role and role not in ['Administrador', 'Coordinador', 'Profesor']:
            return False, "Rol inválido. Los roles permitidos son 'Administrador', 'Coordinador', 'Profesor'."
        
        # Obtener el usuario actual para comparar el nombre de usuario y email si se están actualizando
        current_user, error_msg = self.get_single_user_by_id(user_id)
        if error_msg:
            return False, error_msg # No existe el usuario para actualizar

        # Validaciones de unicidad para username y email si se están actualizando
        if username and username != current_user['nombre_usuario']: # Usar 'nombre_usuario' según tu modelo
            existing_user_by_name = get_user_by_username(username)
            if existing_user_by_name and existing_user_by_name['id_usuario'] != user_id:
                return False, f"El nombre de usuario '{username}' ya está en uso por otro usuario."
        
        if email and email != current_user['correo_electronico']: # Usar 'correo_electronico' según tu modelo
            all_users, _ = self.get_all_system_users()
            for u in all_users:
                if u['correo_electronico'] == email and u['id_usuario'] != user_id:
                    return False, f"El correo electrónico '{email}' ya está registrado por otro usuario."

        # Preparar los argumentos para la función update_user del modelo
        update_kwargs = {}
        if username is not None:
            update_kwargs['nombre_usuario'] = username
        if password is not None:
            update_kwargs['contrasena'] = password # Pasa la contraseña en texto plano, el modelo la hasheará
        if role is not None:
            update_kwargs['rol'] = role
        if full_name is not None:
            update_kwargs['nombre_completo'] = full_name
        if email is not None:
            update_kwargs['correo_electronico'] = email
        if activo is not None:
            update_kwargs['activo'] = activo

        try:
            success = update_user(user_id, **update_kwargs)
            if success:
                # Si el usuario logueado es el que se actualizó, refrescar sus datos
                if UserController._logged_in_user and UserController._logged_in_user['id_usuario'] == user_id:
                    UserController._logged_in_user = get_user_by_id(user_id)[0] # get_user_by_id retorna (user, error_msg)
                return True, None
            else:
                return False, "No se pudo actualizar el usuario. Puede que no exista o no hubo cambios."
        except Error as e:
            if "1062" in str(e):
                return False, "Error de duplicidad al actualizar: el nombre de usuario o correo ya existen."
            return False, f"Error de base de datos al actualizar usuario: {e}"
        except Exception as e:
            return False, f"Error inesperado al actualizar usuario: {e}"

    def delete_existing_user(self, user_id):
        """
        Elimina un usuario del sistema.

        Args:
            user_id (int): El ID del usuario a eliminar.

        Returns:
            tuple: (bool, str or None)
                   - True si la eliminación fue exitosa.
                   - Un mensaje de error si falla.
        """
        if not isinstance(user_id, int):
            return False, "El ID de usuario debe ser un número entero."
        
        if UserController._logged_in_user and UserController._logged_in_user['id_usuario'] == user_id:
            return False, "No puedes eliminar tu propia cuenta mientras estás logueado."

        try:
            success = delete_user(user_id)
            if success:
                return True, None
            else:
                return False, f"No se encontró un usuario con ID {user_id} para eliminar."
        except Error as e:
            return False, f"Error de base de datos al eliminar usuario: {e}"
        except Exception as e:
            return False, f"Error inesperado al eliminar usuario: {e}"