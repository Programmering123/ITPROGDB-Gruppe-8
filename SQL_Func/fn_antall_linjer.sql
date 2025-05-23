CREATE DEFINER=`root`@`localhost` FUNCTION `fn_antall_linjer`(in_ordreNr INT) RETURNS int
    DETERMINISTIC
BEGIN
  DECLARE v_count INT;       #Returnerer antall ordrelinjer i en gitt ordre.

  SELECT COUNT(*) 
    INTO v_count
  FROM ordrelinje
  WHERE OrdreNr = in_ordreNr;

  RETURN v_count;
END