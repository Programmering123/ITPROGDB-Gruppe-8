# 📦 ITPROGDB-Gruppe-8: Handel- og Lagerstyringsapp

## 🚀 Innledning

Dette prosjektet har som mål å utvikle en brukervennlig GUI-applikasjon for å effektivisere handel og lagerstyring for en kunde. Applikasjonen kobler seg direkte til kundens eksisterende database, og gir en intuitiv måte å administrere varer, ordrer og kunder.

## 🎯 Oppgave

* Utvikle en Python GUI-applikasjon som interagerer med en eksisterende database.
* Implementere funksjonalitet for å vise varelager, håndtere ordrer og administrere kunder.
* Sørge for sikkerhet mot SQL-injection og validere brukerinndata.
* Bruke "Stored Procedures" for spesifikke databaseoperasjoner (f.eks. kundeoversikt).
* Valgfritt: Generere PDF-fakturaer.
# TODO: Tegne ut GUI i plantegning.
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

## 📂 Struktur

# Starte Virtual Environment, kjør disse kommandoene: 
Set-ExecutionPolicy Unrestricted -Scope Process
.\.venv\Scripts\activate

# Innstallerer moduler:
pip install -r .\requirements.txt

Kan testes ved å kjøre pip list, for å se om det er riktige pakker innstallert


# Database SP(Store Procedure)
## Enten kjør som spørring :
DELIMITER //
CREATE PROCEDURE LeggTilKunde(
    IN p_fornavn VARCHAR(255),
    IN p_etternavn VARCHAR(255),
    IN p_adresse VARCHAR(255),
    IN p_postnr VARCHAR(10)
)
BEGIN
    -- Hvis du ikke bruker AUTO_INCREMENT for KNr:
    SELECT MAX(KNr) INTO @siste_knr FROM Kunder;
    SET @ny_knr = IFNULL(@siste_knr, 0) + 1;
    INSERT INTO kunde (KNr, Fornavn, Etternavn, Adresse, PostNr) VALUES (@ny_knr, p_fornavn, p_etternavn, p_adresse, p_postnr);
    -- Hvis du bruker AUTO_INCREMENT, trenger du ikke hente KNr her.
END //
DELIMITER ;
## Eller legg inn i SP i MySQL Workbench:
CREATE DEFINER=`root`@`localhost` PROCEDURE `LeggTilKunde`(
    IN p_fornavn VARCHAR(255),
    IN p_etternavn VARCHAR(255),
    IN p_adresse VARCHAR(255),
    IN p_postnr VARCHAR(10)
)
BEGIN
    SELECT MAX(KNr) INTO @siste_knr FROM Kunde;
    SET @ny_knr = IFNULL(@siste_knr, 0) + 1;
    INSERT INTO kunde (KNr, Fornavn, Etternavn, Adresse, PostNr) VALUES (@ny_knr, p_fornavn, p_etternavn, p_adresse, p_postnr);
END
