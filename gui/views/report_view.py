# gui/views/report_view.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Importar los controladores necesarios para los filtros y para generar el reporte
from controllers.report_controller import ReportController
from controllers.period_controller import PeriodController
from controllers.subject_controller import SubjectController
from controllers.participant_controller import ParticipantController

# Importaciones para ReportLab
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch # Para el espaciado

class ReportView(ttk.Frame): 
    """
    Vista para la generación de reportes dinámicos.
    Permite al usuario seleccionar filtros y ver los resultados en una tabla.
    """
    def __init__(self, master, app_controller_callback):
        super().__init__(master, padding="15 15 15 15")
        self.master = master
        self.app_controller_callback = app_controller_callback

        self.report_controller = self.app_controller_callback.controllers["report_controller"]
        self.period_controller = self.app_controller_callback.controllers["period_controller"]
        self.subject_controller = self.app_controller_callback.controllers["subject_controller"]
        self.participant_controller = self.app_controller_callback.controllers["participant_controller"]

        self.selected_report_type = tk.StringVar(self) 
        self.selected_report_type.set("Proyectos") 

        self.filter_period_id = tk.StringVar(self)
        self.filter_subject_id = tk.StringVar(self)
        self.filter_student_id = tk.StringVar(self)
        self.filter_teacher_id = tk.StringVar(self)
        self.filter_participant_type = tk.StringVar(self) 

        self.period_names_to_ids = {} 
        self.subject_names_to_ids = {} 
        self.participant_names_to_ids = {} 

        self.results_frame = None 
        self.report_tree = None
        self.tree_scrollbar_y = None
        self.tree_scrollbar_x = None

        self.setup_ui()
        self._load_filter_options() 

    def setup_ui(self):
        """Configura la interfaz de usuario de la vista de reportes."""
        self.pack(expand=True, fill='both')

        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, pady=(0, 15))

        back_button = ttk.Button(top_frame, text="Volver al Dashboard",
                                 command=self.app_controller_callback.show_dashboard_view,
                                 style='TButton')
        back_button.pack(side=tk.LEFT, anchor=tk.NW, padx=0, pady=0) 

        ttk.Label(top_frame, text="Generación de Reportes",
                  font=("Arial", 22, "bold")).pack(side=tk.TOP, expand=True, fill=tk.X, pady=(0, 5))

        report_type_frame = ttk.LabelFrame(self, text="Seleccionar Tipo de Reporte", padding="10 10 10 10")
        report_type_frame.pack(fill=tk.X, pady=10)

        ttk.Radiobutton(report_type_frame, text="Reporte de Proyectos", variable=self.selected_report_type,
                        value="Proyectos", command=self._toggle_filters).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(report_type_frame, text="Reporte de Participantes", variable=self.selected_report_type,
                        value="Participantes", command=self._toggle_filters).pack(side=tk.LEFT, padx=10)

        self.filter_options_frame = ttk.LabelFrame(self, text="Opciones de Filtro", padding="10 10 10 10")
        self.filter_options_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.project_filters_frame = ttk.Frame(self.filter_options_frame)
        self.project_filters_frame.pack(fill=tk.BOTH, expand=True) 
        self._setup_project_filters(self.project_filters_frame)

        self.participant_filters_frame = ttk.Frame(self.filter_options_frame)
        self._setup_participant_filters(self.participant_filters_frame)
        
        # Frame para los botones de acción (Generar y Exportar)
        action_buttons_frame = ttk.Frame(self)
        action_buttons_frame.pack(pady=15)

        ttk.Button(action_buttons_frame, text="Generar Reporte", command=self._generate_report_button_click).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_buttons_frame, text="Exportar a PDF", command=self._export_to_pdf_button_click).pack(side=tk.LEFT, padx=5)

        self.results_frame = ttk.LabelFrame(self, text="Resultado del Reporte", padding="10 10 10 10")
        self.results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self._create_report_treeview() 

        self.status_label = ttk.Label(self, text="", foreground="red")
        self.status_label.pack(pady=5)

        self._toggle_filters() 

    def _create_report_treeview(self):
        """Crea y empaqueta un nuevo Treeview con sus scrollbars."""
        if self.report_tree:
            self.report_tree.destroy()
        if self.tree_scrollbar_y:
            self.tree_scrollbar_y.destroy()
        if self.tree_scrollbar_x:
            self.tree_scrollbar_x.destroy()

        self.report_tree = ttk.Treeview(self.results_frame, show="headings")
        self.report_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tree_scrollbar_y = ttk.Scrollbar(self.results_frame, orient="vertical", command=self.report_tree.yview)
        self.tree_scrollbar_y.pack(side=tk.RIGHT, fill="y")
        self.report_tree.configure(yscrollcommand=self.tree_scrollbar_y.set)

        self.tree_scrollbar_x = ttk.Scrollbar(self.results_frame, orient="horizontal", command=self.report_tree.xview)
        self.tree_scrollbar_x.pack(side=tk.BOTTOM, fill="x")
        self.report_tree.configure(xscrollcommand=self.tree_scrollbar_x.set)

    def _setup_project_filters(self, parent_frame):
        # Filtro por Período
        ttk.Label(parent_frame, text="Período:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.period_combobox = ttk.Combobox(parent_frame, textvariable=self.filter_period_id, state="readonly")
        self.period_combobox.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        self.period_combobox.set("--- Seleccionar ---")

        # Filtro por Materia
        ttk.Label(parent_frame, text="Materia:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.subject_combobox = ttk.Combobox(parent_frame, textvariable=self.filter_subject_id, state="readonly")
        self.subject_combobox.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        self.subject_combobox.set("--- Seleccionar ---")

        # Filtro por Estudiante
        ttk.Label(parent_frame, text="Estudiante:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.student_combobox = ttk.Combobox(parent_frame, textvariable=self.filter_student_id, state="readonly")
        self.student_combobox.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)
        self.student_combobox.set("--- Seleccionar ---")

        # Filtro por Docente
        ttk.Label(parent_frame, text="Docente:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.teacher_combobox = ttk.Combobox(parent_frame, textvariable=self.filter_teacher_id, state="readonly")
        self.teacher_combobox.grid(row=3, column=1, padx=5, pady=5, sticky=tk.EW)
        self.teacher_combobox.set("--- Seleccionar ---")

        parent_frame.columnconfigure(1, weight=1)

    def _setup_participant_filters(self, parent_frame):
        # Filtro por Período
        ttk.Label(parent_frame, text="Período:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.participant_period_combobox = ttk.Combobox(parent_frame, textvariable=self.filter_period_id, state="readonly")
        self.participant_period_combobox.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        self.participant_period_combobox.set("--- Seleccionar ---")

        # Filtro por Tipo de Participante
        ttk.Label(parent_frame, text="Tipo de Participante:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Radiobutton(parent_frame, text="Estudiante", variable=self.filter_participant_type, value="Estudiante").grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Radiobutton(parent_frame, text="Docente", variable=self.filter_participant_type, value="Docente").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        ttk.Radiobutton(parent_frame, text="Todos", variable=self.filter_participant_type, value="").grid(row=1, column=3, padx=5, pady=5, sticky=tk.W) 
        self.filter_participant_type.set("") 

        parent_frame.columnconfigure(1, weight=1)

    def _load_filter_options(self):
        # Cargar períodos
        periods, error = self.period_controller.get_all_system_periods()
        if not error:
            period_names = ["--- Seleccionar ---"]
            self.period_names_to_ids = {"--- Seleccionar ---": None}
            for p in periods:
                name = p['nombre_periodo']
                period_names.append(name)
                self.period_names_to_ids[name] = p['id_periodo']
            self.period_combobox['values'] = period_names
            self.participant_period_combobox['values'] = period_names
        else:
            messagebox.showerror("Error de Carga", f"No se pudieron cargar periodos: {error}")

        # Cargar materias
        subjects, error = self.subject_controller.get_all_system_subjects()
        if not error:
            subject_names = ["--- Seleccionar ---"]
            self.subject_names_to_ids = {"--- Seleccionar ---": None}
            for s in subjects:
                name = f"{s['nombre_materia']} ({s['codigo_materia']})"
                subject_names.append(name)
                self.subject_names_to_ids[name] = s['id_materia']
            self.subject_combobox['values'] = subject_names
        else:
            messagebox.showerror("Error de Carga", f"No se pudieron cargar materias: {error}")

        # Cargar participantes (para filtros de estudiante/docente)
        participants, error = self.participant_controller.get_all_system_participants()
        if not error:
            student_names = ["--- Seleccionar ---"]
            teacher_names = ["--- Seleccionar ---"]
            self.participant_names_to_ids = {"--- Seleccionar ---": None}
            
            for p in participants:
                full_name = f"{p['nombre']} {p['apellido']} (CI: {p['cedula']})"
                self.participant_names_to_ids[full_name] = p['id_participante']
                if p['tipo_participante'] == 'Estudiante':
                    student_names.append(full_name)
                elif p['tipo_participante'] == 'Docente':
                    teacher_names.append(full_name)
            
            self.student_combobox['values'] = student_names
            self.teacher_combobox['values'] = teacher_names
        else:
            messagebox.showerror("Error de Carga", f"No se pudieron cargar participantes: {error}")

    def _toggle_filters(self):
        report_type = self.selected_report_type.get()
        
        self.project_filters_frame.pack_forget()
        self.participant_filters_frame.pack_forget()

        self._clear_filter_selections()

        if report_type == "Proyectos":
            self.project_filters_frame.pack(fill=tk.BOTH, expand=True)
        elif report_type == "Participantes":
            self.participant_filters_frame.pack(fill=tk.BOTH, expand=True)

        self.update_idletasks()
        self.master.update_idletasks()

    def _clear_filter_selections(self):
        self.filter_period_id.set("--- Seleccionar ---")
        self.filter_subject_id.set("--- Seleccionar ---")
        self.filter_student_id.set("--- Seleccionar ---")
        self.filter_teacher_id.set("--- Seleccionar ---")
        self.filter_participant_type.set("") 

    def _generate_report_button_click(self):
        self.status_label.config(text="") 
        
        self._create_report_treeview() 
        
        report_type = self.selected_report_type.get()

        if report_type == "Proyectos":
            self._generate_projects_report()
        elif report_type == "Participantes":
            self._generate_participants_report()

    def _generate_projects_report(self):
        period_name = self.filter_period_id.get()
        period_id = self.period_names_to_ids.get(period_name)

        subject_name = self.filter_subject_id.get()
        subject_id = self.subject_names_to_ids.get(subject_name)

        student_name = self.filter_student_id.get()
        student_id = self.participant_names_to_ids.get(student_name)

        teacher_name = self.filter_teacher_id.get()
        teacher_id = self.participant_names_to_ids.get(teacher_name)
        
        projects, error = self.report_controller.generate_projects_report(
            period_id=period_id,
            student_id=student_id,
            teacher_id=teacher_id,
            subject_id=subject_id
        )

        if error:
            self.status_label.config(text=f"Error al generar reporte: {error}", foreground="red")
            messagebox.showerror("Error de Reporte", error)
        else:
            self._display_projects_report(projects)
            self.status_label.config(text=f"Reporte de Proyectos generado. Encontrados {len(projects)} proyectos.", foreground="green")

    def _display_projects_report(self, projects):
        """Muestra los resultados del reporte de proyectos en el Treeview."""
        columns = ("ID", "Nombre", "Descripción", "Período", "Materia", "Participantes")
        self.report_tree["columns"] = columns
        self.report_tree["displaycolumns"] = columns 

        self.report_tree.heading("ID", text="ID", anchor=tk.W)
        self.report_tree.heading("Nombre", text="Nombre del Proyecto", anchor=tk.W)
        self.report_tree.heading("Descripción", text="Descripción", anchor=tk.W)
        self.report_tree.heading("Período", text="Período", anchor=tk.W)
        self.report_tree.heading("Materia", text="Materia", anchor=tk.W)
        self.report_tree.heading("Participantes", text="Participantes", anchor=tk.W)

        self.report_tree.column("ID", width=50, stretch=tk.NO)
        self.report_tree.column("Nombre", width=200, stretch=tk.YES)
        self.report_tree.column("Descripción", width=300, stretch=tk.YES)
        self.report_tree.column("Período", width=150, stretch=tk.NO)
        self.report_tree.column("Materia", width=150, stretch=tk.NO)
        self.report_tree.column("Participantes", width=250, stretch=tk.YES)

        if projects: 
            for proj in projects:
                participants_str = ", ".join([f"{p['nombre']} {p['apellido']} ({p['tipo_participante'][0]})" for p in proj.get('participantes', [])])
                self.report_tree.insert("", tk.END, values=(
                    proj['id_proyecto'],
                    proj['nombre_proyecto'],
                    proj['descripcion'],
                    f"{proj['nombre_periodo']} ({proj['periodo_inicio'].strftime('%Y-%m-%d')} a {proj['periodo_fin'].strftime('%Y-%m-%d')})",
                    f"{proj['nombre_materia']} ({proj['codigo_materia']})",
                    participants_str
                ))
        else:
            self.report_tree.insert("", tk.END, values=("", "", "No se encontraron proyectos para los filtros seleccionados.", "", "", ""))
            self.report_tree.item(self.report_tree.get_children()[-1], tags=('no_data_message',))
            try:
                self.report_tree.tag_configure('no_data_message', background='lightyellow', foreground='gray')
            except tk.TclError:
                pass 
            self.status_label.config(text="No se encontraron proyectos.", foreground="orange")


    def _generate_participants_report(self):
        period_name = self.filter_period_id.get()
        period_id = self.period_names_to_ids.get(period_name)

        participant_type = self.filter_participant_type.get()
        if participant_type == "": 
            participant_type = None

        participants, error = self.report_controller.generate_participants_report(
            period_id=period_id,
            participant_type=participant_type
        )

        if error:
            self.status_label.config(text=f"Error al generar reporte: {error}", foreground="red")
            messagebox.showerror("Error de Reporte", error)
        else:
            self._display_participants_report(participants)
            self.status_label.config(text=f"Reporte de Participantes generado. Encontrados {len(participants)} participantes.", foreground="green")


    def _display_participants_report(self, participants):
        """Muestra los resultados del reporte de participantes en el Treeview."""
        columns = ("ID", "Nombre Completo", "CI", "Tipo", "Carrera", "Proyectos Asociados")
        self.report_tree["columns"] = columns
        self.report_tree["displaycolumns"] = columns

        self.report_tree.heading("ID", text="ID", anchor=tk.W)
        self.report_tree.heading("Nombre Completo", text="Nombre Completo", anchor=tk.W)
        self.report_tree.heading("CI", text="Cédula", anchor=tk.W)
        self.report_tree.heading("Tipo", text="Tipo", anchor=tk.W)
        self.report_tree.heading("Carrera", text="Carrera", anchor=tk.W)
        self.report_tree.heading("Proyectos Asociados", text="Proyectos Asociados", anchor=tk.W)

        self.report_tree.column("ID", width=50, stretch=tk.NO)
        self.report_tree.column("Nombre Completo", width=180, stretch=tk.YES)
        self.report_tree.column("CI", width=100, stretch=tk.NO)
        self.report_tree.column("Tipo", width=100, stretch=tk.NO)
        self.report_tree.column("Carrera", width=150, stretch=tk.YES)
        self.report_tree.column("Proyectos Asociados", width=300, stretch=tk.YES)

        if participants: 
            for part in participants:
                self.report_tree.insert("", tk.END, values=(
                    part['id_participante'],
                    f"{part['nombre']} {part['apellido']}",
                    part['cedula'],
                    part['tipo_participante'],
                    part['carrera'] if part['carrera'] else "N/A",
                    part['proyectos_asociados'] if part['proyectos_asociados'] else "Ninguno"
                ))
        else:
            self.report_tree.insert("", tk.END, values=("", "", "No se encontraron participantes para los filtros seleccionados.", "", "", ""))
            self.report_tree.item(self.report_tree.get_children()[-1], tags=('no_data_message',))
            try:
                self.report_tree.tag_configure('no_data_message', background='lightyellow', foreground='gray')
            except tk.TclError:
                pass 
            self.status_label.config(text="No se encontraron participantes.", foreground="orange")

    def _export_to_pdf_button_click(self):
        """
        Maneja el clic en el botón 'Exportar a PDF'.
        Recopila los datos del Treeview y los exporta a un archivo PDF.
        """
        # Obtener los encabezados de las columnas visibles
        columns = [self.report_tree.heading(col, "text") for col in self.report_tree["displaycolumns"]]
        
        # Obtener los datos de las filas
        data = []
        for item_id in self.report_tree.get_children():
            # Filtrar el mensaje de "No se encontraron datos"
            row_values = self.report_tree.item(item_id, 'values')
            if row_values and "No se encontraron" in str(row_values[0]): # Asumo que el mensaje está en la primera columna
                continue
            data.append(row_values)
        
        if not data:
            messagebox.showinfo("Exportar a PDF", "No hay datos para exportar al PDF.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
            title="Guardar Reporte como PDF"
        )

        if not file_path:
            return # El usuario canceló la operación

        try:
            doc = SimpleDocTemplate(file_path, pagesize=A4)
            styles = getSampleStyleSheet()
            
            # Definir un estilo para los párrafos dentro de las celdas
            # Este estilo permite que el texto se envuelva automáticamente
            cell_style = ParagraphStyle(
                'CellBodyText',
                parent=styles['Normal'],
                fontSize=8, # Un tamaño de fuente un poco más pequeño para tablas densas
                leading=10, # Espaciado entre líneas
                wordWrap='CJK', # Asegura que palabras largas sin espacios se rompan (útil para URLs, etc.)
                alignment=0, # TA_LEFT
            )

            # Preparar los datos de la tabla, envolviendo el texto largo en Paragraphs
            processed_data = []
            
            # Añadir encabezados
            processed_data.append([Paragraph(header, styles['h4']) for header in columns]) # Encabezados también como Paragraphs
            
            report_type = self.selected_report_type.get()

            for row_values in data:
                current_row = []
                # Para cada columna, decidimos si usar Paragraph o una cadena simple
                if report_type == "Proyectos":
                    # Columns: "ID", "Nombre", "Descripción", "Período", "Materia", "Participantes"
                    # ID: Texto simple
                    current_row.append(str(row_values[0])) 
                    # Nombre: Puede ser largo
                    current_row.append(Paragraph(str(row_values[1]), cell_style))
                    # Descripción: Larga
                    current_row.append(Paragraph(str(row_values[2]), cell_style))
                    # Período: Moderado
                    current_row.append(Paragraph(str(row_values[3]), cell_style))
                    # Materia: Moderado
                    current_row.append(Paragraph(str(row_values[4]), cell_style))
                    # Participantes: Muy largo
                    current_row.append(Paragraph(str(row_values[5]), cell_style))
                elif report_type == "Participantes":
                    # Columns: "ID", "Nombre Completo", "CI", "Tipo", "Carrera", "Proyectos Asociados"
                    # ID: Texto simple
                    current_row.append(str(row_values[0]))
                    # Nombre Completo: Moderado
                    current_row.append(Paragraph(str(row_values[1]), cell_style))
                    # CI: Texto simple
                    current_row.append(str(row_values[2]))
                    # Tipo: Texto simple
                    current_row.append(str(row_values[3]))
                    # Carrera: Moderado
                    current_row.append(Paragraph(str(row_values[4]), cell_style))
                    # Proyectos Asociados: Muy largo
                    current_row.append(Paragraph(str(row_values[5]), cell_style))
                
                processed_data.append(current_row)

            # Título del reporte
            title_text = f"Reporte de {report_type}"
            title = Paragraph(title_text, styles['h1'])

            # Configurar el estilo de la tabla
            table = Table(processed_data) # Usar los datos procesados con Paragraphs
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#666666')), # Encabezado más oscuro
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F5F5F5')), # Filas de datos
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0,0), (-1,-1), 'TOP'), # Alinear contenido al TOP para mejor lectura
                # No necesitamos 'WORDWRAP' en TableStyle si usamos Paragraphs
            ]))

            # Ajustar el ancho de las columnas manualmente para un mejor control
            # Estos anchos son ejemplos y deben ser ajustados según tus datos reales
            # Suma de anchos debe ser <= (A4[0] - 2 * inch)
            available_width = A4[0] - 2 * inch # Ancho de página - márgenes (aprox 595 - 72 - 72 = 451 puntos)

            if report_type == "Proyectos":
                # Anchos en puntos (1 pulgada = 72 puntos)
                # ID, Nombre, Descripción, Período, Materia, Participantes
                # 50, 100, 150, 80, 80, 150 -> Suma = 610, muy grande
                # Ajustando a un total de ~450 puntos
                table._argW = [
                    0.5 * inch,  # ID (36 pts)
                    1.2 * inch,  # Nombre del Proyecto (86.4 pts)
                    1.8 * inch,  # Descripción (129.6 pts)
                    1.0 * inch,  # Período (72 pts)
                    1.0 * inch,  # Materia (72 pts)
                    2.0 * inch   # Participantes (144 pts)
                ]
            elif report_type == "Participantes":
                # Anchos en puntos
                # ID, Nombre Completo, CI, Tipo, Carrera, Proyectos Asociados
                table._argW = [
                    0.5 * inch,  # ID (36 pts)
                    1.5 * inch,  # Nombre Completo (108 pts)
                    0.8 * inch,  # CI (57.6 pts)
                    0.8 * inch,  # Tipo (57.6 pts)
                    1.2 * inch,  # Carrera (86.4 pts)
                    2.2 * inch   # Proyectos Asociados (158.4 pts)
                ]
            
            # Asegúrate de que la suma de los anchos de columna no exceda el ancho disponible
            # Si excede, ReportLab podría lanzar un error o generar un PDF mal formado.
            # Puedes imprimir sum(table._argW) y available_width para depurar.

            elements = [title, Spacer(1, 0.2*inch), table] # Añadir un espacio después del título
            doc.build(elements)

            messagebox.showinfo("Exportar a PDF", f"Reporte exportado exitosamente a:\n{file_path}")
            self.status_label.config(text=f"Reporte exportado a PDF: {file_path}", foreground="green")

        except Exception as e:
            messagebox.showerror("Error de Exportación", f"Ocurrió un error al exportar el reporte a PDF:\n{e}")
            self.status_label.config(text=f"Error al exportar a PDF: {e}", foreground="red")