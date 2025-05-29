-- MySQL dump 10.13  Distrib 8.4.5, for Linux (x86_64)
--
-- Host: localhost    Database: expoferia
-- ------------------------------------------------------
-- Server version	8.4.5

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Certificates`
--

DROP TABLE IF EXISTS `Certificates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Certificates` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int DEFAULT NULL,
  `project_id` int DEFAULT NULL,
  `emition_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `student_id` (`student_id`),
  KEY `project_id` (`project_id`),
  CONSTRAINT `Certificates_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `Student` (`student_id`),
  CONSTRAINT `Certificates_ibfk_2` FOREIGN KEY (`project_id`) REFERENCES `Proyecto` (`project_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Certificates`
--

LOCK TABLES `Certificates` WRITE;
/*!40000 ALTER TABLE `Certificates` DISABLE KEYS */;
INSERT INTO `Certificates` VALUES (1,1,1,'2024-05-25 10:00:00'),(2,3,2,'2024-05-25 10:05:00'),(3,5,3,'2024-05-25 10:10:00'),(4,7,4,'2024-05-25 10:15:00'),(5,9,5,'2024-05-25 10:20:00');
/*!40000 ALTER TABLE `Certificates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Logs`
--

DROP TABLE IF EXISTS `Logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `action` text,
  `date_hour` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `Logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `Users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Logs`
--

LOCK TABLES `Logs` WRITE;
/*!40000 ALTER TABLE `Logs` DISABLE KEYS */;
INSERT INTO `Logs` VALUES (1,1,'Inicio de sesiÃ³n','2024-05-26 08:00:00'),(2,2,'CreaciÃ³n de proyecto','2024-05-26 08:05:00'),(3,3,'AsignaciÃ³n de estudiante','2024-05-26 08:10:00'),(4,4,'EmisiÃ³n de certificado','2024-05-26 08:15:00'),(5,5,'ActualizaciÃ³n de datos','2024-05-26 08:20:00');
/*!40000 ALTER TABLE `Logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Participations`
--

DROP TABLE IF EXISTS `Participations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Participations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int DEFAULT NULL,
  `project_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `student_id` (`student_id`),
  KEY `project_id` (`project_id`),
  CONSTRAINT `Participations_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `Student` (`student_id`),
  CONSTRAINT `Participations_ibfk_2` FOREIGN KEY (`project_id`) REFERENCES `Proyecto` (`project_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Participations`
--

LOCK TABLES `Participations` WRITE;
/*!40000 ALTER TABLE `Participations` DISABLE KEYS */;
INSERT INTO `Participations` VALUES (1,1,1),(2,2,1),(3,3,2),(4,4,2),(5,5,3),(6,6,3),(7,7,4),(8,8,4),(9,9,5),(10,10,5);
/*!40000 ALTER TABLE `Participations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Proyecto`
--

DROP TABLE IF EXISTS `Proyecto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Proyecto` (
  `project_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `register_date` date DEFAULT NULL,
  `teacher_id` int DEFAULT NULL,
  `estado` enum('activo','aprobado','rechazado') DEFAULT 'activo',
  PRIMARY KEY (`project_id`),
  KEY `teacher_id` (`teacher_id`),
  CONSTRAINT `Proyecto_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `Users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Proyecto`
--

LOCK TABLES `Proyecto` WRITE;
/*!40000 ALTER TABLE `Proyecto` DISABLE KEYS */;
INSERT INTO `Proyecto` VALUES (1,'Sistema de Inventario','Proyecto de control de inventario para laboratorio.','2024-05-20',3,'activo'),(2,'Plataforma Educativa','Proyecto educativo virtual.','2024-05-21',4,'activo'),(3,'App de Salud','AplicaciÃ³n de monitoreo de signos vitales.','2024-05-22',5,'activo'),(4,'Sistema de Biblioteca','Control digital de prÃ©stamos y devoluciones.','2024-05-23',4,'aprobado'),(5,'GestiÃ³n de Eventos','AplicaciÃ³n para coordinar eventos acadÃ©micos.','2024-05-24',3,'rechazado');
/*!40000 ALTER TABLE `Proyecto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Student`
--

DROP TABLE IF EXISTS `Student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Student` (
  `student_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `cedula` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`student_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Student`
--

LOCK TABLES `Student` WRITE;
/*!40000 ALTER TABLE `Student` DISABLE KEYS */;
INSERT INTO `Student` VALUES (1,'Carlos PÃ©rez','carlos@example.com','V12345678'),(2,'Ana Torres','ana@example.com','V23456789'),(3,'Luis GÃ³mez','luis@example.com','V34567890'),(4,'MarÃ­a LÃ³pez','maria@example.com','V45678901'),(5,'Pedro Rivas','pedro@example.com','V56789012'),(6,'LucÃ­a MartÃ­nez','lucia@example.com','V67890123'),(7,'Jorge SÃ¡nchez','jorge@example.com','V78901234'),(8,'Elena Ruiz','elena@example.com','V89012345'),(9,'AndrÃ©s Delgado','andres@example.com','V90123456'),(10,'SofÃ­a Romero','sofia@example.com','V01234567');
/*!40000 ALTER TABLE `Student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `role` enum('admin','coordinador','profesor') DEFAULT NULL,
  `password` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Users`
--

LOCK TABLES `Users` WRITE;
/*!40000 ALTER TABLE `Users` DISABLE KEYS */;
INSERT INTO `Users` VALUES (1,'Admin Principal','admin@expo.com','admin','e3afed0047b08059d0fada10f400c1e5'),(2,'Coordinador 1','coord1@expo.com','coordinador','e3afed0047b08059d0fada10f400c1e5'),(3,'Profesor A','profesor1@expo.com','profesor','e3afed0047b08059d0fada10f400c1e5'),(4,'Profesor B','profesor2@expo.com','profesor','e3afed0047b08059d0fada10f400c1e5'),(5,'Profesor C','profesor3@expo.com','profesor','e3afed0047b08059d0fada10f400c1e5');
/*!40000 ALTER TABLE `Users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-29  2:35:29
