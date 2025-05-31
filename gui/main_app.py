# gui/main_app.py
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk

# Importar todos los controladores (ahora son clases)
from controllers.user_controller import UserController
from controllers.participant_controller import ParticipantController
from controllers.subject_controller import SubjectController
from controllers.period_controller import PeriodController
from controllers.project_controller import ProjectController
from controllers.report_controller import ReportController

# Importar las vistas
from gui.views.welcome_view import WelcomeView   
from gui.views.login_view import LoginView
from gui.views.register_view import RegisterView
from gui.views.dashboard_view import DashboardView 
from gui.views.data_admin_view import DataAdminView # ¡Nueva importación!
from gui.views.report_view import ReportView # ¡Nueva importación!

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
            "report_controller": ReportController()
        }

        self.main_container = ttk.Frame(self, padding="10 10 10 10")
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        self.current_view = None
        self.logged_in_user_data = None 

        self.show_welcome_view() 

    def show_welcome_view(self): 
        """
        Muestra la vista de bienvenida.
        """
        self._clear_current_view()
        self.current_view = WelcomeView(self.main_container, self)
        self.current_view.pack(expand=True, fill='both')

    def show_login_view(self):
        """
        Muestra la vista de inicio de sesión.
        """
        self._clear_current_view()
        self.current_view = LoginView(self.main_container, self) 
        self.current_view.pack(expand=True, fill='both')

    def show_register_view(self):
        """
        Muestra la vista de registro de nuevo usuario.
        """
        self._clear_current_view()
        self.current_view = RegisterView(self.main_container, self)
        self.current_view.pack(expand=True, fill='both')

    def on_login_success(self, user_data): 
        """
        Método de callback llamado por LoginView cuando el inicio de sesión es exitoso.
        """
        self.logged_in_user_data = user_data 
        print(f"Usuario '{user_data['nombre_usuario']}' (ID: {user_data['id_usuario']}) ha iniciado sesión exitosamente.")
        self.show_dashboard_view() 

    def show_dashboard_view(self): 
        """
        Muestra la vista del dashboard principal.
        """
        self._clear_current_view()
        user_role = self.logged_in_user_data['rol'] if self.logged_in_user_data else None
        self.current_view = DashboardView(self.main_container, self, user_role=user_role)
        self.current_view.pack(expand=True, fill='both')

    def show_data_admin_view(self): # ¡Nuevo método para mostrar la vista de administración!
        """
        Muestra la vista de administración de datos.
        """
        if self.logged_in_user_data and self.logged_in_user_data['rol'] in ['Administrador', 'Coordinador']:
            self._clear_current_view()
            user_role = self.logged_in_user_data['rol']
            self.current_view = DataAdminView(self.main_container, self, user_role=user_role)
            self.current_view.pack(expand=True, fill='both')
        else:
            messagebox.showwarning("Acceso Denegado", "No tiene permisos para acceder a la administración de datos.")

    def show_reports_view(self): 
        """
        Muestra la vista de reportes.
        """
        if self.logged_in_user_data and self.logged_in_user_data['rol'] in ['Administrador', 'Coordinador', 'Profesor']:
            self._clear_current_view()
            # Instancia ReportView y pásale self (la MainApp)
            self.current_view = ReportView(self.main_container, self)
            self.current_view.pack(expand=True, fill='both')
            # Si estás usando el scroll vertical en MainApp, recuerda actualizar el layout
            # self.update_idletasks()
            # self.canvas.configure(scrollregion=self.canvas.bbox("all")) # Si aplicaste la solución Canvas
        else:
            messagebox.showwarning("Acceso Denegado", "No tiene permisos para ver los reportes.")


    def logout_and_show_login(self): 
        """
        Cierra la sesión del usuario actual y vuelve a la vista de login.
        """
        if self.controllers["user_controller"].logout_user():
            self.logged_in_user_data = None 
            print("Sesión cerrada exitosamente. Volviendo a la pantalla de login.")
            self.show_login_view()
        else:
            print("Error al cerrar sesión.") 

    def _clear_current_view(self):
        """
        Destruye la vista actualmente mostrada en el contenedor principal, si existe.
        """
        if self.current_view:
            self.current_view.destroy()
            self.current_view = None

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()