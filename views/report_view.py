# views/report_view.py
import sys
import os

# Ajustar sys.path para importar modelos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar funciones de reporte y modelos auxiliares para listar opciones
from models.report_model import get_filtered_projects_report, get_filtered_participants_report
from models.period_model import get_all_periods, get_period_by_id
from models.subject_model import get_all_subjects, get_subject_by_id
from models.participant_model import get_all_participants, get_participant_by_id

# Importar utilidades de CLI (duplicadas temporalmente o desde cli_utils.py)
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

# --- Mueve show_reports() aquí y renómbrala a show_reports_menu() ---
def show_reports_menu(): # Renombrada de show_reports a show_reports_menu
    """Lógica para generar y mostrar reportes dinámicos."""
    print("\n--- Sección de Reportes ---")
    report_options = [
        "Reporte de Proyectos",
        "Reporte de Participantes",
        "Volver al Menú Principal"
    ]
    while True:
        display_menu(report_options)
        choice = get_menu_choice(len(report_options))

        if choice == 1:
            print("\n  --- Generar Reporte de Proyectos ---")
            period_id = None
            student_id = None
            teacher_id = None
            subject_id = None

            print("\nOpciones de Filtro (dejar en blanco para no aplicar filtro):")

            # Filtro por Período
            show_periods = input("¿Desea filtrar por Período? (s/n): ").strip().lower()
            if show_periods == 's':
                periods = get_all_periods()
                if periods:
                    print("\nPeríodos disponibles:")
                    for p in periods:
                        print(f"ID: {p['id_periodo']}, Nombre: {p['nombre_periodo']} ({p['fecha_inicio']} a {p['fecha_fin']})")
                    period_id_str = input("  Ingrese el ID del Período: ").strip()
                    if period_id_str.isdigit():
                        period_id = int(period_id_str)
                        if not get_period_by_id(period_id):
                            print("    ID de período no válido. No se aplicará este filtro.")
                            period_id = None
                    else:
                        print("    Entrada inválida. No se aplicará este filtro.")

            # Filtro por Materia
            show_subjects = input("¿Desea filtrar por Materia? (s/n): ").strip().lower()
            if show_subjects == 's':
                subjects = get_all_subjects()
                if subjects:
                    print("\nMaterias disponibles:")
                    for m in subjects:
                        print(f"ID: {m['id_materia']}, Código: {m['codigo_materia']}, Nombre: {m['nombre_materia']}")
                    subject_id_str = input("  Ingrese el ID de la Materia: ").strip()
                    if subject_id_str.isdigit():
                        subject_id = int(subject_id_str)
                        if not get_subject_by_id(subject_id):
                            print("    ID de materia no válido. No se aplicará este filtro.")
                            subject_id = None
                    else:
                        print("    Entrada inválida. No se aplicará este filtro.")

            # Filtro por Participante (Estudiante)
            show_students = input("¿Desea filtrar por Participante (Estudiante)? (s/n): ").strip().lower()
            if show_students == 's':
                students = [p for p in get_all_participants() if p['tipo_participante'] == 'Estudiante']
                if students:
                    print("\nEstudiantes disponibles:")
                    for s in students:
                        print(f"ID: {s['id_participante']}, Nombre: {s['nombre']} {s['apellido']} (CI: {s['cedula']})")
                    student_id_str = input("  Ingrese el ID del Estudiante: ").strip()
                    if student_id_str.isdigit():
                        student_id = int(student_id_str)
                        temp_student = get_participant_by_id(student_id)
                        if not temp_student or temp_student['tipo_participante'] != 'Estudiante':
                            print("    ID de estudiante no válido o no es un estudiante. No se aplicará este filtro.")
                            student_id = None
                    else:
                        print("    Entrada inválida. No se aplicará este filtro.")

            # Filtro por Participante (Docente)
            show_teachers = input("¿Desea filtrar por Participante (Docente)? (s/n): ").strip().lower()
            if show_teachers == 's':
                teachers = [p for p in get_all_participants() if p['tipo_participante'] == 'Docente']
                if teachers:
                    print("\nDocentes disponibles:")
                    for t in teachers:
                        print(f"ID: {t['id_participante']}, Nombre: {t['nombre']} {t['apellido']} (CI: {t['cedula']})")
                    teacher_id_str = input("  Ingrese el ID del Docente: ").strip()
                    if teacher_id_str.isdigit():
                        teacher_id = int(teacher_id_str)
                        temp_teacher = get_participant_by_id(teacher_id)
                        if not temp_teacher or temp_teacher['tipo_participante'] != 'Docente':
                            print("    ID de docente no válido o no es un docente. No se aplicará este filtro.")
                            teacher_id = None
                    else:
                        print("    Entrada inválida. No se aplicará este filtro.")

            # Llamar a la función de reporte con los filtros seleccionados
            projects = get_filtered_projects_report(
                period_id=period_id,
                student_id=student_id,
                teacher_id=teacher_id,
                subject_id=subject_id
            )

            print("\n--- RESULTADOS DEL REPORTE DE PROYECTOS ---")
            if projects:
                for proj in projects:
                    print(f"\nID Proyecto: {proj['id_proyecto']}, Nombre: {proj['nombre_proyecto']}")
                    print(f"  Descripción: {proj['descripcion']}")
                    print(f"  Período: {proj['nombre_periodo']} ({proj['periodo_inicio']} a {proj['periodo_fin']})")
                    print(f"  Materia: {proj['nombre_materia']} ({proj['codigo_materia']})")
                    print("  Participantes:")
                    if proj.get('participantes'):
                        for part in proj['participantes']:
                            print(f"    - {part['tipo_participante']}: {part['nombre']} {part['apellido']} (CI: {part['cedula']})")
                    else:
                        print("    (Sin participantes asociados)")
            else:
                print("No se encontraron proyectos con los filtros seleccionados.")

        elif choice == 2:
            print("\n  --- Generar Reporte de Participantes ---")
            period_id = None
            participant_type = None

            print("\nOpciones de Filtro (dejar en blanco para no aplicar filtro):")

            # Filtro por Período
            show_periods = input("¿Desea filtrar por Período? (s/n): ").strip().lower()
            if show_periods == 's':
                periods = get_all_periods()
                if periods:
                    print("\nPeríodos disponibles:")
                    for p in periods:
                        print(f"ID: {p['id_periodo']}, Nombre: {p['nombre_periodo']} ({p['fecha_inicio']} a {p['fecha_fin']})")
                    period_id_str = input("  Ingrese el ID del Período: ").strip()
                    if period_id_str.isdigit():
                        period_id = int(period_id_str)
                        if not get_period_by_id(period_id):
                            print("    ID de período no válido. No se aplicará este filtro.")
                            period_id = None
                    else:
                        print("    Entrada inválida. No se aplicará este filtro.")

            # Filtro por Tipo de Participante
            show_type = input("¿Desea filtrar por Tipo de Participante (Estudiante/Docente)? (s/n): ").strip().lower()
            if show_type == 's':
                while True:
                    p_type = input("  Ingrese el Tipo de Participante (Estudiante o Docente): ").strip()
                    if p_type in ['Estudiante', 'Docente']:
                        participant_type = p_type
                        break
                    else:
                        print("    Tipo de participante inválido. Debe ser 'Estudiante' o 'Docente'.")

            # Llamar a la función de reporte con los filtros seleccionados
            participants = get_filtered_participants_report(
                period_id=period_id,
                participant_type=participant_type
            )

            print("\n--- RESULTADOS DEL REPORTE DE PARTICIPANTES ---")
            if participants:
                for part in participants:
                    print(f"\nID Participante: {part['id_participante']}, Nombre: {part['nombre']} {part['apellido']}")
                    print(f"  Tipo: {part['tipo_participante']}, CI: {part['cedula']}")
                    if part['carrera']:
                        print(f"  Carrera: {part['carrera']}")
                    print(f"  Proyectos Asociados: {part['proyectos_asociados'] if part['proyectos_asociados'] else 'Ninguno'}")
            else:
                print("No se encontraron participantes con los filtros seleccionados.")

        elif choice == 3:
            break # Volver al Menú Principal