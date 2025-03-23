
#Temp
#Her skal apien komme

# Tester tilkobling til database
import mysql.connector
from dotenv import load_dotenv, dotenv_values
import os
from pathlib import Path
dotenv_path = Path('secrets.env') # sliter med at den ikke leser denne automatisk...
load_dotenv(dotenv_path=dotenv_path)
# load_dotenv() # De 2 foregående linjene skulle vært erstattet med denne, eller 3, siden jeg må importere Path i tillegg.
# Setter opp variabler fra .env fil, tilpasset hver database.
DB_USER = os.getenv("DB_USER")
DB_HOST = os.getenv("DB_HOST")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

mydb = mysql.connector.connect( # Tilkoblingen til databasen
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database = 'varehusdb' # Valgt database.
)
mycursor = mydb.cursor() # Dette er vel en virituell markør
mycursor.execute("SELECT * FROM kunde") # Spørringen
myresult = mycursor.fetchall() # Lagrer resultat fra spørring
for x in myresult: # Skriver ut spørring
    print(x) 

# Referanse: https://www.w3schools.com/python/python_mysql_select.asp
# print(mydb)