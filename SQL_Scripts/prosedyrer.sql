DELIMITER $$

-- 1) Hent en enkel kundepost basert på kundenummer
CREATE PROCEDURE sp_hent_kunde(
    IN in_KNr INT
)
BEGIN
    SELECT 
      k.KNr,
      k.Fornavn,
      k.Etternavn,
      k.Adresse,
      k.PostNr,
      p.Poststed
    FROM kunde AS k
    JOIN poststed AS p USING (PostNr)
    WHERE k.KNr = in_KNr;
END$$

-- 2) Hent en liste over alle ordre for en gitt kunde
CREATE PROCEDURE sp_hent_ordrer_for_kunde(
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
END$$

-- 3) Hent detaljer for én ordre, inkludert vareinfo per linje
CREATE PROCEDURE sp_hent_ordredetaljer(
    IN in_ordreNr INT
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
END$$

-- 4) Hent alle varedetaljer (for eksempel til katalogvisning)
CREATE PROCEDURE sp_hent_alle_varer()
BEGIN
    SELECT 
      VNr,
      Betegnelse,
      Pris,
      Antall,
      Hylle
    FROM vare;
END$$

DELIMITER ;
