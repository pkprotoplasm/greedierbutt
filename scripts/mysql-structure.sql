-- MariaDB dump 10.19  Distrib 10.5.19-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: greedierbutt
-- ------------------------------------------------------
-- Server version	10.5.19-MariaDB-0+deb11u2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Temporary table structure for view `alldaily_scores_ab`
--

DROP TABLE IF EXISTS `alldaily_scores_ab`;
/*!50001 DROP VIEW IF EXISTS `alldaily_scores_ab`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `alldaily_scores_ab` AS SELECT
 1 AS `player`,
  1 AS `avatar`,
  1 AS `scoreid`,
  1 AS `date`,
  1 AS `steamid`,
  1 AS `scorerank`,
  1 AS `timerank`,
  1 AS `score`,
  1 AS `stage_bonus`,
  1 AS `exploration_bonus`,
  1 AS `schwag_bonus`,
  1 AS `rush_bonus`,
  1 AS `bluebaby_bonus`,
  1 AS `lamb_bonus`,
  1 AS `megasatan_bonus`,
  1 AS `damage_penalty`,
  1 AS `hits_taken`,
  1 AS `time_penalty`,
  1 AS `item_penalty`,
  1 AS `level`,
  1 AS `time`,
  1 AS `goal` */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `alldaily_scores_abp`
--

DROP TABLE IF EXISTS `alldaily_scores_abp`;
/*!50001 DROP VIEW IF EXISTS `alldaily_scores_abp`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `alldaily_scores_abp` AS SELECT
 1 AS `player`,
  1 AS `avatar`,
  1 AS `scoreid`,
  1 AS `date`,
  1 AS `steamid`,
  1 AS `scorerank`,
  1 AS `timerank`,
  1 AS `score`,
  1 AS `stage_bonus`,
  1 AS `exploration_bonus`,
  1 AS `schwag_bonus`,
  1 AS `rush_bonus`,
  1 AS `bluebaby_bonus`,
  1 AS `lamb_bonus`,
  1 AS `megasatan_bonus`,
  1 AS `damage_penalty`,
  1 AS `hits_taken`,
  1 AS `time_penalty`,
  1 AS `item_penalty`,
  1 AS `level`,
  1 AS `time`,
  1 AS `goal` */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `alldaily_scores_rep`
--

DROP TABLE IF EXISTS `alldaily_scores_rep`;
/*!50001 DROP VIEW IF EXISTS `alldaily_scores_rep`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `alldaily_scores_rep` AS SELECT
 1 AS `player`,
  1 AS `avatar`,
  1 AS `scoreid`,
  1 AS `date`,
  1 AS `steamid`,
  1 AS `scorerank`,
  1 AS `timerank`,
  1 AS `score`,
  1 AS `stage_bonus`,
  1 AS `exploration_bonus`,
  1 AS `schwag_bonus`,
  1 AS `rush_bonus`,
  1 AS `bluebaby_bonus`,
  1 AS `lamb_bonus`,
  1 AS `megasatan_bonus`,
  1 AS `damage_penalty`,
  1 AS `hits_taken`,
  1 AS `time_penalty`,
  1 AS `item_penalty`,
  1 AS `level`,
  1 AS `time`,
  1 AS `goal` */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `badgeinfo`
--

DROP TABLE IF EXISTS `badgeinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `badgeinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `description` varchar(2000) NOT NULL,
  `color` varchar(128) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `badges`
--

