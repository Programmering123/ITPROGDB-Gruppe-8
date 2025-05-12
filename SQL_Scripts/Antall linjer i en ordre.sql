DELIMITER $$

CREATE FUNCTION fn_antall_linjer(in_ordreNr INT)
  RETURNS INT
  DETERMINISTIC
BEGIN
  DECLARE v_count INT;

  SELECT COUNT(*) 
    INTO v_count
  FROM ordrelinje
  WHERE OrdreNr = in_ordreNr;

  RETURN v_count;
END$$

DELIMITER ;
