# 📦 ITPROGDB-Gruppe-8: Varelageret

## 🚀 Innledning

Dette prosjektet har som mål å utvikle en brukervennlig GUI-applikasjon for å effektivisere handel og lagerstyring for en kunde. Applikasjonen kobler seg direkte til kundens eksisterende database, og gir en intuitiv måte å administrere varer, ordrer og kunder.

## 🎯 Oppgave

* Utvikle en Python GUI-applikasjon som interagerer med en eksisterende database.
* Implementere funksjonalitet for å vise varelager, håndtere ordrer og administrere kunder.
* Sørge for sikkerhet mot SQL-injection og validere brukerinndata.
* Bruke "Stored Procedures" for spesifikke databaseoperasjoner (f.eks. kundeoversikt).
* Valgfritt: Generere PDF-fakturaer.

### ⚙️ Funksjonalitet

* **Varelager:**
    * Vis liste over varer (varenummer, navn, antall, pris).
    * API-tilgang for visning av varelager i nettleser.
* **Ordrehåndtering:**
    * Vis alle ordrer.
    * Detaljert ordrevisning (varer, antall, priser, kundeinfo, totalpris).
    * Valgfri: Generering av PDF-fakturaer med unike fakturanummer.
* **Kundebehandling:**
    * Vis alle kunder (via "Stored Procedures").
    * Legg til og fjern kunder.
* **Sikkerhet:**
    * Beskyttelse mot SQL-injection.
    * Validering av inndata.
    * Feilhåndtering og sikkerhetsnett mot utilsiktede programstopp.

### 🛠️ Teknologi

* **Programmeringsspråk:** Python
* **GUI-Bibliotek:** Tkinter/Customtkinter
* **Database:** MySQL, mysql-connector-python
* **API:** Flask & Angular
* **PDF-Generering:** FPDF

## 📦 Leveranse

* Programkode (.py eller .zip).
* Gruppelogg.
* Individuelle refleksjonsnotater (video).
* Rapport (10-12 sider).
* Presentasjon (15-20 minutter).

## 📂 Oppsett

# Autokonfigurasjon:
* Anbefales å opprette egen bruker/passord i database
* "assets/varehusdb.sql" Må åpnes og kjøres på lokal database
* Kjør "init.py" i python f eks. "py.exe init.py" følg instrukser
* Kjør "pip install -r requirements.txt"
* Start programmet "py app.py"

# Manuell oppsett
* Anbefales å opprette egen bruker/passord i database
* "assets/varehusdb.sql" Må åpnes og kjøres på lokal database.
* i tillegg må "assets/fakturatabell.sql" åpnes og kjøres på lokal database.
* alle prosedyrer i "assets/sql_sp/" mappen må opprettes i lokal database.
* "pip install -r requirements.txt" må kjøres for å installere nødvendige biblioteker.
* Opprett "secrets.env" fil i rotmappe, denne skal inneholde:
```
DB_HOST = "localhost"
DB_USER = "brukernavn"
DB_PASSWORD = "passord"
DB_PORT = "3306"
```
* Start programmet: "py app.py"

# WebAPI:
"py -m api.app" Åpne så http://localhost:5000 i nettleseren


# Utvikling
## Starte Virtual Environment, kjør disse kommandoene: 
Set-ExecutionPolicy Unrestricted -Scope Process
.\.venv\Scripts\activate

## Innstallerer moduler:
pip install -r .\requirements.txt
Kan testes ved å kjøre pip list, for å se om det er riktige pakker innstallert



