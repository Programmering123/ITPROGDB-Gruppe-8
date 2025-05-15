CREATE DEFINER=`root`@`localhost` FUNCTION `fn_lagerstatus`(in_VNr CHAR(5)) RETURNS varchar(10) CHARSET utf8mb4
    DETERMINISTIC
BEGIN
  DECLARE v_ant INT;
  DECLARE v_status VARCHAR(10);

  SELECT Antall INTO v_ant
    FROM vare
   WHERE VNr = in_VNr;

  IF v_ant < 5 THEN
    SET v_status = 'Lavt';
  ELSEIF v_ant BETWEEN 5 AND 20 THEN
    SET v_status = 'OK';
  ELSE
    SET v_status = 'Høyt';
  END IF;

  RETURN v_status;
END