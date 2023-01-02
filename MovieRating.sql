-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';


-- -----------------------------------------------------
-- Schema movie_rating
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `movie_rating` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `movie_rating` ;

-- -----------------------------------------------------
-- Table `movie_rating`.`movie_ratings`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movie_rating`.`movie_ratings` (
  `movie_id` BIGINT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(300) NOT NULL,
  `rating` DECIMAL(2,1) NOT NULL,
  `region` VARCHAR(300) NULL DEFAULT NULL,
  `date` DATE NULL DEFAULT NULL,
  PRIMARY KEY (`movie_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `movie_rating`.`movie_tags`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movie_rating`.`movie_tags` (
  `tag_id` BIGINT NOT NULL AUTO_INCREMENT,
  `tag1` VARCHAR(45) NULL DEFAULT NULL,
  `tag2` VARCHAR(45) NULL DEFAULT NULL,
  `tag3` VARCHAR(45) NULL DEFAULT NULL,
  `tag4` VARCHAR(45) NULL DEFAULT NULL,
  `tag5` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`tag_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `movie_rating`.`rating_distributions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movie_rating`.`rating_distributions` (
  `distribution_id` INT NOT NULL AUTO_INCREMENT,
  `one` DECIMAL(3,1) NULL DEFAULT NULL,
  `two` DECIMAL(3,1) NULL DEFAULT NULL,
  `three` DECIMAL(3,1) NULL DEFAULT NULL,
  `four` DECIMAL(3,1) NULL DEFAULT NULL,
  `five` DECIMAL(3,1) NULL DEFAULT NULL,
  PRIMARY KEY (`distribution_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
