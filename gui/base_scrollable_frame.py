import tkinter as tk
from tkinter import ttk

class BaseScrollableFrame(ttk.Frame):
    """
    Un ttk.Frame que contiene un Canvas y un Scrollbar vertical,
    permitiendo que el contenido de su scrollable_frame interno se desplace.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs) # Permite pasar padding u otros kwargs

        # Crear un Canvas
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Crear un Scrollbar y vincularlo al Canvas
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")

        # Configurar el Canvas para usar el scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Crear un frame dentro del Canvas para el contenido real
        # Este es el frame donde todas las vistas hijas empaquetarán sus widgets
        self.scrollable_content_frame = ttk.Frame(self.canvas)

        # Vincular el scrollable_content_frame al Canvas
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_content_frame, anchor="nw")

        # Vincular eventos para ajustar el scrollbar y el área de desplazamiento
        self.scrollable_content_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Opcional: Permitir el desplazamiento con la rueda del ratón
        # self.canvas.bind_all("<MouseWheel>", self._on_mousewheel) # Ya se maneja en MainApp para el contexto global
        # self.canvas.bind_all("<Button-4>", self._on_mousewheel) 
        # self.canvas.bind_all("<Button-5>", self._on_mousewheel) 

    def _on_frame_configure(self, event):
        """Ajusta la región de desplazamiento del canvas cuando el frame de contenido cambia de tamaño."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        # print(f"Scrollable Frame size: {self.scrollable_content_frame.winfo_width()}x{self.scrollable_content_frame.winfo_height()}")

    def _on_canvas_configure(self, event):
        """Ajusta el ancho del frame de contenido para que coincida con el ancho del canvas."""
        # Esto es importante para que el contenido no se desborde horizontalmente sin necesidad
        canvas_width = event.width
        self.canvas.itemconfigure(self.canvas_window, width=canvas_width)
        # print(f"Canvas size: {canvas_width}x{event.height}")