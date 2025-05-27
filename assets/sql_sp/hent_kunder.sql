CREATE PROCEDURE `hent_kunder`()
BEGIN
  SELECT
    k.KNr,
    k.Fornavn,
    k.Etternavn,
    k.Adresse,
    k.PostNr
  FROM kunde AS k
  LIMIT 3000;
END