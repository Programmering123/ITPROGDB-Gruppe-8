* Først må databasen bli opprettet. Antar vi gjør dette i MySQL Workbench. Importer SQL fil varehusDB.sql og kjør denne - Alle tabeller skal dukke opp.
* Det er mulig å opprette egen bruker til database ved å gå på "Server/Users and Priviledges" Brukernavn og passord må brukes senere.



* Opprett en fil til som slutter på .env (f.eks. secrets.env ) Her må vi definere variabler som skal bruker i api/database.py - Legger inn mal her, men bruk egne brukernavn/passord.:

DB_HOST = "localhost"
DB_USER = "DittBrukernavn"
DB_PASSWORD = "DittPassord"
DB_PORT = "3306"

* Sånn - da skal filer som ikke blir syncet med github være i orden.
* Kjør disse kommandoene i terminalen i VSCode f eks, evt i cmd, men sikkert lurt å gjøre det i GitHub Repo mappen. (Ikke ta med kommentarene mine )
py -m pip install mysql-connector-python # for tilkobling til mysql DB
python -m pip install python-dotenv # For å inkludere sjult .env fil.
python -m pip install path # For å definere env fil . Usikker på om vi må ha denne., prøv gjerne først uten.

* Nå skal dere teoretisk kunne kjøre database.py og få ut data fra databasen! :)
