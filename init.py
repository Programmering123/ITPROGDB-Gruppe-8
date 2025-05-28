"""
Dette er init.py filen for varehus appen.
Den brukes til å initialisere og tilpasse databasen til appen.
Skal kun kjøres én gang for å sette opp databasen.
Denne filen oppretter også nødvendige prosedyrer i databasen.
"""

import logging
from pathlib import Path
from dotenv import load_dotenv
import getpass
dotenv_path = Path('secrets.env')
load_dotenv(dotenv_path=dotenv_path, override=True)  # Laster inn .env filen for å hente database informasjon

import api.database as db
import mysql.connector


def opprett_prosedyrer():
    """
    Funksjon for å opprette alle prosedyrer i databasen.
    """
    procedyrer = [
# Hente alle ordrer:
"""
CREATE PROCEDURE `hent_ordrer`()
BEGIN
  SELECT
	o.OrdreNr,
	CONCAT(k.Fornavn, ' ', k.Etternavn) AS KundeNavn,
	o.OrdreDato,
	o.BetaltDato,
	o.KNr
  FROM ordre AS o
    JOIN kunde AS k ON o.KNr = k.KNr
  LIMIT 3000;
END;
""",
# Hente alle kunder:
"""
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
END;
""",
# Hente hele varelager:
"""
CREATE PROCEDURE `hent_varelager`()
BEGIN
  SELECT
    v.VNr,
    v.Betegnelse,
    v.Antall,
    v.Pris
  FROM vare AS v
  LIMIT 3000;
END;
""",
# Oppdatere kunde:
"""
CREATE PROCEDURE `oppdater_kunde`(
	IN kundenummer VARCHAR(10),
    IN fornavn VARCHAR(255),
    IN etternavn VARCHAR(255),
    IN adresse VARCHAR(255),
    IN postnr VARCHAR(10)
)
BEGIN
	UPDATE `varehusdb`.`kunde` 
    SET `Adresse` = adresse,
    `Fornavn` = fornavn,
	`Etternavn` = etternavn,
    `Postnr` = postnr
    WHERE (`KNr` = kundenummer);
END;
""",
# Opprette kunde:                                                                       
"""
CREATE PROCEDURE `opprett_kunde`(
    IN fornavn VARCHAR(255),
    IN etternavn VARCHAR(255),
    IN adresse VARCHAR(255),
    IN postnr VARCHAR(10)
)
BEGIN
    SELECT MAX(KNr) INTO @siste_knr FROM kunde;
    SET @ny_knr = IFNULL(@siste_knr, 0) + 1;
    INSERT INTO kunde (KNr, Fornavn, Etternavn, Adresse, PostNr) VALUES (@ny_knr, fornavn, etternavn, adresse, postnr);
END;
""",
# Opprette faktura PDF:
"""
CREATE TABLE `varehusdb`.`faktura` (
  `FakturaNR` INT NOT NULL AUTO_INCREMENT,
  `FakturaNavn` VARCHAR(45) NULL,
  `ForfallDato` DATE NULL,
  `FakturaDato` DATE NULL,
  `OrdreNr` INT NOT NULL,
  PRIMARY KEY (`FakturaNR`),
  INDEX `FK_OrdreFaktura_idx` (`OrdreNr` ASC) VISIBLE,
  UNIQUE INDEX `FakturaNR_UNIQUE` (`FakturaNR` ASC) VISIBLE,
  CONSTRAINT `FK_OrdreFaktura`
    FOREIGN KEY (`OrdreNr`)
    REFERENCES `varehusdb`.`ordre` (`OrdreNr`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
"""
    ]
    try:
        databasen = db.tilkobling_database()
        spørring = databasen.cursor()
        for prosedyre in procedyrer:
            try:
                spørring.execute(prosedyre)                                     # Utfører hver enkel prosedyre
                databasen.commit()                                              # Utfører handling
                print(f"Prosedyre opprettet: {prosedyre.split()[2]}")           # tilbakemelding om at prosedyren er opprettet
                logging.info("Prosedyrer opprettet i databasen")                # Logger at prosedyrer er opprettet
            except mysql.connector.Error as err:
                if err.errno == 1064:                                           # Hvis det er feil i SQL syntaks    
                    logging.error(f"Feil i SQL syntaks: {err}")
                    print(f"Feil i SQL syntaks: {prosedyre.split()[2]}")        
                elif err.errno == 1304:                                         # Hvis det allerede existerer en prosedyre med samme navn                   
                    logging.error(f"Prosedyre eksisterer allerede: {err}")      
                    print(f"Prosedyre eksisterer allerede: {prosedyre.split()[2]}")   
                else:                                                           # Logger andre feil ved oppretting av prosedyre
                    logging.error(f"Feil ved oppretting av prosedyre: {err}")
                    print(f"Feilet oppretting av prosedyre: {prosedyre.split()[2]}")
    except mysql.connector.Error as err:
        print(f"Klarte ikke koble til database for å opprette prosedyrer: {err}")# Logger feil ved oppretting av prosedyrer
        print("Vennligst legg inn prosedyrer manuelt i databasen.")             # Informerer om at det må legges inn prosedyrer manuelt i databasen
    finally:
        if databasen:
            databasen.close()
        if spørring:
            spørring.close()

