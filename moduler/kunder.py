"""
Oppgavetekst:
Vise alle kunder som er registrert i databasen. OBS! Her skal dere bruke «Stored Procedures». 
Legge til og fjerne kunder fra databasen.  
"""
import customtkinter

from api.database import hent_kunder, kunde_oppdater, kunde_opprett # Importer funksjoner for å hente kunder og legge til kunder fra databasen
from moduler.tabellmodul import TabellModul # Importer TabellModul fra tabellmodul.py
from moduler.hjelpere import validering_postnr_sanntid                          # Importer valideringsfunksjon for postnummer 
from moduler.hjelpere import validering_adresse_sanntid                         # Importer valideringsfunksjon for adresse 
from moduler.hjelpere import validering_navn_sanntid                         # Importer valideringsfunksjon for adresse 

""" Her lager vi en kunde modul som arver fra TabellModul."""
"""
Denne modulen skal vise informasjon om alle kunder. 
Den skal også gi mulighet for å opprette ny kunde
Ved dobbeltklikk på dataliste så skal den åpne funksjonen vis_detaljer
Hvor den skal gi mulighet til å behandle datalinje.
"""
class KunderModul(TabellModul):
    """
    KunderModul er en klasse som arver fra TabellModul.
    Den viser informasjon om alle kunder i databasen og gir mulighet for å opprette og redigere kunder.
    """
    def __init__(self, master):
        super().__init__(master)
        # Spørring: KNr, Fornavn, Etternavn, Addresse, PostNr
        self.kolonner = [
            "Kundenummer", 
            "Fornavn", 
            "Etternavn", 
            "Adresse", 
            "Postnummer"
            ] # TODO: Sjekk ut og hent riktig data.
        self.vis()
    def ekstra_funksjoner(self):
        self.knapp_opprett_kunde = customtkinter.CTkButton(
            master=self.meny_ramme, # Plassering av knapp for å opprette ny kunde
            text="Opprett ny kunde",
            command=self.vis_detaljer,
            width=30,
        )
        self.knapp_opprett_kunde.grid(row=0, column=3, sticky="ne", padx=10, pady=10) # Plassering av knapp for å opprette ny kunde

    def hent_data(self):
        return hent_kunder()  # Henter kunder fra databasen