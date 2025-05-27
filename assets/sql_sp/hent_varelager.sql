CREATE PROCEDURE `hent_varelager`()
BEGIN
  SELECT
    v.VNr,
    v.Betegnelse,
    v.Antall,
    v.Pris
  FROM vare AS v
  LIMIT 3000;
END