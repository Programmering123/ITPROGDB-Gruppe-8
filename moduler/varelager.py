"""
varelager modul for å vise varelageret i GUI
Denne er basert på tabellmodulen, og viser varelageret i en tabell.
"""
from api.database import hent_varelager
from moduler.tabell import Tabell # Importer TabellModul fra tabellmodul.py

class Varelager(Tabell):
    def __init__(self, master):
        super().__init__(master)
        # Spørring: KNr, Fornavn, Etternavn, Addresse, PostNr
        self.kolonner = [
            "Varenummer",
            "Betegnelse",
            "Antall", 
            "Pris"
            ] 

    def hent_data(self):
        return hent_varelager()  # Henter kunder fra databasen
    
    def vis_detaljer(self, data):
        pass

    def valg_filter_boks(self):                                                 
        pass                                                                    # Ikke i bruk i denne modulen. 

    def knapp_detaljer_opprett(self, _master):
        pass                                                                    # Fjerner knappen for detaljer i varelageret, da det ikke er nødvendig å vise detaljer for hver enkelt vare.

