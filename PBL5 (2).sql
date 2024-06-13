-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.4.28-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.7.0.6850
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for pbl5
CREATE DATABASE IF NOT EXISTS `pbl5` /*!40100 DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci */;
USE `pbl5`;

-- Dumping structure for table pbl5.role
CREATE TABLE IF NOT EXISTS `role` (
  `ID` int(10) NOT NULL AUTO_INCREMENT,
  `code` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table pbl5.role: ~2 rows (approximately)
INSERT INTO `role` (`ID`, `code`, `name`) VALUES
	(1, 'u-001', 'user'),
	(2, 'a-001', 'admin');

-- Dumping structure for table pbl5.user
CREATE TABLE IF NOT EXISTS `user` (
  `ID` int(10) NOT NULL AUTO_INCREMENT,
  `lastname` varchar(50) NOT NULL,
  `firstname` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `gender` varchar(50) NOT NULL,
  `id_role` int(10) NOT NULL,
  `avatar` varchar(500) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `FK_user_role` (`id_role`),
  CONSTRAINT `FK_user_role` FOREIGN KEY (`id_role`) REFERENCES `role` (`ID`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table pbl5.user: ~12 rows (approximately)
INSERT INTO `user` (`ID`, `lastname`, `firstname`, `email`, `username`, `password`, `gender`, `id_role`, `avatar`, `phone`) VALUES
	(12, '', '', '', 'hoangcheck3', '123', '', 2, '../DB/images.jpg', '123'),
	(13, 'hoang', 'bui', 'duyhoang.it.2003', 'hoang', '123', 'nam', 2, '../DB/hoang.png', '123'),
	(34, '', '', '', 'hoang6', '123', '', 1, '../DB/images.jpg', '123'),
	(35, '', '', '', 'hoang7', '123', '', 1, '../DB/images.jpg', '123'),
	(36, '', '', '', 'phuc123@gmail.com', 'duyhophuc', '', 1, '../DB/images.jpg', '0123456789'),
	(37, '', '', '', 'hoang@gmail.com', '123', '', 1, '../DB/images.jpg', '123'),
	(38, 'hoang', 'hoang', 'hoagng@gmail.com', 'hoangxxx@gmail.com', '123', 'nam', 1, '../DB/hoang.png', '0357757617'),
	(39, '', '', '', 'hoangx1', '123', '', 1, '../DB/images.jpg', '123'),
	(40, '', '', '', 'hoangxxxx', '123', '', 1, '../DB/images.jpg', '123'),
	(41, '', '', '', 'hoangx2', '123', '', 1, '../DB/images.jpg', '123'),
	(42, '', '', '', 'hoangx3', '123', '', 1, '../DB/images.jpg', '123');

-- Dumping structure for table pbl5.user_word
CREATE TABLE IF NOT EXISTS `user_word` (
  `ID_word` int(11) NOT NULL,
  `ID_user` int(11) NOT NULL,
  `point` int(11) NOT NULL,
  KEY `FK_user_word_user` (`ID_user`),
  KEY `FK_user_word_word` (`ID_word`),
  CONSTRAINT `FK_user_word_user` FOREIGN KEY (`ID_user`) REFERENCES `user` (`ID`) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT `FK_user_word_word` FOREIGN KEY (`ID_word`) REFERENCES `word` (`ID`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table pbl5.user_word: ~7 rows (approximately)
INSERT INTO `user_word` (`ID_word`, `ID_user`, `point`) VALUES
	(1, 13, 100),
	(3, 13, 60),
	(1, 12, 100),
	(3, 12, 50),
	(5, 12, 100),
	(9, 12, 100),
	(3, 34, 100),
	(7, 13, 80),
	(9, 13, 77);

-- Dumping structure for table pbl5.word
CREATE TABLE IF NOT EXISTS `word` (
  `ID` int(10) NOT NULL AUTO_INCREMENT,
  `path_video` varchar(500) NOT NULL,
  `word` varchar(50) NOT NULL,
  `point` int(10) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table pbl5.word: ~20 rows (approximately)
INSERT INTO `word` (`ID`, `path_video`, `word`, `point`) VALUES
	(1, '../DB/video/opaque.mp4', 'Opaque', 100),
	(2, '../DB/video/red.mp4', 'Red', 100),
	(3, '../DB/video/green.mp4', 'Green', 100),
	(4, '../DB/video/yellow.mp4', 'Yellow', 100),
	(5, '../DB/video/bright.mp4', 'Bright', 100),
	(6, '../DB/video/light-blue.mp4', 'Light-Blue', 100),
	(7, '../DB/video/colors.mp4', 'Colors', 100),
	(8, '../DB/video/pink.mp4', 'Pink', 100),
	(9, '../DB/video/women.mp4', 'Women', 100),
	(10, '../DB/video/enemy.mp4', 'Enemy', 100),
	(11, '../DB/video/son.mp4', 'Son', 100),
	(12, '../DB/video/man.mp4', 'Man', 100),
	(13, '../DB/video/away.mp4', 'Away', 100),
	(14, '../DB/video/drawer.mp4', 'Drawer', 100),
	(15, '../DB/video/born.mp4', 'Born', 100),
	(16, '../DB/video/learn.mp4', 'Lear', 100),
	(17, '../DB/video/call.mp4', 'Call', 100),
	(18, '../DB/video/skimmer.mp4', 'Skimmer', 100),
	(19, '../DB/video/bitter.mp4', 'Bitter', 100),
	(20, '../DB/video/sweet.mp4', 'Sweet', 100);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
