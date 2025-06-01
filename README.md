# Gestor de Expoferias

Aplicación de gestión para eventos expoferias con funcionalidades de administración de usuarios, participantes, proyectos y generación de reportes.

## Requisitos Previos

- Python 3.8 o superior
- MySQL Server 8.0 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd gestor-expoferias
   ```

2. **Crear un entorno virtual (recomendado)**
   ```bash
   # En Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # En Linux/MacOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar la base de datos**
   - Crear una base de datos MySQL llamada `gestor_expoferias`
   - Importar el esquema inicial desde `db/database.sql`

## Ejecutar en modo desarrollo

```bash
python launch.py
```

## Construir ejecutable

Para crear un ejecutable con PyInstaller:

1. Instalar PyInstaller si no está instalado:
   ```bash
   pip install pyinstaller
   ```

2. Ejecutar el script de construcción:
   ```bash
   python build.py
   ```

3. El ejecutable se creará en el directorio `dist/GestorExpoferias/`

## Estructura del Proyecto

```
gestor-expoferias/
├── assets/               # Recursos estáticos (imágenes, iconos, etc.)
├── controllers/          # Controladores de la aplicación
├── db/                   # Archivos de base de datos y migraciones
├── gui/                  # Interfaz gráfica
│   ├── views/            # Vistas de la aplicación
│   └── main_app.py       # Aplicación principal
├── models/               # Modelos de datos
├── templates/            # Plantillas para correos y reportes
├── .env.example          # Plantilla de variables de entorno
├── build.py              # Script de construcción
├── config.py             # Configuración de la aplicación
├── launch.py             # Punto de entrada principal
├── README.md             # Este archivo
└── requirements.txt      # Dependencias del proyecto
```

## Configuración

1. Copiar `.env.example` a `.env` y configurar las variables de entorno necesarias.
2. Asegurarse de que la base de datos esté configurada correctamente en `config.py`.

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Soporte

Para soporte, por favor abra un issue en el repositorio o contacte al equipo de desarrollo.
