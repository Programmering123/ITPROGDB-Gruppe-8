"""
database.py - Databasehåndtering for Varelageret

Dette er en database modul for å håndtere tilkobling og spørringer til en MySQL database.
Den bruker mysql-connector-python for å koble til databasen og utføre spørringer.
Den bruker også dotenv for å håndtere sensitive data som brukernavn og passord.
Den inneholder funksjoner for å hente ordrer, ordrelinjer, varelager, kunder og postnummer.
Den inneholder også funksjoner for å oppdatere og opprette kunder, samt slette kunder.
Den inneholder også en funksjon for å lagre fakturaer i databasen.
Den inneholder også en funksjon for å validere inndata.
"""
from typing import Dict, Any, Optional, Union, List
from decimal import Decimal
import mysql.connector  
from dotenv import load_dotenv, dotenv_values
import os
from pathlib import Path
import decimal
import logging
# Henter variabler fra .env filen
dotenv_path = Path('secrets.env')
load_dotenv(dotenv_path=dotenv_path)

# Setter opp variabler fra .env fil, tilpasset hver unike database.

logging.basicConfig(
    filename='./logg/log.txt',                                                  # Filnavn for loggfilen
    level=logging.DEBUG,                                                        # Logg nivå
    format='%(asctime)s:%(levelname)s:%(message)s'                              # Format for loggmeldinger
)
logging.debug("Logger opprettet")                                               # Logger at logger er opprettet

"""
Initierer, ved å sjekke om vi kan koble til databasen.
er det angitt brukernavn og passord i .env filen.?
Kan vi angi egen bruker og passord. 
Kan vi kryptere passordet i .env filen?
Instruks: Bruker i database trenger kun tilgang til stored procedure.
Under oppsett så trenger vi tilgang til hele databasen.
Kun stored procedure i databasen, ingen spørringer.
eller.
"""
# Funksjon for å koble til databasen

def tilkobling_database():
    DB_USER = os.getenv("DB_USER")
    DB_HOST = os.getenv("DB_HOST")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_PORT = os.getenv("DB_PORT")
    try:
        tilkobling = mysql.connector.connect(                                   # Tilkoblingen til databasen
            host=DB_HOST,
            user=DB_USER,
            password = DB_PASSWORD,                                             # Passord til databasen
            database = 'varehusdb',                                             # Valgt database
            port=DB_PORT                                                        # Port til databasen
        )
        logging.info("Tilkobling til database opprettet")                       # Logger at vi har opprettet tilkobling 
        return tilkobling                   
    except mysql.connector.Error as err:
        logging.error(f"Feil ved tilkobling til database: {err}")               # Logger ved feil tilkobling
        raise ConnectionError(
            "Kunne ikke koble til database. Sjekk .env filen og at databasen er oppe."
            )                                                                   # Kaster en feilmelding hvis tilkobling mislykkes

## ORDREHÅNDTERING 
def hent_ordrer():   
    """ Henter alle ordrer fra databasen.""" 
    try:
        logging.info("Henter ordrelinjer fra databasen")                        # Logger at vi henter ordrelinjer
        databasen = tilkobling_database()                                       # Koble til databasen
        spørring = databasen.cursor()                                           # Starter spørring
        spørring.callproc('hent_ordrer')                                        # Starter prosedyre
        for resultater in spørring.stored_results():
            svar = resultater.fetchall()                                        # Henter alle resultater fra prosedyren
        return svar                                                             # Returnerer alle ordrer fra databasen
    except mysql.connector.Error as err:
        logging.error(f"Feil ved henting av ordrelinjer: {err}")
        return []

