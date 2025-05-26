"""
Oppgavetekst:
Vise alle kunder som er registrert i databasen. OBS! Her skal dere bruke «Stored Procedures». 
Legge til og fjerne kunder fra databasen.  
"""
import customtkinter
from CTkMessagebox import CTkMessagebox

from api.database import hent_kunder as db_kunder_hent
from api.database import oppdater_kunde as db_kunde_oppdater
from api.database import opprett_kunde as db_kunde_opprett                      # Importer funksjoner for å hente kunder og legge til kunder fra databasen
from api.database import slett_kunde  as db_kunde_slett                         # Funksjon for å slette kunde, renamet for lettleselighet
from api.database import hent_kunder_filter as db_kunder_hent_filter            # Importer funksjon for å hente kunder med filter
from moduler.tabell import Tabell                                               # Importer TabellModul
from moduler.hjelpere import validering_postnr_sanntid                          # Importer valideringsfunksjon for postnummer 
from moduler.hjelpere import validering_adresse_sanntid                         # Importer valideringsfunksjon for adresse 
from moduler.hjelpere import validering_navn_sanntid                            # Importer valideringsfunksjon for adresse 
from moduler.hjelpere import bruker_varsel                                      # Importer bruker varsel for å vise meldinger til bruker

""" Her lager vi en kunde modul som arver fra TabellModul."""
"""
Denne modulen skal vise informasjon om alle kunder. 
Den skal også gi mulighet for å opprette ny kunde
Ved dobbeltklikk på dataliste så skal den åpne funksjonen vis_detaljer
Hvor den skal gi mulighet til å behandle datalinje.
"""
class Kunder(Tabell):
    """
    KunderModul er en klasse som arver fra TabellModul.
    Den viser informasjon om alle kunder i databasen og gir mulighet for å opprette og redigere kunder.
    """
    def __init__(self, master):
        super().__init__(master)
        self.kolonner = [
            "Kundenummer", 
            "Fornavn", 
            "Etternavn", 
            "Adresse", 
            "Postnummer"
            ]
        self.kundenummer: int | None = None                                      
        self.knapp_detaljer_betinget = False
        self.filter: bool = False

    def knapp_detaljer_opprett(self, _master):
        """
        Opprettelse av universal knapp, denne kontrolleres av mesterklasse.
        Args:
            _master (customtkinter.CTkFrame): Ramme der knappen skal opprettes.
        """
        self.knapp_detaljer = customtkinter.CTkButton(
            master=_master, 
            text="Opprett ny kunde",                                            # Tekst for knappen for å opprette ny kunde
            command=self.vis_detaljer,                                                                  
            state="normal",                                                     # Setter knapp til disabled hvis det ikke er valgt noe
            width=140,
        )
        self.knapp_detaljer.grid(row=0, column=3, sticky="ne", padx=10, pady=10)

    def valg_filter_boks(self):
        """
        Funksjon for å filtrere data i tabellen.
        Denne funksjonen er tom, da vi ikke har noe filter i denne modulen.
        """
        self.velg_filter = customtkinter.CTkCheckBox(
            master=self.meny_ramme,
            text="Vis kunder uten ordre",
            command=self.valg_filter_boks_oppdater,
        )                
        self.velg_filter.grid(row=0, column=2, sticky="nw", padx=10, pady=10) 
    
    def valg_filter_boks_oppdater(self):
        self.filter = not self.filter
        if self.filter:
            self.data = db_kunder_hent_filter()                                        # Henter data fra databasen
            self.let_i_data(self.leteord.get())                                 # Oppdaterer tabellen med data fra databasen
        else:
            self.data = self.hent_data()                                            # Henter data fra databasen
            self.let_i_data(self.leteord.get())                                 # Oppdaterer tabellen med data fra databasen

    def knapp_oppdater_tilstand(self, event):
        pass                                                                    # Fjerner funksjon for å oppdatere tilstand på knappen

    def hent_data(self):
        """Henter data fra databasen og returnerer det som en liste."""
        return db_kunder_hent()                                                 # Henter kundedata fra databasen
    
    def vis_detaljer(self, kundedata: list=[]):
        """ 
        Denne funksjonen brukes i kunder.py til å vise redigeringsvindu
        Den kan valgfritt ta imot kundedata for redigering, eller oppretter kunde uten kundedata
        Den benytter seg av master og bruker detaljvisningrammen som er opprettet i TabellModul. 
        """
        # her kan vi sjekke om len på kundedata != 0 , så kan vi evt hente ut data.... 
        if len(kundedata) != 0:
            self.kundenummer, fornavn, etternavn, adresse, postnr = kundedata   # Legger dataen til passende variabler
        
        if not self.vis_detalj_ramme():
            bruker_varsel("Feil ved oppretting av detaljvisningramme", "error") # Viser feilmelding til bruker
            return False


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
        self.lag_tittel(ramme_tittel)                                           # Lager tittel for vindu, med kundedata hvis det er sendt inn.

        if self.kundenummer:                                                    # Sjekker om det er sendt inn kundedata.
            self.lag_knapp_slett_kunde(ramme_tittel)                            # Lager slett kunde knapp hvis det er sendt inn kundedata.

        # Inputfelt for kunderedigering:
        self.input_fornavn = self.lag_inputfelt(
            ramme_hoved, "Fornavn:", 0, validering_navn_sanntid
        )                                                                       # Lager inputfelt for fornavn, med validering
        self.input_etternavn = self.lag_inputfelt(
            ramme_hoved, "Etternavn", 1, validering_navn_sanntid
        )                                                                       # Lager inputfelt for etternavn, med validering
        self.input_adresse = self.lag_inputfelt(
            ramme_hoved, "Adresse", 2, validering_adresse_sanntid
        )                                                                       # Lager inputfelt for adresse, med validering
        self.input_postnr = self.lag_inputfelt(
            ramme_hoved, "Postnummer:", 3, validering_postnr_sanntid
        )                                                                       # Lager inputfelt for postnummer, med validering

        # Forskjellig tekst og kommando for å opprette eller redigere kunde:
        self.lag_knapp_lagre(ramme_hoved)
        
        # innsetting av verdier, i forbindelse med redigering av kunde:
        if self.kundenummer:                                                    # Dette skal kun gjøres hvis det er sendt kundedata.
            self.input_fornavn[1].insert(0, fornavn)
            self.input_etternavn[1].insert(0, etternavn)
            self.input_adresse[1].insert(0, adresse)
            self.input_postnr[1].insert(0, postnr)

    def lag_tittel(self, ramme: customtkinter.CTkFrame) -> None:
            """
            Lager tittel for redigering eller oppretting.
            Argumenter:
                master_ (customtkinter.CTkFrame): Rammen der tittelen skal plasseres.
            """
            if self.kundenummer:                                                # Sjekker om det er mottatt kundedata.
                tittel=f"Rediger kunde: {self.kundenummer}"                     # Setter tittel til kundenummeret som er valgt. 
            else:
                tittel="Opprett ny kunde"
            etikett_tittel = customtkinter.CTkLabel(
                master=ramme,
                text=tittel,
                font=("Roboto", 20),
            )
            etikett_tittel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    def lag_inputfelt(
            self, 
            ramme: customtkinter.CTkFrame, 
            etikett_: str, 
            rad: int, 
            validering=None
        ) -> tuple[
            customtkinter.CTkLabel, 
            customtkinter.CTkEntry, 
            customtkinter.CTkLabel | None
        ]:
        """
        Lager dynamisk inputfelt for opprettelse av kundedata.
        Oppretter validering om det er sendt inn som argument.
        Argumenter:
            ramme (customtkinter.CTkFrame): Rammen/master der inputfeltet skal plasseres.
            etikett (str): Teksten som skal vises på etiketten.
            rad (int): Radnummeret for etiketten i grid-layoutet.
            validering (function): Valideringsfunksjon for inputfeltet.
        Returverdi:
            tuple: En tuple med etikett, inputfelt og feilmelding.
        """
        etikett = customtkinter.CTkLabel(                                       # Lager etikett for inputfeltet 
            master=ramme,
            text=etikett_,
            font=("Roboto", 14),
            anchor="e",
        )
        etikett.grid(row=rad, column=0, sticky="nsew", padx=10, pady=10)
        inputfelt = customtkinter.CTkEntry(                                     # Lager inputfelt for å opprette ny kunde  
            master=ramme,
            width=200,
        )
        inputfelt.grid(row=rad, column=1, sticky="nsew", padx=10, pady=10)
        feilmelding = None
        if(validering != None):                                                 # Sjekker om validering er sendt inn som argument.
            inputfelt.configure(                                                # Setter opp validering for inputfeltet
                validate="key",
                validatecommand=(
                    self.master.register(
                        lambda postnr: validering(postnr, feilmelding, rad)     # Oppretter lambda for å kunne sende flere argumenter
                    ),
                    "%P"
                )
            )
            feilmelding = customtkinter.CTkLabel(                               # Lager etikett for feilmelding. Teksten blir angitt av valideringsfunksjonen.
                master=ramme,
                font=("Roboto", 14),
                anchor="w",
                text_color="red",
            )
            feilmelding.grid_forget()                                           # Skjuler feilmelding som standard.
        return etikett, inputfelt, feilmelding
    
    def lag_knapp_slett_kunde(self, ramme: customtkinter.CTkFrame) -> None:
        """
        Lager slett kunde knapp for å slette kunde.
        Argumenter:
            ramme (customtkinter.CTkFrame): Rammen der knappen skal plasseres.
        """
        knapp_slett = customtkinter.CTkButton(
            master=ramme,
            text="Slett kunde",
            command=self.slett_kunde,
            width=140,
        )
        knapp_slett.grid(row=0, column=1, sticky="ne", padx=10, pady=10)

    def vis_detalj_ramme(self) -> bool:
        if self.detalj_visning_ramme:                                           # Sjekker om detaljvisningrammen er opprettet. # TODO: Har ingen else... trenger vi den?
            self.detalj_visning_ramme.lift(self.tabell_visning_ramme)           # Løfter detaljvisningrammen opp så den blir synlig.
            self.detalj_visning_ramme.grid(
                row=0, column=0, sticky="nsew", padx=10, pady=10
            )                                                                   # Plassering av ramme
            self.detalj_visning_ramme.grid_rowconfigure(0, weight=0)            # Rad 0 skal holde seg til innholdet.
            self.detalj_visning_ramme.grid_rowconfigure(1, weight=1)            # Rad 1 skal fylle opp plassen i vinduet.
            self.detalj_visning_ramme.grid_columnconfigure(0, weight=1)         # Kolonne 0 skal fylle opp plassen i vinduet.
            return True
        else:
            return False                                                        # TODO: Feilhåndtering hvis detaljvisningrammen ikke er opprettet.



    def lag_knapp_lagre(self, master_: customtkinter.CTkFrame) -> None:
        """
        Lager lagre-knapp for å opprette eller redigere kunde.
        """
        if self.kundenummer:                                                 # Sjekker om det er mottatt kundedata eller ny kunde
            lagre_text = "Lagre endringer"                                      
        else:
            lagre_text = "Opprett ny kunde"                                     

        knapp_lagre = customtkinter.CTkButton(
            master=master_,
            text=lagre_text,
            command=self.lagre_kunde
        )
  
        knapp_lagre.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

    def lagre_kunde(self) -> None:
        """
        Funksjon for å lagre kunde i databasen.
        Henter data fra inputfeltene og sender dem til opprett eller oppdater funksjonen.
        """
        self.kundenummer = int(self.kundenummer) if self.kundenummer else None  # Gjør kundenummer til int eller None hvis det ikke er sendt inn.
        fornavn = self.input_fornavn[1].get()                                   # Henter fornavn fra inputfeltet
        etternavn = self.input_etternavn[1].get()                               # Henter etternavn fra inputfeltet
        adresse = self.input_adresse[1].get()                                   # Henter adresse fra inputfeltet
        postnr = int(self.input_postnr[1].get())                                # Henter postnummer fra inputfeltet

        if self.kundenummer:                                                    # Sjekker vi skal oppdatere eller opprette kunde
            try:
                db_kunde_oppdater(self.kundenummer, fornavn, etternavn, adresse, str(postnr))
                print(f"Kunde {self.kundenummer} oppdatert med data: {fornavn} {etternavn}, {adresse}, {postnr}") # TODO: Fjernes
                self.tabell_visning_ramme.lift(self.detalj_visning_ramme)       # Løfter tabellvisningrammen opp så den blir synlig
                self.detalj_visning_ramme.grid_forget()                         # Skjuler detaljvisningrammen etter lagring av kunde.
                #TODO: Legg til oppdatering av tabellen her.
            except:
                print("Feil ved oppdatering av kunde")                          # TODO: Legg til feilmelding til bruker.
        else:
            try:    
                db_kunde_opprett(fornavn, etternavn, adresse, str(postnr))
                print(f"Opprettet ny kunde med data: {fornavn} {etternavn}, {adresse}, {postnr}") # TODO: Fjernes
                self.tabell_visning_ramme.lift(self.detalj_visning_ramme)       # Løfter tabellvisningrammen opp så den blir synlig
                self.detalj_visning_ramme.grid_forget()                         # Skjuler detaljvisningrammen etter lagring av kunde.
                # TODO: Legg til oppatering av tabellen her.
            except:
                print("Feil ved oppretting av kunde")                           # TODO: Legg til feilmelding til bruker.
    
    def slett_kunde(self) -> bool:
        """Funksjon for å slette kunde i databasen.
        
        Bekrefter sletting av kunde til bruker og sletter kunden fra db

        Args:
            kundenummer (int): Kundenummeret til kunden som skal slettes.
        Returns:
            bool: True hvis sletting var vellykket, False hvis sletting ble avbrutt eller feilet.
        """
        if self.bekreft() == True:                                              # Bekreftelse på sletting av kunde
            print(f"Godkjent sletting av kunde {self.kundenummer}")                               # TODO: Fjernes
        else:
            return False                                                        # Avbryter sletting av kunde hvis bruker trykker nei.
        if self.kundenummer == None:                                            # Sjekker om kundenummer er None
            bruker_varsel("Ingen kunde valgt", "error")                         # Viser varsel til bruker om at ingen kunde er valgt
            return False         
        resultat = db_kunde_slett(self.kundenummer)                             # Sletter kunde fra databasen og lagrer resultatet i variabel
        if  resultat==0:
            bruker_varsel("Ordre bundet mot kunde, kan ikke slette", "warning") # Viser varsel til bruker om at ingen kunde er valgt
        if resultat:    
            bruker_varsel("Kunde er slettet", "check")                          # Sjekker om slettingen var vellykket
            self.leteord.delete(0, "end")                                       # Fjerner søketeksten
            self.filter = False
            self.velg_filter.deselect()                                         
            self.data = self.hent_data()                                        # Henter data fra databasen på nytt
            self.let_i_data("")                                                 # Oppdaterer tabellen etter sletting av kunde
            self.tabell_visning_ramme.lift(self.detalj_visning_ramme)           # Løfter tabellvisningrammen opp så den blir synlig
            self.detalj_visning_ramme.grid_forget()                             # Skjuler detaljvisningrammen etter sletting av kunde.
        return True



    def bekreft(self) -> bool:
        """
        Bekreftelse på sletting av kunde.
        Spør bruker om de er sikker på at de vil slette kunden.
        """
        result = CTkMessagebox(
            title="Bekreft sletting",
            message="Er du sikker på at du vil slette kunden?",
            icon="warning",
            option_1="Ja",
            option_2="Nei",
        )
        svar = True if result.get()=="Ja" else False                            # Setter svar til True hvis bruker trykker ja, ellers False.   
        return svar

