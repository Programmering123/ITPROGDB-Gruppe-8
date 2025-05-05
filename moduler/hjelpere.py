"""
Varierte hjelpefunksjoner for å håndtere data og konverteringer.

Funksjoner for å håndtere data og konverteringer til gjenbruk i andre moduler
og klasser.
"""
import customtkinter # Importerer kun for typehinting.
from api.database import tilgjengelige_postnumre


def validering_postnr_sanntid(postnr: str, etikett: customtkinter.CTkEntry) -> bool:
    """
    Validerer postnummeret i sanntid.
    Argumenter:
        postnr (str): Postnummeret som skal valideres.
    Returverdi:
        bool: True hvis postnummeret er gyldig, False ellers.
    """
    if postnr == "":
        # etikett.grid_forget()                             # Setter farge på inputfeltet til hvit hvis det er tomt felt
        return True                                                             # Tillatter tomt felt

    if not (0 < len(postnr) <= 4 and postnr.isdigit()):
        # etikett.grid(row=3, column=2, sticky="nsew", padx=10, pady=10)                             # Setter farge på inputfeltet til rød hvis det ikke er gyldig postnummer
        return False                                                            # Hvis det ikke er tall, eller lengden er feil, returner False

    for number in tilgjengelige_postnumre:                                      # Sjekker om postnummeret er gyldig
        if postnr == number[: len(postnr)]:                                     # Sammenligner gitt tall med lik andel av postnr
            # etikett.grid_forget()                     # Setter farge på inputfeltet til grønn hvis det er gyldig postnummer
            return True
    # etikett.grid(row=3, column=2, sticky="nsew", padx=10, pady=10)                                     # Setter farge på inputfeltet til rød hvis det ikke er gyldig postnummer
    return False                                                                 # Returner False hvis det ikke er gyldig postnummer

