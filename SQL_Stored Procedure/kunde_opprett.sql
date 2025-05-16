CREATE DEFINER=`root`@`localhost` PROCEDURE `kunde_opprett`(
    IN fornavn VARCHAR(255),
    IN etternavn VARCHAR(255),
    IN adresse VARCHAR(255),
    IN postnr VARCHAR(10)
)
BEGIN
    SELECT MAX(KNr) INTO @siste_knr FROM kunde;
    SET @ny_knr = IFNULL(@siste_knr, 0) + 1;
    INSERT INTO kunde (KNr, Fornavn, Etternavn, Adresse, PostNr) VALUES (@ny_knr, fornavn, etternavn, adresse, postnr);
END