# Funksjon for å hente all data fra spesifikk ordre:
def hent_ordre(ordre_id: int) -> Dict[str, Any]:
    """
    Funksjon for å hente spesifik ordre fra databasen.
    Args:
        ordre_id: int mer enn 0 og maks 10 desimaler
    Returns:
        Dict: med ordre data
    """
    logging.info(f"Henter spesifik ordre med ID: {ordre_id}")                   # Logger at vi henter spesifik ordre
    if ordre_id and isinstance(ordre_id, int) and ordre_id > 0:                 # Sjekker om ordre_id er gyldig
        try:
            databasen = tilkobling_database() 
            spørring = databasen.cursor() 
            spørring.execute(f"""
                SELECT 
                    OrdreNr,
                    OrdreDato,
                    SendtDato,
                    BetaltDato,
                    KNr 
                FROM ordre 
                WHERE OrdreNr = {ordre_id}
                """)                                                            # Henter alle(begrenset til 1000) rader fra definerte kolonner i vare schemaet.
            resultat = spørring.fetchone()                                      # Lagrer resultat fra spørring, kun en linje
            if resultat:                                                        # Gjør om resultatet til dictionary hvis det ikke er tomt:
                kolonner = [beskrivelse[0] for beskrivelse in spørring.description] # Henter kolonnebeskrivelser
                resultat: dict[str, Any] = dict(zip(kolonner, resultat))        # Lager en dict av resultatet med kolonnenavn som nøkler
            return resultat                                                     # Returnerer resultatet
        except mysql.connector.Error as err:
            logging.error(f"Feil ved henting av spesifikke ordrelinjer: {err}")
            return []
        finally:
            if databasen:
                databasen.close()
            if spørring:
                spørring.close()
    else:
        print("Ingen ordre valgt.")
        return []
    
# Funksjon for henting av ordrelinjer:
def hent_ordrelinjer(ordre_id):
    """
    Funksjon for å hente ordrelinjer for en spesifik ordre.
    Args:
        ordre_id: int mer enn 0 og maks 10 desimaler
    Returns:
        List: med ordrelinjer
    """
    try:
        databasen = tilkobling_database()                                       # Koble til databasen
        spørring = databasen.cursor()                                           # Dette er en virituell "markør"
        spørring.execute(f"""
            SELECT 
                ordrelinje.VNr,
                Betegnelse,
                ordrelinje.Antall,
                PrisPrEnhet
            FROM varehusdb.ordrelinje 
            INNER JOIN vare ON ordrelinje.VNr = vare.VNr 
            WHERE OrdreNr = {ordre_id} 
            LIMIT 1000;
            """)                                                                # Henter alle(begrenset til 1000) rader fra definerte kolonner i vare tabellen.
        resultat:list[tuple[str, str, int, Decimal]] = spørring.fetchall()      # Lagrer resultat fra spørring
        return resultat # Returnerer resultatet
    except mysql.connector.Error as err:
        logging.error(f"Feil ved henting av ordrelinjer: {err}")
        return []
    finally:
        if databasen:
            databasen.close()
        if spørring:
            spørring.close()

## VARELAGERHÅNDTERING
# Funksjon for å hente varelageret:
def hent_varelager():
    try:
        databasen = tilkobling_database() # Koble til databasen
        spørring = databasen.cursor() # Dette er en virituell "markør"
        spørring.callproc('hent_varelager') # Velger prosedyre for henting av varelager
        for resultater in spørring.stored_results():    
            svar = resultater.fetchall() # Henter alle resultater fra prosedyren
        return svar # Returnerer resultatet
    except mysql.connector.Error as err:
        logging.error(f"Feil ved henting av varelager: {err}")  
        return []