def opprett_login():
    """
    Funksjon for å opprette en login til databasen.
    """
    brukernavn = input("Skriv inn bruker til databasen: ")                      # Spør bruker om brukernavn
    passord = getpass.getpass("Skriv inn passord til databasen: ")              # Spør bruker om passord
    hostnavn = input("Skriv inn adresse til databasen (standard localhost): ")  # Spør bruker om hostnavn
    port = input("Skriv inn port til databasen (standard 3306): ")              # Spør bruker om port
    if hostnavn == "":                                                          # Hvis hostnavn er tomt, bruk standard localhost
        hostnavn = "localhost"
    if port == "":                                                              # Hvis port er tomt, bruk standard 3306
        port = "3306"
    prosjektrot = Path(__file__).resolve().parent                               # Finner prosjektrot, som er 1 nivåer opp fra denne filen   
    fil = prosjektrot / "secrets.env"                                           # Full sti til .env filen
    with open(fil, 'w') as f:                                                   # Åpner .env filen for skriving
        f.write(f"DB_USER={brukernavn}\n")                                      # Skriver brukernavn til .env filen
        f.write(f"DB_PASSWORD={passord}\n")                                     # Skriver passord til .env filen
        f.write(f"DB_HOST={hostnavn}\n")                                        # Skriver hostnavn til .env filen
        f.write(f"DB_PORT={port}\n")                                            # Skriver port til .env filen
    print(f"Login lagret i .env filen: {fil}")                                  # Informerer om at login er opprettet
    return True

def initier_database():
    """
    Funksjon for å initialisere databasen.
    Denne funksjonen sjekker om databasen eksisterer, og oppretter den hvis den ikke gjør det.
    """
    load_dotenv(dotenv_path=Path('secrets.env'), override=True)                                        # Laster inn .env filen
    def database_test():
        """ lokal funksjon for å teste database tilkobling """
        databasen = db.tilkobling_database()                                    # Prøver å koble til databasen igjen
        if databasen and databasen.is_connected():                              # Sjekker om tilkoblingen er vellykket
            logging.info("Tilkobling til database vellykket")
            databasen.close()                                                   # Lukker tilkoblingen
            return True
        else:
            return False
    try:
        if database_test():                                                     # Prøver å koble til databasen
            print("Tilkobling til database vellykket")                          # Informerer om at tilkoblingen er vellykket
            return True
    except Exception as e:
        logging.warning("Første tilkobling feilet, prøver å opprette login: {e}")# Logger at første tilkobling feilet
        print(f" Første tilkobling feilet:, prøver å opprette env fil...")      # Tilbakemelding til bruker første tilkobling feilet
        if opprett_login():
            load_dotenv(dotenv_path=Path('secrets.env'), override=True)         # Laster inn .env filen på nytt
            try:
                database_test()
                print("Tilkobling til database vellykket etter .env opprettet") # Informerer om at tilkoblingen er vellykket etter .env opprettet
                return True
            except Exception as e:
                print(f"Feil ved tilkobling til database etter .env opprettet: {e}")

if __name__ == "__main__":
    if initier_database():
        print("Database initialisert ")                                         # Informerer om at databasen er initialisert og prosedyrer er opprettet
        if opprett_prosedyrer():
            print("Prosedyrer opprettet i databasen.")
            
    else:
        print("Database initialisering feilet. Slett .env filen og prøv igjen.")
