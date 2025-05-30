# gui/views/register_view.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys

# Asegúrate de que el path a 'controllers' esté en PYTHONPATH o ajusta la importación
from controllers.user_controller import UserController

class RegisterView(tk.Frame):
    """
    Vista de registro de usuario para la aplicación.
    Permite a los usuarios crear una nueva cuenta.
    """
    def __init__(self, master, app_controller_callback):
        """
        Constructor de RegisterView.

        Args:
            master (tk.Tk or ttk.Frame): La ventana principal o frame padre.
            app_controller_callback (callable): Una función de callback en main_app.py
                                                 para navegar de vuelta al login
                                                 o al dashboard.
        """
        super().__init__(master)
        self.master = master
        self.app_controller_callback = app_controller_callback
        self.user_controller = UserController() # Instancia del controlador de usuario

        self.setup_ui()

    def setup_ui(self):
        """
        Configura los widgets de la interfaz de usuario para la pantalla de registro.
        """
        self.pack(expand=True, fill='both')
        
        register_frame = ttk.Frame(self, padding=20, borderwidth=2, relief="groove")
        register_frame.place(relx=0.5, rely=0.5, anchor='center')

        ttk.Label(register_frame, text="Crear Nuevo Usuario", font=("Arial", 16, "bold")).pack(pady=10)

        # Nombre de Usuario
        ttk.Label(register_frame, text="Nuevo Usuario:").pack(anchor='w', pady=(10, 0))
        self.new_username_entry = ttk.Entry(register_frame, width=30)
        self.new_username_entry.pack(pady=5)
        self.new_username_entry.focus_set()

        # Contraseña
        ttk.Label(register_frame, text="Contraseña:").pack(anchor='w', pady=(10, 0))
        self.new_password_entry = ttk.Entry(register_frame, show="*", width=30)
        self.new_password_entry.pack(pady=5)

        # Confirmar Contraseña
        ttk.Label(register_frame, text="Confirmar Contraseña:").pack(anchor='w', pady=(10, 0))
        self.confirm_password_entry = ttk.Entry(register_frame, show="*", width=30)
        self.confirm_password_entry.pack(pady=5)

        # Mensaje de error/éxito
        self.message_label = ttk.Label(register_frame, text="", foreground="red")
        self.message_label.pack(pady=5)

        # Botón de Registro
        register_button = ttk.Button(register_frame, text="Registrar", command=self.handle_register, width=20)
        register_button.pack(pady=(20, 5))

        # Botón de Volver al Login
        back_button = ttk.Button(register_frame, text="Volver al Login", command=self.app_controller_callback.show_login_view, width=20)
        back_button.pack(pady=5)

    def handle_register(self):
        """
        Maneja el evento de clic en el botón de registro.
        Valida los datos y llama al controlador para crear el usuario.
        """
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        self.message_label.config(text="", foreground="red") # Limpiar mensaje anterior

        if not username or not password or not confirm_password:
            self.message_label.config(text="Todos los campos son obligatorios.")
            return

        if password != confirm_password:
            self.message_label.config(text="Las contraseñas no coinciden.")
            self.new_password_entry.delete(0, tk.END)
            self.confirm_password_entry.delete(0, tk.END)
            return
        
        if len(password) < 6:
            self.message_label.config(text="La contraseña debe tener al menos 6 caracteres.")
            return

        user_id, error_message = self.user_controller.register_new_user(username, password, "Administrador")

        if user_id:
            messagebox.showinfo("Registro Exitoso", f"Usuario '{username}' creado con éxito!")
            # Después del registro, puedes llevarlo de vuelta al login o directamente al dashboard
            self.app_controller_callback.show_login_view() # O .on_login_success(user_id) si quieres loggearlo automáticamente
        else:
            self.message_label.config(text=error_message, foreground="red")
            messagebox.showerror("Error de Registro", error_message)