# Funksjon for å hentet varer til API-en, som er en liste med dictionaries.
def hent_varer():
    """ Funksjon for å hente varer fra databasen som en liste med dictionaries.
    Denne er kun for brukt til API-en, og ikke for GUI-en.
    Returns:
        List[Dict[str, Union[int, str, float]]]: Liste med dictionaries som inneholder varer.
    """
    databasen = None
    spørring = None
    try:
        databasen = tilkobling_database()
        if not databasen or not databasen.is_connected():
            logging.error("Feil: Kunne ikke koble til database eller ugyldig forbindelse.")
            return []                                                           # Returner tom liste hvis ingen gyldig tilkobling

        spørring = databasen.cursor()
        sql_query = "SELECT VNr, Betegnelse, Antall, Pris FROM vare LIMIT 1000"
        kolonnenavn_for_zip = ["VNr", "Betegnelse", "Antall", "Pris"]           # Kolonnenavn for å lage dict med zip
        spørring.execute(sql_query)
        hentet_tuples = spørring.fetchall()
        
        # Lager dict-liste fra tuples, basert på kolonnenavn:
        resultat_liste_med_dicts = [dict(zip(kolonnenavn_for_zip, rad)) for rad in hentet_tuples]
        
        # iterer gjennom listen og konverter Pris og Antall
        for vare_dict in resultat_liste_med_dicts:
            # Konverter Pris
            if 'Pris' in vare_dict and vare_dict['Pris'] is not None:
                if isinstance(vare_dict['Pris'], decimal.Decimal):
                    vare_dict['Pris'] = float(vare_dict['Pris'])
                else:
                    try: # Hvis det allerede er en streng eller et annet tallformat
                        vare_dict['Pris'] = float(vare_dict['Pris'])
                    except (ValueError, TypeError):
                        logging.warning(f"Advarsel: Kunne ikke konvertere Pris '{vare_dict['Pris']}' til float for VNr '{vare_dict.get('VNr')}'. Setter til None.")
                        vare_dict['Pris'] = None # Eller en annen feilhåndtering
            
            # Sikre at Antall er int (bør være det fra databasen hvis kolonnen er INT)
            if 'Antall' in vare_dict and vare_dict['Antall'] is not None:
                if isinstance(vare_dict['Antall'], decimal.Decimal): # I tilfelle Antall også er Decimal
                    vare_dict['Antall'] = int(vare_dict['Antall'])
                else:
                    try:
                        vare_dict['Antall'] = int(vare_dict['Antall'])
                    except (ValueError, TypeError):
                        logging.warning(f"Advarsel: Kunne ikke konvertere Antall '{vare_dict['Antall']}' til int for VNr '{vare_dict.get('VNr')}'. Setter til None.")
                        vare_dict['Antall'] = None 
        
        return resultat_liste_med_dicts

    except mysql.connector.Error as db_err:
        logging.error(f"Databasefeil ved henting av varer: {db_err}")
        print(f"Databasefeil ved henting av varer: {db_err}")
        return []
    except Exception as e:
        # Fang andre uventede feil
        logging.error(f"Uventet feil ved henting av varer: {type(e).__name__} - {e}")
        return []
    finally:
        # Sørg for å lukke cursor og tilkobling
        if spørring:
            try:
                spørring.close()
            except Exception as e_cursor:
                logging.error(f"Feil ved lukking av cursor: {e_cursor}")
        if databasen and databasen.is_connected():
            try:
                databasen.close()
            except Exception as e_db:
                logging.error(f"Feil ved lukking av database: {e_db}")


## KUNDERHÅNDTERING:
# Funksjon for å hente alle kunder.
def hent_kunder():
    """
    Funksjon for å hente alle kunder fra databasen.
    Returns:
        List: [(KNr, Fornavn, Etternavn, Adresse, PostNr)]
    """
    try:
        databasen = tilkobling_database() 
        spørring = databasen.cursor() 
        spørring.callproc('hent_kunder')                                        # Velger prosedyre for henting av kundedata
        for resultater in spørring.stored_results():
            svar = resultater.fetchall()                                        # Henter alle resultater fra prosedyren
        return svar # Returnerer resultatet
    except mysql.connector.Error as err:
        logging.error(f"Feil ved henting av kunder: {err}")                     # Logger feil ved henting av kunder
        return []

def hent_kunde(kunde_id: int) -> Any:
    """
    Funksjon for å hente all info om spesifik kunde fra databasen.
    Args:
        kunde_id: int mer enn 0 og maks 10 desimaler
    Returns:
        Tuple: (KNr, Fornavn, Etternavn, Adresse, PostNr, Poststed)
    """
    if(kunde_id != None):
        try:
            databasen = tilkobling_database() # Koble til databasen
            spørring = databasen.cursor() # Dette er en virituell "markør"
            spørring.execute(f"SELECT kunde.KNr, kunde.Fornavn, kunde.Etternavn, kunde.Adresse, kunde.PostNr, poststed.Poststed FROM kunde INNER JOIN poststed ON kunde.PostNr = poststed.PostNr WHERE kunde.Knr = {kunde_id} LIMIT 1") 
            
            resultat = spørring.fetchone() # Lagrer resultat fra spørring
            return resultat # Returnerer resultatet
        except mysql.connector.Error as err:
            print(f"Feil ved henting av spesifikke kunder: {err}")
            return []
    else:
        print("Ingen kunder valgt.")
        return []

