"""
Varierte hjelpefunksjoner for å håndtere data og konverteringer.

Funksjoner for å håndtere data og konverteringer til gjenbruk i andre moduler
og klasser.
"""
from api.database import tilgjengelige_postnumre


def validering_postnr_sanntid(postnr: str) -> bool:
    """
    Validerer postnummeret i sanntid.
    Argumenter:
        postnr (str): Postnummeret som skal valideres.
    Returverdi:
        bool: True hvis postnummeret er gyldig, False ellers.
    """
    if postnr == "":
        return True                                                             # Tillatter tomt felt

    if not (0 < len(postnr) <= 4 and postnr.isdigit()):
        return False                                                            # Hvis det ikke er tall, eller lengden er feil, returner False

    for number in tilgjengelige_postnumre:                                      # Sjekker om postnummeret er gyldig
        if postnr == number[: len(postnr)]:                                     # Sammenligner gitt tall med lik andel av postnr
            return True

    return False                                                                # Returner False hvis det ikke er gyldig postnummer

