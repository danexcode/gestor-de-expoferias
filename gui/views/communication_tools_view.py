import tkinter as tk
from tkinter import ttk, messagebox
import os # Importar para manejar rutas de archivos
import re

# Importa las vistas
from gui.views.email_list_generator_view import EmailListGeneratorView 
from gui.base_scrollable_frame import BaseScrollableFrame 

# Ahora hereda de BaseScrollableFrame
class CommunicationToolsView(BaseScrollableFrame): 
    def __init__(self, master, app_controller_callback):
        super().__init__(master, padding="15 15 15 15") 
        self.master = master
        self.app_controller_callback = app_controller_callback
        
        self.communication_controller = self.app_controller_callback.controllers["communication_controller"]

        self.setup_ui()

    def setup_ui(self):
        self.pack(expand=True, fill='both')

        top_frame = ttk.Frame(self.scrollable_content_frame) # ¡Cambiado!
        top_frame.pack(fill=tk.X, pady=(0, 15))

        back_button = ttk.Button(top_frame, text="Volver al Dashboard",
                                 command=self.app_controller_callback.show_dashboard_view,
                                 style='TButton')
        back_button.pack(side=tk.LEFT, anchor=tk.NW, padx=0, pady=0) 

        ttk.Label(top_frame, text="Herramientas de Comunicación y Certificados",
                  font=("Arial", 22, "bold")).pack(side=tk.TOP, expand=True, fill=tk.X, pady=(0, 5))

        self.notebook = ttk.Notebook(self.scrollable_content_frame) # ¡Cambiado!
        self.notebook.pack(expand=True, fill='both', pady=10)

        # --- Pestaña para Generar Lista de Emails ---
        self.email_list_tab = ttk.Frame(self.notebook) 
        self.notebook.add(self.email_list_tab, text="Generar Lista de Emails")
        self.email_list_generator_view = EmailListGeneratorView(
            self.email_list_tab, self.app_controller_callback, self.communication_controller
        )
        self.email_list_generator_view.pack(expand=True, fill='both')

        # --- Pestaña para Generación de Certificados ---
        self.certificates_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.certificates_tab, text="Generar Certificados")
        self.setup_certificates_tab() # ¡Nuevo método para configurar esta pestaña!

    def setup_certificates_tab(self):
        """Configura los widgets para la pestaña de Generación de Certificados."""
        # Frame de filtros y acciones para certificados
        cert_controls_frame = ttk.LabelFrame(self.certificates_tab, text="Seleccionar Proyecto y Participantes", padding="10")
        cert_controls_frame.pack(fill=tk.X, pady=10)

        # Filtro de búsqueda de proyectos
        ttk.Label(cert_controls_frame, text="Buscar Proyecto:").pack(padx=5)
        self.project_search_entry = ttk.Entry(cert_controls_frame)
        self.project_search_entry.pack(expand=True, fill=tk.X, padx=5)
        self.project_search_entry.bind("<KeyRelease>", self._filter_projects_display)

        # Treeview para mostrar proyectos y sus participantes
        self.projects_tree = ttk.Treeview(self.certificates_tab, columns=("ID", "Nombre Proyecto", "Descripción", "Periodo", "Participantes"), show="headings")
        self.projects_tree.pack(fill=tk.BOTH, expand=True, pady=5)

        self.projects_tree.heading("ID", text="ID", anchor=tk.W)
        self.projects_tree.heading("Nombre Proyecto", text="Nombre Proyecto", anchor=tk.W)
        self.projects_tree.heading("Descripción", text="Descripción", anchor=tk.W)
        self.projects_tree.heading("Periodo", text="Periodo", anchor=tk.W)
        self.projects_tree.heading("Participantes", text="Participantes", anchor=tk.W)

        self.projects_tree.column("ID", width=50, stretch=tk.NO)
        self.projects_tree.column("Nombre Proyecto", width=150, stretch=tk.YES)
        self.projects_tree.column("Descripción", width=200, stretch=tk.YES)
        self.projects_tree.column("Periodo", width=100, stretch=tk.NO)
        self.projects_tree.column("Participantes", width=300, stretch=tk.YES)

        # Scrollbars para el Treeview de proyectos
        project_tree_scrollbar_y = ttk.Scrollbar(self.certificates_tab, orient="vertical", command=self.projects_tree.yview)
        project_tree_scrollbar_y.pack(side=tk.RIGHT, fill="y")
        self.projects_tree.configure(yscrollcommand=project_tree_scrollbar_y.set)

        # Vincular evento de clic para selección de proyecto
        self.projects_tree.bind("<<TreeviewSelect>>", self._on_project_select)

        # Frame para detalles del proyecto seleccionado y acciones
        selected_project_frame = ttk.LabelFrame(self.certificates_tab, text="Detalles del Proyecto y Generación", padding="10")
        selected_project_frame.pack(fill=tk.X, pady=10)

        ttk.Label(selected_project_frame, text="Proyecto Seleccionado:").pack(padx=5)
        self.selected_project_name_label = ttk.Label(selected_project_frame, text="Ninguno", font=("Arial", 12, "bold"))
        self.selected_project_name_label.pack(expand=True, fill=tk.X, padx=5)

        ttk.Label(selected_project_frame, text="Participantes Seleccionados:").pack(pady=5, anchor=tk.W)
        self.selected_participants_text = tk.Text(selected_project_frame, wrap=tk.WORD, height=4, state=tk.DISABLED)
        self.selected_participants_text.pack(fill=tk.X, pady=5)

        self.generate_certs_button = ttk.Button(selected_project_frame, text="Generar Certificados Seleccionados", 
                                                command=self._generate_selected_certificates, style='Accent.TButton')
        self.generate_certs_button.pack(pady=10)
        
        self.cert_status_label = ttk.Label(self.certificates_tab, text="", foreground="blue")
        self.cert_status_label.pack(pady=5)

        self.loaded_projects_data = [] # Para almacenar todos los proyectos cargados
        self.selected_project_id = None
        self.selected_project_name = None
        self.selected_project_participants = [] # Almacena {nombre, cedula, email}

        self._load_projects_for_certificates()


    def _load_projects_for_certificates(self):
        """Carga los proyectos en el Treeview para la generación de certificados."""
        self.projects_tree.delete(*self.projects_tree.get_children())
        self.loaded_projects_data = []
        
        projects, error = self.communication_controller.get_projects_for_certificates()
        if error:
            messagebox.showerror("Error de Carga", f"No se pudieron cargar los proyectos: {error}")
            return
        
        self.loaded_projects_data = projects
        self._display_projects(self.loaded_projects_data)

    def _display_projects(self, projects_list):
        self.projects_tree.delete(*self.projects_tree.get_children())
        for p in projects_list:
            # Mantener la cadena original del controlador aquí.
            # El Treeview la mostrará como una sola línea si la columna es ancha,
            # o el desborde horizontal si es más estrecha.
            self.projects_tree.insert("", tk.END, values=(
                p['id_proyecto'],
                p['nombre_proyecto'],
                p['descripcion'],
                p['nombre_periodo'],
                p['participantes_info'] # <-- ¡CAMBIO AQUÍ! No .replace('\n')
            ))

    def _filter_projects_display(self, event=None):
        """Filtra los proyectos visibles en el Treeview según el texto de búsqueda."""
        search_term = self.project_search_entry.get().lower()
        
        filtered_projects = []
        for p in self.loaded_projects_data:
            if search_term in str(p['nombre_proyecto']).lower() or \
               search_term in str(p['descripcion']).lower() or \
               search_term in str(p['nombre_periodo']).lower() or \
               search_term in str(p['participantes_info']).lower():
                filtered_projects.append(p)
        
        self._display_projects(filtered_projects)

    def _on_project_select(self, event):
        selected_item = self.projects_tree.focus()
        if not selected_item:
            self.selected_project_id = None
            self.selected_project_name = None
            self.selected_project_participants = []
            self.selected_project_name_label.config(text="Ninguno")
            self.selected_participants_text.config(state=tk.NORMAL)
            self.selected_participants_text.delete("1.0", tk.END)
            self.selected_participants_text.config(state=tk.DISABLED)
            return

        values = self.projects_tree.item(selected_item, 'values')
        self.selected_project_id = values[0]
        self.selected_project_name = values[1]
        self.selected_project_name_label.config(text=self.selected_project_name)

        participants_info_str = values[4] # Esta cadena ya tiene el '\n' si lo pusiste en _display_projects
        parsed_participants = []

        if participants_info_str and participants_info_str != "N/A":
            # La expresión regular debe ser más flexible para el email (puede ser un email o 'N/A')
            # Usaremos una regex que coincida con el patrón de cada participante
            # y re.findall para obtener todas las ocurrencias.
            # Capturamos: Nombre Completo, CI, Email (que puede ser 'N/A' o un email real)
            # patron_participante = re.compile(r"(.+?)\s+\(CI:\s*([\w\d]+)\s*-\s*([^)]+)\)")
            
            # Ajuste de la regex para que sea más robusta:
            # (.+?) - Captura el nombre completo (no codicioso)
            # \s+\(CI:\s* - Espacios, "(CI:", espacios
            # ([\w\d]+) - Captura la cédula (letras o dígitos, uno o más)
            # \s*-\s* - Espacios, "-", espacios
            # (?:([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})|N/A) - **GRUPO SIN CAPTURA (?:...)**
            #                                                               **Alternativa (email O N/A)**
            #                                                                  Captura un email O la cadena "N/A"
            # \) - Literal ")"
            
            # Vamos a usar una regex que capture la información dentro de los paréntesis para el email/N/A
            # y luego decodificarlo.

            # REFINAMIENTO CRÍTICO DE LA REGEX:
            # Captura 1: Nombre completo
            # Captura 2: Cédula
            # Captura 3: Contenido del email (puede ser un email real o 'N/A')
            # Usamos re.MULTILINE si la cadena de entrada del Treeview puede tener saltos de línea reales.
            # Sin embargo, el split anterior ya manejaba eso.
            # Lo más seguro es que el string `participants_info_str` venga con '\n' si así se insertó.
            # Necesitamos que la regex funcione por CADA LÍNEA del Treeview.
            
            # El problema es que values[4] ahora contiene saltos de línea si se usó .replace('; ', '\n')
            # Necesitamos que el findall trabaje sobre cada línea o que la regex sea multilínea.
            # Mejor, volvemos a hacer el split por '\n' o '; ' para procesar cada item individualmente.
            
            # La cadena participants_info_str ya tiene '\n' si se usó en _display_projects
            # Si se usó .replace('; ', '\n') en _display_projects, la cadena se verá así:
            # "Carlos Reyes (CI: 99999999 - carlos.r@example.com)\nCarlos Reyes (CI: 99999999 - carlos.r@example.com)\nJuan 2 Juan 2 (CI: 67654321 - None)"

            # Por lo tanto, el split debe ser por '\n' o por el separador original si no se hizo replace.
            # Recomiendo que en _display_projects NO se haga el .replace('\n') al insertar en Treeview,
            # y que el split sea por '; ' aquí. Así, values[4] siempre es la cadena del controlador.

            # VOLVEMOS A LA SOLUCIÓN ANTERIOR DEL CONTROLADOR Y VISTA:
            # La cadena del controlador es "PART1; PART2; PART3".
            # La columna del Treeview la muestra con \n por el _display_projects.
            # Cuando values[4] se recupera, puede que el Treeview ya haya "interpretado" los \n.
            # Es mejor parsear la cadena original del controlador.

            # Revertir la línea en _display_projects para que no cambie el string:
            # self.projects_tree.insert("", tk.END, values=(..., p['participantes_info'])) # NO participants_display

            # Y aquí en _on_project_select:
            # Usa la regex para encontrar CADA PATRÓN de participante en la cadena original
            # independientemente de si tiene '; ' o '\n'.
            
            # La regex para encontrar cada participante:
            # (.+?) => Nombre completo (cualquier cosa no codiciosa hasta el siguiente patrón)
            # \s+\(CI:\s* => Espacio, (CI:, espacio
            # ([\w\d]+) => Cédula (letras o dígitos)
            # \s*-\s* => Espacio, -, espacio
            # (.*?)\) => Email o 'N/A' o lo que sea que esté antes del paréntesis de cierre (no codicioso)
            #            (.*?): esto es crucial para capturar "None" o "N/A"
            patron_participante_robusto = re.compile(r"(.+?)\s+\(CI:\s*([\w\d]+)\s*-\s*(.*?)\)")

            # Usamos findall en la cadena completa. Esto es más robusto que split + loop + search.
            # re.findall devolverá una lista de tuplas.
            matches = patron_participante_robusto.findall(participants_info_str)

            if matches:
                for match in matches:
                    nombre_completo = match[0].strip()
                    cedula = match[1].strip()
                    email_raw = match[2].strip() # Esto puede ser un email, 'None', o 'N/A'

                    parsed_participants.append({
                        "nombre_completo": nombre_completo,
                        "cedula": cedula,
                        "email": email_raw # Guardamos el raw email para los certificados
                    })
            else:
                # Fallback si no se encuentra ningún patrón.
                # Esto es para asegurar que al menos el nombre se muestre si el formato es totalmente inesperado.
                if participants_info_str and participants_info_str != "N/A":
                    messagebox.showwarning("Advertencia de Parseo", 
                                           "No se pudieron extraer los detalles completos de los participantes. "
                                           "Mostrando nombres parciales. Verifique el formato de la DB.")
                    # Intenta dividir por el separador del controlador y mostrar nombres básicos
                    temp_parts = participants_info_str.split('; ')
                    for part in temp_parts:
                        # Extraer solo lo que parece un nombre antes del primer paréntesis
                        name_match = re.match(r"(.+?)(?:\s+\(|;|$)", part)
                        nombre_basico = name_match.group(1).strip() if name_match else part.strip()
                        parsed_participants.append({
                            "nombre_completo": nombre_basico,
                            "cedula": "N/A", # No se pudo parsear
                            "email": "N/A" # No se pudo parsear
                        })
        
        self.selected_project_participants = parsed_participants

        self.selected_participants_text.config(state=tk.NORMAL)
        self.selected_participants_text.delete("1.0", tk.END)

        # Formatear la visualización para el Text widget
        participants_display_for_text = "\n".join([f"{p['nombre_completo']} (CI: {p['cedula']})" for p in self.selected_project_participants])
        
        self.selected_participants_text.insert("1.0", participants_display_for_text)
        self.selected_participants_text.config(state=tk.DISABLED)

    def _generate_selected_certificates(self):
        """Genera certificados para los participantes del proyecto seleccionado."""
        if not self.selected_project_id:
            messagebox.showwarning("Selección Requerida", "Por favor, selecciona un proyecto para generar certificados.")
            return

        if not self.selected_project_participants:
            messagebox.showwarning("No Participantes", "El proyecto seleccionado no tiene participantes asociados para generar certificados.")
            return

        self.cert_status_label.config(text="Generando certificados...", foreground="blue")
        self.update_idletasks() # Actualiza la UI para mostrar el mensaje

        template_path = os.path.join(os.path.dirname(__file__), "..", "..", "Formato.pptx") # Ajusta esta ruta si Formato.pptx no está en la raíz del proyecto
        template_path = os.path.abspath(template_path) # Obtener la ruta absoluta

        output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "certificados_generados")
        output_dir = os.path.abspath(output_dir)

        generated_count = 0
        failed_count = 0
        failed_certs = []

        for participant in self.selected_project_participants:
            if participant['nombre_completo'] and participant['cedula']: # Asegurarse de tener los datos mínimos
                cert_path, error = self.communication_controller.generate_certificate(
                    participant_name=participant['nombre_completo'],
                    participant_ci=participant['cedula'],
                    project_name=self.selected_project_name,
                    template_path=template_path,
                    output_dir=output_dir
                )
                if cert_path:
                    generated_count += 1
                else:
                    failed_count += 1
                    failed_certs.append(f"{participant['nombre_completo']}: {error}")
            else:
                failed_count += 1
                failed_certs.append(f"{participant['nombre_completo']}: Información incompleta (Nombre o Cédula).")


        if generated_count > 0:
            messagebox.showinfo("Generación Completa", 
                                f"Se generaron {generated_count} certificado(s) exitosamente en:\n{output_dir}")
            if failed_count > 0:
                messagebox.showwarning("Errores en la Generación", 
                                       f"Fallaron {failed_count} certificado(s):\n" + "\n".join(failed_certs))
            self.cert_status_label.config(text=f"Generación completada. Creados: {generated_count}, Fallidos: {failed_count}", foreground="green")
        else:
            messagebox.showerror("Error en la Generación", 
                                  f"No se pudo generar ningún certificado. Fallaron {failed_count} certificado(s):\n" + "\n".join(failed_certs))
            self.cert_status_label.config(text="Error: No se pudo generar ningún certificado.", foreground="red")


    # Mantén los métodos existentes de email_list_generator_view que se copiaron aquí
    # (e.g., _load_periods, _load_recipients, _display_recipients, etc.)
    # Asegúrate de que esos métodos no interfieran con la nueva lógica de certificados.
    # Si estas vistas (EmailListGeneratorView y CommunicationToolsView) son completamente separadas
    # entonces los métodos de EmailListGeneratorView no deberían estar aquí, sino solo en su propia clase.
    # Solo tienes que tener cuidado de qué métodos pertenecen a qué vista.
    # Los métodos que estaban originalmente en CommunicationToolsView antes de añadir la pestaña de certificados
    # (como el back_button command, etc.) deben permanecer.
    
    # NOTA: Los métodos como _load_periods, _load_recipients, _display_recipients, etc.
    # NO DEBEN ESTAR EN CommunicationToolsView si ya están en EmailListGeneratorView.
    # Asegúrate de que EmailListGeneratorView herede correctamente de BaseScrollableFrame
    # y que estos métodos estén en EmailListGeneratorView.
    # La CommunicationToolsView solo necesita los métodos relacionados con el notebook y la pestaña de certificados.    
        self.email_list_generator_view.pack(expand=True, fill='both')

        # Pestaña para Generación de Certificados (aún vacía)
        self.certificates_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.certificates_tab, text="Generar Certificados")
        ttk.Label(self.certificates_tab, text="¡Aquí irán las opciones para generar certificados!").pack(pady=50)