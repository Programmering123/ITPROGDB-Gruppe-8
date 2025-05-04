

# Tester tilkobling til database
import mysql.connector
from dotenv import load_dotenv, dotenv_values
import os
from pathlib import Path
from typing import Dict, Any, Optional, Union

# Henter variabler fra .env filen
dotenv_path = Path('secrets.env')
load_dotenv(dotenv_path=dotenv_path)

# Setter opp variabler fra .env fil, tilpasset hver unike database.
DB_USER = os.getenv("DB_USER")
DB_HOST = os.getenv("DB_HOST")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

# Funksjon for å koble til databasen
def tilkobling_database():
    return mysql.connector.connect( # Tilkoblingen til databasen
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database = 'varehusdb' # Valgt database.
    )

# TODO: Opprette flere funksjoner for hver spørring vi trenger (hva slags spørringer må vi ha? Se i oppgaven.)
# Funksjon for å hentre ordrer: # TODO: Tenker at denne SQLen kan være fin å ha som stored procedure i databasen.
def hent_ordrer(): 
    try:
        databasen = tilkobling_database() # Koble til databasen
        spørring = databasen.cursor() # Dette er vel en virituell "markør"
        # Spørringen henter alle rader fra definerte kolonner, og satt LIMIT til 3000 rader, 
        # virker som om dette virker bra og for denne datamengden er det en fin løsning, 
        # ved større datamengder så måtte vi nok begrenset henting.
        spørring.execute(f"SELECT OrdreNr, Fornavn, OrdreDato, BetaltDato, ordre.KNr FROM ordre INNER JOIN kunde ON ordre.KNr = kunde.KNr LIMIT 0,3000") # Spørringen 
        resultat = spørring.fetchall() # Lagrer resultat fra spørring
        return resultat # Returnerer resultatet
    except mysql.connector.Error as err:
        print(f"Feil ved henting av ordrelinjer: {err}")
        return []
# Funksjon for å hente all data fra spesifikk ordre:
def hent_spesifikk_ordre(ordre_id: int) -> Optional[Dict[str, Any]]:
    if(ordre_id != None):
        try:
            databasen = tilkobling_database() # Koble til databasen
            spørring = databasen.cursor() # Dette er en virituell "markør"
            spørring.execute(f"SELECT OrdreNr, OrdreDato, SendtDato, BetaltDato, KNr FROM ordre WHERE OrdreNr = {ordre_id}") # Henter alle(begrenset til 1000) rader fra definerte kolonner i vare schemaet.
            resultat = spørring.fetchone() # Lagrer resultat fra spørring
            if resultat: # Gjør om resultatet til object <3
                kolonner = [beskrivelse[0] for beskrivelse in spørring.description] # Henter kolonnebeskrivelser
                resultat = dict(zip(kolonner, resultat)) # Lager en dict av resultatet med kolonnenavn som nøkler
            return resultat # Returnerer resultatet
        except mysql.connector.Error as err:
            print(f"Feil ved henting av ordredata: {err}")
            return []
    else:
        print("Ingen ordre valgt.")
        return []
    
# Funksjon for henting av ordrelinjer:
def hent_ordrelinjer(ordre_id):
    try:
        databasen = tilkobling_database() # Koble til databasen
        spørring = databasen.cursor() # Dette er en virituell "markør"
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
        # TODO: Legg til logging av feil her.?
        print(f"Feil ved henting av ordrelinjer: {err}")
        return []
    finally:
        if databasen:
            databasen.close()

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
        print(f"Feil ved henting av varelager: {err}")
        return []

# Funksjon for å hente alle kunder.
def hent_kunder(): #TODO: Korriger denne til å hente en stored procedure i databasen, opprett en stored procedure.
    try:
        databasen = tilkobling_database() # Koble til databasen
        spørring = databasen.cursor() # Dette er en virituell "markør"
        spørring.execute("SELECT KNr, Fornavn, Etternavn, Adresse, PostNr FROM kunde LIMIT 1000") # Henter alle(begrenset til 1000) rader fra definerte kolonner i vare schemaet.
        resultat = spørring.fetchall() # Her skal vi bare ha 1 linje, så vi bruker fetchone() i stedet for fetchall()
        return resultat # Returnerer resultatet
    except mysql.connector.Error as err:
        print(f"Feil ved henting av kunder: {err}")
        return []
    
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

def kunde_valider_helper(streng: Union[str, int], fra: int, til: int, tall: bool= False)->bool:
    """
    Også en funksjon for validering Testing. Dynamisk sjekk om streng stemmer med kravene.
    Args:
        streng: Streng for testing
        fra: Minimum lengde
        til: Maksimum lengde
        tall: True hvis int, standard str
    Returns:
        Bool
    """
    if tall:  
        if not isinstance(streng, int):
            return False # Må være int
        return fra < streng < til
    else:
        if not isinstance(streng, str):
            return False 
        return fra < len(streng) < til 
tilgjengelige_postnumre: list[str]= hent_postnr() # Henter postnr fra databasen denne trengs bare hentes 1 gang.


def kunde_oppdater(
        kundenummer: int,
        fornavn: str,
        etternavn: str,
        adresse: str,
        postnr: int
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
        kunde_valider_helper(kundenummer, 2, 999999999, True) and
        kunde_valider_helper(fornavn, 2, 32) and
        kunde_valider_helper(etternavn, 2, 32) and
        kunde_valider_helper(adresse, 2, 32) and
        kunde_valider_helper(postnr, 0000, 9999, True)
    ):
        kunde_data = (kundenummer, fornavn, etternavn, adresse, postnr)
        try:
            databasen = tilkobling_database() # koble til databasen
            spørring = databasen.cursor() 
            spørring.callproc('kunde_oppdater', kunde_data ) 
            databasen.commit()
            return True
        except:
            raise ConnectionError("Tilbkobling til database mislykket")
        finally:
            databasen.close()
    else:
        raise ValueError("Angitt data er ugyldig")

def kunde_opprett( 
        fornavn: str, 
        etternavn: str, 
        adresse: str,   
        postnr: int    
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

# Referanse: https://www.w3schools.com/python/python_mysql_select.asp
# print(mydb)