# gui/views/data_admin_view.py
import tkinter as tk
from tkinter import ttk, messagebox
import sys

# Importar los controladores necesarios
from controllers.user_controller import UserController
from controllers.participant_controller import ParticipantController 
# from controllers.subject_controller import SubjectController
# from controllers.period_controller import PeriodController
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
        self.participant_controller = ParticipantController() # Instancia del controlador de Participantes
        # self.subject_controller = SubjectController()
        # self.period_controller = PeriodController()
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
        self._setup_participant_tab() # Llamar a la configuración de participantes

        # --- Pestaña de Materias (Placeholder) ---
        self.subject_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.subject_tab, text="Materias")
        ttk.Label(self.subject_tab, text="Gestión de Materias (próximamente)").pack(pady=50)

        # --- Pestaña de Periodos (Placeholder) ---
        self.period_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.period_tab, text="Periodos")
        ttk.Label(self.period_tab, text="Gestión de Periodos (próximamente)").pack(pady=50)

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
            self.load_participant_data() # Cargar datos de participantes
        # Añade aquí la carga de datos para otras pestañas

    # =======================================================
    # Métodos y Widgets para la Pestaña de USUARIOS (sin cambios)
    # =======================================================
    def _setup_user_tab(self):
        # ... (Tu código de la pestaña de usuarios) ...
        tree_frame = ttk.Frame(self.user_tab)
        tree_frame.pack(pady=10, fill='both', expand=True)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        self.user_tree = ttk.Treeview(tree_frame, columns=("ID", "Usuario", "Rol", "Nombre Completo", "Email", "Activo"), show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.user_tree.yview)
        scrollbar.pack(side='right', fill='y')

        self.user_tree.heading("ID", text="ID")
        self.user_tree.heading("Usuario", text="Usuario")
        self.user_tree.heading("Rol", text="Rol")
        self.user_tree.heading("Nombre Completo", text="Nombre Completo")
        self.user_tree.heading("Email", text="Email")
        self.user_tree.heading("Activo", text="Activo")

        self.user_tree.column("ID", width=50, stretch=tk.NO)
        self.user_tree.column("Usuario", width=120, stretch=tk.NO)
        self.user_tree.column("Rol", width=100, stretch=tk.NO)
        self.user_tree.column("Nombre Completo", width=180, stretch=tk.NO)
        self.user_tree.column("Email", width=200, stretch=tk.NO)
        self.user_tree.column("Activo", width=70, stretch=tk.NO, anchor=tk.CENTER)

        self.user_tree.pack(fill='both', expand=True)

        self.user_tree.bind("<<TreeviewSelect>>", self._load_user_data_to_form)

        input_frame = ttk.LabelFrame(self.user_tab, text="Detalles del Usuario", padding=15)
        input_frame.pack(pady=20, fill='x', expand=False) 

        ttk.Label(input_frame, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.user_id_entry = ttk.Entry(input_frame, width=10, state='readonly')
        self.user_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(input_frame, text="Usuario:").grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.username_entry = ttk.Entry(input_frame, width=30)
        self.username_entry.grid(row=0, column=3, padx=5, pady=5, sticky='w')

        ttk.Label(input_frame, text="Contraseña:").grid(row=0, column=4, padx=5, pady=5, sticky='w')
        self.password_entry = ttk.Entry(input_frame, width=30, show="*")
        self.password_entry.grid(row=0, column=5, padx=5, pady=5, sticky='w')

        ttk.Label(input_frame, text="Rol:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.role_combobox = ttk.Combobox(input_frame, values=['Administrador', 'Coordinador', 'Profesor'], state='readonly', width=27)
        self.role_combobox.grid(row=1, column=1, padx=5, pady=5, sticky='w', columnspan=2)
        self.role_combobox.set('Profesor')

        ttk.Label(input_frame, text="Nombre Completo:").grid(row=1, column=3, padx=5, pady=5, sticky='w')
        self.fullname_entry = ttk.Entry(input_frame, width=30)
        self.fullname_entry.grid(row=1, column=4, padx=5, pady=5, sticky='w', columnspan=2)

        ttk.Label(input_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.email_entry = ttk.Entry(input_frame, width=30)
        self.email_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w', columnspan=2)

        ttk.Label(input_frame, text="Activo:").grid(row=2, column=3, padx=5, pady=5, sticky='w')
        self.activo_var = tk.BooleanVar(value=True) 
        self.activo_checkbutton = ttk.Checkbutton(input_frame, text="Sí", variable=self.activo_var)
        self.activo_checkbutton.grid(row=2, column=4, padx=5, pady=5, sticky='w')

        buttons_frame = ttk.Frame(self.user_tab)
        buttons_frame.pack(pady=10)

        ttk.Button(buttons_frame, text="Añadir Usuario", command=self._add_user).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Editar Usuario", command=self._edit_user).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Eliminar Usuario", command=self._delete_user).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Limpiar Campos", command=self._clear_user_form).pack(side='left', padx=5)


    def load_user_data(self):
        # ... (Tu código de carga de usuarios) ...
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
        
        users, error = self.user_controller.get_all_system_users()
        if error:
            messagebox.showerror("Error de Carga", f"No se pudieron cargar los usuarios: {error}")
            return

        for user in users:
            self.user_tree.insert("", "end", values=(
                user.get('id_usuario'), 
                user.get('nombre_usuario'), 
                user.get('rol'), 
                user.get('nombre_completo', ''),
                user.get('correo_electronico', ''),
                "Sí" if user.get('activo') else "No"
            ))

    def _load_user_data_to_form(self, event):
        # ... (Tu código de carga de datos a formulario de usuarios) ...
        selected_item = self.user_tree.focus()
        if not selected_item:
            self._clear_user_form()
            return

        values = self.user_tree.item(selected_item, 'values')
        if values:
            self.user_id_entry.config(state='normal')

            self.user_id_entry.delete(0, tk.END)
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END) 
            self.fullname_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)

            self.user_id_entry.insert(0, values[0]) 
            self.username_entry.insert(0, values[1]) 
            self.role_combobox.set(values[2]) 
            self.fullname_entry.insert(0, values[3]) 
            self.email_entry.insert(0, values[4]) 
            self.activo_var.set(values[5] == "Sí") 

            self.user_id_entry.config(state='readonly')

    def _clear_user_form(self):
        # ... (Tu código de limpieza de formulario de usuarios) ...
        self.user_tree.selection_remove(self.user_tree.selection())
        
        self.user_id_entry.config(state='normal') 
        self.user_id_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.role_combobox.set('Profesor') 
        self.fullname_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.activo_var.set(True)

        self.user_id_entry.config(state='readonly')

    def _add_user(self):
        # ... (Tu código de añadir usuario) ...
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_combobox.get()
        full_name = self.fullname_entry.get() if self.fullname_entry.get() else None
        email = self.email_entry.get() if self.email_entry.get() else None

        if not username or not password or not role:
            messagebox.showerror("Error de Entrada", "Usuario, Contraseña y Rol son obligatorios para añadir.")
            return

        user_id, error = self.user_controller.register_new_user(username, password, role, full_name, email)
        if user_id:
            messagebox.showinfo("Éxito", f"Usuario '{username}' añadido con ID: {user_id}")
            self.load_user_data()
            self._clear_user_form()
        else:
            messagebox.showerror("Error al Añadir Usuario", error)

    def _edit_user(self):
        # ... (Tu código de editar usuario) ...
        user_id_str = self.user_id_entry.get()
        if not user_id_str:
            messagebox.showerror("Error", "Seleccione un usuario de la lista para editar.")
            return
        
        try:
            user_id = int(user_id_str)
        except ValueError:
            messagebox.showerror("Error", "ID de usuario inválido.")
            return

        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_combobox.get()
        full_name = self.fullname_entry.get() if self.fullname_entry.get() else None
        email = self.email_entry.get() if self.email_entry.get() else None
        activo = self.activo_var.get()

        update_data = {}
        update_data['username'] = username
        if password:
            update_data['password'] = password
        update_data['role'] = role
        update_data['full_name'] = full_name
        update_data['email'] = email
        update_data['activo'] = activo

        success, error = self.user_controller.update_existing_user(user_id, **update_data)
        if success:
            messagebox.showinfo("Éxito", f"Usuario con ID {user_id} actualizado.")
            self.load_user_data()
            self._clear_user_form()
        else:
            messagebox.showerror("Error al Editar Usuario", error)

    def _delete_user(self):
        # ... (Tu código de eliminar usuario) ...
        user_id_str = self.user_id_entry.get()
        if not user_id_str:
            messagebox.showerror("Error", "Seleccione un usuario de la lista para eliminar.")
            return
        
        try:
            user_id = int(user_id_str)
        except ValueError:
            messagebox.showerror("Error", "ID de usuario inválido.")
            return

        confirm = messagebox.askyesno("Confirmar Eliminación", 
                                      f"¿Está seguro de que desea eliminar el usuario con ID {user_id}?")
        if confirm:
            success, error = self.user_controller.delete_existing_user(user_id)
            if success:
                messagebox.showinfo("Éxito", f"Usuario con ID {user_id} eliminado.")
                self.load_user_data()
                self._clear_user_form()
            else:
                messagebox.showerror("Error al Eliminar Usuario", error)


    # =======================================================
    # Métodos y Widgets para la Pestaña de PARTICIPANTES
    # =======================================================
    def _setup_participant_tab(self):
        """
        Configura los widgets para la gestión de participantes dentro de su pestaña.
        """
        # Frame superior para el Treeview de la lista de participantes
        tree_frame = ttk.Frame(self.participant_tab)
        tree_frame.pack(pady=10, fill='both', expand=True)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        self.participant_tree = ttk.Treeview(tree_frame, 
                                            columns=("ID", "Tipo", "Nombre", "Apellido", "Cédula", "Email", "Teléfono", "Carrera"), 
                                            show="headings", 
                                            yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.participant_tree.yview)
        scrollbar.pack(side='right', fill='y')

        # Definir encabezados de las columnas (basado en tu esquema 'participantes')
        self.participant_tree.heading("ID", text="ID")
        self.participant_tree.heading("Tipo", text="Tipo")
        self.participant_tree.heading("Nombre", text="Nombre")
        self.participant_tree.heading("Apellido", text="Apellido")
        self.participant_tree.heading("Cédula", text="Cédula")
        self.participant_tree.heading("Email", text="Email")
        self.participant_tree.heading("Teléfono", text="Teléfono")
        self.participant_tree.heading("Carrera", text="Carrera")

        # Configurar anchos de columna (ajusta según necesites)
        self.participant_tree.column("ID", width=50, stretch=tk.NO)
        self.participant_tree.column("Tipo", width=80, stretch=tk.NO)
        self.participant_tree.column("Nombre", width=120, stretch=tk.NO)
        self.participant_tree.column("Apellido", width=120, stretch=tk.NO)
        self.participant_tree.column("Cédula", width=100, stretch=tk.NO)
        self.participant_tree.column("Email", width=180, stretch=tk.NO)
        self.participant_tree.column("Teléfono", width=100, stretch=tk.NO)
        self.participant_tree.column("Carrera", width=150, stretch=tk.NO)

        self.participant_tree.pack(fill='both', expand=True)

        # Vincular el evento de selección en el Treeview
        self.participant_tree.bind("<<TreeviewSelect>>", self._load_participant_data_to_form)

        # Frame inferior para los formularios de entrada y botones de acción
        input_frame = ttk.LabelFrame(self.participant_tab, text="Detalles del Participante", padding=15)
        input_frame.pack(pady=20, fill='x', expand=False) 

        # Campos de entrada
        # Fila 1
        ttk.Label(input_frame, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.participant_id_entry = ttk.Entry(input_frame, width=10, state='readonly')
        self.participant_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(input_frame, text="Tipo:").grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.participant_type_combobox = ttk.Combobox(input_frame, values=['Estudiante', 'Docente'], state='readonly', width=15)
        self.participant_type_combobox.grid(row=0, column=3, padx=5, pady=5, sticky='w')
        self.participant_type_combobox.set('Estudiante') # Valor por defecto

        ttk.Label(input_frame, text="Nombre:").grid(row=0, column=4, padx=5, pady=5, sticky='w')
        self.participant_name_entry = ttk.Entry(input_frame, width=30)
        self.participant_name_entry.grid(row=0, column=5, padx=5, pady=5, sticky='w')

        # Fila 2
        ttk.Label(input_frame, text="Apellido:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.participant_last_name_entry = ttk.Entry(input_frame, width=30)
        self.participant_last_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(input_frame, text="Cédula:").grid(row=1, column=2, padx=5, pady=5, sticky='w')
        self.participant_cedula_entry = ttk.Entry(input_frame, width=20)
        self.participant_cedula_entry.grid(row=1, column=3, padx=5, pady=5, sticky='w')
        
        ttk.Label(input_frame, text="Teléfono:").grid(row=1, column=4, padx=5, pady=5, sticky='w')
        self.participant_phone_entry = ttk.Entry(input_frame, width=20)
        self.participant_phone_entry.grid(row=1, column=5, padx=5, pady=5, sticky='w')

        # Fila 3
        ttk.Label(input_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.participant_email_entry = ttk.Entry(input_frame, width=40)
        self.participant_email_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w', columnspan=3)

        ttk.Label(input_frame, text="Carrera:").grid(row=2, column=4, padx=5, pady=5, sticky='w')
        self.participant_carrera_entry = ttk.Entry(input_frame, width=20)
        self.participant_carrera_entry.grid(row=2, column=5, padx=5, pady=5, sticky='w')

        # Botones de acción para Participantes
        buttons_frame = ttk.Frame(self.participant_tab)
        buttons_frame.pack(pady=10)

        ttk.Button(buttons_frame, text="Añadir Participante", command=self._add_participant).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Editar Participante", command=self._edit_participant).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Eliminar Participante", command=self._delete_participant).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Limpiar Campos", command=self._clear_participant_form).pack(side='left', padx=5)

    def load_participant_data(self):
        """
        Carga los datos de los participantes desde el controlador y los muestra en el Treeview.
        """
        for item in self.participant_tree.get_children():
            self.participant_tree.delete(item)
        
        # Llama al método correcto en el controlador
        participants, error = self.participant_controller.get_all_system_participants()
        if error:
            messagebox.showerror("Error de Carga", f"No se pudieron cargar los participantes: {error}")
            return

        for p in participants:
            self.participant_tree.insert("", "end", values=(
                p.get('id_participante'), 
                p.get('tipo_participante'), 
                p.get('nombre'), 
                p.get('apellido'), 
                p.get('cedula', ''), 
                p.get('correo_electronico', ''), 
                p.get('telefono', ''),
                p.get('carrera', '')
            ))

    def _load_participant_data_to_form(self, event):
        """
        Carga los datos de un participante seleccionado en el Treeview a los campos del formulario.
        """
        selected_item = self.participant_tree.focus()
        if not selected_item:
            self._clear_participant_form()
            return

        values = self.participant_tree.item(selected_item, 'values')
        if values:
            self.participant_id_entry.config(state='normal')

            self.participant_id_entry.delete(0, tk.END)
            self.participant_type_combobox.set('')
            self.participant_name_entry.delete(0, tk.END)
            self.participant_last_name_entry.delete(0, tk.END)
            self.participant_cedula_entry.delete(0, tk.END)
            self.participant_email_entry.delete(0, tk.END)
            self.participant_phone_entry.delete(0, tk.END)
            self.participant_carrera_entry.delete(0, tk.END)

            self.participant_id_entry.insert(0, values[0])
            self.participant_type_combobox.set(values[1])
            self.participant_name_entry.insert(0, values[2])
            self.participant_last_name_entry.insert(0, values[3])
            self.participant_cedula_entry.insert(0, values[4])
            self.participant_email_entry.insert(0, values[5])
            self.participant_phone_entry.insert(0, values[6])
            self.participant_carrera_entry.insert(0, values[7])

            self.participant_id_entry.config(state='readonly')

    def _clear_participant_form(self):
        """
        Limpia todos los campos del formulario de participante.
        """
        self.participant_tree.selection_remove(self.participant_tree.selection())
        
        self.participant_id_entry.config(state='normal')
        self.participant_id_entry.delete(0, tk.END)
        self.participant_type_combobox.set('Estudiante') # Volver a valor por defecto
        self.participant_name_entry.delete(0, tk.END)
        self.participant_last_name_entry.delete(0, tk.END)
        self.participant_cedula_entry.delete(0, tk.END)
        self.participant_email_entry.delete(0, tk.END)
        self.participant_phone_entry.delete(0, tk.END)
        self.participant_carrera_entry.delete(0, tk.END)
        self.participant_id_entry.config(state='readonly')

    def _add_participant(self):
        """
        Maneja la adición de un nuevo participante.
        """
        tipo_participante = self.participant_type_combobox.get()
        nombre = self.participant_name_entry.get()
        apellido = self.participant_last_name_entry.get()
        cedula = self.participant_cedula_entry.get()
        correo_electronico = self.participant_email_entry.get()
        telefono = self.participant_phone_entry.get()
        carrera = self.participant_carrera_entry.get()

        # Validaciones de la vista
        if not all([tipo_participante, nombre, apellido, cedula]): # Cédula es obligatoria según tu controlador
            messagebox.showerror("Error de Entrada", "Tipo, Nombre, Apellido y Cédula son obligatorios.")
            return

        # El controlador maneja la lógica de la carrera para docentes, así que pasamos lo que venga
        participant_id, error = self.participant_controller.add_new_participant(
            tipo_participante, nombre, apellido, cedula, 
            correo_electronico if correo_electronico else None, # Pasamos None si está vacío
            telefono if telefono else None,
            carrera if carrera else None
        )
        if participant_id:
            messagebox.showinfo("Éxito", f"Participante '{nombre} {apellido}' añadido con ID: {participant_id}")
            self.load_participant_data()
            self._clear_participant_form()
        else:
            messagebox.showerror("Error al Añadir Participante", error)

    def _edit_participant(self):
        """
        Maneja la edición de un participante existente.
        """
        participant_id_str = self.participant_id_entry.get()
        if not participant_id_str:
            messagebox.showerror("Error", "Seleccione un participante de la lista para editar.")
            return
        
        try:
            participant_id = int(participant_id_str)
        except ValueError:
            messagebox.showerror("Error", "ID de participante inválido.")
            return

        # Recoger todos los campos y enviarlos al controlador
        tipo_participante = self.participant_type_combobox.get()
        nombre = self.participant_name_entry.get()
        apellido = self.participant_last_name_entry.get()
        cedula = self.participant_cedula_entry.get()
        correo_electronico = self.participant_email_entry.get()
        telefono = self.participant_phone_entry.get()
        carrera = self.participant_carrera_entry.get()

        # Tu controlador espera los argumentos explícitamente, no un diccionario **kwargs
        success, error = self.participant_controller.update_existing_participant(
            participant_id, 
            tipo_participante, 
            nombre, 
            apellido, 
            cedula if cedula else None, 
            correo_electronico if correo_electronico else None, 
            telefono if telefono else None, 
            carrera if carrera else None
        )
        if success:
            messagebox.showinfo("Éxito", f"Participante con ID {participant_id} actualizado.")
            self.load_participant_data()
            self._clear_participant_form()
        else:
            messagebox.showerror("Error al Editar Participante", error)

    def _delete_participant(self):
        """
        Maneja la eliminación de un participante.
        """
        participant_id_str = self.participant_id_entry.get()
        if not participant_id_str:
            messagebox.showerror("Error", "Seleccione un participante de la lista para eliminar.")
            return
        
        try:
            participant_id = int(participant_id_str)
        except ValueError:
            messagebox.showerror("Error", "ID de participante inválido.")
            return

        confirm = messagebox.askyesno("Confirmar Eliminación", 
                                      f"¿Está seguro de que desea eliminar el participante con ID {participant_id}?")
        if confirm:
            success, error = self.participant_controller.delete_existing_participant(participant_id)
            if success:
                messagebox.showinfo("Éxito", f"Participante con ID {participant_id} eliminado.")
                self.load_participant_data()
                self._clear_participant_form()
            else:
                messagebox.showerror("Error al Eliminar Participante", error)