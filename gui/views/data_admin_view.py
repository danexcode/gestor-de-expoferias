# gui/views/data_admin_view.py
import tkinter as tk
from tkinter import ttk, messagebox
import sys
from datetime import datetime

# Importar los controladores necesarios
from controllers.user_controller import UserController
from controllers.participant_controller import ParticipantController
from controllers.subject_controller import SubjectController
from controllers.period_controller import PeriodController
from controllers.project_controller import ProjectController

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
        self.period_controller = PeriodController()
        self.project_controller = ProjectController() # ¡NUEVA INSTANCIA DEL CONTROLADOR!

        # Variables para los Combobox de Periodos y Materias
        self.period_options = {} # {nombre: id}
        self.subject_options = {} # {nombre: id}
        self.load_combobox_data() # Cargar datos para los combobox al inicio

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

        # --- Pestaña de Periodos ---
        self.period_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.period_tab, text="Periodos")
        self._setup_period_tab()

        # --- Pestaña de Proyectos ¡NUEVO! ---
        self.project_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.project_tab, text="Proyectos")
        self._setup_project_tab() # ¡Llamar a la configuración de proyectos!

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
        elif selected_tab == "Periodos":
            self.load_period_data()
        elif selected_tab == "Proyectos":
            self.load_project_data()
            self.load_combobox_data() # Recargar datos de combobox por si hay cambios
            self.load_all_participants_for_project_selection() # Cargar participantes disponibles
        # Añade aquí la carga de datos para otras pestañas

    def load_combobox_data(self):
        """Carga los datos para los Comboboxes de Periodos y Materias."""
        # Cargar períodos
        periods, error_p = self.period_controller.get_all_system_periods()
        if not error_p:
            self.period_options = {p['nombre_periodo']: p['id_periodo'] for p in periods}
        else:
            self.period_options = {}
            print(f"Advertencia: No se pudieron cargar periodos para combobox: {error_p}") # Solo para depuración

        # Cargar materias
        subjects, error_s = self.subject_controller.get_all_system_subjects()
        if not error_s:
            self.subject_options = {s['nombre_materia']: s['id_materia'] for s in subjects}
        else:
            self.subject_options = {}
            print(f"Advertencia: No se pudieron cargar materias para combobox: {error_s}") # Solo para depuración


    # =======================================================
    # Métodos y Widgets para la Pestaña de USUARIOS
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
    # Métodos y Widgets para la Pestaña de PARTICIPANTES (sin cambios)
    # =======================================================
    def _setup_participant_tab(self):
        # ... (Tu código de la pestaña de participantes) ...
        tree_frame = ttk.Frame(self.participant_tab)
        tree_frame.pack(pady=10, fill='both', expand=True)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        self.participant_tree = ttk.Treeview(tree_frame, 
                                            columns=("ID", "Tipo", "Nombre", "Apellido", "Cédula", "Email", "Teléfono", "Carrera"), 
                                            show="headings", 
                                            yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.participant_tree.yview)
        scrollbar.pack(side='right', fill='y')

        self.participant_tree.heading("ID", text="ID")
        self.participant_tree.heading("Tipo", text="Tipo")
        self.participant_tree.heading("Nombre", text="Nombre")
        self.participant_tree.heading("Apellido", text="Apellido")
        self.participant_tree.heading("Cédula", text="Cédula")
        self.participant_tree.heading("Email", text="Email")
        self.participant_tree.heading("Teléfono", text="Teléfono")
        self.participant_tree.heading("Carrera", text="Carrera")

        self.participant_tree.column("ID", width=50, stretch=tk.NO)
        self.participant_tree.column("Tipo", width=80, stretch=tk.NO)
        self.participant_tree.column("Nombre", width=120, stretch=tk.NO)
        self.participant_tree.column("Apellido", width=120, stretch=tk.NO)
        self.participant_tree.column("Cédula", width=100, stretch=tk.NO)
        self.participant_tree.column("Email", width=180, stretch=tk.NO)
        self.participant_tree.column("Teléfono", width=100, stretch=tk.NO)
        self.participant_tree.column("Carrera", width=150, stretch=tk.NO)

        self.participant_tree.pack(fill='both', expand=True)

        self.participant_tree.bind("<<TreeviewSelect>>", self._load_participant_data_to_form)

        input_frame = ttk.LabelFrame(self.participant_tab, text="Detalles del Participante", padding=15)
        input_frame.pack(pady=20, fill='x', expand=False) 

        ttk.Label(input_frame, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.participant_id_entry = ttk.Entry(input_frame, width=10, state='readonly')
        self.participant_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(input_frame, text="Tipo:").grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.participant_type_combobox = ttk.Combobox(input_frame, values=['Estudiante', 'Docente'], state='readonly', width=15)
        self.participant_type_combobox.grid(row=0, column=3, padx=5, pady=5, sticky='w')
        self.participant_type_combobox.set('Estudiante')

        ttk.Label(input_frame, text="Nombre:").grid(row=0, column=4, padx=5, pady=5, sticky='w')
        self.participant_name_entry = ttk.Entry(input_frame, width=30)
        self.participant_name_entry.grid(row=0, column=5, padx=5, pady=5, sticky='w')

        ttk.Label(input_frame, text="Apellido:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.participant_last_name_entry = ttk.Entry(input_frame, width=30)
        self.participant_last_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(input_frame, text="Cédula:").grid(row=1, column=2, padx=5, pady=5, sticky='w')
        self.participant_cedula_entry = ttk.Entry(input_frame, width=20)
        self.participant_cedula_entry.grid(row=1, column=3, padx=5, pady=5, sticky='w')
        
        ttk.Label(input_frame, text="Teléfono:").grid(row=1, column=4, padx=5, pady=5, sticky='w')
        self.participant_phone_entry = ttk.Entry(input_frame, width=20)
        self.participant_phone_entry.grid(row=1, column=5, padx=5, pady=5, sticky='w')

        ttk.Label(input_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.participant_email_entry = ttk.Entry(input_frame, width=40)
        self.participant_email_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w', columnspan=3)

        ttk.Label(input_frame, text="Carrera:").grid(row=2, column=4, padx=5, pady=5, sticky='w')
        self.participant_carrera_entry = ttk.Entry(input_frame, width=20)
        self.participant_carrera_entry.grid(row=2, column=5, padx=5, pady=5, sticky='w')

        buttons_frame = ttk.Frame(self.participant_tab)
        buttons_frame.pack(pady=10)

        ttk.Button(buttons_frame, text="Añadir Participante", command=self._add_participant).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Editar Participante", command=self._edit_participant).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Eliminar Participante", command=self._delete_participant).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Limpiar Campos", command=self._clear_participant_form).pack(side='left', padx=5)

    def load_participant_data(self):
        # ... (Tu código de carga de participantes) ...
        for item in self.participant_tree.get_children():
            self.participant_tree.delete(item)
        
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
        # ... (Tu código de carga de datos a formulario de participantes) ...
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
        # ... (Tu código de limpieza de formulario de participantes) ...
        self.participant_tree.selection_remove(self.participant_tree.selection())
        
        self.participant_id_entry.config(state='normal')
        self.participant_id_entry.delete(0, tk.END)
        self.participant_type_combobox.set('Estudiante') 
        self.participant_name_entry.delete(0, tk.END)
        self.participant_last_name_entry.delete(0, tk.END)
        self.participant_cedula_entry.delete(0, tk.END)
        self.participant_email_entry.delete(0, tk.END)
        self.participant_phone_entry.delete(0, tk.END)
        self.participant_carrera_entry.delete(0, tk.END)
        self.participant_id_entry.config(state='readonly')

    def _add_participant(self):
        # ... (Tu código de añadir participante) ...
        tipo_participante = self.participant_type_combobox.get()
        nombre = self.participant_name_entry.get()
        apellido = self.participant_last_name_entry.get()
        cedula = self.participant_cedula_entry.get()
        correo_electronico = self.participant_email_entry.get()
        telefono = self.participant_phone_entry.get()
        carrera = self.participant_carrera_entry.get()

        if not all([tipo_participante, nombre, apellido, cedula]): 
            messagebox.showerror("Error de Entrada", "Tipo, Nombre, Apellido y Cédula son obligatorios.")
            return

        participant_id, error = self.participant_controller.add_new_participant(
            tipo_participante, nombre, apellido, cedula, 
            correo_electronico if correo_electronico else None, 
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
        # ... (Tu código de editar participante) ...
        participant_id_str = self.participant_id_entry.get()
        if not participant_id_str:
            messagebox.showerror("Error", "Seleccione un participante de la lista para editar.")
            return
        
        try:
            participant_id = int(participant_id_str)
        except ValueError:
            messagebox.showerror("Error", "ID de participante inválido.")
            return

        tipo_participante = self.participant_type_combobox.get()
        nombre = self.participant_name_entry.get()
        apellido = self.participant_last_name_entry.get()
        cedula = self.participant_cedula_entry.get()
        correo_electronico = self.participant_email_entry.get()
        telefono = self.participant_phone_entry.get()
        carrera = self.participant_carrera_entry.get()

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
        # ... (Tu código de eliminar participante) ...
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

    # =======================================================
    # ¡NUEVO CÓDIGO! Métodos y Widgets para la Pestaña de MATERIAS
    # =======================================================
    def _setup_subject_tab(self):
        """
        Configura los widgets para la gestión de materias dentro de su pestaña.
        """
        tree_frame = ttk.Frame(self.subject_tab)
        tree_frame.pack(pady=10, fill='both', expand=True)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        self.subject_tree = ttk.Treeview(tree_frame, 
                                          columns=("ID", "Código", "Nombre", "Créditos"), 
                                          show="headings", 
                                          yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.subject_tree.yview)
        scrollbar.pack(side='right', fill='y')

        self.subject_tree.heading("ID", text="ID")
        self.subject_tree.heading("Código", text="Código de Materia")
        self.subject_tree.heading("Nombre", text="Nombre de Materia")
        self.subject_tree.heading("Créditos", text="Créditos")

        self.subject_tree.column("ID", width=50, stretch=tk.NO)
        self.subject_tree.column("Código", width=150, stretch=tk.NO)
        self.subject_tree.column("Nombre", width=300, stretch=tk.YES)
        self.subject_tree.column("Créditos", width=80, stretch=tk.NO, anchor=tk.CENTER)

        self.subject_tree.pack(fill='both', expand=True)

        self.subject_tree.bind("<<TreeviewSelect>>", self._load_subject_data_to_form)

        input_frame = ttk.LabelFrame(self.subject_tab, text="Detalles de la Materia", padding=15)
        input_frame.pack(pady=20, fill='x', expand=False) 

        ttk.Label(input_frame, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.subject_id_entry = ttk.Entry(input_frame, width=10, state='readonly')
        self.subject_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(input_frame, text="Código:").grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.subject_code_entry = ttk.Entry(input_frame, width=25)
        self.subject_code_entry.grid(row=0, column=3, padx=5, pady=5, sticky='w')

        ttk.Label(input_frame, text="Nombre:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.subject_name_entry = ttk.Entry(input_frame, width=50)
        self.subject_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w', columnspan=3)

        ttk.Label(input_frame, text="Créditos:").grid(row=1, column=4, padx=5, pady=5, sticky='w')
        self.subject_credits_entry = ttk.Entry(input_frame, width=10)
        self.subject_credits_entry.grid(row=1, column=5, padx=5, pady=5, sticky='w')

        buttons_frame = ttk.Frame(self.subject_tab)
        buttons_frame.pack(pady=10)

        ttk.Button(buttons_frame, text="Añadir Materia", command=self._add_subject).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Editar Materia", command=self._edit_subject).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Eliminar Materia", command=self._delete_subject).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Limpiar Campos", command=self._clear_subject_form).pack(side='left', padx=5)

    def load_subject_data(self):
        """
        Carga los datos de las materias desde el controlador y los muestra en el Treeview.
        """
        for item in self.subject_tree.get_children():
            self.subject_tree.delete(item)
        
        # ¡MODIFICACIÓN!: Llama al método correcto en el controlador
        subjects, error = self.subject_controller.get_all_system_subjects()
        if error:
            messagebox.showerror("Error de Carga", f"No se pudieron cargar las materias: {error}")
            return

        for s in subjects:
            self.subject_tree.insert("", "end", values=(
                s.get('id_materia'), 
                s.get('codigo_materia'), 
                s.get('nombre_materia'), 
                s.get('creditos')
            ))

    def _load_subject_data_to_form(self, event):
        """
        Carga los datos de una materia seleccionada en el Treeview a los campos del formulario.
        """
        selected_item = self.subject_tree.focus()
        if not selected_item:
            self._clear_subject_form()
            return

        values = self.subject_tree.item(selected_item, 'values')
        if values:
            self.subject_id_entry.config(state='normal')

            self.subject_id_entry.delete(0, tk.END)
            self.subject_code_entry.delete(0, tk.END)
            self.subject_name_entry.delete(0, tk.END)
            self.subject_credits_entry.delete(0, tk.END)

            self.subject_id_entry.insert(0, values[0])
            self.subject_code_entry.insert(0, values[1])
            self.subject_name_entry.insert(0, values[2])
            self.subject_credits_entry.insert(0, values[3])

            self.subject_id_entry.config(state='readonly')

    def _clear_subject_form(self):
        """
        Limpia todos los campos del formulario de materia.
        """
        self.subject_tree.selection_remove(self.subject_tree.selection())
        
        self.subject_id_entry.config(state='normal')
        self.subject_id_entry.delete(0, tk.END)
        self.subject_code_entry.delete(0, tk.END)
        self.subject_name_entry.delete(0, tk.END)
        self.subject_credits_entry.delete(0, tk.END)
        self.subject_id_entry.config(state='readonly')

    def _add_subject(self):
        """
        Maneja la adición de una nueva materia.
        """
        codigo_materia = self.subject_code_entry.get().strip()
        nombre_materia = self.subject_name_entry.get().strip()
        creditos_str = self.subject_credits_entry.get().strip()

        if not all([codigo_materia, nombre_materia]):
            messagebox.showerror("Error de Entrada", "Código y Nombre de la materia son obligatorios.")
            return
        
        creditos = None
        if creditos_str: # Solo intenta convertir si el campo no está vacío
            try:
                creditos = int(creditos_str)
                if creditos <= 0:
                    messagebox.showerror("Error de Entrada", "Los créditos deben ser un número entero positivo.")
                    return
            except ValueError:
                messagebox.showerror("Error de Entrada", "Los créditos deben ser un número entero válido.")
                return

        # ¡MODIFICACIÓN!: Llama al método correcto en el controlador
        subject_id, error = self.subject_controller.add_new_subject(codigo_materia, nombre_materia, creditos)
        if subject_id:
            messagebox.showinfo("Éxito", f"Materia '{nombre_materia}' añadida con ID: {subject_id}")
            self.load_subject_data()
            self._clear_subject_form()
        else:
            messagebox.showerror("Error al Añadir Materia", error)

    def _edit_subject(self):
        """
        Maneja la edición de una materia existente.
        """
        subject_id_str = self.subject_id_entry.get()
        if not subject_id_str:
            messagebox.showerror("Error", "Seleccione una materia de la lista para editar.")
            return
        
        try:
            subject_id = int(subject_id_str)
        except ValueError:
            messagebox.showerror("Error", "ID de materia inválido.")
            return

        # Recoger los campos para actualizar
        update_data = {}
        codigo_materia = self.subject_code_entry.get().strip()
        nombre_materia = self.subject_name_entry.get().strip()
        creditos_str = self.subject_credits_entry.get().strip()

        if codigo_materia:
            update_data['codigo_materia'] = codigo_materia
        if nombre_materia:
            update_data['nombre_materia'] = nombre_materia
        
        if creditos_str:
            try:
                creditos = int(creditos_str)
                if creditos <= 0:
                    messagebox.showerror("Error de Entrada", "Los créditos deben ser un número entero positivo.")
                    return
                update_data['creditos'] = creditos
            except ValueError:
                messagebox.showerror("Error de Entrada", "Los créditos deben ser un número entero válido.")
                return
        else: # Si el campo de créditos está vacío, lo enviamos como None
             update_data['creditos'] = None # Permite desasignar créditos si la DB lo permite

        if not update_data:
            messagebox.showinfo("Información", "No hay campos para actualizar.")
            return

        # ¡MODIFICACIÓN!: Pasa el diccionario con **kwargs
        success, error = self.subject_controller.update_existing_subject(subject_id, **update_data)
        if success:
            messagebox.showinfo("Éxito", f"Materia con ID {subject_id} actualizada.")
            self.load_subject_data()
            self._clear_subject_form()
        else:
            messagebox.showerror("Error al Editar Materia", error)

    def _delete_subject(self):
        """
        Maneja la eliminación de una materia.
        """
        subject_id_str = self.subject_id_entry.get()
        if not subject_id_str:
            messagebox.showerror("Error", "Seleccione una materia de la lista para eliminar.")
            return
        
        try:
            subject_id = int(subject_id_str)
        except ValueError:
            messagebox.showerror("Error", "ID de materia inválido.")
            return

        confirm = messagebox.askyesno("Confirmar Eliminación", 
                                      f"¿Está seguro de que desea eliminar la materia con ID {subject_id}?")
        if confirm:
            success, error = self.subject_controller.delete_existing_subject(subject_id)
            if success:
                messagebox.showinfo("Éxito", f"Materia con ID {subject_id} eliminada.")
                self.load_subject_data()
                self._clear_subject_form()
            else:
                messagebox.showerror("Error al Eliminar Materia", error)


    # =======================================================
    # Métodos y Widgets para la Pestaña de PERIODOS
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

    # =======================================================
    # ¡NUEVO CÓDIGO! Métodos y Widgets para la Pestaña de PROYECTOS
    # =======================================================
    def _setup_project_tab(self):
        """
        Configura los widgets para la gestión de proyectos dentro de su pestaña.
        """
        # Frame principal para la organización de la pestaña
        main_frame = ttk.Frame(self.project_tab)
        main_frame.pack(pady=10, fill='both', expand=True)

        # Frame para el Treeview de proyectos (sin cambios)
        project_list_frame = ttk.LabelFrame(main_frame, text="Lista de Proyectos", padding=10)
        project_list_frame.pack(fill='both', expand=True,  padx=5, pady=5)

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
        self.project_tree.column("Descripción", width=250, stretch=tk.YES) 

        self.project_tree.pack(fill='both', expand=True)
        self.project_tree.bind("<<TreeviewSelect>>", self._load_project_data_to_form)

        # Frame para los detalles del proyecto y gestión de participantes
        # Este es el frame original, ahora contendrá el canvas
        details_frame = ttk.LabelFrame(main_frame, text="Detalles del Proyecto y Participantes", padding=10)
        details_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # --- INICIO DE CAMBIOS PARA EL SCROLL VERTICAL EN details_frame ---
        
        # 1. Crear un Canvas dentro de details_frame
        canvas = tk.Canvas(details_frame)
        canvas.pack(side="left", fill="both", expand=True)

        # 2. Crear una Scrollbar y asociarla al Canvas
        scrollbar = ttk.Scrollbar(details_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        # 3. Configurar el Canvas para usar la scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox("all")))
        
        # 4. Crear un Frame interno que contendrá todos los widgets
        # Este frame es el que realmente se desplaza dentro del canvas
        inner_frame = ttk.Frame(canvas)

        # 5. Colocar el inner_frame dentro del canvas.
        # Es crucial usar create_window para que el contenido del frame se desplace.
        # anchor='nw' asegura que el frame se alinee en la esquina superior izquierda.
        # window=inner_frame le dice al canvas qué widget debe "contener" para el desplazamiento.
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        # Configurar el peso de las columnas en inner_frame (no details_frame directamente)
        # Esto asegura que la columna 1 (donde están los Entry y Text) se expanda
        inner_frame.grid_columnconfigure(1, weight=1) 
        inner_frame.grid_columnconfigure(2, weight=1) 

        # Ahora todos los controles van al inner_frame en lugar de details_frame
        ttk.Label(inner_frame, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.project_id_entry = ttk.Entry(inner_frame, width=10, state='readonly')
        self.project_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew') 

        ttk.Label(inner_frame, text="Nombre:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.project_name_entry = ttk.Entry(inner_frame) 
        self.project_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew', columnspan=3)

        ttk.Label(inner_frame, text="Descripción:").grid(row=2, column=0, padx=5, pady=5, sticky='nw')
        self.project_description_text = tk.Text(inner_frame, height=4) 
        self.project_description_text.grid(row=2, column=1, padx=5, pady=5, sticky='ew', columnspan=3)

        ttk.Label(inner_frame, text="Período:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.project_period_combobox = ttk.Combobox(inner_frame, state="readonly") 
        self.project_period_combobox.grid(row=3, column=1, padx=5, pady=5, sticky='ew', columnspan=3)
        self.project_period_combobox['values'] = list(self.period_options.keys())

        ttk.Label(inner_frame, text="Materia:").grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.project_subject_combobox = ttk.Combobox(inner_frame, state="readonly") 
        self.project_subject_combobox.grid(row=4, column=1, padx=5, pady=5, sticky='ew', columnspan=3)
        self.project_subject_combobox['values'] = list(self.subject_options.keys())

        # Frame para la gestión de participantes (ahora dentro de inner_frame)
        participants_management_frame = ttk.LabelFrame(inner_frame, text="Gestión de Participantes", padding=10)
        participants_management_frame.grid(row=5, column=0, columnspan=4, padx=5, pady=10, sticky='nsew') 
        
        # Frame para las dos listas de participantes (sin cambios, ya está dentro de participants_management_frame)
        lists_frame = ttk.Frame(participants_management_frame)
        lists_frame.pack(fill='both', expand=True)

        lists_frame.grid_columnconfigure(0, weight=1) 
        lists_frame.grid_columnconfigure(2, weight=1) 

        ttk.Label(lists_frame, text="Disponibles:").grid(row=0, column=0, pady=2, padx=5, sticky='w', columnspan=1)
        available_participants_frame = ttk.Frame(lists_frame)
        available_participants_frame.grid(row=1, column=0, padx=5, pady=5, sticky='nsew') 
        
        scrollbar_avail = ttk.Scrollbar(available_participants_frame, orient=tk.VERTICAL)
        self.available_participants_tree = ttk.Treeview(available_participants_frame, 
                                                        columns=("ID", "Nombre", "Apellido"), 
                                                        show="headings", 
                                                        selectmode='extended', 
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

        buttons_middle_frame = ttk.Frame(lists_frame)
        buttons_middle_frame.grid(row=1, column=1, padx=10, sticky='ns') 
        ttk.Button(buttons_middle_frame, text=">> Añadir >>", command=self._add_selected_participants).pack(pady=5)
        ttk.Button(buttons_middle_frame, text="<< Remover <<", command=self._remove_selected_participants).pack(pady=5)

        ttk.Label(lists_frame, text="En Proyecto:").grid(row=0, column=2, pady=2, padx=5, sticky='w')
        current_participants_frame = ttk.Frame(lists_frame)
        current_participants_frame.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')

        scrollbar_current = ttk.Scrollbar(current_participants_frame, orient=tk.VERTICAL)
        self.current_participants_tree = ttk.Treeview(current_participants_frame, 
                                                      columns=("ID", "Nombre", "Apellido"), 
                                                      show="headings", 
                                                      selectmode='extended', 
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
        
        # Botones de acción para Proyectos (ahora dentro de inner_frame)
        buttons_frame = ttk.Frame(inner_frame) 
        buttons_frame.grid(row=6, column=0, columnspan=4, pady=10) 

        ttk.Button(buttons_frame, text="Añadir Proyecto", command=self._add_project).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Editar Proyecto", command=self._edit_project).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Eliminar Proyecto", command=self._delete_project).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Limpiar Campos", command=self._clear_project_form).pack(side='left', padx=5)

        # Almacenar los IDs de participantes para la gestión (sin cambios)
        self.current_project_participant_ids = set() 
        self.all_available_participants_data = {} 

    def load_all_participants_for_project_selection(self):
        """
        Carga todos los participantes disponibles para la selección en proyectos.
        """
        self.available_participants_tree.delete(*self.available_participants_tree.get_children())
        self.all_available_participants_data.clear()

        participants, error = self.participant_controller.get_all_system_participants()
        if error:
            messagebox.showerror("Error de Carga", f"No se pudieron cargar los participantes disponibles: {error}")
            return
        
        for p in participants:
            self.all_available_participants_data[p['id_participante']] = p
            # Insertar en el Treeview de disponibles si no está ya en el Treeview de actuales (al cargar un proyecto)
            # Esto se manejará mejor en _load_project_data_to_form para evitar duplicados visuales.
            self.available_participants_tree.insert("", "end", values=(
                p.get('id_participante'), 
                p.get('nombre'), 
                p.get('apellido')
            ), iid=p.get('id_participante')) # Usar el ID como iid para fácil referencia

        # Cuando se carga la pestaña, si no hay un proyecto seleccionado,
        # todos los participantes están en "disponibles".
        # Si ya hay un proyecto seleccionado, _load_project_data_to_form lo ajustará.
        self._sync_participant_trees() # Llamar para asegurar que las listas se sincronicen

    def _sync_participant_trees(self):
        """
        Sincroniza los Treeviews de participantes disponibles y actuales
        basándose en self.current_project_participant_ids y self.all_available_participants_data.
        """
        # Limpiar ambos Treeviews
        self.available_participants_tree.delete(*self.available_participants_tree.get_children())
        self.current_participants_tree.delete(*self.current_participants_tree.get_children())

        # Rellenar Treeview de "En Proyecto"
        for p_id in self.current_project_participant_ids:
            participant_data = self.all_available_participants_data.get(p_id)
            if participant_data:
                self.current_participants_tree.insert("", "end", values=(
                    participant_data['id_participante'], 
                    participant_data['nombre'], 
                    participant_data['apellido']
                ), iid=participant_data['id_participante'])

        # Rellenar Treeview de "Disponibles"
        for p_id, p_data in self.all_available_participants_data.items():
            if p_id not in self.current_project_participant_ids:
                self.available_participants_tree.insert("", "end", values=(
                    p_data['id_participante'], 
                    p_data['nombre'], 
                    p_data['apellido']
                ), iid=p_data['id_participante'])


    def _add_selected_participants(self):
        """
        Mueve los participantes seleccionados de "Disponibles" a "En Proyecto".
        """
        selected_items = self.available_participants_tree.selection()
        if not selected_items:
            messagebox.showinfo("Atención", "Seleccione participantes de la lista 'Disponibles' para añadir.")
            return

        for item_id in selected_items:
            participant_id = int(self.available_participants_tree.item(item_id, 'values')[0])
            self.current_project_participant_ids.add(participant_id)
        
        self._sync_participant_trees()

    def _remove_selected_participants(self):
        """
        Mueve los participantes seleccionados de "En Proyecto" a "Disponibles".
        """
        selected_items = self.current_participants_tree.selection()
        if not selected_items:
            messagebox.showinfo("Atención", "Seleccione participantes de la lista 'En Proyecto' para remover.")
            return

        for item_id in selected_items:
            participant_id = int(self.current_participants_tree.item(item_id, 'values')[0])
            if participant_id in self.current_project_participant_ids:
                self.current_project_participant_ids.remove(participant_id)
        
        self._sync_participant_trees()


    def load_project_data(self):
        """
        Carga los datos de los proyectos desde el controlador y los muestra en el Treeview.
        """
        for item in self.project_tree.get_children():
            self.project_tree.delete(item)
        
        projects, error = self.project_controller.get_all_system_projects()
        if error:
            messagebox.showerror("Error de Carga", f"No se pudieron cargar los proyectos: {error}")
            return

        # Para mostrar nombres de periodo y materia en lugar de IDs
        # invertimos los diccionarios de opciones para búsquedas rápidas
        inv_period_options = {v: k for k, v in self.period_options.items()}
        inv_subject_options = {v: k for k, v in self.subject_options.items()}

        for p in projects:
            period_name = inv_period_options.get(p.get('id_periodo'), f"ID:{p.get('id_periodo')}")
            subject_name = inv_subject_options.get(p.get('id_materia'), f"ID:{p.get('id_materia')}")
            
            self.project_tree.insert("", "end", values=(
                p.get('id_proyecto'), 
                period_name, 
                subject_name, 
                p.get('nombre_proyecto'), 
                p.get('descripcion')
            ))

    def _load_project_data_to_form(self, event):
        """
        Carga los datos de un proyecto seleccionado en el Treeview a los campos del formulario,
        incluyendo los participantes asociados.
        """
        selected_item = self.project_tree.focus()
        if not selected_item:
            self._clear_project_form()
            return

        project_id = int(self.project_tree.item(selected_item, 'values')[0])
        
        project_details, error = self.project_controller.get_project_details(project_id)
        if error:
            messagebox.showerror("Error al Cargar", f"No se pudieron obtener detalles del proyecto: {error}")
            self._clear_project_form()
            return

        self.project_id_entry.config(state='normal')
        self.project_id_entry.delete(0, tk.END)
        self.project_id_entry.insert(0, project_details['id_proyecto'])
        self.project_id_entry.config(state='readonly')

        self.project_name_entry.delete(0, tk.END)
        self.project_name_entry.insert(0, project_details['nombre_proyecto'])

        self.project_description_text.delete('1.0', tk.END)
        self.project_description_text.insert('1.0', project_details['descripcion'])

        # Seleccionar el período y la materia en los comboboxes
        inv_period_options = {v: k for k, v in self.period_options.items()}
        period_name = inv_period_options.get(project_details['id_periodo'], "")
        self.project_period_combobox.set(period_name)

        inv_subject_options = {v: k for k, v in self.subject_options.items()}
        subject_name = inv_subject_options.get(project_details['id_materia'], "")
        self.project_subject_combobox.set(subject_name)

        # Cargar participantes del proyecto
        self.current_project_participant_ids.clear()
        if 'participantes' in project_details and project_details['participantes']:
            for p_data in project_details['participantes']:
                self.current_project_participant_ids.add(p_data['id_participante'])
        
        self._sync_participant_trees()


    def _clear_project_form(self):
        """
        Limpia todos los campos del formulario de proyecto y las listas de participantes.
        """
        self.project_tree.selection_remove(self.project_tree.selection())
        
        self.project_id_entry.config(state='normal')
        self.project_id_entry.delete(0, tk.END)
        self.project_id_entry.config(state='readonly')

        self.project_name_entry.delete(0, tk.END)
        self.project_description_text.delete('1.0', tk.END)
        self.project_period_combobox.set('')
        self.project_subject_combobox.set('')

        self.current_project_participant_ids.clear()
        self._sync_participant_trees() # Resincroniza para mostrar todos disponibles

    def _add_project(self):
        """
        Maneja la adición de un nuevo proyecto.
        """
        nombre_proyecto = self.project_name_entry.get().strip()
        descripcion = self.project_description_text.get('1.0', tk.END).strip()
        
        selected_period_name = self.project_period_combobox.get()
        selected_subject_name = self.project_subject_combobox.get()

        id_periodo = self.period_options.get(selected_period_name)
        id_materia = self.subject_options.get(selected_subject_name)

        if not all([id_periodo, id_materia, nombre_proyecto, descripcion]):
            messagebox.showerror("Error de Entrada", "Todos los campos de proyecto son obligatorios.")
            return

        # Participantes actuales en la lista "En Proyecto"
        # Convertir el set de IDs a una lista para pasar al controlador
        participantes_ids = list(self.current_project_participant_ids)

        project_id, error = self.project_controller.create_new_project(
            id_periodo, id_materia, nombre_proyecto, descripcion, participantes_ids
        )
        if project_id:
            messagebox.showinfo("Éxito", f"Proyecto '{nombre_proyecto}' añadido con ID: {project_id}")
            self.load_project_data()
            self._clear_project_form()
            # Recargar participantes disponibles para el nuevo proyecto
            self.load_all_participants_for_project_selection() 
        else:
            messagebox.showerror("Error al Añadir Proyecto", error)

    def _edit_project(self):
        """
        Maneja la edición de un proyecto existente y la actualización de participantes.
        """
        project_id_str = self.project_id_entry.get()
        if not project_id_str:
            messagebox.showerror("Error", "Seleccione un proyecto de la lista para editar.")
            return
        
        try:
            project_id = int(project_id_str)
        except ValueError:
            messagebox.showerror("Error", "ID de proyecto inválido.")
            return

        update_data = {}
        nombre_proyecto = self.project_name_entry.get().strip()
        descripcion = self.project_description_text.get('1.0', tk.END).strip()
        selected_period_name = self.project_period_combobox.get()
        selected_subject_name = self.project_subject_combobox.get()

        # Obtener los IDs actuales del proyecto para comparar los participantes
        current_project_details, err_details = self.project_controller.get_project_details(project_id)
        if err_details:
            messagebox.showerror("Error", f"No se pudo obtener el proyecto actual para edición: {err_details}")
            return
        
        current_associated_p_ids = {p['id_participante'] for p in current_project_details.get('participantes', [])}
        
        # ID del período y materia, si cambiaron
        new_id_periodo = self.period_options.get(selected_period_name)
        new_id_materia = self.subject_options.get(selected_subject_name)

        if new_id_periodo and new_id_periodo != current_project_details['id_periodo']:
            update_data['id_periodo'] = new_id_periodo
        if new_id_materia and new_id_materia != current_project_details['id_materia']:
            update_data['id_materia'] = new_id_materia
        if nombre_proyecto and nombre_proyecto != current_project_details['nombre_proyecto']:
            update_data['nombre_proyecto'] = nombre_proyecto
        if descripcion and descripcion != current_project_details['descripcion']:
            update_data['descripcion'] = descripcion

        # Si hay datos básicos para actualizar, llama al controlador
        if update_data:
            success_proj, error_proj = self.project_controller.update_existing_project(project_id, **update_data)
            if not success_proj:
                messagebox.showerror("Error al Editar Proyecto", error_proj)
                return # Detener si la actualización básica falla
        else:
            success_proj = True # Si no hay datos básicos para actualizar, se considera éxito en esta parte

        # --- Lógica de actualización de participantes ---
        participants_to_add = list(self.current_project_participant_ids - current_associated_p_ids)
        participants_to_remove = list(current_associated_p_ids - self.current_project_participant_ids)

        success_p_add, error_p_add = True, None
        if participants_to_add:
            success_p_add, error_p_add = self.project_controller.add_participants_to_project_controller(project_id, participants_to_add)

        success_p_remove, error_p_remove = True, None
        if participants_to_remove:
            success_p_remove, error_p_remove = self.project_controller.remove_participants_from_project_controller(project_id, participants_to_remove)

        if success_proj and success_p_add and success_p_remove:
            messagebox.showinfo("Éxito", f"Proyecto con ID {project_id} actualizado.")
            self.load_project_data()
            self._clear_project_form()
            self.load_all_participants_for_project_selection() # Recargar participantes disponibles
        else:
            error_message = ""
            if error_proj:
                error_message += f"Error al actualizar datos del proyecto: {error_proj}\n"
            if error_p_add:
                error_message += f"Error al añadir participantes: {error_p_add}\n"
            if error_p_remove:
                error_message += f"Error al remover participantes: {error_p_remove}\n"
            
            if not error_message: # Si no hubo errores específicos pero no fue success total
                error_message = "No se pudo actualizar el proyecto completamente."
            
            messagebox.showerror("Error al Editar Proyecto", error_message)

    def _delete_project(self):
        """
        Maneja la eliminación de un proyecto.
        """
        project_id_str = self.project_id_entry.get()
        if not project_id_str:
            messagebox.showerror("Error", "Seleccione un proyecto de la lista para eliminar.")
            return
        
        try:
            project_id = int(project_id_str)
        except ValueError:
            messagebox.showerror("Error", "ID de proyecto inválido.")
            return

        confirm = messagebox.askyesno("Confirmar Eliminación", 
                                      f"¿Está seguro de que desea eliminar el proyecto con ID {project_id}?")
        if confirm:
            success, error = self.project_controller.delete_single_project(project_id)
            if success:
                messagebox.showinfo("Éxito", f"Proyecto con ID {project_id} eliminado.")
                self.load_project_data()
                self._clear_project_form()
                self.load_all_participants_for_project_selection() # Recargar participantes disponibles
            else:
                messagebox.showerror("Error al Eliminar Proyecto", error)