CREATE PROCEDURE `oppdater_kunde`(
	IN kundenummer VARCHAR(10),
    IN fornavn VARCHAR(255),
    IN etternavn VARCHAR(255),
    IN adresse VARCHAR(255),
    IN postnr VARCHAR(10)
)
BEGIN
	UPDATE `varehusdb`.`kunde` 
    SET `Adresse` = adresse,
    `Fornavn` = fornavn,
	`Etternavn` = etternavn,
    `Postnr` = postnr
    WHERE (`KNr` = kundenummer);
END