# main.py (NUEVO ARCHIVO EN LA RAÍZ DEL PROYECTO)

# Importar la clase principal de tu aplicación
# Asegúrate de que esta ruta sea correcta desde la raíz del proyecto
from gui.main_app import MainApp

if __name__ == "__main__":
    # Crea la instancia de la aplicación y la inicia
    # MainApp ya hereda de ThemedTk (que es un Tkinter.Tk), por lo tanto,
    # ella misma es la ventana principal y no necesita que le pases 'root'.
    app = MainApp() # <--- ¡CORRECCIÓN AQUÍ! Se llama sin argumentos adicionales.
    app.mainloop()