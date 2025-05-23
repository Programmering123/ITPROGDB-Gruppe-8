CREATE DEFINER=`root`@`localhost` PROCEDURE `opprett_ordre`(
    IN  in_KNr       INT,        #Oppretter en ny ordre med automatisk generert OrdreNr
    IN  in_ordreDato DATE,
    OUT out_ordreNr  INT
)
BEGIN
    -- Finn neste ledige OrdreNr
    SELECT IFNULL(MAX(OrdreNr), 0) + 1
      INTO out_ordreNr
      FROM ordre;

    -- Sett inn raden
    INSERT INTO ordre (OrdreNr, OrdreDato, KNr)
    VALUES (out_ordreNr, in_ordreDato, in_KNr);
END