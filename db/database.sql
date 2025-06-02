-- Creación de la base de datos
CREATE DATABASE IF NOT EXISTS gestor_expoferias;

-- Usar la base de datos
USE gestor_expoferias;

-- 1. Tabla de usuarios
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(50) UNIQUE NOT NULL,
    contrasena_hash VARCHAR(255) NOT NULL,
    rol ENUM('Administrador', 'Coordinador', 'Profesor') NOT NULL,
    nombre_completo VARCHAR(100),
    correo_electronico VARCHAR(100) UNIQUE,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    ultima_sesion DATETIME
);

-- 2. Tabla de participantes (unifica estudiantes y docentes)
CREATE TABLE participantes (
    id_participante INT AUTO_INCREMENT PRIMARY KEY,
    tipo_participante ENUM('Estudiante', 'Docente') NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    cedula VARCHAR(20) UNIQUE,
    correo_electronico VARCHAR(100) UNIQUE,
    telefono VARCHAR(20),
    carrera VARCHAR(100) -- Campo específico para estudiantes, puede ser NULL para docentes
);

-- 3. Tabla de materias
CREATE TABLE materias (
    id_materia INT AUTO_INCREMENT PRIMARY KEY,
    codigo_materia VARCHAR(20) UNIQUE NOT NULL,
    nombre_materia VARCHAR(100) UNIQUE NOT NULL,
    creditos INT
);

-- 4. Tabla de periodos
CREATE TABLE periodos (
    id_periodo INT AUTO_INCREMENT PRIMARY KEY,
    nombre_periodo VARCHAR(50) UNIQUE NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

-- 5. Tabla de proyectos
CREATE TABLE proyectos (
    id_proyecto INT AUTO_INCREMENT PRIMARY KEY,
    id_periodo INT NOT NULL, -- Clave foránea a la tabla periodos
    id_materia INT NOT NULL,
    nombre_proyecto VARCHAR(255) NOT NULL,
    descripcion TEXT,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_periodo) REFERENCES periodos(id_periodo)
    ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_materia) REFERENCES materias(id_materia)
    ON DELETE RESTRICT ON UPDATE CASCADE
);

-- 6. Tabla de unión entre proyectos y participantes
CREATE TABLE proyectos_participantes (
    id_proyecto INT NOT NULL,
    id_participante INT NOT NULL,
    FOREIGN KEY (id_proyecto) REFERENCES proyectos(id_proyecto)
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_participante) REFERENCES participantes(id_participante)
    ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (id_proyecto, id_participante)
);
