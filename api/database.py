

# Tester tilkobling til database
import mysql.connector
from dotenv import load_dotenv, dotenv_values
import os
from pathlib import Path

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

# Funksjon for å hentre ordrer:
def hent_ordrer():
    try:
        databasen = tilkobling_database() # Koble til databasen
        spørring = databasen.cursor() # Dette er vel en virituell "markør"
        # TODO: Har begrenset spørring på 10(LIMIT), kan ikke ha for mange, programmet henger seg. Finne en dynamisk visning her.
        spørring.execute("SELECT OrdreNr, Fornavn, OrdreDato, BetaltDato FROM ordre INNER JOIN kunde ON ordre.KNr = kunde.KNr LIMIT 10") # Spørringen 
        resultat = spørring.fetchall() # Lagrer resultat fra spørring
        return resultat # Returnerer resultatet
    except mysql.connector.Error as err:
        print(f"Feil ved henting av ordrelinjer: {err}")
        return []
# TODO: Opprette flere funksjoner for hver spørring vi trenger (hva slags spørringer må vi ha? Se i oppgaven.)

# Referanse: https://www.w3schools.com/python/python_mysql_select.asp
# print(mydb)