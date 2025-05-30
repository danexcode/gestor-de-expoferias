# gui/views/data_admin_view.py
import tkinter as tk
from tkinter import ttk, messagebox
import sys

# Importar los controladores necesarios
from controllers.user_controller import UserController
# Importa los demás controladores a medida que crees sus pestañas
# from controllers.participant_controller import ParticipantController
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
        """
        Constructor de DataAdminView.

        Args:
            master (tk.Tk or ttk.Frame): La ventana principal o frame padre.
            app_controller_callback (object): Instancia de MainApp para callbacks de navegación.
            user_role (str, optional): Rol del usuario logueado, para control de permisos.
        """
        super().__init__(master)
        self.master = master
        self.app_controller_callback = app_controller_callback
        self.user_role = user_role

        # Inicializar controladores
        self.user_controller = UserController()
        # self.participant_controller = ParticipantController() # Descomentar cuando uses
        # self.subject_controller = SubjectController()
        # self.period_controller = PeriodController()
        # self.project_controller = ProjectController()

        self.setup_ui()
        self.load_user_data() # Cargar datos de usuarios al inicio

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
        self._setup_user_tab() # Configura los elementos de la pestaña de usuarios

        # --- Pestaña de Participantes (Placeholder) ---
        self.participant_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.participant_tab, text="Participantes")
        ttk.Label(self.participant_tab, text="Gestión de Participantes (próximamente)").pack(pady=50)
        # self._setup_participant_tab() # Descomentar e implementar

        # --- Pestaña de Materias (Placeholder) ---
        self.subject_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.subject_tab, text="Materias")
        ttk.Label(self.subject_tab, text="Gestión de Materias (próximamente)").pack(pady=50)
        # self._setup_subject_tab() # Descomentar e implementar

        # --- Pestaña de Periodos (Placeholder) ---
        self.period_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.period_tab, text="Periodos")
        ttk.Label(self.period_tab, text="Gestión de Periodos (próximamente)").pack(pady=50)
        # self._setup_period_tab() # Descomentar e implementar

        # --- Pestaña de Proyectos (Placeholder) ---
        self.project_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.project_tab, text="Proyectos")
        ttk.Label(self.project_tab, text="Gestión de Proyectos (próximamente)").pack(pady=50)
        # self._setup_project_tab() # Descomentar e implementar

        # Botón para volver al Dashboard (fuera de las pestañas)
        back_button = ttk.Button(self, text="Volver al Dashboard", 
                                 command=self.app_controller_callback.show_dashboard_view,
                                 style='TButton')
        back_button.pack(pady=10)

    # =======================================================
    # Métodos y Widgets para la Pestaña de USUARIOS
    # =======================================================
    def _setup_user_tab(self):
        """
        Configura los widgets para la gestión de usuarios dentro de su pestaña.
        """
        # Frame superior para el Treeview de la lista de usuarios
        tree_frame = ttk.Frame(self.user_tab)
        tree_frame.pack(pady=10, fill='both', expand=True)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        self.user_tree = ttk.Treeview(tree_frame, columns=("ID", "Usuario", "Rol", "Nombre Completo", "Email", "Activo"), show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.user_tree.yview)
        scrollbar.pack(side='right', fill='y')

        # Definir encabezados de las columnas
        self.user_tree.heading("ID", text="ID")
        self.user_tree.heading("Usuario", text="Usuario")
        self.user_tree.heading("Rol", text="Rol")
        self.user_tree.heading("Nombre Completo", text="Nombre Completo")
        self.user_tree.heading("Email", text="Email")
        self.user_tree.heading("Activo", text="Activo")

        # Configurar anchos de columna
        self.user_tree.column("ID", width=50, stretch=tk.NO)
        self.user_tree.column("Usuario", width=120, stretch=tk.NO)
        self.user_tree.column("Rol", width=100, stretch=tk.NO)
        self.user_tree.column("Nombre Completo", width=180, stretch=tk.NO)
        self.user_tree.column("Email", width=200, stretch=tk.NO)
        self.user_tree.column("Activo", width=70, stretch=tk.NO, anchor=tk.CENTER)

        self.user_tree.pack(fill='both', expand=True)

        # Vincular el evento de selección en el Treeview para cargar datos en los campos
        self.user_tree.bind("<<TreeviewSelect>>", self._load_user_data_to_form)

        # Frame inferior para los formularios de entrada y botones de acción
        input_frame = ttk.LabelFrame(self.user_tab, text="Detalles del Usuario", padding=15)
        input_frame.pack(pady=20, fill='x', expand=False) # No expandir verticalmente

        # Campos de entrada
        # Fila 1
        ttk.Label(input_frame, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.user_id_entry = ttk.Entry(input_frame, width=10, state='readonly')
        self.user_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(input_frame, text="Usuario:").grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.username_entry = ttk.Entry(input_frame, width=30)
        self.username_entry.grid(row=0, column=3, padx=5, pady=5, sticky='w')

        ttk.Label(input_frame, text="Contraseña:").grid(row=0, column=4, padx=5, pady=5, sticky='w')
        self.password_entry = ttk.Entry(input_frame, width=30, show="*")
        self.password_entry.grid(row=0, column=5, padx=5, pady=5, sticky='w')

        # Fila 2
        ttk.Label(input_frame, text="Rol:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.role_combobox = ttk.Combobox(input_frame, values=['Administrador', 'Coordinador', 'Profesor'], state='readonly', width=27)
        self.role_combobox.grid(row=1, column=1, padx=5, pady=5, sticky='w', columnspan=2)
        self.role_combobox.set('Profesor') # Valor por defecto

        ttk.Label(input_frame, text="Nombre Completo:").grid(row=1, column=3, padx=5, pady=5, sticky='w')
        self.fullname_entry = ttk.Entry(input_frame, width=30)
        self.fullname_entry.grid(row=1, column=4, padx=5, pady=5, sticky='w', columnspan=2)

        # Fila 3
        ttk.Label(input_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.email_entry = ttk.Entry(input_frame, width=30)
        self.email_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w', columnspan=2)

        ttk.Label(input_frame, text="Activo:").grid(row=2, column=3, padx=5, pady=5, sticky='w')
        self.activo_var = tk.BooleanVar(value=True) # Variable para el Checkbutton
        self.activo_checkbutton = ttk.Checkbutton(input_frame, text="Sí", variable=self.activo_var)
        self.activo_checkbutton.grid(row=2, column=4, padx=5, pady=5, sticky='w')

        # Botones de acción
        buttons_frame = ttk.Frame(self.user_tab)
        buttons_frame.pack(pady=10)

        ttk.Button(buttons_frame, text="Añadir Usuario", command=self._add_user).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Editar Usuario", command=self._edit_user).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Eliminar Usuario", command=self._delete_user).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Limpiar Campos", command=self._clear_user_form).pack(side='left', padx=5)

    def load_user_data(self):
        """
        Carga los datos de los usuarios desde el controlador y los muestra en el Treeview.
        """
        for item in self.user_tree.get_children(): # Limpiar Treeview existente
            self.user_tree.delete(item)
        
        users, error = self.user_controller.get_all_system_users()
        if error:
            messagebox.showerror("Error de Carga", f"No se pudieron cargar los usuarios: {error}")
            return

        for user in users:
            # Asegúrate de que las claves del diccionario coincidan con tu modelo
            self.user_tree.insert("", "end", values=(
                user.get('id_usuario'), 
                user.get('nombre_usuario'), 
                user.get('rol'), 
                user.get('nombre_completo', ''), # Usar .get() con valor por defecto
                user.get('correo_electronico', ''),
                "Sí" if user.get('activo') else "No"
            ))

    def _load_user_data_to_form(self, event):
        """
        Carga los datos de un usuario seleccionado en el Treeview a los campos del formulario.
        """
        selected_item = self.user_tree.focus()
        if not selected_item: # Si no hay nada seleccionado
            self._clear_user_form()
            return

        values = self.user_tree.item(selected_item, 'values')
        if values:
            # Desactivar estado de solo lectura para actualizar
            self.user_id_entry.config(state='normal')

            self.user_id_entry.delete(0, tk.END)
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END) # No cargar la contraseña hasheada
            self.fullname_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)

            self.user_id_entry.insert(0, values[0]) # ID
            self.username_entry.insert(0, values[1]) # Usuario
            self.role_combobox.set(values[2]) # Rol
            self.fullname_entry.insert(0, values[3]) # Nombre Completo
            self.email_entry.insert(0, values[4]) # Email
            self.activo_var.set(values[5] == "Sí") # Activo

            # Volver a poner en estado de solo lectura
            self.user_id_entry.config(state='readonly')

    def _clear_user_form(self):
        """
        Limpia todos los campos del formulario de usuario.
        """
        self.user_tree.selection_remove(self.user_tree.selection()) # Deseleccionar en el Treeview
        
        self.user_id_entry.config(state='normal') # Habilitar para limpiar
        self.user_id_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.role_combobox.set('Profesor') # Resetear a valor por defecto
        self.fullname_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.activo_var.set(True)

        self.user_id_entry.config(state='readonly') # Volver a solo lectura

    def _add_user(self):
        """
        Maneja la adición de un nuevo usuario.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_combobox.get()
        full_name = self.fullname_entry.get() if self.fullname_entry.get() else None
        email = self.email_entry.get() if self.email_entry.get() else None

        # Validaciones básicas del lado de la vista (opcional, el controlador también valida)
        if not username or not password or not role:
            messagebox.showerror("Error de Entrada", "Usuario, Contraseña y Rol son obligatorios para añadir.")
            return

        user_id, error = self.user_controller.register_new_user(username, password, role, full_name, email)
        if user_id:
            messagebox.showinfo("Éxito", f"Usuario '{username}' añadido con ID: {user_id}")
            self.load_user_data() # Recargar datos en el Treeview
            self._clear_user_form() # Limpiar campos
        else:
            messagebox.showerror("Error al Añadir Usuario", error)

    def _edit_user(self):
        """
        Maneja la edición de un usuario existente.
        """
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
        password = self.password_entry.get() # La contraseña se hasheará si se proporciona
        role = self.role_combobox.get()
        full_name = self.fullname_entry.get() if self.fullname_entry.get() else None
        email = self.email_entry.get() if self.email_entry.get() else None
        activo = self.activo_var.get()

        # Preparar solo los campos que se van a actualizar
        update_data = {}
        # NOTA: Compara con el usuario actual si necesitas evitar actualizaciones innecesarias o duplicados
        # Para simplificar, pasamos todo y el controlador maneja la lógica.
        update_data['username'] = username
        if password: # Solo actualiza la contraseña si se ingresó una nueva
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
        """
        Maneja la eliminación de un usuario.
        """
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