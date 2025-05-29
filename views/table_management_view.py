# views/table_management_view.py
import sys
import os

# Ajustar sys.path para importar modelos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar modelos (TODAS las funciones CRUD de cada uno)
from models.user_model import *
from models.participant_model import *
from models.subject_model import *
from models.period_model import *
from models.project_model import *

# Importar utilidades de CLI (se asume que estas están en main_menu_view o un archivo común)
# Por ahora, para que este archivo funcione de forma independiente, las duplicamos.
# Idealmente, tendríamos un views/cli_utils.py que las contenga y luego importarlas.
def display_menu(options):
    """Muestra un menú numerado en la consola."""
    print("\n" + "="*40)
    print("           MENÚ PRINCIPAL           ")
    print("="*40)
    for i, option in enumerate(options):
        print(f"{i + 1}. {option}")
    print("="*40)

def get_menu_choice(num_options):
    """Solicita al usuario una elección de menú válida."""
    while True:
        try:
            choice = int(input("Seleccione una opción: "))
            if 1 <= choice <= num_options:
                return choice
            else:
                print("Opción inválida. Por favor, ingrese un número dentro del rango.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número.")

# --- Mueve TODAS las funciones manage_X() aquí ---
# manage_users(), manage_participants(), manage_subjects(), manage_periods(), manage_projects()
# (El contenido completo de estas funciones, tal como las tienes en main.py, iría aquí)

# Por ejemplo, solo el esqueleto para no repetir todo el código:
def manage_users():
    """Lógica para CRUD de Usuarios."""
    print("\n--- Gestión de Usuarios ---")
    user_management_options = [
        "Crear Usuario",
        "Ver Usuarios",
        "Actualizar Usuario",
        "Eliminar Usuario",
        "Volver al Menú Principal"
    ]
    while True:
        display_menu(user_management_options)
        choice = get_menu_choice(len(user_management_options))

        if choice == 1:
            print("\n  --- Crear Usuario ---")
            # Llamar a register_user_cli() o una versión más controlada
            register_user_cli() # Reutilizamos la función de registro para crear usuarios
        elif choice == 2:
            print("\n  --- Ver Usuarios ---")
            users = get_all_users()
            if users:
                for user in users:
                    print(user)
            else:
                print("No hay usuarios registrados.")
        elif choice == 3:
            print("\n  --- Actualizar Usuario ---")
            user_id_str = input("Ingrese el ID del usuario a actualizar: ")
            if not user_id_str.isdigit():
                print("ID de usuario inválido. Por favor, ingrese un número.")
                continue
            user_id = int(user_id_str)

            user_data = get_user_by_id(user_id)
            if not user_data:
                print(f"No se encontró ningún usuario con ID {user_id}.")
                continue

            print(f"Actualizando usuario: {user_data['nombre_usuario']}")
            updates = {}

            new_nombre_usuario = input(f"Nuevo nombre de usuario (actual: {user_data['nombre_usuario']}): ").strip()
            if new_nombre_usuario:
                updates['nombre_usuario'] = new_nombre_usuario

            new_contrasena = input("Nueva contraseña (dejar en blanco para no cambiar): ").strip()
            if new_contrasena:
                updates['contrasena'] = new_contrasena # El modelo se encarga de hashear

            new_rol = input(f"Nuevo rol (Administrador, Coordinador, Profesor, actual: {user_data['rol']}): ").strip()
            if new_rol in ['Administrador', 'Coordinador', 'Profesor']:
                updates['rol'] = new_rol
            elif new_rol: # Si se ingresó algo pero no es válido
                print("Rol inválido. Se mantendrá el rol actual.")

            new_nombre_completo = input(f"Nuevo nombre completo (actual: {user_data['nombre_completo'] if user_data['nombre_completo'] else 'N/A'}): ").strip()
            if new_nombre_completo:
                updates['nombre_completo'] = new_nombre_completo
            elif new_nombre_completo == '': # Si se quiere borrar
                updates['nombre_completo'] = None

            new_correo_electronico = input(f"Nuevo correo electrónico (actual: {user_data['correo_electronico'] if user_data['correo_electronico'] else 'N/A'}): ").strip()
            if new_correo_electronico:
                updates['correo_electronico'] = new_correo_electronico
            elif new_correo_electronico == '': # Si se quiere borrar
                updates['correo_electronico'] = None

            new_activo_str = input(f"¿Nuevo estado activo? (s/n, actual: {'s' if user_data['activo'] else 'n'}): ").strip().lower()
            if new_activo_str in ['s', 'n']:
                updates['activo'] = (new_activo_str == 's')


            if updates:
                update_user(user_id, **updates)
            else:
                print("No se proporcionaron datos válidos para actualizar.")
        elif choice == 4:
            print("\n  --- Eliminar Usuario ---")
            user_id_str = input("Ingrese el ID del usuario a eliminar: ")
            if not user_id_str.isdigit():
                print("ID de usuario inválido. Por favor, ingrese un número.")
                continue
            user_id = int(user_id_str)

            confirm = input(f"¿Está seguro que desea eliminar el usuario con ID {user_id}? (s/n): ").strip().lower()
            if confirm == 's':
                delete_user(user_id)
            else:
                print("Eliminación cancelada.")
        elif choice == 5:
            break # Volver al menú principal

