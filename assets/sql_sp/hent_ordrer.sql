CREATE PROCEDURE `hent_ordrer`()
BEGIN
  SELECT
	o.OrdreNr,
	CONCAT(k.Fornavn, ' ', k.Etternavn) AS KundeNavn,
	o.OrdreDato,
	o.BetaltDato,
	o.KNr
  FROM ordre AS o
    JOIN kunde AS k ON o.KNr = k.KNr
  LIMIT 3000;
END