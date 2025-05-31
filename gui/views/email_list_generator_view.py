import tkinter as tk
from tkinter import ttk, messagebox
import re 

class EmailListGeneratorView(ttk.Frame):
    def __init__(self, master, app_controller_callback, communication_controller):
        super().__init__(master, padding="15 15 15 15")
        self.master = master
        self.app_controller_callback = app_controller_callback
        self.communication_controller = communication_controller 

        self.recipients_data = [] 
        self.selected_recipients_emails = [] 
        self.periods = [] 

        self.setup_ui()
        self._load_periods()
        self._load_recipients()

    def setup_ui(self):
        self.pack(expand=True, fill='both')

        # Frame superior para título (Se eliminó el botón de volver)
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, pady=(0, 15))

        # Eliminar el botón de volver:
        # back_button = ttk.Button(top_frame, text="Volver a Herramientas",
        #                          command=self.app_controller_callback.show_communication_tools_view, 
        #                          style='TButton')
        # back_button.pack(side=tk.LEFT, anchor=tk.NW, padx=0, pady=0) 

        ttk.Label(top_frame, text="Generador de Listas de Emails",
                  font=("Arial", 22, "bold")).pack(side=tk.TOP, expand=True, fill=tk.X, pady=(0, 5)) # Ahora sin side=tk.LEFT

        # --- Sección de Selección y Filtro de Destinatarios ---
        recipients_frame = ttk.LabelFrame(self, text="Seleccionar Destinatarios", padding="10")
        recipients_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Frame de filtros
        filter_frame = ttk.Frame(recipients_frame)
        filter_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(filter_frame, text="Buscar:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(filter_frame)
        self.search_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        self.search_entry.bind("<KeyRelease>", self._filter_recipients_display)

        ttk.Label(filter_frame, text="Filtrar por Periodo:").pack(side=tk.LEFT, padx=(15,5))
        self.period_combobox = ttk.Combobox(filter_frame, state="readonly", width=25)
        self.period_combobox.pack(side=tk.LEFT, padx=5)
        self.period_combobox.bind("<<ComboboxSelected>>", self._filter_recipients_by_period)

        ttk.Button(filter_frame, text="Limpiar Selección", command=self._clear_recipient_selection).pack(side=tk.RIGHT, padx=5)
        ttk.Button(filter_frame, text="Seleccionar Todos", command=self._select_all_recipients).pack(side=tk.RIGHT, padx=5)
        ttk.Button(filter_frame, text="Mostrar Todos", command=self._load_recipients).pack(side=tk.RIGHT, padx=5) 

        # Treeview para mostrar destinatarios
        self.recipients_tree = ttk.Treeview(recipients_frame, columns=("ID", "Nombre", "Email", "Tipo"), show="headings")
        self.recipients_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=5)

        self.recipients_tree.heading("ID", text="ID", anchor=tk.W)
        self.recipients_tree.heading("Nombre", text="Nombre", anchor=tk.W)
        self.recipients_tree.heading("Email", text="Email", anchor=tk.W)
        self.recipients_tree.heading("Tipo", text="Tipo", anchor=tk.W)

        self.recipients_tree.column("ID", width=80, stretch=tk.NO)
        self.recipients_tree.column("Nombre", width=180, stretch=tk.YES)
        self.recipients_tree.column("Email", width=250, stretch=tk.YES)
        self.recipients_tree.column("Tipo", width=100, stretch=tk.NO)

        # Scrollbars para el Treeview
        tree_scrollbar_y = ttk.Scrollbar(recipients_frame, orient="vertical", command=self.recipients_tree.yview)
        tree_scrollbar_y.pack(side=tk.RIGHT, fill="y")
        self.recipients_tree.configure(yscrollcommand=tree_scrollbar_y.set)

        # Vincular evento de clic para selección
        self.recipients_tree.bind("<ButtonRelease-1>", self._on_recipient_click)

        # --- Sección de Lista de Correos Generada ---
        email_output_frame = ttk.LabelFrame(self, text="Lista de Correos Generada", padding="10")
        email_output_frame.pack(fill=tk.X, pady=10)

        self.email_list_text = tk.Text(email_output_frame, wrap=tk.WORD, height=8, width=60)
        self.email_list_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.email_list_text.config(state=tk.DISABLED) # Hacerlo de solo lectura

        output_scrollbar = ttk.Scrollbar(email_output_frame, orient="vertical", command=self.email_list_text.yview)
        output_scrollbar.pack(side=tk.RIGHT, fill="y")
        self.email_list_text.config(yscrollcommand=output_scrollbar.set)

        # Botón para copiar al portapapeles
        copy_button = ttk.Button(self, text="Copiar Correos", command=self._copy_emails_to_clipboard, style='Accent.TButton')
        copy_button.pack(pady=10)

        self.status_label = ttk.Label(self, text="", foreground="red")
        self.status_label.pack(pady=5)

    def _load_periods(self):
        """Carga los períodos disponibles en el combobox."""
        self.periods, error = self.communication_controller.get_periods()
        if error:
            messagebox.showerror("Error de Carga", f"No se pudieron cargar los períodos: {error}")
            return
        
        period_names = ["Todos los períodos"] + [p['nombre_periodo'] for p in self.periods]
        self.period_combobox['values'] = period_names
        self.period_combobox.set("Todos los períodos") 

    def _load_recipients(self):
        """Carga todos los destinatarios elegibles en el Treeview."""
        self.recipients_tree.delete(*self.recipients_tree.get_children()) 
        self.selected_recipients_emails = [] 

        recipients, error = self.communication_controller.get_all_eligible_recipients()
        if error:
            messagebox.showerror("Error de Carga", f"No se pudieron cargar los destinatarios: {error}")
            return
        
        self.recipients_data = recipients 
        self._display_recipients(self.recipients_data) 

    def _display_recipients(self, recipients_list):
        """Muestra una lista dada de destinatarios en el Treeview."""
        self.recipients_tree.delete(*self.recipients_tree.get_children())
        
        current_selection_emails = set(self.selected_recipients_emails)
        self.selected_recipients_emails = []

        for r in recipients_list:
            item_id = self.recipients_tree.insert("", tk.END, values=(r['id'], r['nombre_completo'], r['email'], r['tipo']))
            if r['email'] in current_selection_emails:
                self.recipients_tree.item(item_id, tags=('selected',))
                self.selected_recipients_emails.append(r['email']) 
            else:
                self.recipients_tree.item(item_id, tags=())
        self.recipients_tree.tag_configure('selected', background='lightblue')
        self._update_email_list_output() 

    def _filter_recipients_display(self, event=None):
        """Filtra los destinatarios visibles en el Treeview según el texto de búsqueda."""
        search_term = self.search_entry.get().lower()
        
        current_displayed_recipients = []
        for item_id in self.recipients_tree.get_children():
            values = self.recipients_tree.item(item_id, 'values')
            current_displayed_recipients.append({
                'id': values[0],
                'nombre_completo': values[1],
                'email': values[2],
                'tipo': values[3]
            })

        filtered_by_search = []
        for r in current_displayed_recipients:
            if search_term in str(r['nombre_completo']).lower() or \
               search_term in str(r['email']).lower() or \
               search_term in str(r['tipo']).lower():
                filtered_by_search.append(r)
        
        self.recipients_tree.delete(*self.recipients_tree.get_children())
        for r in filtered_by_search:
            item_id = self.recipients_tree.insert("", tk.END, values=(r['id'], r['nombre_completo'], r['email'], r['tipo']))
            if r['email'] in self.selected_recipients_emails:
                self.recipients_tree.item(item_id, tags=('selected',))
            else:
                self.recipients_tree.item(item_id, tags=())
        self.recipients_tree.tag_configure('selected', background='lightblue')


    def _filter_recipients_by_period(self, event=None):
        """Filtra los destinatarios en el Treeview según el período seleccionado."""
        selected_period_name = self.period_combobox.get()
        selected_period_id = None

        if selected_period_name != "Todos los períodos":
            for p in self.periods:
                if p['nombre_periodo'] == selected_period_name:
                    selected_period_id = p['id_periodo']
                    break
        
        self.selected_recipients_emails = [] 
        self._clear_recipient_selection() 

        if selected_period_id is None:
            self._load_recipients() 
        else:
            participants_for_period, error = self.communication_controller.get_participants_by_period(selected_period_id)
            if error:
                messagebox.showerror("Error de Filtro", f"Error al filtrar por período: {error}")
                return
            
            # Solo mostrar participantes en este caso, NO usuarios de la tabla `usuarios`
            self.recipients_data = participants_for_period 
            self._display_recipients(self.recipients_data)
        
        self.search_entry.delete(0, tk.END)


    def _on_recipient_click(self, event):
        """Maneja el clic en una fila del Treeview para seleccionar/deseleccionar."""
        item = self.recipients_tree.identify_row(event.y)
        if not item:
            return

        values = self.recipients_tree.item(item, 'values')
        email = values[2] 

        if email in self.selected_recipients_emails:
            self.selected_recipients_emails.remove(email)
            self.recipients_tree.item(item, tags=()) 
        else:
            if self._is_valid_email(email):
                self.selected_recipients_emails.append(email)
                self.recipients_tree.item(item, tags=('selected',)) 
            else:
                messagebox.showwarning("Email Inválido", f"El correo '{email}' no tiene un formato válido y no se puede seleccionar.")
        
        self.recipients_tree.tag_configure('selected', background='lightblue') 
        self._update_email_list_output() 

    def _is_valid_email(self, email):
        """Valida el formato de un email usando una expresión regular simple."""
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def _select_all_recipients(self):
        """Selecciona todos los destinatarios visibles y válidos."""
        self.selected_recipients_emails = []
        for item_id in self.recipients_tree.get_children(): 
            values = self.recipients_tree.item(item_id, 'values')
            email = values[2]
            if self._is_valid_email(email):
                self.selected_recipients_emails.append(email)
                self.recipients_tree.item(item_id, tags=('selected',))
            else:
                self.recipients_tree.item(item_id, tags=()) 
        self.recipients_tree.tag_configure('selected', background='lightblue')
        self._update_email_list_output()

    def _clear_recipient_selection(self):
        """Limpia la selección de destinatarios."""
        self.selected_recipients_emails = []
        for item_id in self.recipients_tree.get_children():
            self.recipients_tree.item(item_id, tags=()) 
        self.recipients_tree.tag_configure('selected', background='lightblue')
        self._update_email_list_output()

    def _update_email_list_output(self):
        """Actualiza el Text widget con la lista de correos seleccionados."""
        email_string = ", ".join(self.selected_recipients_emails)
        self.email_list_text.config(state=tk.NORMAL) 
        self.email_list_text.delete("1.0", tk.END)
        self.email_list_text.insert("1.0", email_string)
        self.email_list_text.config(state=tk.DISABLED) 

    def _copy_emails_to_clipboard(self):
        """Copia la lista de correos generada al portapapeles."""
        email_string = self.email_list_text.get("1.0", tk.END).strip()
        if email_string:
            self.clipboard_clear()
            self.clipboard_append(email_string)
            self.update() 
            self.status_label.config(text="Correos copiados al portapapeles.", foreground="green")
        else:
            self.status_label.config(text="No hay correos para copiar.", foreground="orange")