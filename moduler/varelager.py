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
    
    def vis_detaljer(self, data):
        pass
    
