-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: qlnhasachdb
-- ------------------------------------------------------
-- Server version	8.0.19

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
-- Table structure for table `chi_tiet_hoa_don`
--

DROP TABLE IF EXISTS `chi_tiet_hoa_don`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chi_tiet_hoa_don` (
  `id` int NOT NULL AUTO_INCREMENT,
  `so_luong_mua` int NOT NULL,
  `don_gia` float NOT NULL,
  `id_sach` int NOT NULL,
  `id_hoadon` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_sach` (`id_sach`),
  KEY `id_hoadon` (`id_hoadon`),
  CONSTRAINT `chi_tiet_hoa_don_ibfk_1` FOREIGN KEY (`id_sach`) REFERENCES `sach` (`id`),
  CONSTRAINT `chi_tiet_hoa_don_ibfk_2` FOREIGN KEY (`id_hoadon`) REFERENCES `hoa_don` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chi_tiet_hoa_don`
--

LOCK TABLES `chi_tiet_hoa_don` WRITE;
/*!40000 ALTER TABLE `chi_tiet_hoa_don` DISABLE KEYS */;
/*!40000 ALTER TABLE `chi_tiet_hoa_don` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chi_tiet_nhap_phieu_sach`
--

DROP TABLE IF EXISTS `chi_tiet_nhap_phieu_sach`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chi_tiet_nhap_phieu_sach` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_phieu` int NOT NULL,
  `so_luong` int NOT NULL,
  `id_sachnhap` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_phieu` (`id_phieu`),
  KEY `id_sachnhap` (`id_sachnhap`),
  CONSTRAINT `chi_tiet_nhap_phieu_sach_ibfk_1` FOREIGN KEY (`id_phieu`) REFERENCES `phieu_nhap_sach` (`id`),
  CONSTRAINT `chi_tiet_nhap_phieu_sach_ibfk_2` FOREIGN KEY (`id_sachnhap`) REFERENCES `sach` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chi_tiet_nhap_phieu_sach`
--

LOCK TABLES `chi_tiet_nhap_phieu_sach` WRITE;
/*!40000 ALTER TABLE `chi_tiet_nhap_phieu_sach` DISABLE KEYS */;
/*!40000 ALTER TABLE `chi_tiet_nhap_phieu_sach` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hoa_don`
--

DROP TABLE IF EXISTS `hoa_don`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hoa_don` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ngay_nhap` date DEFAULT NULL,
  `id_khachhang` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_khachhang` (`id_khachhang`),
  CONSTRAINT `hoa_don_ibfk_1` FOREIGN KEY (`id_khachhang`) REFERENCES `khach_hang` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hoa_don`
--

LOCK TABLES `hoa_don` WRITE;
/*!40000 ALTER TABLE `hoa_don` DISABLE KEYS */;
/*!40000 ALTER TABLE `hoa_don` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `khach_hang`
--

DROP TABLE IF EXISTS `khach_hang`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `khach_hang` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ho_ten` varchar(100) NOT NULL,
  `ngay_sinh` date DEFAULT NULL,
  `dia_chi` varchar(150) DEFAULT NULL,
  `dien_thoai` varchar(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `khach_hang`
--

LOCK TABLES `khach_hang` WRITE;
/*!40000 ALTER TABLE `khach_hang` DISABLE KEYS */;
/*!40000 ALTER TABLE `khach_hang` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `phieu_nhap_sach`
--

DROP TABLE IF EXISTS `phieu_nhap_sach`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `phieu_nhap_sach` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ngay_nhap` date DEFAULT NULL,
  `id_thukho` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_thukho` (`id_thukho`),
  CONSTRAINT `phieu_nhap_sach_ibfk_1` FOREIGN KEY (`id_thukho`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `phieu_nhap_sach`
--

LOCK TABLES `phieu_nhap_sach` WRITE;
/*!40000 ALTER TABLE `phieu_nhap_sach` DISABLE KEYS */;
INSERT INTO `phieu_nhap_sach` VALUES (4,'2020-12-04',1);
/*!40000 ALTER TABLE `phieu_nhap_sach` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `phieu_thu_tien`
--

DROP TABLE IF EXISTS `phieu_thu_tien`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `phieu_thu_tien` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ngay_thu_tien` date NOT NULL,
  `tong_tien_thu` float NOT NULL,
  `id_user` int NOT NULL,
  `id_khachhang` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_user` (`id_user`),
  KEY `id_khachhang` (`id_khachhang`),
  CONSTRAINT `phieu_thu_tien_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `user` (`id`),
  CONSTRAINT `phieu_thu_tien_ibfk_2` FOREIGN KEY (`id_khachhang`) REFERENCES `khach_hang` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `phieu_thu_tien`
--

LOCK TABLES `phieu_thu_tien` WRITE;
/*!40000 ALTER TABLE `phieu_thu_tien` DISABLE KEYS */;
/*!40000 ALTER TABLE `phieu_thu_tien` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sach`
--

DROP TABLE IF EXISTS `sach`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sach` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ten_sach` varchar(250) NOT NULL,
  `tac_gia` varchar(100) NOT NULL,
  `the_loai` varchar(100) NOT NULL,
  `don_gia` float NOT NULL,
  `so_luong` int NOT NULL,
  `hinh` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sach`
--

LOCK TABLES `sach` WRITE;
/*!40000 ALTER TABLE `sach` DISABLE KEYS */;
INSERT INTO `sach` VALUES (2,'Whale Day','Billy Collins','tuổi teen',50000,10,'images/sach1.jpg'),(3,'The Vanishing Half','Brit Bennett','Ngoại văn',90000,10,'images/sach2.jpg'),(4,'A Promise Land','Barack Obama','Tự truyện',100000,10,'images/sach3.jpg'),(5,'Leave the World Behind','Rumaan Alam','Novel',120000,10,'images/sach4.jpg'),(6,'Stamped: Racism, Antiracism, and You: A Remix of the National Book Award-winning Stamped from the Beginning','Jason Reynolds','Ngoại văn',190000,10,'images/sach5.jpg'),(7,'Untamed','Glennon Doyle','Ngoại văn',200000,10,'images/sach6.jpg'),(8,'Caste','Isabel Wilkerson','Ngoại văn',200000,10,'images/sach7.jpg'),(9,'Hamnet','Maggie O\'Farrell','Ngoại văn',120000,10,'images/sach8.jpg');
/*!40000 ALTER TABLE `sach` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ho_ten` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `avata` varchar(100) DEFAULT NULL,
  `user_role` enum('ADMIN','Thu_kho','Thu_ngan') NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `user_chk_1` CHECK ((`active` in (0,1)))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'thukho','d','thukho','202cb962ac59075b964b07152d234b70',NULL,NULL,'Thu_kho');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'qlnhasachdb'
--

--
-- Dumping routines for database 'qlnhasachdb'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-12-05  1:23:55
