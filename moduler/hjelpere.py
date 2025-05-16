"""
Varierte hjelpefunksjoner for å håndtere data og konverteringer.

Funksjoner for å håndtere data og konverteringer til gjenbruk i andre moduler
og klasser.
"""
import customtkinter # Importerer kun for typehinting.
from CTkMessagebox import CTkMessagebox
from api.database import tilgjengelige_postnumre
import re

def validering_postnr_sanntid(
        postnr: str,
        feilmelding: customtkinter.CTkLabel,
        rad: int
    ) -> bool:
    """
    Validerer postnummeret i sanntid.
    Argumenter:
        postnr (str): Postnummeret som skal valideres.
        feilmelding (customtkinter.CTkLabel): Etikett for å vise feilmelding.
        rad (int): Radnummeret for etiketten i grid-layoutet.
    Returverdi:
        bool: True hvis postnummeret er gyldig, False ellers.
    """
    if postnr == "":
        feilmelding.grid_forget()                                               # Skjuler feilmelding
        return True                                                             # Tillatter tomt felt
    if not (0 < len(postnr) <= 4 and postnr.isdigit()):                         # Sjekker om postnummeret er et tall og har riktig lengde
        feilmelding.configure(text = "Kun tall og 4 siffer")                    # Feilmelding til bruker
        feilmelding.grid(row=rad, column=2, sticky="nsew", padx=10, pady=10)    # Viser feilmelding
        return False                                                            # Hvis det ikke er tall, eller lengden er feil, returner False
    for number in tilgjengelige_postnumre:                                      # Sjekker om postnummeret er gyldig
        if postnr == number[: len(postnr)]:                                     # Sammenligner gitt tall med lik andel av postnr
            feilmelding.grid_forget()                                           # Gjemmer feilmelding
            return True
    feilmelding.configure(text = "Ikke gyldig postnummer")                      # Feilmelding til bruker
    feilmelding.grid(row=rad, column=2, sticky="nsew", padx=10, pady=10)        # Viser feilmelding
    return False                                                                # Returner False hvis det ikke er gyldig postnummer

def validering_adresse_sanntid(
        adresse: str,
        feilmelding: customtkinter.CTkEntry,
        rad: int
    ) -> bool:
    """
    Validerer adressen i sanntid. 
    Gir feilmelding til angitt etikett hvis adressen er ugyldig.
    Adressen kan inneholde bokstaver, tall, mellomrom, punktum og bindestrek.
    Argumenter:
        adresse (str): Adressen som skal valideres.`
        etikett (customtkinter.CTkEntry): Etikett for å vise feilmelding.
    Returverdi:
        bool: True hvis adressen er gyldig, False ellers.
    """
    if adresse == "":
        feilmelding.grid_forget()                                               # Skjuler feilmelding
        return True    
    if not (len(adresse) <= 30):                                                # Sjekker lengden på adressen   
        feilmelding.configure(text = "Maks 30 tegn")                            # Feilmelding til bruker
        feilmelding.grid(row=rad, column=2, sticky="nsew", padx=10, pady=10)    # Viser feilmelding
        return False
    tillatt_regex = r"^[a-zA-Z0-9æøåÆØÅéÉ\s.,-]+$"                                # Regex for tillatte karakterer
    if not re.match(tillatt_regex, adresse):                                    # Sjekker om adressen inneholder tillatte karakterer 
        feilmelding.configure(text = "Kun bokstaver og tall")                   # Feilmelding til bruker
        feilmelding.grid(row=rad, column=2, sticky="nsew", padx=10, pady=10)    # Viser feilmelding
        return False
    feilmelding.grid_forget()                                                   # Skjuler feilmelding
    return True

def validering_navn_sanntid(
        navn: str,
        feilmelding: customtkinter.CTkEntry,
        rad: int
    ) -> bool:
    """
    Validerer navnet i sanntid. 
    Gir feilmelding til angitt etikett hvis navnet er ugyldig.
    Navnet kan inneholde bokstaver, mellomrom, punktum og bindestrek.
    Argumenter:
        navn (str): Navnet som skal valideres.`
        etikett (customtkinter.CTkEntry): Etikett for å vise feilmelding.
    Returverdi:
        bool: True hvis navnet er gyldig, False ellers.
    """
    if navn == "":
        feilmelding.grid_forget()                                               # Skjuler feilmelding
        return True    
    if not (len(navn) <= 30):                                                   # Sjekker lengden på navnet   
        feilmelding.configure(text = "Maks 30 tegn")                            # Feilmelding til bruker
        feilmelding.grid(row=rad, column=2, sticky="nsew", padx=10, pady=10)    # Viser feilmelding
        return False
    tillatt_regex = r"^[a-zA-ZæøåÆØÅéÉ\s.,-]+$"                                   # Regex for tillatte karakterer
    if not re.match(tillatt_regex, navn):                                       # Sjekker om navnet inneholder tillatte karakterer 
        feilmelding.configure(text = "Kun bokstaver")                           # Feilmelding til bruker
        feilmelding.grid(row=rad, column=2, sticky="nsew", padx=10, pady=10)    # Viser feilmelding
        return False
    feilmelding.grid_forget()                                                   # Skjuler feilmelding
    return True

def bruker_varsel(
        melding: str,
        icon: str,
    ) -> CTkMessagebox:
    """
    Viser en varselmelding via CTkMessagebox.

    Args:
        melding (str): Meldingsteksten som skal vises.
        icon (str): Ikon som skal brukes "ckeck", "warning" eller "info".
    """
    if icon not in ["warning", "info", "check"]:                                # Sjekker om ikonet er gyldig
        raise ValueError("Ikon må være 'warning', 'check' eller 'info'")        # Hever feil hvis ikonet ikke er gyldig
    boks = CTkMessagebox(
        title="Varsel",
        message=melding,
        icon=icon,
        option_1="OK",
    )                                                                           # Viser melding til bruker
    return boks