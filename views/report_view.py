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

            # ... el resto del código de show_reports (reporte de proyectos) iría aquí ...
            # Esto incluye la lógica de pedir los filtros y llamar a get_filtered_projects_report

            # Ejemplo de la llamada final:
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

            # ... el resto del código de show_reports (reporte de participantes) iría aquí ...
            # Esto incluye la lógica de pedir los filtros y llamar a get_filtered_participants_report

            # Ejemplo de la llamada final:
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