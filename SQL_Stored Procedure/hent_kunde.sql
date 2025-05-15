CREATE DEFINER=`root`@`localhost` PROCEDURE `hent_kunde`(
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
END