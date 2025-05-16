CREATE DEFINER=`root`@`localhost` PROCEDURE `hent_ordrer_for_kunde`(
    IN in_KNr INT         #Returnerer en oversikt over alle ordrer for én kunde med:
                           #TotalBelop,Antallordrelinjer

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