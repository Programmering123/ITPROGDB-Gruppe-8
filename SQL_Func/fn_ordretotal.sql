CREATE DEFINER=`root`@`localhost` FUNCTION `fn_ordretotal`(in_ordreNr INT) RETURNS decimal(12,2)
    DETERMINISTIC
BEGIN
  DECLARE v_total DECIMAL(12,2);

  SELECT COALESCE(SUM(PrisPrEnhet * Antall), 0)
    INTO v_total
  FROM ordrelinje
  WHERE OrdreNr = in_ordreNr;       #Summerer hele ordrebeløpet. Brukbar i faktura, oppsummeringer og rapporter.


  RETURN v_total;
END