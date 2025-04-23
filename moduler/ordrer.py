# Oppgavetekst: 
# Ha funksjonalitet som lister opp alle ordrer som ligger i databasen.   
# Kunne velge en spesifikk ordre og vise hva slags varer, antall av hver vare som har blitt solgt, 
# pris pr.vare, pris ganger antall, kunde m/navn og adresse og total pris
import customtkinter
from api.database import hent_ordrer
from moduler.tabellmodul import TabellModul # Importer TabellModul fra tabellmodul.py

class OrdrerModul(TabellModul):
    def __init__(self, master):
        super().__init__(master)
        # Spørring: KNr, Fornavn, Etternavn, Addresse, PostNr
        self.kolonner = [
            "Ordrenummer",
            "Kunde",
            "Dato",
            "Status"
            ] # TODO: Sjekk ut og hent riktig data.

    def hent_data(self):
        return hent_ordrer()  # Henter kunder fra databasen
    
        # Her lager jeg detaljvisning av varen:
    def vis_detaljer(self, ordre):
        # Lager en ny ramme for detaljvisning:
        valgt_ordre = self.tree.focus()
        verdier = self.tree.item(valgt_ordre)["values"]
        if verdier:
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

            # label for kundeinfo:
            label_kundeinfo = customtkinter.CTkLabel(
                master=ramme_kundeinfo,
                text=f"Kunde: {verdier[1]}",
                font=("Arial", 16, "bold"),
            )
            label_kundeinfo.grid(row=0,column=0,sticky="nw", padx=10, pady=10)

            # label for dato:
            label_dato = customtkinter.CTkLabel(
                master=ramme_ordreinfo,
                text=f"Ordredato: {verdier[2]}",
                font=("Arial", 16, "bold"),
            )
            label_dato.grid(row=0,column=0,sticky="new", padx=10, pady=10)

        
    def lukk_detaljer(self):
        if self.detalj_visning_ramme:
            self.detalj_visning_ramme.lower(self.tabell_visning_ramme) # Flytter detaljvisningrammen i bakgrunnen
            for data in self.detalj_visning_ramme.winfo_children():
                data.destroy()


