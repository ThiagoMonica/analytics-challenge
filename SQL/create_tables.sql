-- MySQL Script generated by MySQL Workbench
-- Tue Apr  1 15:14:53 2025
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema db_marketplace
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema db_marketplace
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `db_marketplace` DEFAULT CHARACTER SET utf8 ;
USE `db_marketplace` ;

-- -----------------------------------------------------
-- Table `db_marketplace`.`Customer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_marketplace`.`Customer` (
  `id` BIGINT NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `first_name` VARCHAR(255) NOT NULL,
  `last_name` VARCHAR(255) NULL,
  `gender` VARCHAR(255) NULL,
  `address` VARCHAR(255) NOT NULL,
  `birth_date` DATE NOT NULL,
  `phone` VARCHAR(255) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db_marketplace`.`Category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_marketplace`.`Category` (
  `id` BIGINT NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db_marketplace`.`Item`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_marketplace`.`Item` (
  `id` BIGINT NOT NULL,
  `title` VARCHAR(255) NOT NULL,
  `description` VARCHAR(255) NULL,
  `price` FLOAT NOT NULL,
  `status` INT NULL,
  `deactivation_date` DATE NULL,
  `category_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_Item_Category1_idx` (`category_id` ASC) VISIBLE,
  CONSTRAINT `fk_Item_Category1`
    FOREIGN KEY (`category_id`)
    REFERENCES `db_marketplace`.`Category` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db_marketplace`.`Order`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_marketplace`.`Order` (
  `id` BIGINT NOT NULL,
  `quantity` INT NOT NULL,
  `purchase_date` DATETIME NULL,
  `total` FLOAT NOT NULL,
  `Customer_id` BIGINT NOT NULL,
  `Item_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`, `Customer_id`, `Item_id`),
  INDEX `fk_Order_Customer1_idx` (`Customer_id` ASC) VISIBLE,
  INDEX `fk_Order_Item1_idx` (`Item_id` ASC) VISIBLE,
  CONSTRAINT `fk_Order_Customer1`
    FOREIGN KEY (`Customer_id`)
    REFERENCES `db_marketplace`.`Customer` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Order_Item1`
    FOREIGN KEY (`Item_id`)
    REFERENCES `db_marketplace`.`Item` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
