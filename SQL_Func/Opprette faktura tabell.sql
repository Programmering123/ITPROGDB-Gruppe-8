CREATE TABLE `varehusdb`.`faktura` (
  `FakturaNR` INT NOT NULL AUTO_INCREMENT,
  `FakturaNavn` VARCHAR(45) NULL,
  `ForfallDato` DATE NULL,
  `FakturaDato` DATE NULL,
  `OrdreNr` INT NOT NULL,
  PRIMARY KEY (`FakturaNR`),
  INDEX `FK_OrdreFaktura_idx` (`OrdreNr` ASC) VISIBLE,
  UNIQUE INDEX `FakturaNR_UNIQUE` (`FakturaNR` ASC) VISIBLE,
  CONSTRAINT `FK_OrdreFaktura`
    FOREIGN KEY (`OrdreNr`)
    REFERENCES `varehusdb`.`ordre` (`OrdreNr`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
