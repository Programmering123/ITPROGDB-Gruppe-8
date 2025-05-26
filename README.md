# 📦 ITPROGDB-Gruppe-8: Handel- og Lagerstyringsapp

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
* **GUI-Bibliotek:** (Tkinter/Customtkinter - begrunnelse i rapport)
* **Database:** (Navn på brukt database)
* **API:** (Evt. brukte api)
* **PDF-Generering:** (Evt. brukte pdf bibloteker)

## 📦 Leveranse

* Programkode (.py eller .zip).
* Gruppelogg.
* Individuelle refleksjonsnotater (video).
* Rapport (10-12 sider).
* Presentasjon (15-20 minutter).

## 📂 Oppsett

# Autokonfigurasjon:



# Starte Virtual Environment, kjør disse kommandoene: 
Set-ExecutionPolicy Unrestricted -Scope Process
.\.venv\Scripts\activate




# Innstallerer moduler:
pip install -r .\requirements.txt
Kan testes ved å kjøre pip list, for å se om det er riktige pakker innstallert

# Konfigurering Mysql database:
Opprett en fil i root som heter secrets.env
Denne skal inneholde:
DB_HOST = "localhost"
DB_USER = "brukernavn"
DB_PASSWORD = "passord"
DB_PORT = "3306"

# Definering av variabler og typebeskrivelse:
variabler prøver vi å definere som <hva>_<navn>. F.eks. en knapp til kunder : knapp_kunder = customtkinter.CTkButton()...
Også fint å prøve å typebeskrive funksjoner og variabler. F.eks. tekst_knapp_kunder: str = "Kunder". Her er det definert at tekst_knapp_kunder er en string, Kan også definere for funksjoner: def funksjon(streng: str)-> bool: Her får man tydelig tilbakemelding at denne funksjonen returnerer en Boolean(True/False). 
Standard Font i programmet er "Roboto".

# WebAPI:
py -m api.app

