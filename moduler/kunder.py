# TODO: Lage visning og behandling av kunder Her går det ann å leke seg med customktinker. 
"""
Oppgavetekst:
Vise alle kunder som er registrert i databasen. OBS! Her skal dere bruke «Stored Procedures». 
Legge til og fjerne kunder fra databasen.  
"""
from typing import Dict
from tkinter import ttk
import customtkinter

from api.database import hent_kunder, kunde_oppdater, kunde_opprett # Importer funksjoner for å hente kunder og legge til kunder fra databasen
from moduler.tabellmodul import TabellModul # Importer TabellModul fra tabellmodul.py
from moduler.hjelpere import validering_postnr_sanntid                          # Importer valideringsfunksjon for postnummer fra hjelpfunksjoner.py

""" Her lager vi en kunde modul som arver fra TabellModul."""
"""
Denne modulen skal vise informasjon om alle kunder. 
Den skal også gi mulighet for å opprette ny kunde
Ved dobbeltklikk på dataliste så skal den åpne funksjonen vis_detaljer
Hvor den skal gi mulighet til å behandle datalinje.
"""
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
        #CHECKOUT: dekativert for test.. self.meny_ramme.grid_columnconfigure(0, weight=1)

        self.knapp_opprett_kunde = customtkinter.CTkButton(
            master=self.meny_ramme, # Plassering av knapp for å opprette ny kunde
            text="Opprett ny kunde",
            command=self.vis_detaljer,
            width=30,
        )
        #CHECKOUT: sjekk column 2 er endret til 3 
        self.knapp_opprett_kunde.grid(row=0, column=3, sticky="ne", padx=10, pady=10) # Plassering av knapp for å opprette ny kunde

    def hent_data(self):
        return hent_kunder()  # Henter kunder fra databasen
    
    """ Funksjon for å opprette kunde i databasen: """
    """ 
    Denne har jeg lyst til å lage dynamisk. 
    Tenketanker:
    opprette det visuelle i en funksjon
    en funksjon for oppretting av ny kunde og
    en funksjon for redigering av kunde - Denne sender med data.
    Eller bare en funksjon som har IF KNr -> rediger else: ny kunde.... 
    """
    def vis_detaljer_grafisk(self, kundedata: list=[]):
        pass                                                                    # Placeholder for å lage grafisk visning av kunde data.
    
    def vis_detaljer(self, kundedata: list=[]):
        """ 
        Denne funksjonen bruker i kunder.py til å vise redigeringsvindu
        Den kan valgfritt ta imot kundedata for redigering, eller oppretter kunde uten kundedata 
        Nå finner den rader som er valgt og henter dataen der selv, men tenker det
        er optimalt om vi får mottatt dataen som et argument
        """
        # her kan vi sjekke om len på kundedata != 0 , så kan vi evt hente ut data....
        if len(kundedata) != 0:
            kundenummer, fornavn, etternavn, adresse, postnr = kundedata        # Legger dataen til passende variabler
            print(f" Valgt data: {kundenummer}, {fornavn}, {etternavn}, {adresse}, {postnr}")# TODO: Fjernes
            print(f"Fått data: {kundedata}") # TODO: Fjernes
        
        ## Ha en funksjon her som drar inn GUI innholdet.
        if self.detalj_visning_ramme:                                           # Sjekker om detaljvisningrammen er opprettet. # TODO: Har ingen else... trenger vi den?
            self.detalj_visning_ramme.lift(self.tabell_visning_ramme)           # Løfter detaljvisningrammen opp så den blir synlig.
            self.detalj_visning_ramme.grid(row=0, column=0, sticky="nsew", padx=10, pady=10) # Plassering av ramme
            self.detalj_visning_ramme.grid_rowconfigure(0, weight=0)            # Rad 0 skal holde seg til innholdet.
            self.detalj_visning_ramme.grid_rowconfigure(1, weight=1)            # Rad 1 skal fylle opp plassen i vinduet.
            self.detalj_visning_ramme.grid_columnconfigure(0, weight=1)         # Kolonne 0 skal fylle opp plassen i vinduet.

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

        # Tittel for vindu:
        if len(kundedata) != 0:                                                 # Sjekker om det er mottatt kundedata.
            tittel=f"Rediger kunde: {kundenummer}"                              # Setter tittel til kundenummeret som er valgt. 
        else:
            tittel="Opprett ny kunde"
        etikett_tittel = customtkinter.CTkLabel(
            master=ramme_tittel,
            text=tittel,
            font=("Roboto", 20),
        )
        etikett_tittel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Inputfelt for kunderedigering:
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
        # Valideringsfunksjon for postnummer: TODO: Denne trenger kanskje ikke være her... strukturmessig.
        try:
            valider_postnr_kommando = self.master.register(validering_postnr_sanntid) # Registrerer valideringsfunksjonen for postnummeret.
        except:
            print("Feil ved registrering av valideringsfunksjon for postnummeret.")
        input_postnr = customtkinter.CTkEntry(
            master=ramme_hoved,
            validate="key",
            validatecommand=(valider_postnr_kommando, "%P"),                    # Validerer postnummeret med valideringsfunksjonen.
            width=200,
        )
        # Forskjellig tekst og kommando for å opprette eller redigere kunde:
        if len(kundedata) != 0:                                                 # Sjekker om det er mottatt kundedata eller ny kunde
            lagre_text = "Lagre endringer"                                      
            lagre_kommando = lambda: kunde_oppdater(
                int(kundenummer),                                               
                input_fornavn.get(), 
                input_etternavn.get(),
                input_adresse.get(),
                int(input_postnr.get())                                         
            )
        else:
            lagre_text = "Opprett ny kunde"                                     
            lagre_kommando = lambda: kunde_opprett(
                input_fornavn.get(), 
                input_etternavn.get(), 
                input_adresse.get(), 
                int(input_postnr.get())                                         
            )
        knapp_lagre = customtkinter.CTkButton(
            master=ramme_hoved,
            text=lagre_text,
            command=lagre_kommando
        )
  
        # Plassering av etiketter og inputfelt i ramme_hoved :
        etikett_input_fornavn.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        input_fornavn.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        etikett_input_etternavn.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        input_etternavn.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        etikett_input_adresse.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        input_adresse.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)
        etikett_input_postnr.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
        input_postnr.grid(row=3, column=1, sticky="nsew", padx=10, pady=10)
        knapp_lagre.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        
        # innsetting av verdier, i forbindelse med redigering
        if len(kundedata)!=0:                                                   # Dette skal kun gjøres hvis det er sendt kundedata.
            input_fornavn.insert(0, fornavn)
            input_etternavn.insert(0, etternavn)
            input_adresse.insert(0, adresse)
            input_postnr.insert(0, postnr)



    def kunde_db_opprett(self, fornavn: str, etternavn: str, adresse: str, postnr: int) -> None:
        """Oppretter en ny kunde i databasen."""
        print(f"Oppretter ny kunde: {fornavn} {etternavn}, {adresse}, {postnr}")
        if kunde_opprett(fornavn, etternavn, adresse, postnr): # Legger til kunde i databasen
            # funksjon for å vise alle kunder ellerno her # TODO:
            pass

    def kunde_db_oppdater(self, kundenummer:int, fornavn: str, etternavn: str, adresse: str, postnr: int)->bool:
        """Kall for å endre kunde i database"""
        kundenummer = int(kundenummer)
        postnr = int(postnr)
        print(f"Oppdaterer kunde {kundenummer} med data: Navn: {fornavn} {etternavn}, Adresse: {adresse},Postnr: {postnr}")
        return kunde_oppdater(kundenummer, fornavn, etternavn, adresse, postnr)