def hent_kunder_filter()-> list[Any]:
    """
    Funksjon for å hente kunder med filter.
    Returns:
        List: med kundedata
    """
    try:
        databasen = tilkobling_database() # Koble til databasen
        spørring = databasen.cursor() # Dette er en virituell "markør"
        spørring.execute("SELECT KNr, Fornavn, Etternavn, Adresse, PostNr FROM kunde WHERE NOT EXISTS (SELECT 1 FROM ordre WHERE ordre.KNr = kunde.KNr )") 
        resultat = spørring.fetchall() # Lagrer resultat fra spørring
        return resultat # Returnerer resultatet
    except mysql.connector.Error as err:
        print(f"Feil ved henting av kunder: {err}")
        return []

def slett_kunde(kunde_id: int)-> int:
    """
    Funksjon for å slette en kunde i databasen.
    Args: 
        kunde_id: int mer enn 0 og maks 10 desimaler
    Returns: 
        kunde_id hvis sletting var vellykket, 0 ellers.
    """
    if kunde_id is not None and kunde_id > 0:                     # Sjekker om kunde_id er gyldig
        try:
            databasen = tilkobling_database()                                   # Koble til databasen
            spørring = databasen.cursor()                                       # Dette er en virituell "markør"
            spørring.execute(f"DELETE FROM kunde WHERE kunde.KNr = {kunde_id}") 
            databasen.commit()                                                  # Utfører handling
        except mysql.connector.IntegrityError as err:
            logging.error(f"Feil ved sletting av kunde: {err}")                  # Logger feil ved sletting av kunde
            return 0                                                            # Returnerer 0 hvis sletting mislyktes
        except mysql.connector.Error as err:
            logging.error(f"Feil ved sletting av kunde: {err}")                  # Logger feil ved sletting av kunde
            return 0                                                            # Returnerer 0 hvis sletting mislyktes
        finally:
            if databasen:
                databasen.close()
            if spørring:
                spørring.close()
        return kunde_id
    else:
        return 0
    
def oppdater_kunde(
        kundenummer: int,
        fornavn: str,
        etternavn: str,
        adresse: str,
        postnr: str
)-> bool:
    """ 
    Funksjon for å oppdatere en kunde i databasen. 
    Args: 
        kundenummer: int mer enn 0 og maks 10 desimaler
        fornavn: String på mer enn 2 karakterer og mindre enn 32 karakterer.
        etternavn: String på mer enn 2 karakterer og mindre enn 32 karakterer. 
        adresse: String på mer enn 2 karakterer og mindre nn 32 karakterer.
        postnr: int på 4 tall.
    Returns:
        True, hvis vellykket
    Raises:
        ValueError: Hvis feil inndata.
        ConnectionError: Hvis feil med tilkobling.
    """
    if(
        kunde_valider_helper(kundenummer, 2, 999999999, tall=True) and
        kunde_valider_helper(fornavn, 2, 32) and
        kunde_valider_helper(etternavn, 2, 32) and
        kunde_valider_helper(adresse, 2, 32) and
        kunde_valider_helper(postnr, 0000, 9999, postnr=True)
    ):
        kunde_data = (kundenummer, fornavn, etternavn, adresse, postnr)
        try:
            databasen = tilkobling_database() # koble til databasen
            spørring = databasen.cursor() 
            spørring.callproc('oppdater_kunde', kunde_data ) 
            databasen.commit()
            return True
        except:
            raise ConnectionError("Tilkobling til database mislykket")
        finally:
            databasen.close()
    else:
        raise ValueError("Angitt data er ugyldig")

# Funksjon for å opprette en kunde i databasen.
def opprett_kunde( 
        fornavn: str, 
        etternavn: str, 
        adresse: str,   
        postnr: str    
    )->bool:
    """
    Funksjon for å legge til en kunde i databasen. 
    Args:
        fornavn: String på mer enn 2 karakterer og mindre enn 32 karakterer.
        etternavn: String på mer enn 2 karakterer og mindre enn 32 karakterer. 
        adresse: String på mer enn 2 karakterer og mindre nn 32 karakterer.
        postnr: int på 4 tall.
    Returns:
        True, hvis vellykket
    Raises:
        ValueError: Hvis feil inndata.
        ConnectionError: Hvis feil med tilkobling.
    """
    if(
        kunde_valider_helper(fornavn, 2, 32) and
        kunde_valider_helper(etternavn, 2, 32) and
        kunde_valider_helper(adresse, 2, 32) and
        kunde_valider_helper(postnr, 3, 5)
    ):
        kunde_data = (fornavn, etternavn, adresse, postnr)
        try:
            databasen = tilkobling_database()                                   
            spørring = databasen.cursor() 
            spørring.callproc('opprett_kunde', kunde_data)                      # Sender kunde_data til kunde_opprett SP
            databasen.commit()
            return True
        except:
            raise ConnectionError("Tilkobling til database mislykket")
        finally:
            databasen.close()
    else:
        raise ValueError("Angitt data er ugyldig")


