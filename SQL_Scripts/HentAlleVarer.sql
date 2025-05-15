CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_hent_alle_varer`()
BEGIN
    SELECT 
      VNr,
      Betegnelse,
      Pris,
      Antall,
      Hylle
    FROM vare;
END