def manage_participants():
    """Lógica para CRUD de Participantes."""
    print("\n--- Gestión de Participantes ---")
    # Lógica similar a manage_users, usando funciones de participant_model
    participant_management_options = [
        "Crear Participante",
        "Ver Participantes",
        "Actualizar Participante",
        "Eliminar Participante",
        "Volver al Menú Principal"
    ]
    while True:
        display_menu(participant_management_options)
        choice = get_menu_choice(len(participant_management_options))

        if choice == 1:
            print("\n  --- Crear Participante ---")
            # Aquí iría la lógica para pedir los datos y llamar a create_participant()
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            cedula = input("Cedula: ")
            correo = input("Correo (opcional): ")
            telefono = input("Telefono (opcional): ")
            tipo = input("Tipo (Estudiante/Docente): ")
            carrera = None
            if tipo == "Estudiante":
                carrera = input("Carrera (solo para Estudiantes): ")

            create_participant(tipo, nombre, apellido, cedula, correo if correo else None, telefono if telefono else None, carrera if carrera else None)

        elif choice == 2:
            print("\n  --- Ver Participantes ---")
            participants = get_all_participants()
            if participants:
                for p in participants:
                    print(p)
            else:
                print("No hay participantes registrados.")
        elif choice == 3:
            print("\n  --- Actualizar Participante ---")
            part_id_str = input("Ingrese el ID del participante a actualizar: ")
            if not part_id_str.isdigit():
                print("ID de participante inválido. Por favor, ingrese un número.")
                continue
            part_id = int(part_id_str)

            participant_data = get_participant_by_id(part_id)
            if not participant_data:
                print(f"No se encontró ningún participante con ID {part_id}.")
                continue

            print(f"Actualizando participante: {participant_data['nombre']} {participant_data['apellido']}")
            updates = {}

            new_nombre = input(f"Nuevo nombre (actual: {participant_data['nombre']}): ").strip()
            if new_nombre: updates['nombre'] = new_nombre
            new_apellido = input(f"Nuevo apellido (actual: {participant_data['apellido']}): ").strip()
            if new_apellido: updates['apellido'] = new_apellido
            new_cedula = input(f"Nueva cédula (actual: {participant_data['cedula']}): ").strip()
            if new_cedula: updates['cedula'] = new_cedula # Considerar unicidad si el modelo no la valida automáticamente

            new_correo = input(f"Nuevo correo electrónico (actual: {participant_data['correo_electronico'] if participant_data['correo_electronico'] else 'N/A'}): ").strip()
            if new_correo: updates['correo_electronico'] = new_correo
            elif new_correo == '': updates['correo_electronico'] = None

            new_telefono = input(f"Nuevo teléfono (actual: {participant_data['telefono'] if participant_data['telefono'] else 'N/A'}): ").strip()
            if new_telefono: updates['telefono'] = new_telefono
            elif new_telefono == '': updates['telefono'] = None

            if participant_data['tipo_participante'] == 'Estudiante':
                new_carrera = input(f"Nueva carrera (actual: {participant_data['carrera'] if participant_data['carrera'] else 'N/A'}): ").strip()
                if new_carrera: updates['carrera'] = new_carrera
                elif new_carrera == '': updates['carrera'] = None
            elif participant_data['tipo_participante'] == 'Docente':
                # No se permite cambiar carrera para docentes, o se podría validar si el tipo de participante cambia
                pass

            if updates:
                update_participant(part_id, **updates)
            else:
                print("No se proporcionaron datos válidos para actualizar.")
        elif choice == 4:
            print("\n  --- Eliminar Participante ---")
            part_id_str = input("Ingrese el ID del participante a eliminar: ")
            if not part_id_str.isdigit():
                print("ID de participante inválido. Por favor, ingrese un número.")
                continue
            part_id = int(part_id_str)

            confirm = input(f"¿Está seguro que desea eliminar el participante con ID {part_id}? (s/n): ").strip().lower()
            if confirm == 's':
                delete_participant(part_id)
            else:
                print("Eliminación cancelada.")
        elif choice == 5:
            break

