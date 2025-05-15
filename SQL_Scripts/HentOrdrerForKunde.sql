CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_hent_ordrer_for_kunde`(
    IN in_KNr INT
)
BEGIN
    SELECT 
      o.OrdreNr,
      o.OrdreDato,
      o.SendtDato,
      o.BetaltDato,
      SUM(ol.PrisPrEnhet * ol.Antall) AS TotalBelop,
      COUNT(*)               AS AntallLinjer
    FROM ordre AS o
    JOIN ordrelinje AS ol USING (OrdreNr)
    WHERE o.KNr = in_KNr
    GROUP BY o.OrdreNr;
END