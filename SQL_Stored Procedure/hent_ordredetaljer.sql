CREATE DEFINER=`root`@`localhost` PROCEDURE `hent_ordredetaljer`(
    IN in_ordreNr INT                #Returnerer alle detaljer om en spesifikk ordre: produkter, priser, mengder, og totalpris pr. linje.
)
BEGIN
    SELECT 
      o.OrdreNr,
      o.OrdreDato,
      o.SendtDato,
      o.BetaltDato,
      k.KNr,
      CONCAT(k.Fornavn, ' ', k.Etternavn) AS KundeNavn,
      ol.VNr,
      v.Betegnelse,
      ol.PrisPrEnhet,
      ol.Antall,
      (ol.PrisPrEnhet * ol.Antall) AS LinjeTotal
    FROM ordre       AS o
    JOIN kunde       AS k ON o.KNr = k.KNr
    JOIN ordrelinje  AS ol ON o.OrdreNr = ol.OrdreNr
    JOIN vare        AS v ON ol.VNr   = v.VNr
    WHERE o.OrdreNr = in_ordreNr;
END