def manage_subjects():
    """Lógica para CRUD de Materias."""
    print("\n--- Gestión de Materias ---")
    # Lógica similar a manage_users, usando funciones de subject_model
    subject_management_options = [
        "Crear Materia",
        "Ver Materias",
        "Actualizar Materia",
        "Eliminar Materia",
        "Volver al Menú Principal"
    ]
    while True:
        display_menu(subject_management_options)
        choice = get_menu_choice(len(subject_management_options))

        if choice == 1:
            print("\n  --- Crear Materia ---")
            codigo = input("Código de Materia: ")
            nombre = input("Nombre de Materia: ")
            creditos = input("Créditos (opcional, entero): ")
            create_subject(codigo, nombre, int(creditos) if creditos.isdigit() else None)
        elif choice == 2:
            print("\n  --- Ver Materias ---")
            subjects = get_all_subjects()
            if subjects:
                for s in subjects:
                    print(s)
            else:
                print("No hay materias registradas.")
        elif choice == 3:
            print("\n  --- Actualizar Materia ---")
            materia_id_str = input("Ingrese el ID de la materia a actualizar: ")
            if not materia_id_str.isdigit():
                print("ID de materia inválido. Por favor, ingrese un número.")
                continue
            materia_id = int(materia_id_str)

            subject_data = get_subject_by_id(materia_id)
            if not subject_data:
                print(f"No se encontró ninguna materia con ID {materia_id}.")
                continue

            print(f"Actualizando materia: {subject_data['nombre_materia']}")
            updates = {}

            new_codigo = input(f"Nuevo código de materia (actual: {subject_data['codigo_materia']}): ").strip()
            if new_codigo:
                updates['codigo_materia'] = new_codigo
            new_nombre = input(f"Nuevo nombre de materia (actual: {subject_data['nombre_materia']}): ").strip()
            if new_nombre:
                updates['nombre_materia'] = new_nombre
            new_creditos_str = input(f"Nuevos créditos (actual: {subject_data['creditos'] if subject_data['creditos'] else 'N/A'}, entero): ").strip()
            if new_creditos_str:
                if new_creditos_str.isdigit():
                    updates['creditos'] = int(new_creditos_str)
                else:
                    print("Créditos inválidos. Se ignorará la actualización de créditos.")
            elif new_creditos_str == '':
                updates['creditos'] = None # Para permitir borrar los créditos

            if updates:
                update_subject(materia_id, **updates)
            else:
                print("No se proporcionaron datos válidos para actualizar.")
        elif choice == 4:
            print("\n  --- Eliminar Materia ---")
            materia_id_str = input("Ingrese el ID de la materia a eliminar: ")
            if not materia_id_str.isdigit():
                print("ID de materia inválido. Por favor, ingrese un número.")
                continue
            materia_id = int(materia_id_str)

            confirm = input(f"¿Está seguro que desea eliminar la materia con ID {materia_id}? (s/n): ").strip().lower()
            if confirm == 's':
                delete_subject(materia_id)
            else:
                print("Eliminación cancelada.")
        elif choice == 5:
            break

