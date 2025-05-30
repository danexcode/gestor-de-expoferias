# gui/views/login_view.py
import tkinter as tk
from tkinter import messagebox
import sys

# Asegúrate de que el path a 'controllers' esté en PYTHONPATH o ajusta la importación
# Si ejecutas desde 'run.py' en la raíz del proyecto, esta importación debería funcionar.
# Si tienes problemas, puedes añadir esto:
# sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from controllers.user_controller import UserController

class LoginView(tk.Frame):
    """
    Vista de inicio de sesión para la aplicación.
    Permite a los usuarios ingresar sus credenciales y autenticarse.
    """
    def __init__(self, master, app_controller_callback):
        """
        Constructor de LoginView.

        Args:
            master (tk.Tk or tk.Frame): La ventana principal o frame padre.
            app_controller_callback (callable): Una función de callback en main_app.py
                                                 para notificar el éxito del login
                                                 y pasar el user_id.
        """
        super().__init__(master)
        self.master = master
        self.app_controller_callback = app_controller_callback
        self.user_controller = UserController() # Instancia del controlador de usuario

        self.setup_ui() # Configura los elementos de la interfaz de usuario

    def setup_ui(self):
        """
        Configura los widgets de la interfaz de usuario para la pantalla de inicio de sesión.
        """
        # Configuración del frame principal para centrar el contenido
        self.pack(expand=True, fill='both') # Hace que el frame ocupe todo el espacio disponible
        
        # Frame para centrar los widgets de login
        login_frame = tk.Frame(self, padx=20, pady=20, bd=2, relief="groove")
        login_frame.place(relx=0.5, rely=0.5, anchor='center') # Centra el frame en la ventana

        tk.Label(login_frame, text="Inicio de Sesión", font=("Arial", 16, "bold")).pack(pady=10)

        # Nombre de Usuario
        tk.Label(login_frame, text="Usuario:").pack(anchor='w', pady=(10, 0))
        self.username_entry = tk.Entry(login_frame, width=30)
        self.username_entry.pack(pady=5)
        self.username_entry.focus_set() # Pone el foco en este campo al iniciar

        # Contraseña
        tk.Label(login_frame, text="Contraseña:").pack(anchor='w', pady=(10, 0))
        self.password_entry = tk.Entry(login_frame, show="*", width=30) # show="*" para ocultar contraseña
        self.password_entry.pack(pady=5)

        # Botón de Inicio de Sesión
        login_button = tk.Button(login_frame, text="Iniciar Sesión", command=self.handle_login, width=20, height=2)
        login_button.pack(pady=20)

        # Mensaje de error
        self.error_label = tk.Label(login_frame, text="", fg="red")
        self.error_label.pack(pady=5)

        # Vincular la tecla Enter al botón de inicio de sesión
        self.master.bind('<Return>', lambda event=None: login_button.invoke())

    def handle_login(self):
        """
        Maneja el evento de clic en el botón de inicio de sesión.
        Obtiene las credenciales, las envía al controlador y maneja la respuesta.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Limpiar cualquier mensaje de error anterior
        self.error_label.config(text="")

        # Usar el controlador para intentar el login
        user_id, error_message = self.user_controller.login_user(username, password)

        if user_id:
            messagebox.showinfo("Login Exitoso", f"Bienvenido, {username}!")
            # Notificar al main_app que el login fue exitoso, pasando el user_id
            self.app_controller_callback(user_id)
        else:
            # Mostrar el mensaje de error del controlador
            self.error_label.config(text=error_message)
            messagebox.showerror("Error de Login", error_message)
            # Limpiar campos o solo la contraseña por seguridad
            self.password_entry.delete(0, tk.END)