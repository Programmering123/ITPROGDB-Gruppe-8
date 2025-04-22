# TODO: Lage oversikt over varelager, i tillegg mulighet for å legge til og fjerne ting?
# Oppgaveteksten:
# Vise en liste over hvilke varer som er på varelageret, inkludert varenummer, navn på varen, antall og pris.  
# I tillegg til å vise varelageret i selv Python programmet skal dere ved bruk av en API vise varelageret i en nettleser.
import customtkinter
from api.database import hent_varelager
from moduler.tabellmodul import TabellModul # Importer TabellModul fra tabellmodul.py

class VarelagerModul(TabellModul):
    def __init__(self, master):
        super().__init__(master)
        # Spørring: KNr, Fornavn, Etternavn, Addresse, PostNr
        self.kolonner = [
            "Varenummer",
            "Betegnelse",
            "Antall", 
            "Pris"
            ] # TODO: Sjekk ut og hent riktig data.

    def hent_data(self):
        return hent_varelager()  # Henter kunder fra databasen
    
    # Her lager jeg detaljvisning av varen:
    def visning_detaljer(self, varenummer):
        # Lager en ny ramme for detaljvisning:
        detalj_ramme = customtkinter.CTkFrame(master=self.master, fg_color="lightgrey", corner_radius=5)
        detalj_ramme.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        # Setter opp grid for detaljvisning og får den til å ta opp hele høyden og bredden:
        detalj_ramme.grid_rowconfigure(0, weight=1)
        detalj_ramme.grid_columnconfigure(0, weight=1)