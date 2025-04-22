# TODO: Lage visning og behandling av kunder Her går det ann å leke seg med customktinker. 
# Jeg tenker vi kan leke oss litt her først. Husk at riktig moduler må være importert ført. 
from api.database import hent_kunder
from moduler.tabellmodul import TabellModul # Importer TabellModul fra tabellmodul.py

class KunderModul(TabellModul):
    def __init__(self, master):
        super().__init__(master)
        # Spørring: KNr, Fornavn, Etternavn, Addresse, PostNr
        self.kolonner = [
            "Kundenummer", 
            "Fornavn", 
            "Etternavn", 
            "Adresse", 
            "Postnummer"
            ] # TODO: Sjekk ut og hent riktig data.

    def hent_data(self):
        return hent_kunder()  # Henter kunder fra databasen