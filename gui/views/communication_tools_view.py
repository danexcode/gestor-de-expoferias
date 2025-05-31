import tkinter as tk
from tkinter import ttk, messagebox

# Importa la nueva vista (renombrada)
from gui.views.email_list_generator_view import EmailListGeneratorView 

class CommunicationToolsView(ttk.Frame):
    def __init__(self, master, app_controller_callback):
        super().__init__(master, padding="15 15 15 15")
        self.master = master
        self.app_controller_callback = app_controller_callback
        
        # Asegúrate de que los controladores necesarios estén accesibles
        # Renombramos email_controller a communication_controller
        self.communication_controller = self.app_controller_callback.controllers["communication_controller"]

        self.setup_ui()

    def setup_ui(self):
        self.pack(expand=True, fill='both')

        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, pady=(0, 15))

        back_button = ttk.Button(top_frame, text="Volver al Dashboard",
                                 command=self.app_controller_callback.show_dashboard_view,
                                 style='TButton')
        back_button.pack(side=tk.LEFT, anchor=tk.NW, padx=0, pady=0) 

        ttk.Label(top_frame, text="Herramientas de Comunicación y Certificados",
                  font=("Arial", 22, "bold")).pack(side=tk.TOP, expand=True, fill=tk.X, pady=(0, 5))

        # Crear un Notebook (widget de pestañas)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', pady=10)

        # Pestaña para Generar Lista de Emails
        self.email_list_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.email_list_tab, text="Generar Lista de Emails")

        # Instanciar EmailListGeneratorView dentro de la pestaña de email
        self.email_list_generator_view = EmailListGeneratorView(
            self.email_list_tab, self.app_controller_callback, self.communication_controller
        )
        self.email_list_generator_view.pack(expand=True, fill='both')

        # Pestaña para Generación de Certificados (aún vacía)
        self.certificates_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.certificates_tab, text="Generar Certificados")
        ttk.Label(self.certificates_tab, text="¡Aquí irán las opciones para generar certificados!").pack(pady=50)