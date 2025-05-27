"""
Dette er Ordrer modulen for å vise ordrer i GUI.
Denne er basert på tabellmodulen, og viser ordrer i en tabell.
I tillegg har den en detaljvisning som viser detaljer om den valgte ordren.
"""
import logging
from typing import Any, Literal
from decimal import Decimal

import customtkinter
from tkinter import ttk
from api.database import hent_ordrer, hent_ordre, hent_ordrelinjer              # Importerer database funksjoner relatert til ordrer
from api.database import hent_kunde                                             # Importerer database funksjoner relatert til kunder   
from moduler.tabell import Tabell                                               # Importer TabellModul fra tabell.py
from moduler.fakt import generer_faktura                                        # Importer lag_faktura fra fakt.py
from moduler.hjelpere import bruker_varsel                                        # Importerer bruker_varsel funksjonen for å vise varsler til brukeren

class Ordrer(Tabell):
    def __init__(self, master):
        super().__init__(master)
        # Spørring: KNr, Fornavn, Etternavn, Addresse, PostNr
        self.kolonner = [
            "Ordrenummer",
            "Kunde",
            "Ordre Dato",
            "Betalt Dato",
            "Kunde ID"
            ]
        self.knapp_detaljer_betinget = True

    def hent_data(self):
        return hent_ordrer()                                                    # Overstyrer hent_data() fra TabellModul for å hente ordrer fra databasen
    
    def valg_filter_boks(self):
        """
        Ikke i bruk her.
        """
        pass

    def knapp_detaljer_opprett(self, ramme:customtkinter.CTkFrame)->None:
        """
        Opprettelse av detaljer funksjon, denne kontrolleres av mesterklasse.
        Args:
            ramme (customtkinter.CTkFrame): Ramme der knappen skal opprettes.
        """
        self.knapp_detaljer = customtkinter.CTkButton(
            master=ramme, 
            text="Vis detaljer",
            command=lambda: self.vis_detaljer(                                  # Bruker en lambda for å sende argumenter
                self.tabell.item(self.tabell.focus())['values']                 # Sender verdiene til valgt rad som argument til vis_detaljer()
            ),                                                                  
            state="disabled",                                                   # Setter knappen til disabled , blir styrt av self.knapp_detaljer_betinget             
            width=140,
        )
        self.knapp_detaljer.grid(row=0, column=3, sticky="ne", padx=10, pady=10)

        
    # Detaljvisning av ordre:
    def vis_detaljer(self, ordre:list[Any]|Literal['']):
        """
        Funksjon for å vise detaljer om orderen.
        Args:
            ordre (tuple): Informasjon om valgt ordre fra tabell.
        """
        if ordre is not None and isinstance(ordre, list):
            ordre_id, ordre_kunde_id = ordre[0], ordre[4]                       # Henter ordrenummeret og kundenummeret fra den valgte ordren
            ordredata = hent_ordre(ordre_id)                                    # Henter ordredata for den valgte ordren
            ordrelinjer = hent_ordrelinjer(ordre_id)                            # Henter ordrelinjene for den valgte ordren
            kundeinfo = hent_kunde(ordre_kunde_id)                              # Henter kundeinfo for den valgte ordren
        else:
            bruker_varsel(
                "Vennligst velg en ordre for å vise detaljer.",
                "warning")                                                      # Viser varsel til bruker hvis ingen ordre er valgt
            logging.warning("Vis detaljer, Ingen ordre valgt")                  # Logger advarsel hvis ingen ordre er valgt
            return False                                                        # Avlutter funksjonen

        if not self.vis_ramme_detalj():                                         # Tegner frem detaljrammen og sjekker om den er synlig
            logging.error("Feil ved visning av detaljvisningrammen")            # Logger feil hvis detaljvisningrammen ikke kan vises
            return False                                                        
        
        # Header:
        self.opprett_header(ordredata)                                          # Oppretter headeren for detaljvisningrammen     
        # Kundeinfo: 
        self.opprett_kundeinfo(kundeinfo)                                       # Oppretter kundeinfo og ordrelinjer i detaljvisningrammen
        # Ordreinfo:
        self.opprett_ordreinfo(ordredata, ordrelinjer)                          # Oppretter ordreinfo i detaljvisningrammen

    def opprett_header(self, ordredata:dict[str, Any])->None:
        """ Funksjon for å opprette headeren for detaljvisningrammen."""
        # Lager en ny ramme for detaljvisning:
        ramme_header = customtkinter.CTkFrame(
            master=self.detalj_visning_ramme, 
            )
        ramme_header.columnconfigure(0, weight=1)                               # Ta opp hele bredden
        ramme_header.grid(
            row=0, column=0, sticky="new", padx=10, pady=10, columnspan=2
        )                                                                       # Plassering av ramme
        # Knapp for å lukke detaljvisningrammen:
        knapp_lukk = customtkinter.CTkButton(
            master=ramme_header,
            text="Lukk",
            command=self.lukk_detaljer,
        )
        knapp_lukk.grid(row=0,column=2,sticky="w", padx=10, pady=10)            # Plassering av lukkeknapp

        # etikett for ordrenummer:
        label_ordrenummer = customtkinter.CTkLabel(
            master=ramme_header,
            text=f"Ordrenummer: {ordredata['OrdreNr']}",
        #    font=("Arial", 16, "bold"),
        )
        label_ordrenummer.grid(row=0,column=0,sticky="nw", padx=10, pady=10)
        label_ordredato = customtkinter.CTkLabel(
            master=ramme_header,
            text=f"Ordredato: {ordredata['OrdreDato']}",
        )
        label_ordredato.grid(row=0,column=1,sticky="nw", padx=10, pady=10)

        knapp_genere_faktura = customtkinter.CTkButton(
            master=ramme_header,
            text="Generer faktura",
            command=lambda: generer_faktura(ordredata) # Kaller generer_faktura funksjonen med ordrenummeret
        )
        knapp_genere_faktura.grid(row=2,column=2,sticky="nw", padx=10, pady=10)

    def opprett_kundeinfo(self, kundeinfo:dict[str, Any])-> None:
        """ Funksjon for å opprette kundeinfo i detaljvisningrammen."""
        ramme_kundeinfo = customtkinter.CTkFrame(
            master=self.detalj_visning_ramme, 
            width=300, # Setter bredden på ramme_kundeinfo til 200px
            )
        ramme_kundeinfo.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        if not kundeinfo:                                                       # Sjekker om kundeinfo er tom
            logging.warning("Ingen kundeinfo tilgjengelig for denne ordren")    # Logger advarsel hvis ingen kundeinfo er tilgjengelig
            label_ingen_kunde = customtkinter.CTkLabel(
                master=ramme_kundeinfo,
                text="Kundeinfo ikke tilgjengelig",
            )
            label_ingen_kunde.grid(row=0,column=0,sticky="nw", padx=10, pady=10)
            return                                                              # Avslutter funksjonen hvis ingen kundeinfo er tilgjengelig
        if(kundeinfo is not None):                                              # Sikrer at kundeinfo er
            kunde_id = kundeinfo.get("KNr", "Ikke tilgjengelig")                # Henter kunde ID fra kundeinfo, hvis ikke tilgjengelig vises "Ikke tilgjengelig"
            kunde_fornavn = kundeinfo.get("Fornavn", "Ikke tilgjengelig")       # Henter fornavn fra kundeinfo, hvis ikke tilgjengelig vises "Ikke tilgjengelig" 
            kunde_etternavn = kundeinfo.get("Etternavn", "Ikke tilgjengelig")   # Henter etternavn fra kundeinfo, hvis ikke tilgjengelig vises "Ikke tilgjengelig"
            kunde_adresse = kundeinfo.get("Adresse", "Ikke tilgjengelig")       # Henter adresse fra kundeinfo, hvis ikke tilgjengelig vises "Ikke tilgjengelig"
            kunde_postnr = kundeinfo.get("PostNr", "Ikke tilgjengelig")         # Henter postnummer fra kundeinfo, hvis ikke tilgjengelig vises "Ikke tilgjengelig"
            kunde_poststed = kundeinfo.get("Poststed", "Ikke tilgjengelig")     # Henter poststed fra kundeinfo, hvis ikke tilgjengelig vises "Ikke tilgjengelig"
        logging.debug(f"Kundeinfo hentet: {kundeinfo}")                     # Logger at kundeinfo er hentet

        # label for kunde_id:
        label_kunde_id = customtkinter.CTkLabel(
            master=ramme_kundeinfo,
            text=f"Kunde ID: {kunde_id}"  # Henter kunde ID fra kundeinfo, hvis ikke tilgjengelig vises "Ikke tilgjengelig"
        )
        label_kunde_id.grid(row=0,column=0,sticky="nw", padx=10, pady=10)
        # label for kundenavn:
        label_kundenavn = customtkinter.CTkLabel(
            master=ramme_kundeinfo,
            text=f"Kunde: {kunde_fornavn} {kunde_etternavn}",
        )
        label_kundenavn.grid(row=1,column=0,sticky="nw", padx=10, pady=10)
        # label for kundeadresse:
        label_kundeadresse = customtkinter.CTkLabel(
            master=ramme_kundeinfo,
            text=f"Adresse: {kunde_adresse}",
        )
        label_kundeadresse.grid(row=2,column=0,sticky="nw", padx=10, pady=10)
        # label for kundepostnr og poststed:
        label_kundepostnr = customtkinter.CTkLabel(
            master=ramme_kundeinfo,
            text=f"Postnummer: {kunde_postnr} {kunde_poststed}",
        )
        label_kundepostnr.grid(row=3,column=0,sticky="nw", padx=10, pady=10)

    def opprett_ordreinfo(self, ordredata:dict, ordrelinjer:list[tuple[str, str, int, Decimal]])->None:
        """ Funksjon for å opprette ordreinfo i detaljvisningrammen."""
        # ramme for ordreinfo:
        ramme_ordreinfo = customtkinter.CTkFrame(
            master=self.detalj_visning_ramme, 
            )
        ramme_ordreinfo.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)


        # Bestillingsdato::
        label_dato = customtkinter.CTkLabel(
            master=ramme_ordreinfo,
            text=f"Bestillingsdato: {ordredata['OrdreDato']}",
        )
        label_dato.grid(row=0,column=0,sticky="nw", padx=10, pady=10)
        # Status på ordre:
        label_status_text = "Ordrestatus: Ikke sendt" if ordredata['SendtDato'] == None else f"Ordrestatus: Sendt {ordredata['SendtDato']}"
        label_status = customtkinter.CTkLabel(
            master=ramme_ordreinfo,
            text=label_status_text,
        )
        label_status.grid(row=0,column=1,sticky="nw", padx=10, pady=10)

        # Lager en ramme for ordrelinjer:
        ramme_ordrelinjer = customtkinter.CTkFrame(
            master=ramme_ordreinfo, 
            )
        ramme_ordrelinjer.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)# Plassering av ramme
        
        tabell_ordrelinjer = ttk.Treeview(
            master=ramme_ordrelinjer,
            columns=["VNr", "Betegnelse", "Antall", "Pris", "Total"],
            show="headings",
            height=len(ordrelinjer) if ordrelinjer != None else 1,              # Dynamisk høyde på tabellen basert på antall ordrelinjer
        )
        tabell_ordrelinjer.grid(row=0, column=0, sticky="nsew", padx=10, pady=10) # Plassering av ramme
        # Lager en header for ordrelinjer:
        tabell_ordrelinjer.heading("VNr", text="VNr", anchor="w")
        tabell_ordrelinjer.heading("Betegnelse", text="Betegnelse", anchor="w")
        tabell_ordrelinjer.heading("Antall", text="Antall", anchor="w")
        tabell_ordrelinjer.heading("Pris", text="Pris/stk", anchor="w")
        tabell_ordrelinjer.heading("Total", text="Total", anchor="w")
        tabell_ordrelinjer.column("VNr", anchor="w", width=80)
        tabell_ordrelinjer.column("Betegnelse", anchor="w", width=150)
        tabell_ordrelinjer.column("Antall", anchor="w", width=80)
        tabell_ordrelinjer.column("Pris", anchor="w", width=100)
        tabell_ordrelinjer.column("Total", anchor="w", width=120)
        stil = ttk.Style()                                                      
        stil.configure("Treeview", background="white", foreground="black",
                        highlightthickness=1, bordercolor="grey", border=1)     # Styler cellene
        stil.configure("Treeview.Heading", background="white",
                        foreground="black")                                     # Styler kolonneoverskriftene
        
        # Fyller ordrelinjer i tabellen:
        if ordrelinjer != None:
            ordrelinje_total = ""
            for ordrelinje in ordrelinjer:
                # Henter detaljene for den valgte ordren:
                (
                    ordrelinje_vnr,
                    ordrelinje_betegnelse,
                    ordrelinje_antall,
                    ordrelinje_pris
                ) = ordrelinje                                                  # Setter ordrelinjedata til variabler
                ordrelinje_total = ordrelinje_antall * ordrelinje_pris          # Regner ut totalen for ordrelinjen
                tabell_ordrelinjer.insert("", "end", values=(
                    ordrelinje_vnr,
                    ordrelinje_betegnelse,
                    ordrelinje_antall,
                    ordrelinje_pris,
                    ordrelinje_total
                ))
        else:
            tabell_ordrelinjer.insert("", "end", values=(
                "Ingen ordrelinjer tilgjengelig",
                "",
                "",
                "",
                ""
            ))                                                                  # Setter inn en rad med ingen ordrelinjer tilgjengelig

        # Betalingsstatus:
        etikett_betalt = customtkinter.CTkLabel(
            master=ramme_ordreinfo,
            text=f"Betalingsstatus: {'Betalt '+str(ordredata['BetaltDato']) if ordredata['BetaltDato'] != None else 'Ikke betalt'}",
        )
        etikett_betalt.grid(row=2, column=0, sticky="nw", padx=10, pady=10)        

    def vis_ramme_detalj(self)->bool:
        """ Enkel funksjon for å løfte og vise detaljvisningrammen."""
        if self.detalj_visning_ramme:
            self.detalj_visning_ramme.lift(self.tabell_visning_ramme)           # Setter detaljvisningrammen i forgrunnen
            self.detalj_visning_ramme.rowconfigure(1, weight=1)                 # Setter vekten til 1 for å få den til å ta opp hele høyden
            self.detalj_visning_ramme.grid_columnconfigure(0, weight=1)         # Setter vekten til 1 for å få den til å ta opp hele bredden
            self.detalj_visning_ramme.grid_columnconfigure(1, weight=0, minsize=200) 
            self.detalj_visning_ramme.grid_columnconfigure(1, minsize=300)
            self.detalj_visning_ramme.grid(padx=10, pady=10)                    # Plassering av ramme
            return True
        else:
            logging.error("Ingen detaljvisningramme tilgjengelig")              # Logger feil hvis detaljvisningrammen ikke kan vises
            return False                                                                

    def lukk_detaljer(self):
        if self.detalj_visning_ramme:
            self.detalj_visning_ramme.lower(self.tabell_visning_ramme)          # Flytter detaljvisningrammen i bakgrunnen
            for data in self.detalj_visning_ramme.winfo_children():
                data.destroy()

# GUI definisjoner


