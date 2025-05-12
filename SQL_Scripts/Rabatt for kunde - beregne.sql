DELIMITER $$

CREATE FUNCTION fn_rabatt(in_KNr INT)
  RETURNS DECIMAL(4,2)
  DETERMINISTIC
BEGIN
  DECLARE v_antOrdre INT;
  DECLARE v_rabatt DECIMAL(4,2);

  -- Tell fullførte ordre (med BetaltDato ikke NULL)
  SELECT COUNT(*) INTO v_antOrdre
    FROM ordre
   WHERE KNr = in_KNr
     AND BetaltDato IS NOT NULL;

  -- Enkelt eksempel: 1% rabatt per ordre, maks 10%
  SET v_rabatt = LEAST(v_antOrdre * 0.01, 0.10);

  RETURN v_rabatt;
END$$

DELIMITER ;
