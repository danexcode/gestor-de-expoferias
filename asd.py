import tkinter as tk
from tkinter import ttk, messagebox
# Asegúrate de que tus importaciones de controladores y modelos estén aquí
# from controllers.project_controller import ProjectController
# from controllers.participant_controller import ParticipantController
# ... y cualquier otro que uses

class DataAdminView(ttk.Frame):
    def __init__(self, parent, controller, project_controller, participant_controller, period_options, subject_options):
        super().__init__(parent)
        self.controller = controller
        self.project_controller = project_controller
        self.participant_controller = participant_controller
        self.period_options = period_options  # Diccionario {nombre_periodo: id_periodo}
        self.subject_options = subject_options # Diccionario {nombre_materia: id_materia}

        # ... (resto de tu __init__ y setup de otras pestañas) ...

        self._setup_project_tab() # Llama a la configuración de la pestaña de proyectos


    # =======================================================
    # ¡NUEVO CÓDIGO! Métodos y Widgets para la Pestaña de PROYECTOS
    # =======================================================
    def _setup_project_tab(self):
        """
        Configura los widgets para la gestión de proyectos dentro de su pestaña.
        """
        # Frame principal para la organización de la pestaña
        # Usaremos un canvas con un frame interior para el scroll vertical si es necesario
        main_canvas = tk.Canvas(self.project_tab)
        main_canvas.pack(side="left", fill="both", expand=True)

        main_scrollbar = ttk.Scrollbar(self.project_tab, orient="vertical", command=main_canvas.yview)
        main_scrollbar.pack(side="right", fill="y")

        main_canvas.configure(yscrollcommand=main_scrollbar.set)
        main_canvas.bind('<Configure>', lambda e: main_canvas.configure(scrollregion = main_canvas.bbox("all")))

        # Frame que contendrá todo el contenido y se moverá dentro del canvas
        self.scrollable_frame = ttk.Frame(main_canvas)
        main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=main_canvas.winfo_width())

        # Bind para ajustar el ancho del frame desplazable cuando cambia el ancho del canvas
        self.scrollable_frame.bind("<Configure>", 
            lambda e: main_canvas.itemconfig(main_canvas.winfo_children()[0], width=e.width)
        )
        main_canvas.bind('<Configure>', lambda e: main_canvas.itemconfig(main_canvas.winfo_children()[0], width=e.width))

        # Frame para el Treeview de proyectos (parte superior)
        project_list_frame = ttk.LabelFrame(self.scrollable_frame, text="Lista de Proyectos", padding=10)
        project_list_frame.pack(fill='both', expand=True, padx=5, pady=5) # Ahora ocupa todo el ancho

        scrollbar_proj = ttk.Scrollbar(project_list_frame, orient=tk.VERTICAL)
        self.project_tree = ttk.Treeview(project_list_frame, 
                                        columns=("ID", "Período", "Materia", "Nombre", "Descripción"), 
                                        show="headings", 
                                        yscrollcommand=scrollbar_proj.set)
        scrollbar_proj.config(command=self.project_tree.yview)
        scrollbar_proj.pack(side='right', fill='y')

        self.project_tree.heading("ID", text="ID")
        self.project_tree.heading("Período", text="Período")
        self.project_tree.heading("Materia", text="Materia")
        self.project_tree.heading("Nombre", text="Nombre del Proyecto")
        self.project_tree.heading("Descripción", text="Descripción")

        self.project_tree.column("ID", width=50, stretch=tk.NO)
        self.project_tree.column("Período", width=100, stretch=tk.NO)
        self.project_tree.column("Materia", width=150, stretch=tk.NO)
        self.project_tree.column("Nombre", width=200, stretch=tk.YES)
        self.project_tree.column("Descripción", width=250, stretch=tk.YES) # Ajusta ancho según necesidades

        self.project_tree.pack(fill='both', expand=True)
        self.project_tree.bind("<<TreeviewSelect>>", self._load_project_data_to_form)

        # --- Frame para los detalles del proyecto y gestión de participantes (parte inferior) ---
        details_frame = ttk.LabelFrame(self.scrollable_frame, text="Detalles del Proyecto y Participantes", padding=10)
        # Cambiamos side='right' a 'top' (o simplemente lo omitimos, que es el predeterminado para pack)
        details_frame.pack(fill='x', padx=5, pady=5) # 'fill=x' para que se expanda horizontalmente

        # Controles para los detalles del proyecto (usamos grid aquí)
        # Creamos un frame para los inputs de proyecto para centrar mejor
        project_inputs_frame = ttk.Frame(details_frame)
        project_inputs_frame.pack(pady=5, padx=5, fill='x')

        # Usamos grid para organizar los campos de entrada
        project_inputs_frame.columnconfigure(1, weight=1) # Columna del entry/combobox expandible

        ttk.Label(project_inputs_frame, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.project_id_entry = ttk.Entry(project_inputs_frame, width=10, state='readonly')
        self.project_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew') # sticky 'ew' para expandir

        ttk.Label(project_inputs_frame, text="Nombre:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.project_name_entry = ttk.Entry(project_inputs_frame) # Ancho no fijo para que se expanda
        self.project_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(project_inputs_frame, text="Descripción:").grid(row=2, column=0, padx=5, pady=5, sticky='nw')
        self.project_description_text = tk.Text(project_inputs_frame, height=4) # Ancho no fijo
        self.project_description_text.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(project_inputs_frame, text="Período:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.project_period_combobox = ttk.Combobox(project_inputs_frame, state="readonly") # Ancho no fijo
        self.project_period_combobox.grid(row=3, column=1, padx=5, pady=5, sticky='ew')
        self.project_period_combobox['values'] = list(self.period_options.keys())

        ttk.Label(project_inputs_frame, text="Materia:").grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.project_subject_combobox = ttk.Combobox(project_inputs_frame, state="readonly") # Ancho no fijo
        self.project_subject_combobox.grid(row=4, column=1, padx=5, pady=5, sticky='ew')
        self.project_subject_combobox['values'] = list(self.subject_options.keys())

        # Frame para la gestión de participantes
        participants_management_frame = ttk.LabelFrame(details_frame, text="Gestión de Participantes", padding=10)
        # Usamos pack para que esté debajo de los inputs del proyecto
        participants_management_frame.pack(fill='both', expand=True, padx=5, pady=10)
        
        # Frame para las dos listas de participantes (estas se mantienen lado a lado)
        lists_frame = ttk.Frame(participants_management_frame)
        lists_frame.pack(fill='both', expand=True)

        # Asegurarse de que las columnas de las listas se expandan
        lists_frame.columnconfigure(0, weight=1) # Columna para available_participants_frame
        lists_frame.columnconfigure(2, weight=1) # Columna para current_participants_frame

        # Treeview para Participantes Disponibles
        available_participants_label = ttk.Label(lists_frame, text="Disponibles:")
        available_participants_label.grid(row=0, column=0, pady=2, padx=5, sticky='w')
        
        available_participants_frame = ttk.Frame(lists_frame)
        available_participants_frame.grid(row=1, column=0, fill='both', expand=True, padx=5, pady=5, sticky='nsew')
        
        scrollbar_avail = ttk.Scrollbar(available_participants_frame, orient=tk.VERTICAL)
        self.available_participants_tree = ttk.Treeview(available_participants_frame, 
                                                        columns=("ID", "Nombre", "Apellido"), 
                                                        show="headings", 
                                                        selectmode='extended', # Permite multiselección
                                                        yscrollcommand=scrollbar_avail.set)
        scrollbar_avail.config(command=self.available_participants_tree.yview)
        scrollbar_avail.pack(side='right', fill='y')
        self.available_participants_tree.heading("ID", text="ID")
        self.available_participants_tree.heading("Nombre", text="Nombre")
        self.available_participants_tree.heading("Apellido", text="Apellido")
        self.available_participants_tree.column("ID", width=40, stretch=tk.NO)
        self.available_participants_tree.column("Nombre", width=100, stretch=tk.YES)
        self.available_participants_tree.column("Apellido", width=100, stretch=tk.YES)
        self.available_participants_tree.pack(fill='both', expand=True)

        # Botones de añadir/remover entre listas (en el centro)
        buttons_middle_frame = ttk.Frame(lists_frame)
        buttons_middle_frame.grid(row=1, column=1, padx=10, sticky='ns') # Sticky 'ns' para que se estire verticalmente
        ttk.Button(buttons_middle_frame, text=">> Añadir >>", command=self._add_selected_participants).pack(pady=5)
        ttk.Button(buttons_middle_frame, text="<< Remover <<", command=self._remove_selected_participants).pack(pady=5)

        # Treeview para Participantes del Proyecto (actuales)
        current_participants_label = ttk.Label(lists_frame, text="En Proyecto:")
        current_participants_label.grid(row=0, column=2, pady=2, padx=5, sticky='w') # Ajusta columna a 2
        
        current_participants_frame = ttk.Frame(lists_frame)
        current_participants_frame.grid(row=1, column=2, fill='both', expand=True, padx=5, pady=5, sticky='nsew') # Ajusta columna a 2

        scrollbar_current = ttk.Scrollbar(current_participants_frame, orient=tk.VERTICAL)
        self.current_participants_tree = ttk.Treeview(current_participants_frame, 
                                                      columns=("ID", "Nombre", "Apellido"), 
                                                      show="headings", 
                                                      selectmode='extended', # Permite multiselección
                                                      yscrollcommand=scrollbar_current.set)
        scrollbar_current.config(command=self.current_participants_tree.yview)
        scrollbar_current.pack(side='right', fill='y')
        self.current_participants_tree.heading("ID", text="ID")
        self.current_participants_tree.heading("Nombre", text="Nombre")
        self.current_participants_tree.heading("Apellido", text="Apellido")
        self.current_participants_tree.column("ID", width=40, stretch=tk.NO)
        self.current_participants_tree.column("Nombre", width=100, stretch=tk.YES)
        self.current_participants_tree.column("Apellido", width=100, stretch=tk.YES)
        self.current_participants_tree.pack(fill='both', expand=True)

        # Almacenar los IDs de participantes para la gestión
        self.current_project_participant_ids = set() # Usaremos un set para IDs únicos
        self.all_available_participants_data = {} # {id: {data}}

        # Botones de acción para Proyectos
        buttons_frame = ttk.Frame(self.scrollable_frame) # Ahora empaca en el scrollable_frame
        buttons_frame.pack(pady=10, fill='x', padx=5) # Ajusta fila y columnspan

        ttk.Button(buttons_frame, text="Añadir Proyecto", command=self._add_project).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Editar Proyecto", command=self._edit_project).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Eliminar Proyecto", command=self._delete_project).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Limpiar Campos", command=self._clear_project_form).pack(side='left', padx=5)
    
    # ... (el resto de tus métodos como load_all_participants_for_project_selection, _sync_participant_trees, etc., permanecen igual) ...