## DIVERSE FUNKSJONER:
# Funksjon for å hente postnr fra databasen:    
def hent_postnr()-> list[str]:
    """
    Funksjon for å hente postnr fra databasen
    Returns:
        List of postnr
    """
    try:
        databasen = tilkobling_database()                                       # Koble til databasen
        spørring = databasen.cursor()                                           # Dette er en virituell "markør"
        spørring.execute("SELECT PostNr FROM poststed")                         # Henter alle(begrenset til 1000) rader fra definerte kolonner i vare schemaet.
        resultat: List[Any] = spørring.fetchall()                               # Lagrer resultat fra spørring
        return [postnr[0] for postnr in resultat]                               # Returnerer resultatet som liste med bare postnr
    except mysql.connector.Error as err:
        logging.error(f"Feil ved henting av postnr: {err}")                     # Logger feil ved henting av postnr
        return []

def kunde_valider_helper(streng: str | int, fra: int, til: int, tall: bool= False, postnr: bool=False)->bool:
    """
    Også en funksjon for validering Testing. Dynamisk sjekk om streng stemmer med kravene.
    Args:
        streng: Streng å validere
        fra: Minimum lengde
        til: Maksimum lengde
        tall: True hvis int, standard str
        postnr: True hvis postnr, standard False
    Returns:
        Bool
    """
    if tall:  
        if isinstance(streng, int):
            return fra < streng < til                                           # Returnerer True hvis det er mellom angitt verdi
        else:
            return False                                                     
    elif postnr and isinstance(streng, str):                                    # Hvis det er postnr, og postnr er streng
        if not streng.isdigit():                                                # Må være kun tall
            return False
        return len(streng)==4                                                   # Returnerer True hvis det er 4 siffer i strengen
    else:
        if not isinstance(streng, str):
            return False 
        return fra < len(streng) < til 

# Forhåndsdefinerte postnr for å unngå å hente dem fra databasen flere ganger.
tilgjengelige_postnumre: list[str]= []                               # Henter postnr fra databasen denne trengs bare hentes 1 gang.


## Generer faktura database:
def lagre_faktura(
        faktura_navn: str,
        forfall_dato: str,
        faktura_dato: str,
        ordre_nr: int
    ) -> bool:
    """
    Funksjon for å lagre faktura i databasen.
    Args:
        faktura_nr: Fakturanummer
        faktura_navn: Navn på faktura
        forfall_dato: Forfallsdato
        faktura_dato: Fakturadato
        ordre_nr: Ordrenummer
    Returns:
        True hvis vellykket, False ellers.
    """
    try:
        databasen = tilkobling_database()
        spørring = databasen.cursor()
        spørring.execute("INSERT INTO varehusdb.faktura ( FakturaNavn, ForfallDato, FakturaDato, OrdreNr) VALUES ( %s, %s, %s, %s)", (faktura_navn, forfall_dato, faktura_dato, ordre_nr))
        databasen.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Feil ved lagring av faktura: {err}")
        return False
    finally:
        if databasen:
            databasen.close()


if __name__ == "__main__":
    logging.debug("Database.py er kjørt som hovedprogram")                      # Logger at database.py er kjørt som hovedprogram

else:                                                                           # Hvis database.py er importert som modul
    logging.debug("Database.py er importert")
    try:
        tilgjengelige_postnumre = hent_postnr()                                 # Henter postnr fra databasen
        logging.debug(f"Tilgjengelige postnumre er importert.")                 # Logger tilgjengelige postnr
    except Exception as e:
        logging.error(f"Feil ved henting av postnumre: {e}")                    # Logger feil ved henting av postnr
        tilgjengelige_postnumre = []                                            # Setter tilgjengelige postnr til tom liste hvis feil
        print("Kunne ikke hente postnumre fra databasen. Vennligst sjekk loggen.")