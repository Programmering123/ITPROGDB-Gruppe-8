DELIMITER $$

CREATE FUNCTION fn_ordretotal(in_ordreNr INT)
  RETURNS DECIMAL(12,2)
  DETERMINISTIC
BEGIN
  DECLARE v_total DECIMAL(12,2);

  SELECT COALESCE(SUM(PrisPrEnhet * Antall), 0)
    INTO v_total
  FROM ordrelinje
  WHERE OrdreNr = in_ordreNr;

  RETURN v_total;
END$$

DELIMITER ;
