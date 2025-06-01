# gui/main_app.py
import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk

# Importar todos los controladores
from controllers.user_controller import UserController
from controllers.participant_controller import ParticipantController
from controllers.subject_controller import SubjectController
from controllers.period_controller import PeriodController
from controllers.project_controller import ProjectController
from controllers.report_controller import ReportController
from controllers.communication_controller import CommunicationController 

# Importar las vistas y el nuevo BaseScrollableFrame
from gui.views.welcome_view import WelcomeView   
from gui.views.login_view import LoginView
from gui.views.register_view import RegisterView
from gui.views.dashboard_view import DashboardView 
from gui.views.data_admin_view import DataAdminView 
from gui.views.report_view import ReportView 
from gui.views.communication_tools_view import CommunicationToolsView 

class MainApp(ThemedTk):
    """
    Clase principal de la aplicación Tkinter.
    Hereda de ThemedTk para soporte de temas.
    Gestiona la inicialización de controladores y la navegación entre vistas.
    """
    def __init__(self):
        """
        Inicializa la aplicación principal.
        Configura el tema y crea las instancias de los controladores.
        """
        super().__init__()
        self.title("Sistema de Gestión de Proyectos Universitarios")
        self.geometry("1024x768")
        self.resizable(True, True)

        self.set_theme("breeze") 

        self.controllers = {
            "user_controller": UserController(),
            "participant_controller": ParticipantController(),
            "subject_controller": SubjectController(),
            "period_controller": PeriodController(),
            "project_controller": ProjectController(),
            "report_controller": ReportController(),
            "communication_controller": CommunicationController() 
        }

        self.main_container = ttk.Frame(self, padding="10 10 10 10")
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        self.current_view = None
        self.logged_in_user_data = None 

        # Configurar listener global de la rueda del ratón
        self.bind_all("<MouseWheel>", self._on_mousewheel) # Windows/macOS
        self.bind_all("<Button-4>", self._on_mousewheel) # Linux scroll up
        self.bind_all("<Button-5>", self._on_mousewheel) # Linux scroll down

        self.show_welcome_view() 

    def _on_mousewheel(self, event):
        """Maneja el desplazamiento con la rueda del ratón de forma global."""
        # Intenta encontrar el widget que tiene el foco para desplazarlo
        widget = self.focus_get()
        while widget and not hasattr(widget, 'canvas'): # Buscar un ancestro con un 'canvas'
            widget = widget.master
            if widget == self: # Si llegamos a la ventana principal, parar
                break
        
        if hasattr(widget, 'canvas') and widget.canvas.winfo_exists():
            canvas = widget.canvas
            if canvas.yview() == (0.0, 1.0): # Si el canvas no tiene contenido desbordado
                return # No hacer nada
            
            if event.num == 4 or event.delta > 0: # Rueda hacia arriba
                canvas.yview_scroll(-1, "units")
            elif event.num == 5 or event.delta < 0: # Rueda hacia abajo
                canvas.yview_scroll(1, "units")
            
            return "break" # Detener la propagación del evento

    def show_welcome_view(self): 
        self._clear_current_view()
        # Asegúrate de pasar el master correcto (main_container)
        self.current_view = WelcomeView(self.main_container, self)
        self.current_view.pack(expand=True, fill='both')

    def show_login_view(self):
        self._clear_current_view()
        self.current_view = LoginView(self.main_container, self) 
        self.current_view.pack(expand=True, fill='both')

    def show_register_view(self):
        self._clear_current_view()
        self.current_view = RegisterView(self.main_container, self)
        self.current_view.pack(expand=True, fill='both')

    def on_login_success(self, user_data): 
        self.logged_in_user_data = user_data 
        print(f"Usuario '{user_data['nombre_usuario']}' (ID: {user_data['id_usuario']}) ha iniciado sesión exitosamente.")
        self.show_dashboard_view() 

    def show_dashboard_view(self): 
        self._clear_current_view()
        user_role = self.logged_in_user_data['rol'] if self.logged_in_user_data else None
        self.current_view = DashboardView(self.main_container, self, user_role=user_role)
        self.current_view.pack(expand=True, fill='both')

    def show_data_admin_view(self): 
        if self.logged_in_user_data and self.logged_in_user_data['rol'] in ['Administrador', 'Coordinador']:
            self._clear_current_view()
            user_role = self.logged_in_user_data['rol']
            self.current_view = DataAdminView(self.main_container, self, user_role=user_role)
            self.current_view.pack(expand=True, fill='both')
        else:
            messagebox.showwarning("Acceso Denegado", "No tiene permisos para acceder a la administración de datos.")

    def show_reports_view(self): 
        if self.logged_in_user_data and self.logged_in_user_data['rol'] in ['Administrador', 'Coordinador', 'Profesor']:
            self._clear_current_view()
            self.current_view = ReportView(self.main_container, self)
            self.current_view.pack(expand=True, fill='both')
        else:
            messagebox.showwarning("Acceso Denegado", "No tiene permisos para ver los reportes.")

    def show_communication_tools_view(self):
        self._clear_current_view() 
        self.current_view = CommunicationToolsView(self.main_container, self) 
        self.current_view.pack(expand=True, fill='both') 
        self.title("Herramientas de Comunicación y Certificados") 
        print("Mostrando vista de Herramientas de Comunicación y Certificados.")

    def logout_and_show_login(self): 
        if self.controllers["user_controller"].logout_user():
            self.logged_in_user_data = None 
            print("Sesión cerrada exitosamente. Volviendo a la pantalla de login.")
            self.show_login_view()
        else:
            print("Error al cerrar sesión.") 

    def _clear_current_view(self):
        if self.current_view:
            self.current_view.destroy()
            self.current_view = None