def manage_periods():
    """Lógica para CRUD de Períodos."""
    print("\n--- Gestión de Períodos ---")
    period_management_options = [
        "Crear Período",
        "Ver Períodos",
        "Actualizar Período",
        "Eliminar Período",
        "Volver al Menú Principal"
    ]
    while True:
        display_menu(period_management_options)
        choice = get_menu_choice(len(period_management_options))

        if choice == 1:
            print("\n  --- Crear Período ---")
            from datetime import date # Importar aquí para asegurar que esté disponible
            nombre = input("Nombre del Período: ")

            fecha_inicio = None
            while fecha_inicio is None:
                fecha_inicio_str = input("Fecha de Inicio (YYYY-MM-DD): ")
                try:
                    fecha_inicio = date.fromisoformat(fecha_inicio_str)
                except ValueError:
                    print("Formato de fecha de inicio inválido. Por favor, use YYYY-MM-DD.")

            fecha_fin = None
            while fecha_fin is None:
                fecha_fin_str = input("Fecha de Fin (YYYY-MM-DD): ")
                try:
                    fecha_fin = date.fromisoformat(fecha_fin_str)
                except ValueError:
                    print("Formato de fecha de fin inválido. Por favor, use YYYY-MM-DD.")

            # Validación: fecha_inicio debe ser menor o igual a fecha_fin
            if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
                print("Error: La fecha de inicio no puede ser posterior a la fecha de fin.")
                continue # Volver a pedir las fechas

            activo_str = input("¿Está activo? (s/n, predeterminado s): ").strip().lower()
            activo = (activo_str == 's' or not activo_str) # True si es 's' o cadena vacía

            create_period(nombre, fecha_inicio, fecha_fin, activo)

        elif choice == 2:
            print("\n  --- Ver Períodos ---")
            periods = get_all_periods()
            if periods:
                for p in periods:
                    print(p)
            else:
                print("No hay períodos registrados.")
        elif choice == 3:
            print("\n  --- Actualizar Período ---")
            # --- Lógica de Actualización de Período ---
            period_id_str = input("Ingrese el ID del período a actualizar: ")
            if not period_id_str.isdigit():
                print("ID de período inválido. Por favor, ingrese un número.")
                continue
            period_id = int(period_id_str)

            period = get_period_by_id(period_id)
            if not period:
                print(f"No se encontró ningún período con ID {period_id}.")
                continue

            print(f"Actualizando período: {period['nombre_periodo']}")
            updates = {}

            new_nombre = input(f"Nuevo nombre de período (actual: {period['nombre_periodo']}): ").strip()
            if new_nombre:
                updates['nombre_periodo'] = new_nombre

            # Lógica para actualizar fechas con validación
            new_fecha_inicio_str = input(f"Nueva fecha de inicio (YYYY-MM-DD, actual: {period['fecha_inicio']}): ").strip()
            new_fecha_inicio = None
            if new_fecha_inicio_str:
                try:
                    new_fecha_inicio = date.fromisoformat(new_fecha_inicio_str)
                    updates['fecha_inicio'] = new_fecha_inicio
                except ValueError:
                    print("Formato de fecha de inicio inválido. Se ignorará la actualización de esta fecha.")
            
            new_fecha_fin_str = input(f"Nueva fecha de fin (YYYY-MM-DD, actual: {period['fecha_fin']}): ").strip()
            new_fecha_fin = None
            if new_fecha_fin_str:
                try:
                    new_fecha_fin = date.fromisoformat(new_fecha_fin_str)
                    updates['fecha_fin'] = new_fecha_fin
                except ValueError:
                    print("Formato de fecha de fin inválido. Se ignorará la actualización de esta fecha.")
            
            # Re-validar las fechas después de posibles actualizaciones
            final_fecha_inicio = updates.get('fecha_inicio', period['fecha_inicio'])
            final_fecha_fin = updates.get('fecha_fin', period['fecha_fin'])

            if final_fecha_inicio and final_fecha_fin and final_fecha_inicio > final_fecha_fin:
                print("Error: La nueva fecha de inicio no puede ser posterior a la nueva fecha de fin. No se realizará la actualización de fechas.")
                # Eliminar las fechas de updates si la validación falla
                updates.pop('fecha_inicio', None)
                updates.pop('fecha_fin', None)


            new_activo_str = input(f"¿Nuevo estado activo? (s/n, actual: {'s' if period['activo'] else 'n'}): ").strip().lower()
            if new_activo_str in ['s', 'n']:
                updates['activo'] = (new_activo_str == 's')

            if updates:
                update_period(period_id, **updates)
            else:
                print("No se proporcionaron datos válidos para actualizar.")
            # --- Fin Lógica de Actualización ---

        elif choice == 4:
            print("\n  --- Eliminar Período ---")
            # --- Lógica de Eliminación de Período ---
            period_id_str = input("Ingrese el ID del período a eliminar: ")
            if not period_id_str.isdigit():
                print("ID de período inválido. Por favor, ingrese un número.")
                continue
            period_id = int(period_id_str)

            confirm = input(f"¿Está seguro que desea eliminar el período con ID {period_id}? (s/n): ").strip().lower()
            if confirm == 's':
                delete_period(period_id)
            else:
                print("Eliminación cancelada.")
            # --- Fin Lógica de Eliminación ---
        elif choice == 5:
            break

