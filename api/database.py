# Tester tilkobling til database
import mysql.connector  
from dotenv import load_dotenv, dotenv_values
import os
from pathlib import Path
from typing import Dict, Any, Optional, Union
import decimal
import logging
# Henter variabler fra .env filen
dotenv_path = Path('secrets.env')
load_dotenv(dotenv_path=dotenv_path)

# Setter opp variabler fra .env fil, tilpasset hver unike database.
DB_USER = os.getenv("DB_USER")
DB_HOST = os.getenv("DB_HOST")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

logging.basicConfig(
    filename='./logg/log.txt',                                                  # Filnavn for loggfilen
    level=logging.DEBUG,                                                        # Logg nivå
    format='%(asctime)s:%(levelname)s:%(message)s'                              # Format for loggmeldinger
)
logging.debug("Logger opprettet")                                               # Logger at logger er opprettet
# Funksjon for å koble til databasen
def tilkobling_database():
    return mysql.connector.connect(                                             # Tilkoblingen til databasen
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database = 'varehusdb' # Valgt database.
    )

# TODO: Opprette flere funksjoner for hver spørring vi trenger (hva slags spørringer må vi ha? Se i oppgaven.)
# Funksjon for å hentre ordrer: # TODO: Tenker at denne SQLen kan være fin å ha som stored procedure i databasen.
def hent_ordrer(): 
    try:
        logging.info("Henter ordrelinjer fra databasen") # Logger at vi henter ordrelinjer
        databasen = tilkobling_database() # Koble til databasen
        spørring = databasen.cursor() # Dette er vel en virituell "markør"
        # Spørringen henter alle rader fra definerte kolonner, og satt LIMIT til 3000 rader, 
        # virker som om dette virker bra og for denne datamengden er det en fin løsning, 
        # ved større datamengder så måtte vi nok begrenset henting.
        linje = """SELECT OrdreNr, Fornavn, OrdreDato, BetaltDato, ordre.KNr 
        FROM ordre INNER JOIN kunde ON ordre.KNr = kunde.KNr LIMIT 0,3000"""    # Henter alle(begrenset til 1000) rader fra definerte kolonner i vare schemaet.
        spørring.execute(linje)                                                 # Spørringen 
        resultat = spørring.fetchall()                                          # Lagrer resultat fra spørring
        return resultat                                                         # Returnerer resultatet
    except mysql.connector.Error as err:
        logging.error(f"Feil ved henting av ordrelinjer: {err}")
        return []
# Funksjon for å hente all data fra spesifikk ordre:
def hent_spesifikk_ordre(ordre_id: int) -> Optional[Dict[str, Any]]:
    logging.info(f"Henter spesifik ordre med ID: {ordre_id}")                   # Logger at vi henter spesifik ordre
    if(ordre_id != None):
        try:
            databasen = tilkobling_database() 
            spørring = databasen.cursor() 
            spørring.execute(f"SELECT OrdreNr, OrdreDato, SendtDato, BetaltDato, KNr FROM ordre WHERE OrdreNr = {ordre_id}") # Henter alle(begrenset til 1000) rader fra definerte kolonner i vare schemaet.
            resultat = spørring.fetchone()                                      # Lagrer resultat fra spørring, kun en linje
            if resultat:                                                        # Gjør om resultatet til object <3
                kolonner = [beskrivelse[0] for beskrivelse in spørring.description] # Henter kolonnebeskrivelser
                resultat = dict(zip(kolonner, resultat))                        # Lager en dict av resultatet med kolonnenavn som nøkler
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
    try:
        databasen = tilkobling_database()                                       # Koble til databasen
        spørring = databasen.cursor()                                           # Dette er en virituell "markør"
        spørring.execute(f"SELECT ordrelinje.VNr, Betegnelse, ordrelinje.Antall, PrisPrEnhet FROM varehusdb.ordrelinje INNER JOIN vare ON ordrelinje.VNr = vare.VNr WHERE OrdreNr = {ordre_id} LIMIT 1000;") # Henter alle(begrenset til 1000) rader fra definerte kolonner i vare schemaet.
        resultat = spørring.fetchall() # Lagrer resultat fra spørring
        return resultat # Returnerer resultatet
        # Legger denne her: Hvis vi skal bruke stored procedure i stedet for spørring
        # Og hvordan rydde opp resultatet til en dict... 
        # spørring.callproc('HentOrdreDetaljer', (ordre_id,))  # Bruk stored procedure
        # kolonner = ["VNr", "Betegnelse", "Antall", "PrisPrEnhet"]
        # resultat = []
        # for res in spørring.stored_results():
        #     resultat = res.fetchall()
        # return [dict(zip(kolonner, row)) for row in resultat]

    except mysql.connector.Error as err:
        logging.error(f"Feil ved henting av ordrelinjer: {err}")
        return []
    finally:
        if databasen:
            databasen.close()
        if spørring:
            spørring.close()

# Funksjon for å hente varelageret: (oppgave: Vise en liste over hvilke varer som er på varelageret, inkludert varenummer, navn på varen, antall og pris. )
# Tilgjengelige kolonner i vare: VNr, Betegnelse, Pris, KatNr, Antall, Hylle 
def hent_varelager():
    try:
        databasen = tilkobling_database() # Koble til databasen
        spørring = databasen.cursor() # Dette er en virituell "markør"
        spørring.execute("SELECT VNr, Betegnelse, Antall, Pris FROM vare LIMIT 1000") # Henter alle(begrenset til 1000) rader fra definerte kolonner i vare schemaet.
        resultat = spørring.fetchall() # Lagrer resultat fra spørring
        return resultat # Returnerer resultatet
    except mysql.connector.Error as err:
        logging.error(f"Feil ved henting av varelager: {err}")  
        return []

