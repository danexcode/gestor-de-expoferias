# gui/views/dashboard_view.py
import tkinter as tk
from tkinter import ttk
from .background_image_frame import BackgroundImageFrame

class DashboardView(BackgroundImageFrame):
    """
    Vista principal de la aplicación después del login.
    Contiene botones para navegar a las diferentes secciones (Administrador de Datos, Reportes, Comunicación).
    """
    def __init__(self, master, app_controller_callback, user_role=None):
        super().__init__(master)
        self.master = master
        self.app_controller_callback = app_controller_callback
        self.user_role = user_role 

        self.setup_ui()

    def setup_ui(self):
        self.pack(expand=True, fill='both', padx=20, pady=20)

        welcome_label = ttk.Label(self, text=f"Bienvenido al Dashboard {self.user_role if self.user_role else ''}", 
                                  font=("Arial", 24, "bold"))
        welcome_label.pack(pady=40)

        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(pady=20)

        # Botón para el Administrador de Datos
        data_admin_button = ttk.Button(buttons_frame, text="Administrar Datos", 
                                       command=self.show_data_admin, 
                                       width=30, style='Accent.TButton') 
        data_admin_button.pack(pady=10)

        # Botón para Reportes
        reports_button = ttk.Button(buttons_frame, text="Ver Reportes", 
                                    command=self.show_reports, 
                                    width=30)
        reports_button.pack(pady=10)
        
        # --- Nuevo Botón: Comunicación y Certificados ---
        communication_button = ttk.Button(buttons_frame, text="Comunicación y Certificados",
                                          command=self.show_communication_tools,
                                          width=30)
        communication_button.pack(pady=10)
        # -----------------------------------------------
        
        # Botón de Cerrar Sesión
        logout_button = ttk.Button(self, text="Cerrar Sesión", 
                                   command=self.app_controller_callback.logout_and_show_login, 
                                   width=20)
        logout_button.pack(side=tk.BOTTOM, pady=20)

    def show_data_admin(self):
        """
        Maneja la acción del botón 'Administrar Datos'.
        Llama al método correspondiente en el controlador principal (main_app).
        """
        print("Navegando a Administrador de Datos...")
        self.app_controller_callback.show_data_admin_view()

    def show_reports(self):
        """
        Maneja la acción del botón 'Ver Reportes'.
        Llama al método correspondiente en el controlador principal (main_app).
        """
        print("Navegando a Reportes...")
        self.app_controller_callback.show_reports_view()

    def show_communication_tools(self):
        """
        Maneja la acción del botón 'Comunicación y Certificados'.
        Llama al método correspondiente en el controlador principal.
        """
        print("Navegando a Herramientas de Comunicación y Certificados...")
        self.app_controller_callback.show_communication_tools_view() # ¡Nueva llamada!