def manage_projects():
    """Lógica para CRUD de Proyectos y gestión de sus participantes."""
    print("\n--- Gestión de Proyectos ---")
    project_management_options = [
        "Crear Proyecto",
        "Ver Detalles de Proyecto", # Cambiado para ver detalles específicos
        "Ver Todos los Proyectos",
        "Actualizar Proyecto",
        "Eliminar Proyecto",
        "Gestionar Participantes de Proyecto", # Añadir/Eliminar participantes
        "Volver al Menú Principal"
    ]
    while True:
        display_menu(project_management_options)
        choice = get_menu_choice(len(project_management_options))

        if choice == 1:
            print("\n  --- Crear Proyecto ---")
            # 1. Pedir nombre y descripción del proyecto
            nombre_proyecto = input("Nombre del Proyecto: ").strip()
            descripcion = input("Descripción del Proyecto: ").strip()

            # 2. Seleccionar Período
            id_periodo = None
            while id_periodo is None:
                print("\nPeríodos disponibles:")
                periods = get_all_periods(active_only=True) # Podríamos listar solo activos
                if not periods:
                    print("No hay períodos activos registrados. Por favor, registre uno primero.")
                    break # Salir de la creación del proyecto
                for p in periods:
                    print(f"ID: {p['id_periodo']}, Nombre: {p['nombre_periodo']} ({p['fecha_inicio']} a {p['fecha_fin']})")
                
                period_id_str = input("Ingrese el ID del Período para este proyecto: ").strip()
                if period_id_str.isdigit():
                    temp_id_periodo = int(period_id_str)
                    if get_period_by_id(temp_id_periodo):
                        id_periodo = temp_id_periodo
                    else:
                        print("ID de Período no encontrado.")
                else:
                    print("ID de Período inválido.")
            if id_periodo is None: continue # Si no se pudo seleccionar período, volver al menú de proyectos

            # 3. Seleccionar Materia
            id_materia = None
            while id_materia is None:
                print("\nMaterias disponibles:")
                materias = get_all_subjects()
                if not materias:
                    print("No hay materias registradas. Por favor, registre una primero.")
                    break # Salir de la creación del proyecto
                for m in materias:
                    print(f"ID: {m['id_materia']}, Código: {m['codigo_materia']}, Nombre: {m['nombre_materia']}")
                
                materia_id_str = input("Ingrese el ID de la Materia para este proyecto: ").strip()
                if materia_id_str.isdigit():
                    temp_id_materia = int(materia_id_str)
                    if get_subject_by_id(temp_id_materia):
                        id_materia = temp_id_materia
                    else:
                        print("ID de Materia no encontrado.")
                else:
                    print("ID de Materia inválido.")
            if id_materia is None: continue # Si no se pudo seleccionar materia, volver al menú de proyectos

            # 4. Seleccionar Participantes (múltiples)
            participantes_ids = []
            while True:
                print("\nParticipantes disponibles (Estudiantes/Docentes):")
                all_participants = get_all_participants()
                if not all_participants:
                    print("No hay participantes registrados. Considere registrarlos en la sección de Participantes.")
                    break # No se pueden añadir participantes si no hay
                
                for p in all_participants:
                    print(f"ID: {p['id_participante']}, Tipo: {p['tipo_participante']}, Nombre: {p['nombre']} {p['apellido']} (C.I.: {p['cedula']})")
                
                part_id_str = input("Ingrese ID de participante a añadir (o 'f' para finalizar): ").strip().lower()
                if part_id_str == 'f':
                    break
                elif part_id_str.isdigit():
                    part_id = int(part_id_str)
                    # Opcional: Verificar que el participante exista realmente
                    if get_participant_by_id(part_id):
                        if part_id not in participantes_ids:
                            participantes_ids.append(part_id)
                            print(f"Participante {part_id} añadido provisionalmente.")
                        else:
                            print("Este participante ya ha sido seleccionado.")
                    else:
                        print("ID de participante no encontrado.")
                else:
                    print("Entrada inválida. Ingrese un número o 'f'.")
            
            if not participantes_ids:
                print("Advertencia: Se creará el proyecto sin participantes iniciales. Puede añadirlos más tarde.")
            
            # 5. Crear el proyecto
            if id_periodo and id_materia and nombre_proyecto and descripcion:
                create_project(id_periodo, id_materia, nombre_proyecto, descripcion, participantes_ids)
            else:
                print("Datos incompletos para crear el proyecto. Asegúrese de proporcionar nombre, descripción, período y materia.")

        elif choice == 2:
            print("\n  --- Ver Detalles de Proyecto ---")
            project_id_str = input("Ingrese el ID del proyecto a ver: ").strip()
            if not project_id_str.isdigit():
                print("ID de proyecto inválido. Por favor, ingrese un número.")
                continue
            
            project_id = int(project_id_str)
            project_details = get_project_by_id(project_id)
            
            if project_details:
                print("\n--- Detalles del Proyecto ---")
                print(f"ID Proyecto: {project_details['id_proyecto']}")
                print(f"Nombre: {project_details['nombre_proyecto']}")
                print(f"Descripción: {project_details['descripcion']}")
                print(f"Fecha de Registro: {project_details['fecha_registro']}")
                print(f"Período: {project_details['nombre_periodo']} ({project_details['periodo_inicio']} a {project_details['periodo_fin']})")
                print(f"Materia: {project_details['nombre_materia']} ({project_details['codigo_materia']})")
                
                print("\n--- Participantes ---")
                if project_details.get('participantes'):
                    for p in project_details['participantes']:
                        print(f"  - ID: {p['id_participante']}, {p['tipo_participante']}: {p['nombre']} {p['apellido']} (C.I.: {p['cedula']})")
                else:
                    print("  No hay participantes asociados a este proyecto.")
            else:
                print(f"No se encontró ningún proyecto con ID {project_id}.")

        elif choice == 3:
            print("\n  --- Ver Todos los Proyectos (Resumen) ---")
            projects = get_all_projects()
            if projects:
                for proj in projects:
                    # Formateo para mostrar los datos más relevantes de forma concisa
                    print(f"ID: {proj['id_proyecto']}, Nombre: {proj['nombre_proyecto']}, Materia: {proj['nombre_materia']}, Período: {proj['nombre_periodo']}, Fecha Registro: {proj['fecha_registro'].strftime('%Y-%m-%d')}")
            else:
                print("No hay proyectos registrados.")

        elif choice == 4:
            print("\n  --- Actualizar Proyecto ---")
            project_id_str = input("Ingrese el ID del proyecto a actualizar: ").strip()
            if not project_id_str.isdigit():
                print("ID de proyecto inválido. Por favor, ingrese un número.")
                continue
            project_id = int(project_id_str)

            project_data = get_project_by_id(project_id)
            if not project_data:
                print(f"No se encontró ningún proyecto con ID {project_id}.")
                continue

            print(f"Actualizando proyecto: {project_data['nombre_proyecto']}")
            updates = {}

            new_nombre = input(f"Nuevo nombre del proyecto (actual: {project_data['nombre_proyecto']}): ").strip()
            if new_nombre: updates['nombre_proyecto'] = new_nombre
            
            new_descripcion = input(f"Nueva descripción (actual: {project_data['descripcion']}): ").strip()
            if new_descripcion: updates['descripcion'] = new_descripcion
            elif new_descripcion == '': updates['descripcion'] = "" # Permitir vaciar descripción

            # Actualizar Período (opcional)
            print(f"\nPeríodo actual del proyecto: {project_data['nombre_periodo']}")
            change_period = input("¿Desea cambiar el período del proyecto? (s/n): ").strip().lower()
            if change_period == 's':
                print("\nPeríodos disponibles:")
                periods = get_all_periods(active_only=True)
                for p in periods:
                    print(f"ID: {p['id_periodo']}, Nombre: {p['nombre_periodo']}")
                
                new_period_id_str = input("Ingrese el ID del nuevo Período: ").strip()
                if new_period_id_str.isdigit():
                    temp_new_period_id = int(new_period_id_str)
                    if get_period_by_id(temp_new_period_id):
                        updates['id_periodo'] = temp_new_period_id
                    else:
                        print("ID de Período no encontrado. Se mantendrá el período actual.")
                else:
                    print("ID de Período inválido. Se mantendrá el período actual.")

            # Actualizar Materia (opcional)
            print(f"\nMateria actual del proyecto: {project_data['nombre_materia']}")
            change_subject = input("¿Desea cambiar la materia del proyecto? (s/n): ").strip().lower()
            if change_subject == 's':
                print("\nMaterias disponibles:")
                materias = get_all_subjects()
                for m in materias:
                    print(f"ID: {m['id_materia']}, Código: {m['codigo_materia']}, Nombre: {m['nombre_materia']}")
                
                new_subject_id_str = input("Ingrese el ID de la nueva Materia: ").strip()
                if new_subject_id_str.isdigit():
                    temp_new_subject_id = int(new_subject_id_str)
                    if get_subject_by_id(temp_new_subject_id):
                        updates['id_materia'] = temp_new_subject_id
                    else:
                        print("ID de Materia no encontrado. Se mantendrá la materia actual.")
                else:
                    print("ID de Materia inválido. Se mantendrá la materia actual.")
            
            if updates:
                update_project(project_id, **updates)
            else:
                print("No se proporcionaron datos válidos para actualizar el proyecto.")

        elif choice == 5:
            print("\n  --- Eliminar Proyecto ---")
            project_id_str = input("Ingrese el ID del proyecto a eliminar: ").strip()
            if not project_id_str.isdigit():
                print("ID de proyecto inválido. Por favor, ingrese un número.")
                continue
            project_id = int(project_id_str)

            confirm = input(f"¿Está seguro que desea eliminar el proyecto con ID {project_id}? (s/n): ").strip().lower()
            if confirm == 's':
                delete_project(project_id)
            else:
                print("Eliminación cancelada.")

        elif choice == 6: # Gestionar Participantes de Proyecto
            print("\n  --- Gestionar Participantes de Proyecto ---")
            project_id_str = input("Ingrese el ID del proyecto para gestionar sus participantes: ").strip()
            if not project_id_str.isdigit():
                print("ID de proyecto inválido. Por favor, ingrese un número.")
                continue
            project_id = int(project_id_str)

            project_details = get_project_by_id(project_id)
            if not project_details:
                print(f"No se encontró ningún proyecto con ID {project_id}.")
                continue
            
            print(f"\n--- Gestionando participantes para el proyecto: {project_details['nombre_proyecto']} (ID: {project_id}) ---")
            
            # Mostrar participantes actuales
            print("\nParticipantes actuales:")
            if project_details.get('participantes'):
                for p in project_details['participantes']:
                    print(f"  - ID: {p['id_participante']}, {p['tipo_participante']}: {p['nombre']} {p['apellido']}")
            else:
                print("  No hay participantes asociados actualmente.")

            while True:
                part_management_options = [
                    "Añadir Participantes",
                    "Remover Participantes",
                    "Volver a Gestión de Proyectos"
                ]
                display_menu(part_management_options)
                part_choice = get_menu_choice(len(part_management_options))

                if part_choice == 1:
                    print("\n    --- Añadir Participantes ---")
                    new_participants_ids = []
                    while True:
                        print("\nParticipantes disponibles (excepto los ya asociados):")
                        all_participants = get_all_participants()
                        current_associated_ids = [p['id_participante'] for p in project_details.get('participantes', [])]
                        
                        available_for_add = [p for p in all_participants if p['id_participante'] not in current_associated_ids]
                        
                        if not available_for_add:
                            print("No hay más participantes disponibles para añadir o todos ya están asociados.")
                            break
                        
                        for p in available_for_add:
                            print(f"      ID: {p['id_participante']}, {p['tipo_participante']}: {p['nombre']} {p['apellido']}")
                        
                        part_id_str = input("      Ingrese ID de participante a añadir (o 'f' para finalizar): ").strip().lower()
                        if part_id_str == 'f':
                            break
                        elif part_id_str.isdigit():
                            part_id = int(part_id_str)
                            if part_id in current_associated_ids:
                                print("        Este participante ya está asociado al proyecto.")
                            elif get_participant_by_id(part_id): # Verificar que el ID exista
                                if part_id not in new_participants_ids:
                                    new_participants_ids.append(part_id)
                                    print(f"        Participante {part_id} añadido provisionalmente a la lista.")
                                else:
                                    print("        Este participante ya está en la lista de los que se van a añadir.")
                            else:
                                print("        ID de participante no encontrado.")
                        else:
                            print("      Entrada inválida. Ingrese un número o 'f'.")
                    
                    if new_participants_ids:
                        add_participants_to_project(project_id, new_participants_ids)
                        project_details = get_project_by_id(project_id) # Recargar detalles para mostrar los nuevos
                    else:
                        print("No se seleccionaron nuevos participantes para añadir.")

                elif part_choice == 2:
                    print("\n    --- Remover Participantes ---")
                    participants_to_remove_ids = []
                    while True:
                        print("\nParticipantes actuales del proyecto:")
                        if not project_details.get('participantes'):
                            print("No hay participantes para remover de este proyecto.")
                            break
                        
                        for p in project_details['participantes']:
                            print(f"      ID: {p['id_participante']}, {p['tipo_participante']}: {p['nombre']} {p['apellido']}")
                        
                        part_id_str = input("      Ingrese ID de participante a remover (o 'f' para finalizar): ").strip().lower()
                        if part_id_str == 'f':
                            break
                        elif part_id_str.isdigit():
                            part_id = int(part_id_str)
                            current_associated_ids = [p['id_participante'] for p in project_details.get('participantes', [])]
                            if part_id in current_associated_ids:
                                if part_id not in participants_to_remove_ids:
                                    participants_to_remove_ids.append(part_id)
                                    print(f"        Participante {part_id} añadido provisionalmente a la lista de remoción.")
                                else:
                                    print("        Este participante ya está en la lista de los que se van a remover.")
                            else:
                                print("        Este participante no está asociado al proyecto.")
                        else:
                            print("      Entrada inválida. Ingrese un número o 'f'.")
                    
                    if participants_to_remove_ids:
                        remove_participants_from_project(project_id, participants_to_remove_ids)
                        project_details = get_project_by_id(project_id) # Recargar detalles
                    else:
                        print("No se seleccionaron participantes para remover.")

                elif part_choice == 3:
                    break # Volver a gestión de proyectos principal

        elif choice == 7:
            break # Volver al menú principal


def show_table_management_menu():
    """
    Muestra el menú de administración de tablas y maneja la navegación.
    """
    print("\n--- Administración de Tablas ---")
    table_management_options = [
        "Gestionar Usuarios",
        "Gestionar Participantes",
        "Gestionar Materias",
        "Gestionar Períodos",
        "Gestionar Proyectos",
        "Volver al Menú Principal"
    ]
    while True:
        display_menu(table_management_options)
        table_choice = get_menu_choice(len(table_management_options))

        if table_choice == 1:
            manage_users()
        elif table_choice == 2:
            manage_participants()
        elif table_choice == 3:
            manage_subjects()
        elif table_choice == 4:
            manage_periods()
        elif table_choice == 5:
            manage_projects()
        elif table_choice == 6:
            break