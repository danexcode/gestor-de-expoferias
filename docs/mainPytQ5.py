import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QLineEdit, QPushButton, QGraphicsDropShadowEffect, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QIcon, QColor, QFont,QPixmap # Necesitamos QFont para ajustar las fuentes
from PyQt5.QtCore import Qt, QSize # QSize para especificar tamaños mínimos si es necesario
import os

class MiVentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.inicializarUI()

    def inicializarUI(self):
        self.setWindowTitle("UGMA - Expo Feria 2025")
        # Establece un tamaño inicial razonable para la ventana.
        # Con showMaximized() esto solo afectará el estado inicial antes de maximizar.
        self.setGeometry(100, 100, 1000, 700) # Aumentamos el tamaño inicial para que se parezca más a la imagen
        self.setStyleSheet('background-color: #E6F0FF;') # Fondo azul claro de la ventana
        
        # --- Configuración del icono de la ventana (se mantiene) ---
        # Asegúrate de que "Logo.png" exista en el mismo directorio o proporciona la ruta completa
        # if os.path.exists("Logo.png"):
        #     self.setWindowIcon(QIcon("Logo.png"))
        # else:
        #     print("Advertencia: El archivo 'Logo.png' no se encontró.")
        
        self.generar_GUI()
        self.show()

    def generar_GUI(self):
        self.is_Login = False

        # --- LAYOUT PRINCIPAL DE LA VENTANA ---
        # Este layout centralizará el QFrame grande.
        main_window_layout = QHBoxLayout(self) # Usamos QHBoxLayout para centrar horizontalmente
        
        main_window_layout.setContentsMargins(50, 40, 50, 40) # Márgenes para el QFrame dentro de la ventana

        self.setLayout(main_window_layout)


        # --- QFrame principal (el rectángulo grande con sombra) ---
        rectangulo = QFrame(self)
        rectangulo.setStyleSheet("background-color: #FFFFFF; border-radius: 20px;") # Fondo blanco, bordes redondeados
        
        # Sugerencia: Establecer un tamaño máximo para el rectángulo
        # Esto evitará que se estire demasiado cuando la ventana esté maximizada,
        # haciendo que se vea más parecido a la imagen.

        # --- APLICACIÓN DE LA SOMBRA (se mantiene igual) ---
        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setBlurRadius(50) # Sombra difusa
        shadow_effect.setColor(QColor(0, 0, 0, 80)) # Un poco menos opaca para un efecto más sutil
        shadow_effect.setXOffset(0)
        shadow_effect.setYOffset(10)
        rectangulo.setGraphicsEffect(shadow_effect)

        # --- LAYOUT HORIZONTAL DENTRO DEL RECTANGULO (Divide en dos mitades) ---
        rectangulo_content_layout = QHBoxLayout(rectangulo) # Este layout gestiona el contenido interno del 'rectangulo'
        rectangulo.setLayout(rectangulo_content_layout) # Es importante asignar este layout al QFrame 'rectangulo'

        # --- CONTENEDOR DE LA MITAD IZQUIERDA (Bienvenida y Logo) ---
        # Este contenedor es la sección azul oscuro de la imagen.
        contenedor_izquierda = QFrame(rectangulo)
        contenedor_izquierda.setStyleSheet("background-color: #003366; border-top-left-radius: 20px; border-bottom-left-radius: 20px;")
        # Nota: Los bordes redondeados solo se aplican a la izquierda para que coincida con la imagen.
        # El resto del 'rectangulo' se encargará de los bordes redondeados generales.
        
        # Creamos un layout vertical para el contenido de la izquierda
        layout_izquierda = QVBoxLayout(contenedor_izquierda)
        layout_izquierda.setAlignment(Qt.AlignCenter) # Centra el contenido vertical y horizontalmente

        # --- Espacio para el logo (si no quieres usar QLabel para la imagen, déjalo comentado) ---
        # Puedes añadir un QLabel para la imagen del logo
        logo_label = QLabel(contenedor_izquierda)
        # Aquí cargarías tu imagen. Por ahora, solo es un placeholder.
        # pixmap = QPixmap("path/to/your/logo.png")
        # logo_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setText("UGMA") # Texto temporal para el logo si no tienes la imagen
        logo_label.setStyleSheet("color: white; font-size: 36px; font-weight: bold;")
        logo_label.setAlignment(Qt.AlignCenter)
        layout_izquierda.addWidget(logo_label)

        # --- Espacio para el texto "Hola, Bienvenido" ---
        bienvenida_label = QLabel("Hola,\nBienvenido")
        bienvenida_label.setStyleSheet("color: white; font-size: 30px; font-weight: bold;")
        bienvenida_label.setAlignment(Qt.AlignCenter)
        layout_izquierda.addWidget(bienvenida_label)
        
        # Añade un "stretch" al final para empujar el contenido hacia el centro si el diseño lo permite
        layout_izquierda.addStretch(1) 
        # Ajusta los márgenes internos del contenedor izquierdo para el padding
        layout_izquierda.setContentsMargins(30, 50, 30, 50)


        # --- CONTENEDOR DE LA MITAD DERECHA (Formulario de Inicio de Sesión) ---
        # Este contenedor es la sección blanca con los campos de inicio de sesión.
        contenedor_derecha = QFrame(rectangulo)
        contenedor_derecha.setStyleSheet("background-color: #FFFFFF; border-top-right-radius: 20px; border-bottom-right-radius: 20px;")
        # Nota: Los bordes redondeados solo se aplican a la derecha aquí.

        # Creamos un layout vertical para el contenido de la derecha
        layout_derecha = QVBoxLayout(contenedor_derecha)
        layout_derecha.setAlignment(Qt.AlignCenter) # Centra el contenido verticalmente

        # --- Título "INICIAR SESION" ---
        titulo_sesion = QLabel("INICIAR SESION")
        titulo_sesion.setStyleSheet("font-size: 28px; font-weight: bold; color: #333333;") # Color gris oscuro
        titulo_sesion.setAlignment(Qt.AlignCenter)
        layout_derecha.addWidget(titulo_sesion)

        # Añadir un espaciador para separar el título del formulario
        layout_derecha.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Fixed))


        # --- Campo de Usuario ---
        label_usuario = QLabel("usuario")
        label_usuario.setStyleSheet("font-size: 16px; color: #555555;")
        layout_derecha.addWidget(label_usuario)

        input_usuario = QLineEdit()
        input_usuario.setPlaceholderText("SoyUnAdmin") # Texto de ejemplo
        input_usuario.setStyleSheet("""
            QLineEdit {
                font-size: 18px;
                padding: 10px;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                background-color: #F0F0F0; /* Un gris claro para el fondo del input */
            }
            QLineEdit:focus {
                border: 1px solid #0056b3; /* Color de borde al enfocar */
                background-color: #FFFFFF;
            }
        """)
        input_usuario.setFixedHeight(45) # Altura fija para el campo de entrada
        layout_derecha.addWidget(input_usuario)

        # Añadir un pequeño espaciador entre los campos
        layout_derecha.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # --- Campo de Contraseña ---
        label_contrasena = QLabel("contraseña")
        label_contrasena.setStyleSheet("font-size: 16px; color: #555555;")
        layout_derecha.addWidget(label_contrasena)

        input_contrasena = QLineEdit()
        input_contrasena.setPlaceholderText("****")
        input_contrasena.setEchoMode(QLineEdit.Password) # Para ocultar la contraseña
        input_contrasena.setStyleSheet("""
            QLineEdit {
                font-size: 18px;
                padding: 10px;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                background-color: #F0F0F0;
            }
            QLineEdit:focus {
                border: 1px solid #0056b3;
                background-color: #FFFFFF;
            }
        """)
        input_contrasena.setFixedHeight(45)
        layout_derecha.addWidget(input_contrasena)

        # Añadir un espaciador antes del botón de iniciar sesión
        layout_derecha.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # --- Botón "INICIAR SESION" ---
        boton_iniciar_sesion = QPushButton("INICIAR SESION")
        boton_iniciar_sesion.setStyleSheet("""
            QPushButton {
                background-color: #0056b3; /* Azul más oscuro */
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 12px 25px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #004085; /* Azul aún más oscuro al pasar el ratón */
            }
            QPushButton:pressed {
                background-color: #00285a; /* Azul muy oscuro al presionar */
            }
        """)
        boton_iniciar_sesion.setFixedSize(250, 50) # Tamaño fijo para el botón
        layout_derecha.addWidget(boton_iniciar_sesion, alignment=Qt.AlignCenter) # Centrar el botón

        # Añadir un espaciador después del botón
        layout_derecha.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # --- Enlace "¿Olvidaste tu contraseña?" ---
        olvido_contrasena = QLabel("<a href='#'>¿olvidaste tu contraseña?</a>")
        olvido_contrasena.setStyleSheet("font-size: 14px; color: #0056b3;") # Color de enlace azul
        olvido_contrasena.setAlignment(Qt.AlignCenter)
        olvido_contrasena.setOpenExternalLinks(True) # Esto permite que los enlaces abran una URL externa
        layout_derecha.addWidget(olvido_contrasena)

        # --- Enlace "¿No tienes una cuenta? Regístrate" ---
        no_tienes_cuenta = QLabel("<a href='#'>No tienes una cuenta? Regístrate</a>")
        no_tienes_cuenta.setStyleSheet("font-size: 14px; color: #0056b3;")
        no_tienes_cuenta.setAlignment(Qt.AlignCenter)
        no_tienes_cuenta.setOpenExternalLinks(True)
        layout_derecha.addWidget(no_tienes_cuenta)
        
        # Ajusta los márgenes internos del contenedor derecho para el padding
        layout_derecha.setContentsMargins(50, 50, 50, 50) # Márgenes para el padding dentro del formulario


        # --- Añadir los contenedores al layout principal del 'rectangulo' ---
        # Estos se estiran para ocupar el 50% del ancho cada uno
        rectangulo_content_layout.addWidget(contenedor_izquierda, 1) # Factor de estiramiento 1
        rectangulo_content_layout.addWidget(contenedor_derecha, 1) # Factor de estiramiento 1


        # Añadimos 'stretch' arriba y abajo para que el QFrame se centre verticalmente
        main_window_layout.addStretch(1)
        # Finalmente, añade el 'rectangulo' al layout principal (centralizado)
        main_window_layout.addWidget(rectangulo)
        main_window_layout.addStretch(1)


# El bloque if __name__ == "__main__": debe ir fuera de la clase MiVentanaPrincipal
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MiVentanaPrincipal()
    ventana.showMaximized() # Muestra la ventana maximizada
    sys.exit(app.exec_()) # Ejecuta la aplicación y espera a que termine