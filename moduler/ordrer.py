# Oppgavetekst: 
# Ha funksjonalitet som lister opp alle ordrer som ligger i databasen.   
# Kunne velge en spesifikk ordre og vise hva slags varer, antall av hver vare som har blitt solgt, 
# pris pr.vare, pris ganger antall, kunde m/navn og adresse og total pris

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