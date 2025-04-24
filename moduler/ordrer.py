# Oppgavetekst: 
# Ha funksjonalitet som lister opp alle ordrer som ligger i databasen.   
# Kunne velge en spesifikk ordre og vise hva slags varer, antall av hver vare som har blitt solgt, 
# pris pr.vare, pris ganger antall, kunde m/navn og adresse og total pris
import customtkinter
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
            ] # TODO: Sjekk ut og hent riktig data.

    def hent_data(self):
        return hent_ordrer()  # Henter kunder fra databasen
    
        # Her lager jeg detaljvisning av varen:
    def vis_detaljer(self, ordre):
        # Lager en ny ramme for detaljvisning:
        valgt_ordre = self.tree.focus()
        verdier = self.tree.item(valgt_ordre)["values"]
        if verdier:
            ordre_id = verdier[0] # Henter ordrenummeret fra den valgte ordren
            ordre_fornavn = verdier[1] # Henter kundenavnet fra den valgte ordren
            ordre_dato = verdier[2] # Henter ordredatoen fra den valgte ordren
            ordre_betalt = verdier[3] # Henter betalt datoen fra den valgte ordren
            ordre_kunde_id = verdier[4] # Henter kundenummeret fra den valgte ordren
            ordrelinjer = hent_ordrelinjer(ordre_id) # Henter ordrelinjene for den valgte ordren
            kundeinfo = hent_spesifikk_kunde(ordre_kunde_id) # Henter kundeinfo for den valgte ordren
       #     hent_spesifikk_ordre(valgt_ordre)
            # Henter detaljene for den valgte ordren:

            print(f"Valgt ordre: {verdier}")
        if self.detalj_visning_ramme:
            self.detalj_visning_ramme.lift(self.tabell_visning_ramme) # Setter detaljvisningrammen i forgrunnen
            self.detalj_visning_ramme.rowconfigure(1, weight=1) # Setter vekten til 1 for å få den til å ta opp hele høyden
            self.detalj_visning_ramme.grid_columnconfigure(0, weight=1) # Setter vekten til 1 for å få den til å ta opp hele bredden
            self.detalj_visning_ramme.grid_columnconfigure(1, weight=0, minsize=200) 
            self.detalj_visning_ramme.grid_columnconfigure(1, minsize=300)
            self.detalj_visning_ramme.grid(padx=10, pady=10) # Plassering av ramme
            # Lager en ny ramme for detaljvisning:
            ramme_header = customtkinter.CTkFrame(
                master=self.detalj_visning_ramme, 
                )
            ramme_header.columnconfigure(0, weight=1) # Setter vekten til 1 for å få den til å ta opp hele bredden
            ramme_header.grid(row=0, column=0, sticky="new", padx=10, pady=10, columnspan=2) # Plassering av ramme
            # ramme for ordreinfo:
            ramme_ordreinfo = customtkinter.CTkFrame(
                master=self.detalj_visning_ramme, 
                )
            ramme_ordreinfo.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

            # ramme for kundeinfo: 
            ramme_kundeinfo = customtkinter.CTkFrame(
                master=self.detalj_visning_ramme, 
                width=300, # Setter bredden på ramme_kundeinfo til 200px
                )
            ramme_kundeinfo.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

            # Knapp for å lukke detaljvisningrammen:
            knapp_lukk = customtkinter.CTkButton(
                master=ramme_header,
                text="X",
                command=self.lukk_detaljer,
            )
            knapp_lukk.grid(row=0,column=2,sticky="w", padx=10, pady=10) # Plassering av lukkeknapp
            # label for ordrenummer:
            label_ordrenummer = customtkinter.CTkLabel(
                master=ramme_header,
                text=f"Ordrenummer: {verdier[0]}",
                font=("Arial", 16, "bold"),
            )
            label_ordrenummer.grid(row=0,column=0,sticky="nw", padx=10, pady=10)

            if(kundeinfo != None):
                print(f"Kundeinfo: {kundeinfo}")
                # Spørring: "SELECT kunde.KNr, kunde.Fornavn, kunde.Etternavn, kunde.Adresse, kunde.PostNr, poststed.Poststed FROM `kunde` INNER JOIN `poststed` ON `kunde.PostNr` = `poststed.PostNr` WHERE kunde.Knr = {kunde_id} LIMIT=1"
                kunde_id = kundeinfo[0] # Henter kundenummeret fra den valgte ordren
                kunde_fornavn = kundeinfo[1] # Henter kundenavnet fra den valgte ordren
                kunde_etternavn = kundeinfo[2] # Henter kundenavnet fra den valgte ordren
                kunde_adresse = kundeinfo[3] # Henter kundenavnet fra den valgte ordren
                kunde_postnr = kundeinfo[4] # Henter kundenavnet fra den valgte ordren
                kunde_poststed = kundeinfo[5] # Henter kundenavnet fra den valgte ordren
                # label for kunde_id:
                label_kunde_id = customtkinter.CTkLabel(
                    master=ramme_kundeinfo,
                    text=f"Kunde ID: {kunde_id}",
                    font=("Arial", 16, "bold"),
                )
                label_kunde_id.grid(row=0,column=0,sticky="nw", padx=10, pady=10)
                # label for kundenavn:
                label_kundenavn = customtkinter.CTkLabel(
                    master=ramme_kundeinfo,
                    text=f"Kunde: {kunde_fornavn} {kunde_etternavn}",
                    font=("Arial", 16, "bold"),
                )
                label_kundenavn.grid(row=1,column=0,sticky="nw", padx=10, pady=10)
                # label for kundeadresse:
                label_kundeadresse = customtkinter.CTkLabel(
                    master=ramme_kundeinfo,
                    text=f"Adresse: {kunde_adresse}",
                    font=("Arial", 16, "bold"),
                )
                label_kundeadresse.grid(row=2,column=0,sticky="nw", padx=10, pady=10)
                # label for kundepostnr og poststed:
                label_kundepostnr = customtkinter.CTkLabel(
                    master=ramme_kundeinfo,
                    text=f"Postnummer: {kunde_postnr} {kunde_poststed}",
                    font=("Arial", 16, "bold"),
                )
                label_kundepostnr.grid(row=3,column=0,sticky="nw", padx=10, pady=10)
            else:
                label_ingen_kunde = customtkinter.CTkLabel(
                    master=ramme_kundeinfo,
                    text="Kundeinfo ikke tilgjengelig",
                    font=("Arial", 16, "bold"),
                )
                label_ingen_kunde.grid(row=0,column=0,sticky="nw", padx=10, pady=10)


            # label for dato:
            label_dato = customtkinter.CTkLabel(
                master=ramme_ordreinfo,
                text=f"Ordredato: {verdier[2]}",
                font=("Arial", 16, "bold"),
            )
            label_dato.grid(row=0,column=0,sticky="nw", padx=10, pady=10)
            
            if ordrelinjer:
                pass
        
    def lukk_detaljer(self):
        if self.detalj_visning_ramme:
            self.detalj_visning_ramme.lower(self.tabell_visning_ramme) # Flytter detaljvisningrammen i bakgrunnen
            for data in self.detalj_visning_ramme.winfo_children():
                data.destroy()