DROP TABLE IF EXISTS `badges`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `badges` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `scoreid` bigint(20) NOT NULL,
  `dlc` int(11) NOT NULL,
  `badgeid` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_scoreid_dlc` (`scoreid`,`dlc`)
) ENGINE=InnoDB AUTO_INCREMENT=2860454 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `curated`
--

DROP TABLE IF EXISTS `curated`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `curated` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `month` int(2) NOT NULL,
  `day` int(2) NOT NULL,
  `year` int(4) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `description` varchar(8000) DEFAULT NULL,
  `rep` tinyint(1) DEFAULT 0,
  `abp` tinyint(1) DEFAULT 0,
  `ab` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `dailylb_entries_rep`
--

DROP TABLE IF EXISTS `dailylb_entries_rep`;
/*!50001 DROP VIEW IF EXISTS `dailylb_entries_rep`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `dailylb_entries_rep` AS SELECT
 1 AS `entries`,
  1 AS `date` */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `lb_100_ab`
--

DROP TABLE IF EXISTS `lb_100_ab`;
/*!50001 DROP VIEW IF EXISTS `lb_100_ab`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `lb_100_ab` AS SELECT
 1 AS `steamid`,
  1 AS `player`,
  1 AS `avatar`,
  1 AS `avgscorerank`,
  1 AS `avgtimerank`,
  1 AS `avgscorepercentile`,
  1 AS `avgtimepercentile`,
  1 AS `entries`,
  1 AS `zerocount`,
  1 AS `scorerank`,
  1 AS `timerank` */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `lb_100_abp`
--

DROP TABLE IF EXISTS `lb_100_abp`;
/*!50001 DROP VIEW IF EXISTS `lb_100_abp`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `lb_100_abp` AS SELECT
 1 AS `steamid`,
  1 AS `player`,
  1 AS `avatar`,
  1 AS `avgscorerank`,
  1 AS `avgtimerank`,
  1 AS `avgscorepercentile`,
  1 AS `avgtimepercentile`,
  1 AS `entries`,
  1 AS `zerocount`,
  1 AS `scorerank`,
  1 AS `timerank` */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `lb_100_rep`
--

DROP TABLE IF EXISTS `lb_100_rep`;
/*!50001 DROP VIEW IF EXISTS `lb_100_rep`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `lb_100_rep` AS SELECT
 1 AS `steamid`,
  1 AS `player`,
  1 AS `avatar`,
  1 AS `avgscorerank`,
  1 AS `avgtimerank`,
  1 AS `avgscorepercentile`,
  1 AS `avgtimepercentile`,
  1 AS `entries`,
  1 AS `zerocount`,
  1 AS `scorerank`,
  1 AS `timerank` */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `logintokens`
--

DROP TABLE IF EXISTS `logintokens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `logintokens` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `selector` varchar(255) NOT NULL,
  `hashed_validator` varchar(255) NOT NULL,
  `expiry` datetime NOT NULL,
  `steamid` bigint(20) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_steamid` (`steamid`),
  KEY `idx_selector` (`selector`),
  CONSTRAINT `fk_steamid` FOREIGN KEY (`steamid`) REFERENCES `profiles` (`steamid`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=126599 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `metadata`
--

DROP TABLE IF EXISTS `metadata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `metadata` (
  `lastupdate` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `activeplayercount` bigint(20) DEFAULT NULL,
  `scorelinecount` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `profiles`
--

DROP TABLE IF EXISTS `profiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `profiles` (
  `steamid` bigint(20) unsigned NOT NULL,
  `lastupdate` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `personaname` varchar(255) DEFAULT NULL,
  `profileurl` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `avatar` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `avatarmedium` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `avatarfull` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `blacklisted` tinyint(1) NOT NULL,
  `blacklisted_by` bigint(20) DEFAULT NULL,
  `blacklisted_reason` varchar(2048) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `blacklisted_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `moderator` tinyint(1) DEFAULT 0,
  `admin` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`steamid`),
  UNIQUE KEY `idx_steamid` (`steamid`),
  KEY `idx_personaname` (`personaname`),
  KEY `idx_blacklisted` (`blacklisted`),
  KEY `idx_lastupdate` (`lastupdate`),
  KEY `idx_moderator` (`moderator`),
  KEY `idx_admin` (`admin`),
  KEY `idx_steamid_blacklisted_personaname` (`steamid`,`blacklisted`,`personaname`),
  KEY `idx_blacklisted_date` (`blacklisted_date`),
  FULLTEXT KEY `personaname` (`personaname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `reports`
--

DROP TABLE IF EXISTS `reports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reports` (
  `reportid` bigint(20) NOT NULL AUTO_INCREMENT,
  `reporter` bigint(20) DEFAULT NULL,
  `steamid` bigint(20) DEFAULT NULL,
  `scoreid` bigint(20) DEFAULT NULL,
  `reason` varchar(2048) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `approved` tinyint(1) NOT NULL DEFAULT 0,
  `reviewer` bigint(20) DEFAULT NULL,
  `response` varchar(2048) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `processed` tinyint(1) NOT NULL DEFAULT 0,
  `dlc` varchar(10) DEFAULT NULL,
  `reportedon` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`reportid`),
  KEY `idx_steamid` (`steamid`),
  KEY `idx_scoreid` (`scoreid`),
  KEY `idx_approved` (`approved`),
  KEY `idx_processed` (`processed`),
  KEY `idx_reporter` (`reporter`),
  KEY `idx_reviewer` (`reviewer`)
) ENGINE=InnoDB AUTO_INCREMENT=689 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `reports_staging`
--

DROP TABLE IF EXISTS `reports_staging`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reports_staging` (
  `reportid` bigint(20) NOT NULL AUTO_INCREMENT,
  `reporter` bigint(20) DEFAULT NULL,
  `steamid` bigint(20) DEFAULT NULL,
  `scoreid` bigint(20) DEFAULT NULL,
  `reason` varchar(1024) DEFAULT NULL,
  `approved` tinyint(1) NOT NULL DEFAULT 0,
  `reviewer` bigint(20) DEFAULT NULL,
  `response` varchar(1024) DEFAULT NULL,
  `processed` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`reportid`),
  KEY `idx_steamid` (`steamid`),
  KEY `idx_scoreid` (`scoreid`),
  KEY `idx_approved` (`approved`),
  KEY `idx_processed` (`processed`),
  KEY `idx_reporter` (`reporter`),
  KEY `idx_reviewer` (`reviewer`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `score_history`
--

DROP TABLE IF EXISTS `score_history`;
/*!50001 DROP VIEW IF EXISTS `score_history`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `score_history` AS SELECT
 1 AS `player`,
  1 AS `avatar`,
  1 AS `scoreid`,
  1 AS `date`,
  1 AS `steamid`,
  1 AS `scorerank`,
  1 AS `timerank`,
  1 AS `score`,
  1 AS `stage_bonus`,
  1 AS `exploration_bonus`,
  1 AS `schwag_bonus`,
  1 AS `rush_bonus`,
  1 AS `bluebaby_bonus`,
  1 AS `lamb_bonus`,
  1 AS `megasatan_bonus`,
  1 AS `damage_penalty`,
  1 AS `hits_taken`,
  1 AS `time_penalty`,
  1 AS `item_penalty`,
  1 AS `level`,
  1 AS `time`,
  1 AS `goal`,
  1 AS `dlc` */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `scores`
--

DROP TABLE IF EXISTS `scores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scores` (
  `scoreid` bigint(20) NOT NULL AUTO_INCREMENT,
  `date` int(11) NOT NULL,
  `steamid` bigint(20) NOT NULL,
  `rank` bigint(20) DEFAULT NULL,
  `scorerank` bigint(20) DEFAULT NULL,
  `score` bigint(20) DEFAULT NULL,
  `stage_bonus` bigint(20) DEFAULT NULL,
  `exploration_bonus` bigint(20) DEFAULT NULL,
  `schwag_bonus` bigint(20) DEFAULT NULL,
  `rush_bonus` bigint(20) DEFAULT NULL,
  `bluebaby_bonus` bigint(20) DEFAULT NULL,
  `lamb_bonus` bigint(20) DEFAULT NULL,
  `megasatan_bonus` bigint(20) DEFAULT NULL,
  `damage_penalty` bigint(20) DEFAULT NULL,
  `time_penalty` bigint(20) DEFAULT NULL,
  `item_penalty` bigint(20) DEFAULT NULL,
  `level` bigint(20) DEFAULT NULL,
  `time` bigint(20) DEFAULT NULL,
  `timerank` bigint(20) DEFAULT NULL,
  `goal` bigint(20) DEFAULT NULL,
  `details` varchar(128) DEFAULT NULL,
  `hits_taken` bigint(20) GENERATED ALWAYS AS (floor(12 * log(1 - `damage_penalty` / (`exploration_bonus` * 0.8)) / log(0.8))) VIRTUAL,
  `dlc` varchar(5) NOT NULL,
  PRIMARY KEY (`steamid`,`date`,`dlc`),
  UNIQUE KEY `idx_scoreid` (`scoreid`),
  UNIQUE KEY `uc_scores` (`steamid`,`date`,`dlc`),
  KEY `idx_date` (`date`),
  KEY `idx_steamid` (`steamid`),
  KEY `idx_time` (`time`),
  KEY `idx_score` (`score`),
  KEY `idx_goal` (`goal`),
  KEY `idx_fullhistory` (`steamid`,`rank`,`timerank`,`score`,`time`),
  KEY `idx_calculatedrank_goal` (`goal`),
  KEY `idx_calculatedrank_goal_steamid` (`goal`,`steamid`),
  KEY `idx_scorerank` (`scorerank`),
  KEY `idx_recentresults` (`date`,`score`,`time`,`level`,`steamid`),
  KEY `idx_date_scorerank` (`date`,`scorerank`),
  KEY `idx_dlc` (`dlc`),
  KEY `idx_date_dlc` (`date`,`dlc`)
) ENGINE=InnoDB AUTO_INCREMENT=425217164 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `scores_ranked`
--

DROP TABLE IF EXISTS `scores_ranked`;
/*!50001 DROP VIEW IF EXISTS `scores_ranked`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `scores_ranked` AS SELECT
 1 AS `player`,
  1 AS `avatar`,
  1 AS `scoreid`,
  1 AS `date`,
  1 AS `steamid`,
  1 AS `scorerow`,
  1 AS `scorerank`,
  1 AS `timerow`,
  1 AS `timerank`,
  1 AS `score`,
  1 AS `stage_bonus`,
  1 AS `exploration_bonus`,
  1 AS `schwag_bonus`,
  1 AS `rush_bonus`,
  1 AS `bluebaby_bonus`,
  1 AS `lamb_bonus`,
  1 AS `megasatan_bonus`,
  1 AS `damage_penalty`,
  1 AS `hits_taken`,
  1 AS `time_penalty`,
  1 AS `item_penalty`,
  1 AS `level`,
  1 AS `time`,
  1 AS `goal`,
  1 AS `dlc` */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `toprankings`
--

DROP TABLE IF EXISTS `toprankings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `toprankings` (
  `steamid` bigint(20) DEFAULT NULL,
  `avgscorerank` double(20,10) DEFAULT NULL,
  `avgtimerank` double(20,10) DEFAULT NULL,
  `avgscorepercentile` double(20,10) DEFAULT NULL,
  `avgtimepercentile` double(20,10) DEFAULT NULL,
  `entries` int(11) DEFAULT NULL,
  `zerocount` int(11) DEFAULT NULL,
  KEY `idx_steamid` (`steamid`),
  KEY `idx_avgscorepercentile` (`avgscorepercentile`),
  KEY `idx_avgtimepercentile` (`avgtimepercentile`),
  KEY `idx_entries` (`entries`),
  KEY `idx_avgscorerank` (`avgscorerank`),
  KEY `idx_avgtimerank` (`avgtimerank`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `toprankingsab`
--

DROP TABLE IF EXISTS `toprankingsab`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `toprankingsab` (
  `steamid` bigint(20) DEFAULT NULL,
  `avgscorerank` double(20,10) DEFAULT NULL,
  `avgtimerank` double(20,10) DEFAULT NULL,
  `avgscorepercentile` double(20,10) DEFAULT NULL,
  `avgtimepercentile` double(20,10) DEFAULT NULL,
  `entries` int(11) DEFAULT NULL,
  `zerocount` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `toprankingsabp`
--

DROP TABLE IF EXISTS `toprankingsabp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `toprankingsabp` (
  `steamid` bigint(20) DEFAULT NULL,
  `avgscorerank` double(20,10) DEFAULT NULL,
  `avgtimerank` double(20,10) DEFAULT NULL,
  `avgscorepercentile` double(20,10) DEFAULT NULL,
  `avgtimepercentile` double(20,10) DEFAULT NULL,
  `entries` int(11) DEFAULT NULL,
  `zerocount` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `toprankingsr`
--

DROP TABLE IF EXISTS `toprankingsr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `toprankingsr` (
  `steamid` bigint(20) DEFAULT NULL,
  `avgscorerank` double(20,10) DEFAULT NULL,
  `avgtimerank` double(20,10) DEFAULT NULL,
  `avgscorepercentile` double(20,10) DEFAULT NULL,
  `avgtimepercentile` double(20,10) DEFAULT NULL,
  `entries` int(11) DEFAULT NULL,
  `zerocount` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'greedierbutt'
--
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
/*!50003 DROP FUNCTION IF EXISTS `getDate` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
DELIMITER ;;
CREATE DEFINER=`greedierbutt`@`localhost` FUNCTION `getDate`() RETURNS bigint(20)
    NO SQL
    DETERMINISTIC
return @getDate ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
/*!50003 DROP FUNCTION IF EXISTS `sfround` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
DELIMITER ;;
CREATE DEFINER=`greedierbutt`@`localhost` FUNCTION `sfround`(num FLOAT, sf INT) RETURNS float
    DETERMINISTIC
BEGIN

    DECLARE r FLOAT;  

    IF( num IS NULL OR num = 0) THEN 
        SET r = num; 

    ELSE
        SET r = ROUND(num, sf - 1 - FLOOR(LOG10(ABS(num))));
    
    END IF;

    RETURN (r);

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'IGNORE_SPACE,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetPendingReviews` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
DELIMITER ;;
CREATE DEFINER=`greedierbutt`@`localhost` PROCEDURE `GetPendingReviews`(mod_steamid bigint)
BEGIN
SELECT r.reportid AS reportid,
    r.reporter AS reporterid,
    prep.personaname AS reportername,
    prep.avatar as reporter_avatar,
    r.reportedon as reportedon,
    r.steamid AS steamid,
    pcht.personaname AS player,
    pcht.avatar as player_avatar,
    r.scoreid AS scoreid,
    s.date AS scoredate,
    s.dlc AS dlc,
    r.reason AS reason,
    r.approved AS approved,
    r.reviewer AS reviewer,
    prev.personaname AS reviewername,
    r.response AS response,
    r.processed AS processed,
    s.scorerank as scorerank,
    s.timerank as timerank,
    s.stage_bonus as stage_bonus,
    s.exploration_bonus as exploration_bonus,
    s.schwag_bonus as schwag_bonus,
    s.rush_bonus as rush_bonus,
    s.bluebaby_bonus as bluebaby_bonus,
    s.lamb_bonus as lamb_bonus,
    s.megasatan_bonus as megasatan_bonus,
    s.damage_penalty as damage_penalty,
    s.time_penalty as time_penalty,
    s.item_penalty as item_penalty,
    s.score as score,
    s.level as level,
    s.time as time,
    s.goal as goal,
    s.details as details
from reports AS r
    INNER JOIN profiles AS prep ON r.reporter = prep.steamid
    INNER JOIN profiles AS pcht ON r.steamid = pcht.steamid
    INNER JOIN scores AS s on r.scoreid = s.scoreid
    LEFT JOIN profiles AS prev ON r.reviewer = prev.steamid
WHERE r.reviewer IS NULL
    AND r.reporter <> mod_steamid
ORDER BY r.reportid ASC;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetPlayerProfile` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
DELIMITER ;;
CREATE DEFINER=`greedierbutt`@`localhost` PROCEDURE `GetPlayerProfile`(IN dlc varchar(5), IN player_steamid bigint)
BEGIN
        with averages as (
            SELECT
                steamid,
                AVG(scorerank) AS scorerank,
                AVG(timerank) AS timerank,
                AVG(time) AS time,
                AVG(score) AS score
            FROM
                scores
            WHERE steamid = player_steamid AND scores.dlc=dlc
            and goal > 0
            and (score > 0 or time > 0)
            and scorerank between 1 and 999998
            and timerank between 1 and 999998
        ), topscore as (
            select 
                steamid,
                scoreid,
                date,
                score,
                scorerank
            from scores
            where steamid = player_steamid AND scores.dlc=dlc
                and scorerank > 0
                and timerank > 0
            order by score desc
            limit 1
        ), toptime as (
            select
                steamid,
                scoreid,
                date,
                time,
                level,
                timerank
            from scores
            where steamid = player_steamid AND scores.dlc=dlc
                and goal > 1
                and scorerank > 0
                and timerank > 0
            order by time asc
            limit 1
        ), topscorerank as (
            select
                steamid,
                scoreid,
                date,
                score,
                scorerank
            from scores
            where steamid = player_steamid AND scores.dlc=dlc
                and scorerank > 0
                and timerank > 0
            order by scorerank asc
            limit 1
        ), toptimerank as (
            select 
                steamid,
                scoreid,
                date,
                time,
                timerank,
                level
            from scores
            where steamid = player_steamid AND scores.dlc=dlc
                and goal > 1
                and scorerank > 0
                and timerank > 0
            order by timerank asc
            limit 1
        ), totaldailyruns as (
            select steamid, count(scoreid) as runcount
            from scores
            where steamid = player_steamid AND scores.dlc=dlc
        ), totalloggedruns as (
            select steamid, count(scoreid) as runcount
            from scores
            where steamid = player_steamid AND scores.dlc=dlc
            and scorerank>0
            and timerank>0
            and goal>0
        ), totalwins as (
            select steamid, count(scoreid) as runcount
            from scores
            where steamid = player_steamid AND scores.dlc=dlc
            and scorerank>0
            and timerank>0
            and goal>1
        ), streaks AS (
            WITH streakdata AS (
                SELECT
                sr1.steamid,
                date,
                if(goal>1, "W", "L") as winloss,
                (
                    select
                        count(*)
                    from scores sr2
                    WHERE
                        (sr2.goal>1) <> (sr1.goal>1)
                        and sr2.date <= sr1.date
                        and sr2.steamid=sr1.steamid
                    order by date asc
                ) AS rungroup
                FROM scores sr1
                WHERE steamid = player_steamid AND sr1.dlc=dlc
                order by date asc
            )
            SELECT
                steamid,
                winloss,
                MIN(date) AS start_date,
                MAX(date) AS end_date,
                COUNT(*) AS streak
            FROM
                streakdata
            GROUP BY winloss, rungroup
            ORDER BY COUNT(*) DESC
        ), winstreak AS (
            select
                steamid,
                start_date,
                end_date,
                streak
            from
                streaks
            where
                winloss = "W"
            order by
                streak desc
            limit 1
        ), losestreak AS (
            select
                steamid,
                start_date,
                end_date,
                streak
            from
                streaks
            where
                winloss = "L"
            order by
                streak desc
            limit 1
        )
        select
            p.steamid as steamid, 
            p.personaname as personaname,
            p.avatarfull as avatarfull,
            averages.scorerank as avg_scorerank,
            averages.timerank as avg_timerank,
            averages.time as avg_time,
            averages.score as avg_score,
            topscore.scoreid as topscore_scoreid,
            topscore.date as topscore_date,
            topscore.score as topscore_score,
            topscore.scorerank as topscore_scorerank,
            toptime.scoreid as toptime_scoreid,
            toptime.date as toptime_date,
            toptime.time as toptime_time,
            toptime.level as toptime_level,
            toptime.timerank as toptime_timerank,
            topscorerank.scoreid as topscorerank_scoreid,
            topscorerank.date as topscorerank_date,
            topscorerank.score as topscorerank_score,
            topscorerank.scorerank as topscorerank_scorerank,
            toptimerank.scoreid as toptimerank_scoreid,
            toptimerank.date as toptimerank_date,
            toptimerank.time as toptimerank_time,
            toptimerank.level as toptimerank_level,
            toptimerank.timerank as toptimerank_timerank,
            totaldailyruns.runcount as totaldailyruns_count,
            totalloggedruns.runcount as totalloggedruns_count,
            if(isnull(totalwins.runcount), 0, totalwins.runcount) as totalwins_count,
            (if(isnull(totalwins.runcount), 0, totalwins.runcount)/totalloggedruns.runcount)*100 as win_percentage,
            winstreak.start_date as winstreak_startdate,
            winstreak.end_date as winstreak_enddate,
            winstreak.streak as winstreak_length,
            losestreak.start_date as losestreak_startdate,
            losestreak.end_date as losestreak_enddate,
            losestreak.streak as losestreak_length
        from
            (profiles as p
        LEFT JOIN toptime ON toptime.steamid=p.steamid
        LEFT JOIN toptimerank ON toptimerank.steamid=p.steamid
        LEFT JOIN totalwins ON totalwins.steamid=p.steamid
        LEFT JOIN winstreak on winstreak.steamid=p.steamid
        LEFT JOIN losestreak on losestreak.steamid=p.steamid),
            averages,
            topscore,
            topscorerank,
            totaldailyruns,
            totalloggedruns
        where
            p.steamid = player_steamid;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'IGNORE_SPACE,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetPlayerRecentRuns` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
DELIMITER ;;
CREATE DEFINER=`greedierbutt`@`localhost` PROCEDURE `GetPlayerRecentRuns`(dlc varchar(20), player_steamid bigint, run_count int)
BEGIN
        WITH scoredate AS (
            SELECT
                date
            FROM
                scores
            INNER JOIN
                profiles profiles
            ON
                scores.steamid=profiles.steamid
            WHERE
                scores.steamid=player_steamid and
                scores.dlc=dlc
            ORDER BY
                date DESC
            LIMIT run_count
        )
        SELECT * FROM (
            SELECT
                p.personaname AS player,
                p.avatarfull AS avatarfull,
                s.scoreid AS scoreid,
                s.date AS date,
                s.steamid AS steamid,
                s.scorerank AS rank,
                s.timerank AS timerank,
                s.stage_bonus AS stage_bonus,
                s.exploration_bonus AS exploration_bonus,
                s.schwag_bonus AS schwag_bonus,
                s.rush_bonus AS rush_bonus,
                s.bluebaby_bonus AS bluebaby_bonus,
                s.lamb_bonus AS lamb_bonus,
                s.megasatan_bonus AS megasatan_bonus,
                s.damage_penalty AS damage_penalty,
                s.time_penalty AS time_penalty,
                s.item_penalty AS item_penalty,
                s.level AS level,
                s.time AS time,
                s.goal AS goal,
                s.score AS score
            FROM
                scoredate AS sd
            INNER JOIN
                scores AS s
            ON
                s.date=sd.date
            INNER JOIN
                profiles AS p
            ON
                s.steamid=p.steamid
            WHERE
                p.blacklisted=false and
                s.dlc=dlc
        ) AS scores
        WHERE
            scores.steamid=player_steamid
        ORDER BY
            scores.date DESC;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetScore` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
DELIMITER ;;
CREATE DEFINER=`greedierbutt`@`localhost` PROCEDURE `GetScore`(dlc_arg varchar(5), scoreid_arg bigint)
BEGIN
    WITH scoredate AS (
        SELECT date FROM scores WHERE scoreid=scoreid_arg
    ),
    scoreranks AS (
        SELECT
            s.scoreid AS scoreid,
            RANK() OVER(ORDER BY s.score DESC, s.time ASC, s.dlc) AS rank,
            RANK() OVER(ORDER BY s.level DESC, s.time ASC, s.score, s.dlc DESC) AS timerank,
            CUME_DIST() OVER(ORDER BY s.score DESC, s.time ASC, s.dlc) as scorepercentile,
            CUME_DIST() OVER(ORDER BY s.level DESC, s.time ASC, s.score DESC, s.dlc) AS timepercentile
        FROM
            scores s
        INNER JOIN
            scoredate as sd
        ON
            s.date=sd.date
        INNER JOIN
            profiles p
        ON
            s.steamid=p.steamid
        WHERE
            p.blacklisted=false
            and s.dlc=dlc_arg
    )
    SELECT * FROM (
        SELECT
            p.personaname AS player,
            p.avatarfull AS avatarfull,
            s.scoreid AS scoreid,
            s.date AS date,
            s.steamid AS steamid,
            sr.rank AS rank,
            sr.timerank AS timerank,
            s.stage_bonus AS stage_bonus,
            s.exploration_bonus AS exploration_bonus,
            s.schwag_bonus AS schwag_bonus,
            s.rush_bonus AS rush_bonus,
            s.bluebaby_bonus AS bluebaby_bonus,
            s.lamb_bonus AS lamb_bonus,
            s.megasatan_bonus AS megasatan_bonus,
            s.damage_penalty AS damage_penalty,
            s.hits_taken AS hits_taken,
            s.time_penalty AS time_penalty,
            s.item_penalty AS item_penalty,
            s.level AS level,
            s.time AS time,
            s.score AS score,
            s.goal AS goal,
            s.dlc AS dlc,
            (sr.scorepercentile*100) AS scorepercentile,
            (sr.timepercentile*100) AS timepercentile
        FROM
            scores AS s
        INNER JOIN
            scoredate AS sd
        ON
            s.date=sd.date
        INNER JOIN
            profiles AS p
        ON
            s.steamid=p.steamid
        LEFT JOIN
            scoreranks AS sr
        ON
            s.scoreid=sr.scoreid
        WHERE
            s.dlc=dlc_arg
    ) AS score
    WHERE
        scoreid=scoreid_arg and
        dlc=dlc_arg
    LIMIT 1;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SearchPlayersByName` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
DELIMITER ;;
CREATE DEFINER=`greedierbutt`@`localhost` PROCEDURE `SearchPlayersByName`(IN scores_table varchar(50), IN player_NAME VARCHAR(8000))
BEGIN
    SET @scores = scores_table;
    SET @player = player_name;

    SET @sql_text = CONCAT('
        select s.steamid as steamid,
            p.personaname as player,
            p.avatar as avatar,
            count(s.scoreid) as entries,
            avg(s.rank) as avg_rank,
            avg(s.timerank) as avg_timerank
        from ',@scores,' s
            left join profiles p on s.steamid = p.steamid
        where p.personaname LIKE "%',@player,'%"
        group by s.steamid
        order by count(s.scoreid) desc
        limit 100
    ');

    PREPARE stmt1 FROM @sql_text;
    EXECUTE stmt1;
    DEALLOCATE PREPARE stmt1;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SearchPlayersBySteamID` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
DELIMITER ;;
CREATE DEFINER=`greedierbutt`@`localhost` PROCEDURE `SearchPlayersBySteamID`(IN scores_table varchar(50), IN player_steamid BIGINT)
BEGIN
    SET @scores = scores_table;
    SET @player = player_steamid;

    SET @sql_text = CONCAT('
        select s.steamid as steamid,
            p.personaname as player,
            p.avatar as avatar,
            count(s.scoreid) as entries,
            avg(s.rank) as avg_rank,
            avg(s.timerank) as avg_timerank
        from ',@scores,' s
            left join profiles p on s.steamid = p.steamid
        where p.personaname LIKE "%',@player,'%"
        group by s.steamid
        order by count(s.scoreid) desc
        limit 100
    ');

    PREPARE stmt1 FROM @sql_text;
    EXECUTE stmt1;
    DEALLOCATE PREPARE stmt1;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Final view structure for view `lb_100_ab`
--

/*!50001 DROP VIEW IF EXISTS `lb_100_ab`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_unicode_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`greedierbutt`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `lb_100_ab` AS select `t`.`steamid` AS `steamid`,`p`.`personaname` AS `player`,`p`.`avatar` AS `avatar`,`t`.`avgscorerank` AS `avgscorerank`,`t`.`avgtimerank` AS `avgtimerank`,`t`.`avgscorepercentile` AS `avgscorepercentile`,`t`.`avgtimepercentile` AS `avgtimepercentile`,`t`.`entries` AS `entries`,`t`.`zerocount` AS `zerocount`,rank() over ( order by `t`.`avgscorepercentile`) AS `scorerank`,rank() over ( order by `t`.`avgtimepercentile`) AS `timerank` from (`toprankingsab` `t` join `profiles` `p`) where `t`.`steamid` = `p`.`steamid` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `lb_100_abp`
--

/*!50001 DROP VIEW IF EXISTS `lb_100_abp`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_unicode_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`greedierbutt`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `lb_100_abp` AS select `t`.`steamid` AS `steamid`,`p`.`personaname` AS `player`,`p`.`avatar` AS `avatar`,`t`.`avgscorerank` AS `avgscorerank`,`t`.`avgtimerank` AS `avgtimerank`,`t`.`avgscorepercentile` AS `avgscorepercentile`,`t`.`avgtimepercentile` AS `avgtimepercentile`,`t`.`entries` AS `entries`,`t`.`zerocount` AS `zerocount`,rank() over ( order by `t`.`avgscorepercentile`) AS `scorerank`,rank() over ( order by `t`.`avgtimepercentile`) AS `timerank` from (`toprankingsabp` `t` join `profiles` `p`) where `t`.`steamid` = `p`.`steamid` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `lb_100_rep`
--

/*!50001 DROP VIEW IF EXISTS `lb_100_rep`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_unicode_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`greedierbutt`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `lb_100_rep` AS select `t`.`steamid` AS `steamid`,`p`.`personaname` AS `player`,`p`.`avatar` AS `avatar`,`t`.`avgscorerank` AS `avgscorerank`,`t`.`avgtimerank` AS `avgtimerank`,`t`.`avgscorepercentile` AS `avgscorepercentile`,`t`.`avgtimepercentile` AS `avgtimepercentile`,`t`.`entries` AS `entries`,`t`.`zerocount` AS `zerocount`,rank() over ( order by `t`.`avgscorepercentile`) AS `scorerank`,rank() over ( order by `t`.`avgtimepercentile`) AS `timerank` from (`toprankingsr` `t` join `profiles` `p`) where `t`.`steamid` = `p`.`steamid` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `scores_ranked`
--

/*!50001 DROP VIEW IF EXISTS `scores_ranked`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_unicode_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`greedierbutt`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `scores_ranked` AS select `p`.`personaname` AS `player`,`p`.`avatar` AS `avatar`,`s`.`scoreid` AS `scoreid`,`s`.`date` AS `date`,`s`.`steamid` AS `steamid`,row_number() over ( partition by `s`.`date`,`s`.`dlc` order by `s`.`score` desc,`s`.`time`,`p`.`personaname`,`s`.`steamid`) AS `scorerow`,rank() over ( partition by `s`.`date`,`s`.`dlc` order by `s`.`score` desc,`s`.`time`) AS `scorerank`,row_number() over ( partition by `s`.`date`,`s`.`dlc` order by `s`.`level` desc,`s`.`time`,`s`.`score` desc,`p`.`personaname`,`s`.`steamid`) AS `timerow`,rank() over ( partition by `s`.`date`,`s`.`dlc` order by `s`.`level` desc,`s`.`time`,`s`.`score` desc) AS `timerank`,`s`.`score` AS `score`,`s`.`stage_bonus` AS `stage_bonus`,`s`.`exploration_bonus` AS `exploration_bonus`,`s`.`schwag_bonus` AS `schwag_bonus`,`s`.`rush_bonus` AS `rush_bonus`,`s`.`bluebaby_bonus` AS `bluebaby_bonus`,`s`.`lamb_bonus` AS `lamb_bonus`,`s`.`megasatan_bonus` AS `megasatan_bonus`,`s`.`damage_penalty` AS `damage_penalty`,`s`.`hits_taken` AS `hits_taken`,`s`.`time_penalty` AS `time_penalty`,`s`.`item_penalty` AS `item_penalty`,`s`.`level` AS `level`,`s`.`time` AS `time`,`s`.`goal` AS `goal`,`s`.`dlc` AS `dlc` from (`profiles` `p` join `scores` `s` on(`p`.`steamid` = `s`.`steamid`)) where `p`.`blacklisted` = 0 order by `s`.`date` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `scoresunion`
--

/*!50001 DROP VIEW IF EXISTS `scoresunion`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_unicode_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`greedierbutt`@`localhost` SQL SECURITY DEFINER */
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-08-03 16:57:17
