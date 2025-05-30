# gui/main_app.py
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk

# Importar todos los controladores (ahora son clases)
from controllers.user_controller import UserController # Correcto ahora
from controllers.participant_controller import ParticipantController
from controllers.subject_controller import SubjectController
from controllers.period_controller import PeriodController
from controllers.project_controller import ProjectController
from controllers.report_controller import ReportController

# Importar BaseView para que las ventanas secundarias puedan heredar de ella
from gui.base_view import BaseView

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
        self.geometry("1024x768") # Tamaño inicial de la ventana principal
        self.resizable(True, True)

        # --- 1. Configuración del Tema ---
        self.set_theme("arc") # Establece un tema moderno para la aplicación

        # --- 2. Inicialización de Controladores ---
        # Ahora instanciamos las clases controladoras
        self.controllers = {
            "user_controller": UserController(),
            "participant_controller": ParticipantController(),
            "subject_controller": SubjectController(),
            "period_controller": PeriodController(),
            "project_controller": ProjectController(),
            "report_controller": ReportController()
        }

        # --- 3. Contenedor Principal para Vistas ---
        self.main_container = ttk.Frame(self, padding="10 10 10 10")
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        self.current_view = None # Para mantener una referencia a la vista actual

        # --- 4. Mostrar la primera vista (ej. Login) ---
        self.show_welcome_screen()

    def show_welcome_screen(self):
        """
        Muestra una pantalla de bienvenida simple como punto de partida.
        Aquí es donde normalmente cargarías tu vista de login o dashboard.
        """
        self.clear_main_container()
        
        welcome_label = ttk.Label(self.main_container, 
                                  text="¡Bienvenido al Sistema de Gestión de Proyectos!",
                                  font=("Arial", 20, "bold"))
        welcome_label.pack(pady=50)

        info_label = ttk.Label(self.main_container,
                               text="Esta es la ventana principal de tu aplicación.\n"
                                    "Pronto integraremos las vistas de login y CRUD.",
                               font=("Arial", 12))
        info_label.pack(pady=20)
        
        # Ejemplo de botón para probar el tema
        # Aquí pasamos 'self' (la instancia de MainApp, que es ThemedTk) como master
        # y su estilo se hereda automáticamente por la BaseView.
        test_button = ttk.Button(self.main_container, text="Probar Ventana Secundaria", 
                                 command=lambda: BaseView(self, title="Ventana de Prueba").show_info("Prueba", "¡Esta es una ventana secundaria con el tema!"))
        test_button.pack(pady=20)


    def clear_main_container(self):
        """
        Limpia todos los widgets del contenedor principal.
        Útil antes de cargar una nueva vista.
        """
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def start(self):
        """
        Inicia el bucle principal de la aplicación.
        """
        self.mainloop()

# --- Punto de entrada de la aplicación ---
if __name__ == "__main__":
    app = MainApp()
    app.start()