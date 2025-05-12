# Oppgavetekst: 
# Ha funksjonalitet som lister opp alle ordrer som ligger i databasen.   
# Kunne velge en spesifikk ordre og vise hva slags varer, antall av hver vare som har blitt solgt, 
# pris pr.vare, pris ganger antall, kunde m/navn og adresse og total pris
import customtkinter
from tkinter import ttk
from api.database import hent_ordrer, hent_spesifikk_ordre, hent_spesifikk_kunde, hent_ordrelinjer
from moduler.tabellmodul import TabellModul # Importer TabellModul fra tabellmodul.py

class OrdrerModul(TabellModul):
    def __init__(self, master):
        super().__init__(master)
        # Spørring: KNr, Fornavn, Etternavn, Addresse, PostNr
        self.kolonner = [
            "Ordrenummer",
            "Kunde",
            "Ordre Dato",
            "Betalt Dato",
            "Kunde ID"
            ] # TODO: Sjekk ut og hent riktig data. Egentlig bare finne ut hva vi trenger å vise av data.
        self.vis_detalj_tekst = "Vis detaljer"                                  # Tekst for detaljvisning

    def hent_data(self):
        return hent_ordrer()  # Henter kunder fra databasen
    
        # Her lager jeg detaljvisning av varen:
    def vis_detaljer(self, ordre):
        """ Funksjon for å vise detaljvisning av ordren."""
        
        if ordre != None:
            ordre_id, ordre_kunde_id = ordre[0], ordre[4]                       # Henter ordrenummeret og kundenummeret fra den valgte ordren
            ordredata = hent_spesifikk_ordre(ordre_id)                          # Henter ordredata for den valgte ordren
            ordrelinjer = hent_ordrelinjer(ordre_id)                            # Henter ordrelinjene for den valgte ordren
            kundeinfo = hent_spesifikk_kunde(ordre_kunde_id)                    # Henter kundeinfo for den valgte ordren
        else:
            return False                                                        # TODO: Feilhåndtering hvis data ikke blir hentet vellykket

        if not self.vis_ramme_detalj():                                         # Tegner frem detaljrammen og sjekker om den er synlig
            return False                                                        # TODO: Feilhåndtering hvis detaljevisningrammen ikke kan vises
        
        # Header:
        self.opprett_header(ordredata)                                          # Oppretter headeren for detaljvisningrammen     
        # Kundeinfo: 
        self.opprett_kundeinfo(kundeinfo)                                       # Oppretter kundeinfo og ordrelinjer i detaljvisningrammen

        self.opprett_ordreinfo(ordredata, ordrelinjer)                          # Oppretter ordreinfo i detaljvisningrammen

    def opprett_header(self, ordredata:dict)->bool:
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

        # label for ordrenummer:
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
    def opprett_kundeinfo(self, kundeinfo:dict)->bool:
        """ Funksjon for å opprette kundeinfo i detaljvisningrammen."""
        ramme_kundeinfo = customtkinter.CTkFrame(
            master=self.detalj_visning_ramme, 
            width=300, # Setter bredden på ramme_kundeinfo til 200px
            )
        ramme_kundeinfo.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)


        if(kundeinfo != None):                                          # Sikrer at kundeinfo er
            (
                kunde_id, 
                kunde_fornavn, 
                kunde_etternavn, 
                kunde_adresse, 
                kunde_postnr, 
                kunde_poststed
            ) = kundeinfo                                               # Setter kundeinfo til variabler

            # label for kunde_id:
            label_kunde_id = customtkinter.CTkLabel(
                master=ramme_kundeinfo,
                text=f"Kunde ID: {kunde_id}",
            #   font=("Arial", 16, "bold"),
            )
            label_kunde_id.grid(row=0,column=0,sticky="nw", padx=10, pady=10)
            # label for kundenavn:
            label_kundenavn = customtkinter.CTkLabel(
                master=ramme_kundeinfo,
                text=f"Kunde: {kunde_fornavn} {kunde_etternavn}",
            #    font=("Arial", 16, "bold"),
            )
            label_kundenavn.grid(row=1,column=0,sticky="nw", padx=10, pady=10)
            # label for kundeadresse:
            label_kundeadresse = customtkinter.CTkLabel(
                master=ramme_kundeinfo,
                text=f"Adresse: {kunde_adresse}",
            #    font=("Arial", 16, "bold"),
            )
            label_kundeadresse.grid(row=2,column=0,sticky="nw", padx=10, pady=10)
            # label for kundepostnr og poststed:
            label_kundepostnr = customtkinter.CTkLabel(
                master=ramme_kundeinfo,
                text=f"Postnummer: {kunde_postnr} {kunde_poststed}",
            #    font=("Arial", 16, "bold"),
            )
            label_kundepostnr.grid(row=3,column=0,sticky="nw", padx=10, pady=10)
        else:
            label_ingen_kunde = customtkinter.CTkLabel(
                master=ramme_kundeinfo,
                text="Kundeinfo ikke tilgjengelig",
            #    font=("Arial", 16, "bold"),
            )
            label_ingen_kunde.grid(row=0,column=0,sticky="nw", padx=10, pady=10)

    def opprett_ordreinfo(self, ordredata:dict, ordrelinjer:dict)->bool:
        """ Funksjon for å opprette ordreinfo i detaljvisningrammen."""
        # ramme for ordreinfo:
        vis_detalj_knapp = self.vis_detalj_knapp                                # Henter detaljknappen fra TabellModul
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
        stil = ttk.Style()                                                      # TODO: kunne tenkt meg at det ikke var border rundt tabell, men bare strek under radene f feks. cleanere look.
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
                ) = ordrelinje # Setter ordrelinjedata til variabler
                ordrelinje_total = ordrelinje_antall * ordrelinje_pris # Regner ut totalen for ordrelinjen
                tabell_ordrelinjer.insert("", "end", values=(
                    ordrelinje_vnr,
                    ordrelinje_betegnelse,
                    ordrelinje_antall,
                    ordrelinje_pris,
                    ordrelinje_total
                ))
        else:
            tabell_ordrelinjer.insert("", "end", values=("Ingen ordrelinjer tilgjengelig", "", "", "", "")) # Setter inn en rad med ingen ordrelinjer tilgjengelig

        # Betalingsstatus:
        etikett_betalt = customtkinter.CTkLabel(
            master=ramme_ordreinfo,
            text=f"Betalingsstatus: {'Betalt '+str(ordredata['BetaltDato']) if ordredata['BetaltDato'] != None else 'Ikke betalt'}",
        )
        etikett_betalt.grid(row=2, column=0, sticky="nw", padx=10, pady=10)        
        vis_detalj_knapp.configure(
            state="disabled"
        )
        def knapp_oppdater_tilstand(event):
            print("Oppdaterer knapp tilstand")
            if tabell_ordrelinjer.selection():
                print("Valgt ordrelinje")
                vis_detalj_knapp.configure(state="normal") # Aktiverer detaljknappen hvis det er valgt en ordrelinje
            else:
                print("Ingen ordrelinje valgt")
                vis_detalj_knapp.configure(state="disabled")
        tabell_ordrelinjer.bind("<<TreeviewSelect>>", knapp_oppdater_tilstand)

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
            return False                                                        # TODO: Feilhåndtering ?

    def lukk_detaljer(self):
        if self.detalj_visning_ramme:
            self.detalj_visning_ramme.lower(self.tabell_visning_ramme)          # Flytter detaljvisningrammen i bakgrunnen
            for data in self.detalj_visning_ramme.winfo_children():
                data.destroy()


# GUI definisjoner


