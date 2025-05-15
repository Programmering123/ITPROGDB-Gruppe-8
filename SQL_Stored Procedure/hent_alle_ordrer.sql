CREATE DEFINER=`root`@`localhost` PROCEDURE `hent_alle_ordrer`(
  IN p_limit  INT,
  IN p_offset INT
)
BEGIN
  SELECT 
    o.OrdreNr,
    o.OrdreDato,
    o.SendtDato,
    o.BetaltDato,
    o.KNr           AS kundenr,
    k.Fornavn       AS kunde_fornavn,
    k.Etternavn     AS kunde_etternavn,
    k.Adresse
  FROM ordre AS o
    JOIN kunde AS k ON o.KNr = k.KNr
  ORDER BY o.OrdreDato DESC
  LIMIT p_limit OFFSET p_offset;
END