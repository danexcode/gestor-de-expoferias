# gui/views/data_admin_view.py
import tkinter as tk
from tkinter import ttk, messagebox
import sys
from datetime import datetime # ¡NUEVA IMPORTACIÓN! para manejar fechas en la vista

# Importar los controladores necesarios
from controllers.user_controller import UserController
from controllers.participant_controller import ParticipantController
from controllers.subject_controller import SubjectController
from controllers.period_controller import PeriodController # ¡NUEVA IMPORTACIÓN!
# from controllers.project_controller import ProjectController


class DataAdminView(tk.Frame):
    """
    Vista para la administración de datos de la aplicación.
    Permite a los usuarios gestionar usuarios, participantes, materias, periodos y proyectos
    a través de un sistema de pestañas (Notebook).
    """
    def __init__(self, master, app_controller_callback, user_role=None):
        super().__init__(master)
        self.master = master
        self.app_controller_callback = app_controller_callback
        self.user_role = user_role

        # Inicializar controladores
        self.user_controller = UserController()
        self.participant_controller = ParticipantController()
        self.subject_controller = SubjectController()
        self.period_controller = PeriodController() # ¡NUEVA INSTANCIA DEL CONTROLADOR!
        # self.project_controller = ProjectController()

        self.setup_ui()
        self.load_user_data() # Cargar datos de usuarios al inicio

        # Añadir listener para cuando se cambia de pestaña
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_change)

    def setup_ui(self):
        """
        Configura la interfaz de usuario con un Notebook (pestañas) para cada entidad.
        """
        self.pack(expand=True, fill='both', padx=10, pady=10)

        # Título de la vista
        ttk.Label(self, text="Administración de Datos del Sistema", 
                  font=("Arial", 20, "bold")).pack(pady=15)

        # Crear el Notebook (sistema de pestañas)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)

        # --- Pestaña de Usuarios ---
        self.user_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.user_tab, text="Usuarios")
        self._setup_user_tab()

        # --- Pestaña de Participantes ---
        self.participant_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.participant_tab, text="Participantes")
        self._setup_participant_tab()

        # --- Pestaña de Materias ---
        self.subject_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.subject_tab, text="Materias")
        self._setup_subject_tab()

        # --- Pestaña de Periodos ¡MODIFICACIÓN! ---
        self.period_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.period_tab, text="Periodos")
        self._setup_period_tab() # ¡Llamar a la configuración de periodos!

        # --- Pestaña de Proyectos (Placeholder) ---
        self.project_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.project_tab, text="Proyectos")
        ttk.Label(self.project_tab, text="Gestión de Proyectos (próximamente)").pack(pady=50)

        # Botón para volver al Dashboard (fuera de las pestañas)
        back_button = ttk.Button(self, text="Volver al Dashboard", 
                                 command=self.app_controller_callback.show_dashboard_view,
                                 style='TButton')
        back_button.pack(pady=10)

    def _on_tab_change(self, event):
        """
        Maneja el evento de cambio de pestaña en el Notebook.
        Carga los datos de la pestaña activa.
        """
        selected_tab = self.notebook.tab(self.notebook.select(), "text")
        if selected_tab == "Usuarios":
            self.load_user_data()
        elif selected_tab == "Participantes":
            self.load_participant_data()
        elif selected_tab == "Materias":
            self.load_subject_data() 
        elif selected_tab == "Periodos": # ¡NUEVO!
            self.load_period_data()
        # Añade aquí la carga de datos para otras pestañas

    # =======================================================
    # Métodos y Widgets para la Pestaña de USUARIOS (sin cambios)
    # =======================================================
    def _setup_user_tab(self):
        # ... (Tu código de la pestaña de usuarios) ...
        pass

    def load_user_data(self):
        # ... (Tu código de carga de usuarios) ...
        pass

    def _load_user_data_to_form(self, event):
        # ... (Tu código de carga de datos a formulario de usuarios) ...
        pass

    def _clear_user_form(self):
        # ... (Tu código de limpieza de formulario de usuarios) ...
        pass

    def _add_user(self):
        # ... (Tu código de añadir usuario) ...
        pass

    def _edit_user(self):
        # ... (Tu código de editar usuario) ...
        pass

    def _delete_user(self):
        # ... (Tu código de eliminar usuario) ...
        pass


    # =======================================================
    # Métodos y Widgets para la Pestaña de PARTICIPANTES (sin cambios)
    # =======================================================
    def _setup_participant_tab(self):
        # ... (Tu código de la pestaña de participantes) ...
        pass

    def load_participant_data(self):
        # ... (Tu código de carga de participantes) ...
        pass

    def _load_participant_data_to_form(self, event):
        # ... (Tu código de carga de datos a formulario de participantes) ...
        pass

    def _clear_participant_form(self):
        # ... (Tu código de limpieza de formulario de participantes) ...
        pass

    def _add_participant(self):
        # ... (Tu código de añadir participante) ...
        pass

    def _edit_participant(self):
        # ... (Tu código de editar participante) ...
        pass

    def _delete_participant(self):
        # ... (Tu código de eliminar participante) ...
        pass

    # =======================================================
    # Métodos y Widgets para la Pestaña de MATERIAS (sin cambios)
    # =======================================================
    def _setup_subject_tab(self):
        # ... (Tu código de la pestaña de materias) ...
        pass

    def load_subject_data(self):
        # ... (Tu código de carga de materias) ...
        pass

    def _load_subject_data_to_form(self, event):
        # ... (Tu código de carga de datos a formulario de materias) ...
        pass

    def _clear_subject_form(self):
        # ... (Tu código de limpieza de formulario de materias) ...
        pass

    def _add_subject(self):
        # ... (Tu código de añadir materia) ...
        pass

    def _edit_subject(self):
        # ... (Tu código de editar materia) ...
        pass

    def _delete_subject(self):
        # ... (Tu código de eliminar materia) ...
        pass

    # =======================================================
    # ¡NUEVO CÓDIGO! Métodos y Widgets para la Pestaña de PERIODOS
    # =======================================================
    def _setup_period_tab(self):
        """
        Configura los widgets para la gestión de períodos dentro de su pestaña.
        """
        # Frame superior para el Treeview de la lista de períodos
        tree_frame = ttk.Frame(self.period_tab)
        tree_frame.pack(pady=10, fill='both', expand=True)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        self.period_tree = ttk.Treeview(tree_frame, 
                                        columns=("ID", "Nombre", "Fecha Inicio", "Fecha Fin", "Activo"), 
                                        show="headings", 
                                        yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.period_tree.yview)
        scrollbar.pack(side='right', fill='y')

        # Definir encabezados de las columnas (basado en tu esquema 'periodos')
        self.period_tree.heading("ID", text="ID")
        self.period_tree.heading("Nombre", text="Nombre del Período")
        self.period_tree.heading("Fecha Inicio", text="Fecha de Inicio")
        self.period_tree.heading("Fecha Fin", text="Fecha de Fin")
        self.period_tree.heading("Activo", text="Activo")

        # Configurar anchos de columna (ajusta según necesites)
        self.period_tree.column("ID", width=50, stretch=tk.NO)
        self.period_tree.column("Nombre", width=200, stretch=tk.YES)
        self.period_tree.column("Fecha Inicio", width=120, stretch=tk.NO)
        self.period_tree.column("Fecha Fin", width=120, stretch=tk.NO)
        self.period_tree.column("Activo", width=70, stretch=tk.NO, anchor=tk.CENTER)

        self.period_tree.pack(fill='both', expand=True)

        # Vincular el evento de selección en el Treeview
        self.period_tree.bind("<<TreeviewSelect>>", self._load_period_data_to_form)

        # Frame inferior para los formularios de entrada y botones de acción
        input_frame = ttk.LabelFrame(self.period_tab, text="Detalles del Período", padding=15)
        input_frame.pack(pady=20, fill='x', expand=False) 

        # Campos de entrada
        # Fila 1
        ttk.Label(input_frame, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.period_id_entry = ttk.Entry(input_frame, width=10, state='readonly')
        self.period_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(input_frame, text="Nombre:").grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.period_name_entry = ttk.Entry(input_frame, width=30)
        self.period_name_entry.grid(row=0, column=3, padx=5, pady=5, sticky='w', columnspan=2)

        # Fila 2
        ttk.Label(input_frame, text="Fecha Inicio (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.period_start_date_entry = ttk.Entry(input_frame, width=20)
        self.period_start_date_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(input_frame, text="Fecha Fin (YYYY-MM-DD):").grid(row=1, column=2, padx=5, pady=5, sticky='w')
        self.period_end_date_entry = ttk.Entry(input_frame, width=20)
        self.period_end_date_entry.grid(row=1, column=3, padx=5, pady=5, sticky='w')

        ttk.Label(input_frame, text="Activo:").grid(row=1, column=4, padx=5, pady=5, sticky='w')
        self.period_activo_var = tk.BooleanVar(value=True) 
        self.period_activo_checkbutton = ttk.Checkbutton(input_frame, text="Sí", variable=self.period_activo_var)
        self.period_activo_checkbutton.grid(row=1, column=5, padx=5, pady=5, sticky='w')

        # Botones de acción para Períodos
        buttons_frame = ttk.Frame(self.period_tab)
        buttons_frame.pack(pady=10)

        ttk.Button(buttons_frame, text="Añadir Período", command=self._add_period).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Editar Período", command=self._edit_period).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Eliminar Período", command=self._delete_period).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Limpiar Campos", command=self._clear_period_form).pack(side='left', padx=5)

    def load_period_data(self):
        """
        Carga los datos de los períodos desde el controlador y los muestra en el Treeview.
        """
        for item in self.period_tree.get_children():
            self.period_tree.delete(item)
        
        periods, error = self.period_controller.get_all_system_periods()
        if error:
            messagebox.showerror("Error de Carga", f"No se pudieron cargar los períodos: {error}")
            return

        for p in periods:
            # Asegurarse de que las fechas sean objetos date y formatearlas si no lo son
            start_date_str = p['fecha_inicio'].isoformat() if isinstance(p['fecha_inicio'], datetime) or isinstance(p['fecha_inicio'], type(datetime.now().date())) else str(p['fecha_inicio'])
            end_date_str = p['fecha_fin'].isoformat() if isinstance(p['fecha_fin'], datetime) or isinstance(p['fecha_fin'], type(datetime.now().date())) else str(p['fecha_fin'])

            self.period_tree.insert("", "end", values=(
                p.get('id_periodo'), 
                p.get('nombre_periodo'), 
                start_date_str, 
                end_date_str,
                "Sí" if p.get('activo') else "No"
            ))

    def _load_period_data_to_form(self, event):
        """
        Carga los datos de un período seleccionado en el Treeview a los campos del formulario.
        """
        selected_item = self.period_tree.focus()
        if not selected_item:
            self._clear_period_form()
            return

        values = self.period_tree.item(selected_item, 'values')
        if values:
            self.period_id_entry.config(state='normal')

            self.period_id_entry.delete(0, tk.END)
            self.period_name_entry.delete(0, tk.END)
            self.period_start_date_entry.delete(0, tk.END)
            self.period_end_date_entry.delete(0, tk.END)

            self.period_id_entry.insert(0, values[0])
            self.period_name_entry.insert(0, values[1])
            self.period_start_date_entry.insert(0, values[2])
            self.period_end_date_entry.insert(0, values[3])
            self.period_activo_var.set(values[4] == "Sí")

            self.period_id_entry.config(state='readonly')

    def _clear_period_form(self):
        """
        Limpia todos los campos del formulario de período.
        """
        self.period_tree.selection_remove(self.period_tree.selection())
        
        self.period_id_entry.config(state='normal')
        self.period_id_entry.delete(0, tk.END)
        self.period_name_entry.delete(0, tk.END)
        self.period_start_date_entry.delete(0, tk.END)
        self.period_end_date_entry.delete(0, tk.END)
        self.period_activo_var.set(True)
        self.period_id_entry.config(state='readonly')

    def _add_period(self):
        """
        Maneja la adición de un nuevo período.
        """
        nombre_periodo = self.period_name_entry.get().strip()
        fecha_inicio_str = self.period_start_date_entry.get().strip()
        fecha_fin_str = self.period_end_date_entry.get().strip()
        activo = self.period_activo_var.get()

        if not all([nombre_periodo, fecha_inicio_str, fecha_fin_str]):
            messagebox.showerror("Error de Entrada", "Nombre, fecha de inicio y fecha de fin son obligatorios.")
            return

        # El controlador ya maneja la conversión de fecha y las validaciones
        period_id, error = self.period_controller.add_new_period(
            nombre_periodo, fecha_inicio_str, fecha_fin_str, activo
        )
        if period_id:
            messagebox.showinfo("Éxito", f"Período '{nombre_periodo}' añadido con ID: {period_id}")
            self.load_period_data()
            self._clear_period_form()
        else:
            messagebox.showerror("Error al Añadir Período", error)

    def _edit_period(self):
        """
        Maneja la edición de un período existente.
        """
        period_id_str = self.period_id_entry.get()
        if not period_id_str:
            messagebox.showerror("Error", "Seleccione un período de la lista para editar.")
            return
        
        try:
            period_id = int(period_id_str)
        except ValueError:
            messagebox.showerror("Error", "ID de período inválido.")
            return

        update_data = {}
        nombre_periodo = self.period_name_entry.get().strip()
        fecha_inicio_str = self.period_start_date_entry.get().strip()
        fecha_fin_str = self.period_end_date_entry.get().strip()
        activo = self.period_activo_var.get()

        if nombre_periodo:
            update_data['nombre_periodo'] = nombre_periodo
        if fecha_inicio_str:
            update_data['fecha_inicio'] = fecha_inicio_str
        if fecha_fin_str:
            update_data['fecha_fin'] = fecha_fin_str
        
        update_data['activo'] = activo # Siempre se envía el estado activo

        if not update_data:
            messagebox.showinfo("Información", "No hay campos para actualizar.")
            return

        # El controlador ya maneja la conversión de fecha y las validaciones
        success, error = self.period_controller.update_period_details(period_id, **update_data)
        if success:
            messagebox.showinfo("Éxito", f"Período con ID {period_id} actualizado.")
            self.load_period_data()
            self._clear_period_form()
        else:
            messagebox.showerror("Error al Editar Período", error)

    def _delete_period(self):
        """
        Maneja la eliminación de un período.
        """
        period_id_str = self.period_id_entry.get()
        if not period_id_str:
            messagebox.showerror("Error", "Seleccione un período de la lista para eliminar.")
            return
        
        try:
            period_id = int(period_id_str)
        except ValueError:
            messagebox.showerror("Error", "ID de período inválido.")
            return

        confirm = messagebox.askyesno("Confirmar Eliminación", 
                                      f"¿Está seguro de que desea eliminar el período con ID {period_id}?")
        if confirm:
            success, error = self.period_controller.delete_existing_period(period_id)
            if success:
                messagebox.showinfo("Éxito", f"Período con ID {period_id} eliminado.")
                self.load_period_data()
                self._clear_period_form()
            else:
                messagebox.showerror("Error al Eliminar Período", error)