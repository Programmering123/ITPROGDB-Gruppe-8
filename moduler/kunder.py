# TODO: Lage visning og behandling av kunder Her går det ann å leke seg med customktinker. 
"""
Oppgavetekst:
Vise alle kunder som er registrert i databasen. OBS! Her skal dere bruke «Stored Procedures». 
Legge til og fjerne kunder fra databasen.  
"""
from typing import Dict
from tkinter import ttk
import customtkinter
from api.database import hent_kunder, legg_til_kunde # Importer funksjoner for å hente kunder og legge til kunder fra databasen
from moduler.tabellmodul import TabellModul # Importer TabellModul fra tabellmodul.py

""" Her lager vi en kunder modul som arver fra TabellModul."""
class KunderModul(TabellModul):
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
        self.meny_ramme.grid_columnconfigure(0, weight=1) # Sentrerer innhold

        self.knapp_opprett_kunde = customtkinter.CTkButton(
            master=self.meny_ramme, # Plassering av knapp for å opprette ny kunde
            text="Opprett ny kunde",
            command=self.opprett_kunde,
            width=30,
        )
        self.knapp_opprett_kunde.grid(row=0, column=2, sticky="ne", padx=10, pady=10) # Plassering av knapp for å opprette ny kunde

    def hent_data(self):
        return hent_kunder()  # Henter kunder fra databasen
    def opprett_kunde(self):
        """Oppretter en ny kunde i databasen."""
        if self.detalj_visning_ramme:
            self.detalj_visning_ramme.lift(self.tabell_visning_ramme) # Løfter detaljvisningrammen opp
            self.detalj_visning_ramme.grid(row=0, column=0, sticky="nsew", padx=10, pady=10) # Plassering av ramme
            self.detalj_visning_ramme.grid_rowconfigure(0, weight=0) # Låser detaljvisningrammen
            self.detalj_visning_ramme.grid_rowconfigure(1, weight=1)
            self.detalj_visning_ramme.grid_columnconfigure(0, weight=1)

            # lager en ramme info ramme for å opprette ny kunde:
            ramme_tittel = customtkinter.CTkFrame(
                master=self.detalj_visning_ramme,
            )
            ramme_tittel.grid(row=0, column=0, sticky="new", padx=10, pady=10)
            # Ramme for tekstfelt
            ramme_hoved = customtkinter.CTkFrame(
                master=self.detalj_visning_ramme,
            )
            ramme_hoved.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
            etikett_tittel = customtkinter.CTkLabel(
                master=ramme_tittel,
                text="Opprett ny kunde",
                font=("Roboto", 20),
            )
            etikett_tittel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
            """     
            Feltene som skal være med i oppretting av ny kunde: 
            "Kundenummer", 
            "Fornavn", 
            "Etternavn", 
            "Adresse", 
            "Postnummer" 
            """
            etikett_input_fornavn = customtkinter.CTkLabel(
                master=ramme_hoved,
                text="Fornavn:",
                font=("Roboto", 14),
                anchor="e",
            )
            input_fornavn = customtkinter.CTkEntry(
                master=ramme_hoved,
                placeholder_text="Fornavn",
                width=200,
            )
            etikett_input_etternavn = customtkinter.CTkLabel(
                master=ramme_hoved,
                text="Etternavn:",
                font=("Roboto", 14),
                anchor="e",
            )
            input_etternavn = customtkinter.CTkEntry(
                master=ramme_hoved,
                placeholder_text="Etternavn",
                width=200,
            )
            etikett_input_adresse = customtkinter.CTkLabel(
                master=ramme_hoved,
                text="Adresse:",
                font=("Roboto", 14),
                anchor="e",
            )
            input_adresse = customtkinter.CTkEntry(
                master=ramme_hoved,
                placeholder_text="Adresse",
                width=200,
            )
            etikett_input_postnr = customtkinter.CTkLabel(
                master=ramme_hoved,
                text="Postnummer:",
                font=("Roboto", 14),
                anchor="e",
            )
            input_postnr = customtkinter.CTkEntry(
                master=ramme_hoved,
                placeholder_text="Postnummer",
                width=200,
            )
            knapp_opprett = customtkinter.CTkButton(
                master=ramme_hoved,
                text="Opprett",
                command=lambda: self.opprett_kunde_db(
                    input_fornavn.get(), 
                    input_etternavn.get(), 
                    input_adresse.get(), 
                    input_postnr.get()
                )
            )
            # Plassering av etiketter og inputfelt i ramme_hoved:
            etikett_input_fornavn.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
            input_fornavn.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
            etikett_input_etternavn.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
            input_etternavn.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
            etikett_input_adresse.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
            input_adresse.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)
            etikett_input_postnr.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
            input_postnr.grid(row=3, column=1, sticky="nsew", padx=10, pady=10)
            knapp_opprett.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
            
    
    def opprett_kunde_db(self, fornavn: str, etternavn: str, adresse: str, postnr: int):
        """Oppretter en ny kunde i databasen. TODO: Legg til databasefunksjon."""
        print(f"Oppretter ny kunde: {fornavn} {etternavn}, {adresse}, {postnr}")
        legg_til_kunde(fornavn, etternavn, adresse, postnr) # Legger til kunde i databasen
        # TODO: Så må vi oppdatere tabellen med ny kunde..
        