# Funksjon for å hentet varer til API-en, som er en liste med dictionaries.
def hent_varer():
    databasen = None
    spørring = None
    try:
        databasen = tilkobling_database()
        if not databasen or not databasen.is_connected():
            logging.error("Feil: Kunne ikke koble til database eller ugyldig forbindelse.")
            return [] # Returner tom liste hvis ingen gyldig tilkobling

        spørring = databasen.cursor()
        sql_query = "SELECT VNr, Betegnelse, Antall, Pris FROM vare LIMIT 1000"
        kolonnenavn_for_zip = ["VNr", "Betegnelse", "Antall", "Pris"] # Bruker dine opprinnelige navn
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
                        vare_dict['Antall'] = None # Eller en annen feilhåndtering
        
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


# Funksjon for å hente alle kunder.
def kunder_hent(): #TODO: Korriger denne til å hente en stored procedure i databasen, opprett en stored procedure.
    try:
        databasen = tilkobling_database() # Koble til databasen
        spørring = databasen.cursor() # Dette er en virituell "markør"
        spørring.execute("SELECT KNr, Fornavn, Etternavn, Adresse, PostNr FROM kunde LIMIT 1000") # Henter alle(begrenset til 1000) rader fra definerte kolonner i vare schemaet.
        resultat = spørring.fetchall() # Her skal vi bare ha 1 linje, så vi bruker fetchone() i stedet for fetchall()
        return resultat # Returnerer resultatet
    except mysql.connector.Error as err:
        print(f"Feil ved henting av kunder: {err}")
        return []

def kunder_hent_filter():
    """
    Funksjon for å hente kunder med filter.
    Returns:
        List of customers
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

# Funksjon for å slette spesifikk kunde:
def kunde_slett(kunde_id: int)-> int:
    if kunde_id != None:
        try:
            databasen = tilkobling_database()                                   # Koble til databasen
            spørring = databasen.cursor()                                       # Dette er en virituell "markør"
            spørring.execute(f"DELETE FROM kunde WHERE kunde.KNr = {kunde_id}") # TODO: Stored procedure i stedet for spørring
            databasen.commit()                                                  # Utfører handling
        except:
            return 0                                                            # Returnerer 0 hvis sletting mislyktes
        finally:
            if databasen:
                databasen.close()
            if spørring:
                spørring.close()
        return kunde_id
    else:
        return 0


#Funksjon for å hente spesifikk kundeinfo:
def hent_spesifikk_kunde(kunde_id):
    if(kunde_id != None):
        try:
            databasen = tilkobling_database() # Koble til databasen
            spørring = databasen.cursor() # Dette er en virituell "markør"
            spørring.execute(f"SELECT kunde.KNr, kunde.Fornavn, kunde.Etternavn, kunde.Adresse, kunde.PostNr, poststed.Poststed FROM kunde INNER JOIN poststed ON kunde.PostNr = poststed.PostNr WHERE kunde.Knr = {kunde_id} LIMIT 1") # TODO: Stored procedure i stedet for spørring
            
            resultat = spørring.fetchone() # Lagrer resultat fra spørring
            return resultat # Returnerer resultatet
        except mysql.connector.Error as err:
            print(f"Feil ved henting av spesifikke kunder: {err}")
            return []
    else:
        print("Ingen kunder valgt.")
        return []
    
def hent_postnr():
    """
    Funksjon for å hente postnr fra databasen
    Returns:
        List of postnr
    """
    try:
        databasen = tilkobling_database() # Koble til databasen
        spørring = databasen.cursor() # Dette er en virituell "markør"
        spørring.execute("SELECT PostNr FROM poststed") # Henter alle(begrenset til 1000) rader fra definerte kolonner i vare schemaet.
        resultat = spørring.fetchall() # Lagrer resultat fra spørring
        return [postnr[0] for postnr in resultat] # Returnerer resultatet som liste med bare postnr
    except mysql.connector.Error as err:
        print(f"Feil ved henting av postnr: {err}")
        return []

def kunde_valider_helper(streng: Union[str, int], fra: int, til: int, tall: bool= False, postnr: bool=False)->bool:
    """
    Også en funksjon for validering Testing. Dynamisk sjekk om streng stemmer med kravene.
    Args:
        streng: Streng for testing
        fra: Minimum lengde
        til: Maksimum lengde
        tall: True hvis int, standard str
        postnr: True hvis postnr, standard False
    Returns:
        Bool
    """
    if tall:  
        if not isinstance(streng, int):
            return False                                                        
        return fra < streng < til                                               # returnerer True hvis det er mellom angitt verdi
    elif postnr:
        if not streng.isdigit():                                                # Må være kun tall
            return False
        return len(streng)==4                                                   # returnerer True hvis det er 4 siffer
    else:
        if not isinstance(streng, str):
            return False 
        return fra < len(streng) < til 
    
tilgjengelige_postnumre: list[str]= hent_postnr()                               # Henter postnr fra databasen denne trengs bare hentes 1 gang.


def kunde_oppdater(
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
            spørring.callproc('kunde_oppdater', kunde_data ) 
            databasen.commit()
            return True
        except:
            raise ConnectionError("Tilkobling til database mislykket")
        finally:
            databasen.close()
    else:
        raise ValueError("Angitt data er ugyldig")

def kunde_opprett( 
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
            spørring.callproc('kunde_opprett', kunde_data)                      # Sender kunde_data til kunde_opprett SP
            databasen.commit()
            return True
        except:
            raise ConnectionError("Tilkobling til database mislykket")
        finally:
            databasen.close()
    else:
        raise ValueError("Angitt data er ugyldig")

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


