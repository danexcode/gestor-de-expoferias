# gui/base_view.py
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk 
# No es necesario ThemedTk y ThemedStyle aquí si ya MainApp hereda de ThemedTk
# y estamos usando ttk.Frame en las vistas.
# Si tus ventanas secundarias (Toplevel) necesitan su propio estilo, entonces sí.
# Pero para un scrollbar en una Toplevel estándar que usa el estilo global de MainApp,
# con ttk.Frame y ttk.Scrollbar es suficiente.

class BaseView(tk.Toplevel):
    """
    Clase base para todas las ventanas (Toplevel) de la interfaz gráfica de Tkinter.
    Proporciona funcionalidades comunes como manejo de errores, mensajes de éxito,
    y una estructura básica para las ventanas, con soporte para scrollbar.
    """
    def __init__(self, master=None, title="Ventana de la Aplicación"):
        """
        Inicializa la ventana base.

        Args:
            master (tk.Tk or tk.Toplevel, optional): La ventana padre.
            title (str): El título que aparecerá en la barra de la ventana.
        """
        super().__init__(master) # Llama al constructor de tk.Toplevel

        self.title(title)
        self.geometry("1024x768") # Tamaño por defecto, ajustable en subclases
        self.resizable(True, True) # Permite redimensionar
        self.protocol("WM_DELETE_WINDOW", self._on_closing) 

        self.controllers = {} 

        # --- Configuración del área con Scroll ---
        # Contenedor principal que contendrá el Canvas y el Scrollbar
        self.outer_frame = ttk.Frame(self, padding="10 10 10 10")
        self.outer_frame.pack(fill=tk.BOTH, expand=True)

        # Crear un Canvas
        self.canvas = tk.Canvas(self.outer_frame, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Crear un Scrollbar y vincularlo al Canvas
        self.scrollbar = ttk.Scrollbar(self.outer_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")

        # Configurar el Canvas para usar el scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Crear un frame dentro del Canvas para el contenido real
        # Este es el frame donde todas las vistas hijas empaquetarán sus widgets
        self.scrollable_frame = ttk.Frame(self.canvas)

        # Vincular el scrollable_frame al Canvas
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Vincular eventos para ajustar el scrollbar y el área de desplazamiento
        self.scrollable_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Opcional: Permitir el desplazamiento con la rueda del ratón
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel) # Para Windows y macOS
        self.canvas.bind_all("<Button-4>", self._on_mousewheel) # Para Linux (scroll up)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel) # Para Linux (scroll down)


    def _on_frame_configure(self, event):
        """Ajusta la región de desplazamiento del canvas cuando el frame de contenido cambia de tamaño."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        """Ajusta el ancho del frame de contenido para que coincida con el ancho del canvas."""
        # Esto es importante para que el contenido no se desborde horizontalmente sin necesidad
        canvas_width = event.width
        self.canvas.itemconfigure(self.canvas.winfo_children()[0], width=canvas_width)

    def _on_mousewheel(self, event):
        """Maneja el desplazamiento con la rueda del ratón."""
        if self.canvas.yview() == (0.0, 1.0): # Si no hay scrollbar activo o ya estás en el final
            return # No hacer nada

        if event.num == 4 or event.delta > 0: # Rueda hacia arriba
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0: # Rueda hacia abajo
            self.canvas.yview_scroll(1, "units")
        
        return "break" # Evita que el evento se propague más si lo manejamos

    def _on_closing(self):
        """
        Método a ejecutar cuando el usuario intenta cerrar la ventana.
        Por defecto, simplemente cierra la ventana.
        """
        self.destroy()

    def set_controller(self, name, controller_instance):
        """
        Asigna una instancia de un controlador a esta vista.
        Permite que las vistas tengan acceso a los controladores que necesitan.
        """
        self.controllers[name] = controller_instance

    def get_controller(self, name):
        """
        Obtiene una instancia de un controlador previamente asignada.
        """
        return self.controllers.get(name)

    def show_info(self, title, message):
        """Muestra un cuadro de diálogo de información."""
        messagebox.showinfo(title, message)

    def show_warning(self, title, message):
        """Muestra un cuadro de diálogo de advertencia."""
        messagebox.showwarning(title, message)

    def show_error(self, title, message):
        """Muestra un cuadro de diálogo de error."""
        messagebox.showerror(title, message)

    def ask_yes_no(self, title, question):
        """Muestra un cuadro de diálogo de sí/no y retorna True/False."""
        return messagebox.askyesno(title, question)

    def clear_widgets(self, frame=None):
        """
        Elimina todos los widgets de un frame dado, o del scrollable_frame por defecto.
        Útil para cambiar el contenido de una ventana.
        """
        target_frame = frame if frame else self.scrollable_frame
        for widget in target_frame.winfo_children():
            widget.destroy()

    def create_and_pack_label(self, parent, text, font=("Arial", 12), pady=5):
        """Crea y empaqueta un widget Label (ttk.Label para temas)."""
        label = ttk.Label(parent, text=text, font=font) 
        label.pack(pady=pady)
        return label

    def create_and_pack_button(self, parent, text, command, font=("Arial", 10), pady=5, style='TButton'):
        """Crea y empaqueta un widget Button (ttk.Button para temas)."""
        button = ttk.Button(parent, text=text, command=command, style=style) 
        button.pack(pady=pady)
        return button

    def create_and_pack_entry(self, parent, label_text, default_value="", show_char=None):
        """Crea y empaqueta un Label y Entry juntos (ttk.Label, ttk.Entry para temas)."""
        frame = ttk.Frame(parent) 
        frame.pack(pady=5)
        
        ttk.Label(frame, text=label_text).pack(side=tk.LEFT, padx=5) 
        entry = ttk.Entry(frame, show=show_char) 
        entry.insert(0, default_value)
        entry.pack(side=tk.LEFT, padx=5)
        return entry

    def run(self):
        """
        Inicia el bucle principal de la ventana.
        Este método solo debe llamarse en la ventana principal de la aplicación.
        """
        # Este método no es apropiado para BaseView ya que BaseView es un Toplevel
        # y MainApp (que es un ThemedTk) es la que llama mainloop().
        print("Advertencia: run() en BaseView no debe ser llamado directamente. MainApp gestiona el mainloop.")
        pass