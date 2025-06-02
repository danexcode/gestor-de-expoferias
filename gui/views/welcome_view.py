# gui/views/welcome_view.py
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk 
import os 
import sys

class WelcomeView(tk.Frame):
    """
    Vista de bienvenida para la aplicación con una imagen de fondo.
    Muestra un mensaje de bienvenida y un botón para ir a la pantalla de login.
    """
    def __init__(self, master, app_controller_callback):
        """
        Constructor de WelcomeView.

        Args:
            master (tk.Tk or ttk.Frame): La ventana principal o frame padre.
            app_controller_callback (callable): Una función de callback en main_app.py
                                                 para navegar a la vista de login.
        """
        super().__init__(master)
        self.master = master
        self.app_controller_callback = app_controller_callback
        
        # Cargar la imagen de fondo
        self.background_image_filename = "welcome_background.png" # Cambia la ruta a solo el nombre del archivo
        self.photo_image = None # Mantendrá la referencia a la imagen para evitar el garbage collection
        
        self.setup_ui() # Configura los elementos de la interfaz de usuario

    def load_background_image(self, width, height):
        """
        Carga y redimensiona la imagen de fondo para que se ajuste a la ventana.
        """
        # Detecta si está corriendo en PyInstaller
        if hasattr(sys, '_MEIPASS'):
            base_dir = os.path.join(sys._MEIPASS, "assets")
        else:
            base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
        full_image_path = os.path.join(base_dir, self.background_image_filename)

        try:
            original_image = Image.open(full_image_path)
            # Redimensionar la imagen para que coincida con el tamaño de la ventana/frame
            # Se usa Image.Resampling.LANCZOS para mejor calidad al redimensionar
            resized_image = original_image.resize((width, height), Image.Resampling.LANCZOS)
            self.photo_image = ImageTk.PhotoImage(resized_image)
            return self.photo_image
        except FileNotFoundError:
            print(f"ERROR: Archivo de imagen de fondo NO ENCONTRADO en la ruta: {full_image_path}")
            return None
        except Exception as e:
            print(f"ERROR: No se pudo cargar o procesar la imagen de fondo desde '{full_image_path}': {e}")
            return None

    def setup_ui(self):
        """
        Configura los widgets de la interfaz de usuario para la pantalla de bienvenida.
        """
        self.pack(expand=True, fill='both')

        # --- Etiqueta para la imagen de fondo ---
        self.background_label = tk.Label(self)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1) # Ocupa todo el espacio del frame WelcomeView

        # Vincular el evento de redimensionamiento para ajustar la imagen
        self.bind("<Configure>", self._on_resize)
        
        # Frame para el contenido (mensaje y botón) que irá encima de la imagen
        content_frame = ttk.Frame(self, padding=30, borderwidth=2, relief="solid") # Borde para visibilidad
        content_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Mensaje de bienvenida
        ttk.Label(content_frame, text="¡Bienvenido a tu Sistema de Gestión de Proyectos!", 
                  font=("Arial", 18, "bold")).pack(pady=(10, 10))
        
        ttk.Label(content_frame, text="Una herramienta para administrar tus proyectos universitarios de manera eficiente.", 
                  font=("Arial", 12)).pack(pady=(0, 20))

        # Botón para ir al Login
        login_button = ttk.Button(content_frame, text="Iniciar Sesión", 
                                  command=self.app_controller_callback.show_login_view, 
                                  width=25)
        login_button.pack(pady=15)

    def _on_resize(self, event):
        """
        Callback para el evento de redimensionamiento.
        Ajusta la imagen de fondo al nuevo tamaño de la ventana.
        """
        new_width = event.width
        new_height = event.height
        
        if new_width > 0 and new_height > 0: # Asegurarse de que no son cero
            # Cargar y redimensionar la imagen para el nuevo tamaño
            temp_image = self.load_background_image(new_width, new_height)
            if temp_image:
                self.background_label.config(image=temp_image)
                # No es necesario self.background_label.image = temp_image aquí
                # porque load_background_image ya guarda la referencia en self.photo_image
            else:
                # Si la imagen no se carga, establecer un fondo plano
                self.background_label.config(image='', background='white')