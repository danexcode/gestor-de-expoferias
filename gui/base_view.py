# gui/base_view.py
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk # Importar ttk para widgets temáticos
from ttkthemes import ThemedTk, ThemedStyle # Importar ThemedTk y ThemedStyle

class BaseView(tk.Toplevel):
    """
    Clase base para todas las ventanas (Toplevel) de la interfaz gráfica de Tkinter.
    Proporciona funcionalidades comunes como manejo de errores, mensajes de éxito,
    y una estructura básica para las ventanas, con soporte para temas de ttkthemes.
    """
    def __init__(self, master=None, title="Ventana de la Aplicación", style=None):
        """
        Inicializa la ventana base.

        Args:
            master (tk.Tk or tk.Toplevel, optional): La ventana padre.
            title (str): El título que aparecerá en la barra de la ventana.
            style (ttkthemes.ThemedStyle, optional): La instancia de ThemedStyle si la ventana padre
                                                    ya ha configurado los temas.
        """
        # Si master es None, esto implica que esta es la ventana principal de la aplicación.
        # En este caso, deberíamos usar ThemedTk como la clase base real para habilitar los temas globalmente.
        # Si master es una ventana ThemedTk o ThemedToplevel, Toplevel normal está bien,
        # pero para usar widgets ttk, siempre importamos ttk.
        
        # Para simplificar y asegurar que ttkthemes se aplique correctamente,
        # vamos a asumir que la ventana principal será ThemedTk, y el resto Toplevel normales
        # que usan el estilo global.

        if master is None:
            # Si esta es la ventana principal, ThemedTk es lo adecuado.
            # Sin embargo, BaseView ya hereda de tk.Toplevel.
            # Para manejar esto elegantemente, el "maestro" de la aplicación principal
            # debe ser directamente ThemedTk.
            # Este BaseView es para ventanas *secundarias* o subcomponentes.
            # La ventana principal de la aplicación (que hereda de ThemedTk)
            # NO DEBERÍA heredar directamente de BaseView en su __init__ super().
            # En su lugar, debería ser un ThemedTk y luego puede usar los métodos de BaseView
            # copiando su lógica o haciéndola una clase padre "conceptual".

            # RECONSIDERACIÓN: Es mejor que BaseView herede de Toplevel para ventanas secundarias.
            # La ventana principal (MainApp) será la que herede de ThemedTk.
            # BaseView no puede heredar directamente de ThemedTk y Toplevel a la vez de forma sencilla.
            super().__init__(master) # Llama al constructor de tk.Toplevel

            # Si no se pasó un estilo y no hay maestro, esta es probablemente la ventana raíz
            # y es una ThemedTk. Podemos verificar el tipo de master.
            # Pero para ser robustos, asumimos que el estilo lo gestiona la ventana raíz.
            self.style = style # Guardamos la instancia de estilo, que vendrá de ThemedTk
            if self.style is None and master is not None and isinstance(master, (ThemedTk, ThemedToplevel)):
                self.style = master.style # Heredar el estilo del maestro si existe y es temático
            elif self.style is None and master is None: # Si es la ventana raíz y no se le pasó estilo
                # Esto es un caso que no debería ocurrir si MainApp hereda de ThemedTk
                # y no de BaseView directamente.
                print("Advertencia: BaseView inicializada sin estilo en una posible ventana raíz. Los temas pueden no aplicarse correctamente.")
                self.style = ThemedStyle(self) # Crear un estilo para esta instancia

        else: # Si hay un maestro, esta es una ventana secundaria
            super().__init__(master)
            # Intentar obtener el estilo del maestro si no se pasó explícitamente
            if style is None and hasattr(master, 'style') and isinstance(master.style, ThemedStyle):
                self.style = master.style
            else:
                self.style = style # Usar el estilo pasado, o None si no hay ni uno ni otro

        self.title(title)
        self.geometry("800x600") # Tamaño por defecto, ajustable en subclases
        self.resizable(True, True) # Permite redimensionar
        self.protocol("WM_DELETE_WINDOW", self._on_closing) # Manejar el cierre de la ventana

        # Contenedor principal para los widgets, útil para padding y estructura
        # Usamos ttk.Frame para que se vea afectado por los temas
        self.main_frame = ttk.Frame(self, padding="10 10 10 10") # Usar padding de ttk
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.controllers = {} # Diccionario para almacenar instancias de controladores

    def _on_closing(self):
        """
        Método a ejecutar cuando el usuario intenta cerrar la ventana.
        Puede ser sobrescrito por subclases para lógica específica.
        Por defecto, simplemente cierra la ventana.
        """
        self.destroy()

    def set_controller(self, name, controller_instance):
        """
        Asigna una instancia de un controlador a esta vista.
        Permite que las vistas tengan acceso a los controladores que necesitan.

        Args:
            name (str): Un nombre clave para el controlador (ej. 'user_controller').
            controller_instance: La instancia del objeto controlador.
        """
        self.controllers[name] = controller_instance

    def get_controller(self, name):
        """
        Obtiene una instancia de un controlador previamente asignada.

        Args:
            name (str): El nombre clave del controlador.

        Returns:
            object: La instancia del controlador, o None si no se encuentra.
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
        Elimina todos los widgets de un frame dado, o del main_frame por defecto.
        Útil para cambiar el contenido de una ventana.
        """
        target_frame = frame if frame else self.main_frame
        for widget in target_frame.winfo_children():
            widget.destroy()

    def create_and_pack_label(self, parent, text, font=("Arial", 12), pady=5):
        """Crea y empaqueta un widget Label (ttk.Label para temas)."""
        label = ttk.Label(parent, text=text, font=font) # Usar ttk.Label
        label.pack(pady=pady)
        return label

    def create_and_pack_button(self, parent, text, command, font=("Arial", 10), pady=5):
        """Crea y empaqueta un widget Button (ttk.Button para temas)."""
        button = ttk.Button(parent, text=text, command=command) # Usar ttk.Button (font se configura con estilo)
        # Nota: ttk.Button no usa el argumento font directamente, se configura a través del estilo.
        # Podrías crear un estilo para el botón si necesitas cambiar la fuente.
        button.pack(pady=pady)
        return button

    def create_and_pack_entry(self, parent, label_text, default_value="", show_char=None):
        """Crea y empaqueta un Label y Entry juntos (ttk.Label, ttk.Entry para temas)."""
        frame = ttk.Frame(parent) # Usar ttk.Frame
        frame.pack(pady=5)
        
        ttk.Label(frame, text=label_text).pack(side=tk.LEFT, padx=5) # Usar ttk.Label
        entry = ttk.Entry(frame, show=show_char) # Usar ttk.Entry
        entry.insert(0, default_value)
        entry.pack(side=tk.LEFT, padx=5)
        return entry

    def run(self):
        """
        Inicia el bucle principal de la ventana.
        Este método solo debe llamarse en la ventana principal de la aplicación.
        """
        if self.master is None and isinstance(self, ThemedTk): # Solo si esta es la ventana raíz ThemedTk
            self.mainloop()
        elif self.master is None: # Si es Toplevel y no ThemedTk (no debería ser la raíz)
            print("Advertencia: run() llamado en una BaseView que no es ThemedTk y no tiene maestro. Esto puede no funcionar como se espera.")
            self.mainloop()
        else:
            # Para ventanas secundarias, no se llama mainloop()
            print("Info: mainloop() no es necesario para ventanas secundarias.")
            pass