CREATE DEFINER=`root`@`localhost` PROCEDURE `hent_alle_varer`()
BEGIN
    SELECT 
      VNr,
      Betegnelse,
      Pris,
      Antall,
      Hylle
    FROM vare;
END