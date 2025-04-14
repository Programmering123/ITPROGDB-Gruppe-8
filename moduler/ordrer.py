import customtkinter
from api.database import hent_ordrer # Importer databasen fra api/database.py
class OrdrerModul:
    def __init__(self, master):
        self.master = master

    def vis(self):
        kolonner = ["Ordrenummer", "Kunde", "Dato", "Status"] # Kolonnenavnene som vi skal vise
        try: # prøver å hente data fra databasen.
            data = hent_ordrer(10) # Henter ordrer fra databasen
            # Må vaske dataen litt før vi kan bruke den:
            data = [
                [str(celle) if isinstance(celle, (int, str)) else celle.strftime("%Y-%m-%d") for celle in rad]
                for rad in data
            ]
            #print(data)

        except: # Hvis vi ikke får hentet data så legger vi inn en tom liste.
            print("Feil ved henting av ordrer fra databasen.")
            data = []

        # TODO: Lage søkefelt for å søke i ordrer.
        # Ramme for søkefelt og søkeknapp:
        meny_ramme = customtkinter.CTkFrame(master=self.master, fg_color="lightgrey")
        meny_ramme.grid(row=0, column=0, sticky="nwe", padx=10, pady=10)
        # Søkefelt:
        leteord = customtkinter.CTkEntry(
            master=meny_ramme,
            width=300,
            height=30,
            corner_radius=5,
            fg_color="lightgrey",
            text_color="black",
            bg_color="white",
            placeholder_text="Søk i ordrer...",
            placeholder_text_color="grey",
        )
        leteord.grid(row=0, column=0, sticky="nw", padx=10, pady=10)
        # leteord.grid_rowconfigure(0,minsize=30, weight=1) # Gjør søkefeltet dynamisk justerbart.
        # Søkeknapp:
        knapp_søk = customtkinter.CTkButton(
            master=meny_ramme,
            text="Søk",
            command=lambda: print("søkefunksjon.." + leteord.get()), # TODO: Legg inn søkefunksjon her.
        )
        knapp_søk.grid(row=0, column=1, sticky="nw", padx=10, pady=10)

        # Oppretter en ramme for tabellen:
        tabell_ramme = customtkinter.CTkFrame(master=self.master, fg_color="lightgrey", corner_radius=5)
        tabell_ramme.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Setter opp grid for tabellen og får den til å ta opp hele høyden og bredden:
        self.master.grid_rowconfigure(0, weight=0) # Låser ramme_meny
        self.master.grid_rowconfigure(1, weight=1)  # Fleksibel høyde for tabellen
        self.master.grid_columnconfigure(0, weight=1) # Fleksibel bredde for tabellen



        # Setter opp kolonnene i tabellen:
        for i, kolonne in enumerate(kolonner):
            kolonne_tekst = customtkinter.CTkLabel(
                master=tabell_ramme,
                text=kolonne,
                fg_color="lightgrey",
                text_color="black",
                bg_color="white",
                padx=5,
                pady=5
            )
            kolonne_tekst.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)

        # Legger til dataene i tabellen:
        for i, rad in enumerate(data):
            for j, celle in enumerate(rad):
                celle_tekst = customtkinter.CTkLabel(
                    master=tabell_ramme,
                    text=celle,
                    fg_color="white",
                    text_color="black",
                    bg_color="white",
                    padx=5,
                    pady=5
                )
                celle_tekst.grid(row=i+1, column=j, sticky="nsew", padx=1, pady=1)

        
        #Gjør kolonnene i tabbelen dynamisk justerbare:
        for kolonne in range(len(kolonner)):
            tabell_ramme.grid_columnconfigure(kolonne, weight=1)

