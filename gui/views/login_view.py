# gui/views/login_view.py
import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox
import sys

# Asegúrate de que el path a 'controllers' esté en PYTHONPATH o ajusta la importación
from controllers.user_controller import UserController
from .background_image_frame import BackgroundImageFrame

class LoginView(BackgroundImageFrame):
    """
    Vista de inicio de sesión para la aplicación.
    Permite a los usuarios ingresar sus credenciales y autenticarse.
    """
    def __init__(self, master, app_controller_callback):
        """
        Constructor de LoginView.

        Args:
            master (tk.Tk or ttk.Frame): La ventana principal o frame padre.
            app_controller_callback (callable): Una función de callback en main_app.py
                                                 para notificar el éxito del login
                                                 y para navegar a otras vistas (ej. registro).
        """
        super().__init__(master)
        self.master = master
        self.app_controller_callback = app_controller_callback 
        self.user_controller = UserController() 

        self.setup_ui() 

    def setup_ui(self):
        """
        Configura los widgets de la interfaz de usuario para la pantalla de inicio de sesión.
        """
        self.pack(expand=True, fill='both')
        
        login_frame = ttk.Frame(self, padding=20, borderwidth=2, relief="groove")
        login_frame.place(relx=0.5, rely=0.5, anchor='center')

        ttk.Label(login_frame, text="Inicio de Sesión", font=("Arial", 16, "bold")).pack(pady=10)

        # Nombre de Usuario
        ttk.Label(login_frame, text="Usuario:").pack(anchor='w', pady=(10, 0))
        self.username_entry = ttk.Entry(login_frame, width=30)
        self.username_entry.pack(pady=5)
        self.username_entry.focus_set()

        # Contraseña
        ttk.Label(login_frame, text="Contraseña:").pack(anchor='w', pady=(10, 0))
        self.password_entry = ttk.Entry(login_frame, show="*", width=30)
        self.password_entry.pack(pady=5)

        # Botón de Inicio de Sesión
        login_button = ttk.Button(login_frame, text="Iniciar Sesión", command=self.handle_login, width=20)
        login_button.pack(pady=(20, 5)) 

        # Mensaje de error
        self.error_label = ttk.Label(login_frame, text="", foreground="red")
        self.error_label.pack(pady=5)

        # Botón de Crear Usuario
        create_user_button = ttk.Button(login_frame, text="Crear Nuevo Usuario", 
                                        command=self.app_controller_callback.show_register_view, 
                                        width=20)
        create_user_button.pack(pady=10)

        # Vincular la tecla Enter al botón de inicio de sesión
        self.master.bind('<Return>', lambda event=None: login_button.invoke())

    def handle_login(self):
        """
        Maneja el evento de clic en el botón de inicio de sesión.
        Obtiene las credenciales, las envía al controlador y maneja la respuesta.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()

        self.error_label.config(text="")

        # El login_user del controlador ahora devuelve el diccionario completo del usuario
        # O None y un mensaje de error.
        user_data, error_message = self.user_controller.login_user(username, password)

        if user_data: # Si user_data no es None, el login fue exitoso
            messagebox.showinfo("Login Exitoso", f"Bienvenido, {user_data['nombre_usuario']}!") # Usar el nombre del usuario
            # ¡IMPORTANTE!: Pasar el diccionario completo user_data al callback
            self.app_controller_callback.on_login_success(user_data) 
        else:
            self.error_label.config(text=error_message)
            messagebox.showerror("Error de Login", error_message)
            self.password_entry.delete(0, tk.END)