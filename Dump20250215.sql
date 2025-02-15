-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: appraisal_system
-- ------------------------------------------------------
-- Server version	8.0.34

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `acad_years`
--

DROP TABLE IF EXISTS `acad_years`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `acad_years` (
  `year_id` int NOT NULL AUTO_INCREMENT,
  `acad_years` varchar(45) DEFAULT NULL,
  `form_id` int DEFAULT NULL,
  `user_id` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`year_id`),
  UNIQUE KEY `year_id_UNIQUE` (`year_id`),
  UNIQUE KEY `form_id_UNIQUE` (`form_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acad_years`
--

LOCK TABLES `acad_years` WRITE;
/*!40000 ALTER TABLE `acad_years` DISABLE KEYS */;
INSERT INTO `acad_years` VALUES (1,'2024/25',932757,'123456'),(2,'2021/22',286196,'123456'),(3,'2032/33',246856,'123456'),(4,'2031/32',911545,'123456'),(5,'2024/25',130525,'124'),(6,'2024/25',515988,'125'),(7,'2024/25',895485,'321'),(9,'2024/25',918700,'128'),(10,'2021/22',768631,'123'),(11,'2027/28',802018,'123'),(12,'2023/24',708474,'123'),(14,'2024/25',329472,'123');
/*!40000 ALTER TABLE `acad_years` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `certifications`
--

DROP TABLE IF EXISTS `certifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `certifications` (
  `form_id` varchar(45) DEFAULT NULL,
  `name` varchar(45) DEFAULT NULL,
  `uploads` varchar(245) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `certifications`
--

LOCK TABLES `certifications` WRITE;
/*!40000 ALTER TABLE `certifications` DISABLE KEYS */;
/*!40000 ALTER TABLE `certifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contribution_to_society`
--

DROP TABLE IF EXISTS `contribution_to_society`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contribution_to_society` (
  `form_id` varchar(45) DEFAULT NULL,
  `semester` varchar(45) DEFAULT NULL,
  `activity` varchar(45) DEFAULT NULL,
  `points` varchar(45) DEFAULT NULL,
  `order_cpy` varchar(45) DEFAULT NULL,
  `uploads` varchar(225) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contribution_to_society`
--

LOCK TABLES `contribution_to_society` WRITE;
/*!40000 ALTER TABLE `contribution_to_society` DISABLE KEYS */;
INSERT INTO `contribution_to_society` VALUES ('515988','I','awd','3','awd','C:\\Users\\mayank salvi\\Desktop\\appraisal system\\uploads\\e_reciept.pdf');
/*!40000 ALTER TABLE `contribution_to_society` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `copyright`
--

DROP TABLE IF EXISTS `copyright`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `copyright` (
  `form_id` varchar(45) DEFAULT NULL,
  `name` varchar(45) DEFAULT NULL,
  `month` varchar(45) DEFAULT NULL,
  `reg_no` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `copyright`
--

LOCK TABLES `copyright` WRITE;
/*!40000 ALTER TABLE `copyright` DISABLE KEYS */;
INSERT INTO `copyright` VALUES ('515988','awd','awd','awd');
/*!40000 ALTER TABLE `copyright` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `department_act`
--

DROP TABLE IF EXISTS `department_act`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `department_act` (
  `form_id` varchar(45) DEFAULT NULL,
  `semester` varchar(45) DEFAULT NULL,
  `activity` varchar(45) DEFAULT NULL,
  `points` varchar(45) DEFAULT NULL,
  `order_cpy` varchar(45) DEFAULT NULL,
  `uploads` varchar(255) DEFAULT NULL,
  `assessment` varchar(45) DEFAULT NULL,
  `feedback` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `department_act`
--

LOCK TABLES `department_act` WRITE;
/*!40000 ALTER TABLE `department_act` DISABLE KEYS */;
INSERT INTO `department_act` VALUES ('515988','I','adw','3','awd','C:\\Users\\mayank salvi\\Desktop\\appraisal system\\uploads\\Exp7_Minor.pdf',NULL,NULL),('515988','I','abc','3','abc',NULL,NULL,NULL),('515988','','adadf','2','assf',NULL,NULL,NULL);
/*!40000 ALTER TABLE `department_act` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `external_projects`
--

DROP TABLE IF EXISTS `external_projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `external_projects` (
  `form_id` varchar(45) DEFAULT NULL,
  `role` varchar(45) DEFAULT NULL,
  `desc` varchar(45) DEFAULT NULL,
  `contribution` varchar(45) DEFAULT NULL,
  `university` varchar(45) DEFAULT NULL,
  `duration` varchar(45) DEFAULT NULL,
  `comments` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `external_projects`
--

LOCK TABLES `external_projects` WRITE;
/*!40000 ALTER TABLE `external_projects` DISABLE KEYS */;
/*!40000 ALTER TABLE `external_projects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback` (
  `form_id` varchar(45) NOT NULL,
  `feedback` varchar(425) DEFAULT NULL,
  PRIMARY KEY (`form_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback`
--

LOCK TABLES `feedback` WRITE;
/*!40000 ALTER TABLE `feedback` DISABLE KEYS */;
/*!40000 ALTER TABLE `feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `form1_tot`
--

DROP TABLE IF EXISTS `form1_tot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `form1_tot` (
  `form_id` int NOT NULL,
  `total` varchar(45) DEFAULT NULL,
  `teaching` varchar(45) DEFAULT NULL,
  `feedback` varchar(45) DEFAULT NULL,
  `hodas1` varchar(45) DEFAULT NULL,
  `hodas2` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`form_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `form1_tot`
--

LOCK TABLES `form1_tot` WRITE;
/*!40000 ALTER TABLE `form1_tot` DISABLE KEYS */;
INSERT INTO `form1_tot` VALUES (130525,'0','0','0',NULL,NULL),(515988,'0','0','0',NULL,NULL);
/*!40000 ALTER TABLE `form1_tot` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `form2_tot`
--

DROP TABLE IF EXISTS `form2_tot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `form2_tot` (
  `form_id` int NOT NULL,
  `total` varchar(45) DEFAULT NULL,
  `dept` varchar(45) DEFAULT NULL,
  `institute` varchar(45) DEFAULT NULL,
  `hodas3` varchar(45) DEFAULT NULL,
  `hodas4` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`form_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `form2_tot`
--

LOCK TABLES `form2_tot` WRITE;
/*!40000 ALTER TABLE `form2_tot` DISABLE KEYS */;
INSERT INTO `form2_tot` VALUES (515988,'10','5','5',NULL,NULL);
/*!40000 ALTER TABLE `form2_tot` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `form3_tot`
--

DROP TABLE IF EXISTS `form3_tot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `form3_tot` (
  `form_id` int NOT NULL,
  `total` varchar(45) DEFAULT NULL,
  `acr` varchar(45) DEFAULT NULL,
  `society` varchar(45) DEFAULT NULL,
  `hodas5` varchar(45) DEFAULT NULL,
  `hodas6` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`form_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `form3_tot`
--

LOCK TABLES `form3_tot` WRITE;
/*!40000 ALTER TABLE `form3_tot` DISABLE KEYS */;
INSERT INTO `form3_tot` VALUES (515988,'13','10','3',NULL,NULL);
/*!40000 ALTER TABLE `form3_tot` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `institute_act`
--

DROP TABLE IF EXISTS `institute_act`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `institute_act` (
  `form_id` varchar(45) DEFAULT NULL,
  `semester` varchar(45) DEFAULT NULL,
  `activity` varchar(45) DEFAULT NULL,
  `points` varchar(45) DEFAULT NULL,
  `order_cpy` varchar(45) DEFAULT NULL,
  `uploads` varchar(255) DEFAULT NULL,
  `assessment` varchar(45) DEFAULT NULL,
  `feedback` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `institute_act`
--

LOCK TABLES `institute_act` WRITE;
/*!40000 ALTER TABLE `institute_act` DISABLE KEYS */;
INSERT INTO `institute_act` VALUES ('515988','II','awda','3','awd','C:\\Users\\mayank salvi\\Desktop\\appraisal system\\uploads\\assignment_1.pdf',NULL,NULL),('515988','II','abcd','3','agc',NULL,NULL,NULL),('515988','I','asds','2','adf',NULL,NULL,NULL);
/*!40000 ALTER TABLE `institute_act` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mem_uni`
--

DROP TABLE IF EXISTS `mem_uni`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mem_uni` (
  `form_id` varchar(45) DEFAULT NULL,
  `name` varchar(45) DEFAULT NULL,
  `roles` varchar(45) DEFAULT NULL,
  `designation` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mem_uni`
--

LOCK TABLES `mem_uni` WRITE;
/*!40000 ALTER TABLE `mem_uni` DISABLE KEYS */;
/*!40000 ALTER TABLE `mem_uni` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resource_person`
--

DROP TABLE IF EXISTS `resource_person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `resource_person` (
  `form_id` varchar(45) DEFAULT NULL,
  `name` varchar(45) DEFAULT NULL,
  `dept` varchar(45) DEFAULT NULL,
  `name_oi` varchar(45) DEFAULT NULL,
  `num_op` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resource_person`
--

LOCK TABLES `resource_person` WRITE;
/*!40000 ALTER TABLE `resource_person` DISABLE KEYS */;
/*!40000 ALTER TABLE `resource_person` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `self_imp`
--

DROP TABLE IF EXISTS `self_imp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `self_imp` (
  `form_id` varchar(45) DEFAULT NULL,
  `title` varchar(45) DEFAULT NULL,
  `month` varchar(45) DEFAULT NULL,
  `name_of_conf` varchar(45) DEFAULT NULL,
  `issn` varchar(45) DEFAULT NULL,
  `co_auth` varchar(45) DEFAULT NULL,
  `link` varchar(225) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `self_imp`
--

LOCK TABLES `self_imp` WRITE;
/*!40000 ALTER TABLE `self_imp` DISABLE KEYS */;
INSERT INTO `self_imp` VALUES ('515988','awd','awd','awd','awd','awd','wad');
/*!40000 ALTER TABLE `self_imp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students_feedback`
--

DROP TABLE IF EXISTS `students_feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students_feedback` (
  `form_id` int DEFAULT NULL,
  `semester` varchar(45) DEFAULT NULL,
  `course_code` varchar(45) DEFAULT NULL,
  `total_points` int DEFAULT NULL,
  `points_obtained` varchar(45) DEFAULT NULL,
  `uploads` varchar(255) DEFAULT NULL,
  `assessment` varchar(45) DEFAULT NULL,
  `srno` int DEFAULT NULL,
  KEY `form_id_idx` (`form_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students_feedback`
--

LOCK TABLES `students_feedback` WRITE;
/*!40000 ALTER TABLE `students_feedback` DISABLE KEYS */;
INSERT INTO `students_feedback` VALUES (515988,'I','Mathematics-I',5,'3',NULL,NULL,1),(515988,'I','Physics',5,'2',NULL,NULL,2);
/*!40000 ALTER TABLE `students_feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teaching_process`
--

DROP TABLE IF EXISTS `teaching_process`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teaching_process` (
  `form_id` int DEFAULT NULL,
  `semester` varchar(45) DEFAULT NULL,
  `course_code` varchar(45) DEFAULT NULL,
  `classes_scheduled` int DEFAULT NULL,
  `classes_held` int DEFAULT NULL,
  `totalpoints` int DEFAULT NULL,
  `assessment` varchar(45) DEFAULT NULL,
  `srno` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teaching_process`
--

LOCK TABLES `teaching_process` WRITE;
/*!40000 ALTER TABLE `teaching_process` DISABLE KEYS */;
INSERT INTO `teaching_process` VALUES (515988,'I','Mathematics-I',5,4,0,NULL,1),(515988,'I','Physics',5,3,0,NULL,2);
/*!40000 ALTER TABLE `teaching_process` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `total`
--

DROP TABLE IF EXISTS `total`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `total` (
  `form_id` int NOT NULL,
  `acad_years` varchar(45) DEFAULT NULL,
  `total` varchar(45) DEFAULT NULL,
  `hodtotal` varchar(45) DEFAULT NULL,
  `user_id` varchar(45) DEFAULT NULL,
  `dept` varchar(45) DEFAULT NULL,
  `name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`form_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `total`
--

LOCK TABLES `total` WRITE;
/*!40000 ALTER TABLE `total` DISABLE KEYS */;
INSERT INTO `total` VALUES (123456,'2024/25','70','68','128','IT','gandhar'),(515988,'2024/25','58','19','125','IT','mayank salvi'),(654321,'2023/24','72','70','213','IT','omkar');
/*!40000 ALTER TABLE `total` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `userid` int NOT NULL,
  `gmail` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  `role` varchar(45) NOT NULL,
  `dept` varchar(45) NOT NULL,
  `name` varchar(45) NOT NULL,
  `designation` varchar(45) DEFAULT NULL,
  `d_o_j` varchar(45) DEFAULT NULL,
  `dob` varchar(45) DEFAULT NULL,
  `edu_q` varchar(45) DEFAULT NULL,
  `exp` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`userid`),
  UNIQUE KEY `userid_UNIQUE` (`userid`),
  UNIQUE KEY `gmail_UNIQUE` (`gmail`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'principal@apsit.edu.in','Salvi@123','Principal','NULL','xyz','Principal','2024-09-01','2004-12-03','phd','10 years'),(123,'mayank@apsit.edu.in','Salvi@123','Faculty','IT','mayank','Assistant Professor','2024-09-29','2024-09-25','btech','nothing'),(124,'mayanksalvi@apsit.edu.in','Salvi@123','Faculty','IT','mayank salvi','Assistant Professor','2024-09-30','2024-10-06','Btech','3 years'),(125,'mayanksalvi180@apsit.edu.in','Salvi@123','Faculty','IT','mayank salvi','Assistant Professor','2024-09-30','2024-10-07','btech','3 years'),(127,'mayanksalvi180@gmail.com','abcd1234','Faculty','IT','vb','assistant professor','2024-10-16','2024-05-07','ME','5 Yrs'),(128,'xyz@apsit.edu.in','Salvi@123','Faculty','IT','gandhar','Assistant Professor','2024-10-01','2024-10-07','be','nothing\r\n'),(213,'hod1@apsit.edu.in','Salvi@123','Higher Authority','IT','omkar','Head of Department','2024-10-06','2024-09-30','phd','9 years'),(321,'aniruddha@apsit.edu.in','Salvi@123','Faculty','CS','aniruddha sangle','Professor','2024-09-30','2024-10-06','btech ','3 years '),(412,'dhanashreemayank@gmail.com','mayank@123','Faculty','CS','mayank','student','2024-09-03','2024-10-06','btech','4 years'),(456,'rrr@apsit.edu.in','Salvi@123','Faculty','MECH','m','Professor','2024-10-24','2024-10-31','i','i'),(12345,'gandhar@apsit.edu.in','Salvi@123','Faculty','MECH','gandhar rane','Professor','2019-06-28','1997-08-20','PHD','very good'),(123456,'abcd@gmail.com','abcd1234','Faculty','IT','mayank','student','2024-09-25','2004-12-03','12th pass','nothing'),(654321,'hod@gmail.com','abcd1234','Head of Dept.','IT','mayank','HOD','2024-09-01','2004-12-03','Phd','9 years');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-02-15 11:32:35
