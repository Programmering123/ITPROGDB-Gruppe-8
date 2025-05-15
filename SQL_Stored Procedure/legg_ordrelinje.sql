CREATE DEFINER=`root`@`localhost` PROCEDURE `legg_ordrelinje`(
    IN in_ordreNr INT,
    IN in_VNr      CHAR(5),
    IN in_antall   INT
)
BEGIN
    DECLARE gjeldendePris DECIMAL(8,2);

    -- Hent pris fra vare-tabellen
    SELECT Pris
      INTO gjeldendePris
      FROM vare
     WHERE VNr = in_VNr;

    -- Legg til ordrelinje
    INSERT INTO ordrelinje (OrdreNr, VNr, PrisPrEnhet, Antall)
    VALUES (in_ordreNr, in_VNr, gjeldendePris, in_antall);

    -- Trekk fra lagerbeholdning
    UPDATE vare
       SET Antall = Antall - in_antall
     WHERE VNr = in_VNr;

    -- Logg prisendring i prishistorikk
    INSERT INTO prishistorikk (VNr, Dato, GammelPris)
    VALUES (in_VNr, CURRENT_DATE(), gjeldendePris);
END