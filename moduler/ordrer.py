import customtkinter
from api.database import hent_ordrer # Importer databasen fra api/database.py
class OrdrerModul:
    def __init__(self, master):
        self.master = master

    def vis(self):
        try:
            data = hent_ordrer() # Henter ordrer fra databasen
            print(data)
            data = [
                [str(celle) if isinstance(celle, (int, str)) else celle.strftime("%Y-%m-%d") for celle in rad]
                for rad in data
            ]
            print(data)

        except:
            print("Feil ved henting av ordrer fra databasen.")
            data = []
        # data = [ # TODO: Hente data fra api/database
        #     ["123", "Kunde A", "2023-10-01", "Fullført",],
        #     ["124", "Kunde B", "2023-10-02", "Under behandling",],
        #     ["125", "Kunde C", "2023-10-03", "Avbrutt",],
        #     ["126", "Kunde D", "2023-10-04", "Fullført",],
        #     ["127", "Kunde E", "2023-10-05", "Under behandling",],
        #     ["128", "Kunde F", "2023-10-06", "Avbrutt",],            
        # ]   # Eksempeldata for ordrer 

        kolonner = ["Ordrenummer", "Kunde", "Dato", "Status"] # Kolonnenavnene

        # Oppretter en ramme for tabellen:
        tabell_ramme = customtkinter.CTkFrame(master=self.master, fg_color="lightgrey", corner_radius=5)
        tabell_ramme.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)


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

