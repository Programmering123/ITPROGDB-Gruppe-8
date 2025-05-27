import os
import datetime
import logging
from decimal import Decimal
from datetime import datetime, timedelta
from fpdf import FPDF
from typing import Any
from random import randint
from moduler.hjelpere import bruker_varsel
from CTkMessagebox import CTkMessagebox
from api.database import lagre_faktura, hent_kunde, hent_ordrelinjer

def generer_faktura(ordredata: dict[str, Any]) -> None:

        ordre_id = ordredata['OrdreNr']
        kundeinfo = hent_kunde(ordredata['KNr'])                                # Henter kundeinfo
        ordrelinjer = hent_ordrelinjer(ordre_id)                                # Henter ordrelinjer
        
        belop = sum(linje[2] * linje[3] for linje in ordrelinjer)               # Beregner totalbeløp eks. mva
        #   Forbereder data for faktura i en Dictionary:
        fakturadata:dict[str, Any] = {
            'kunde_nr': kundeinfo['KNr'],
            'kunde_navn': f"{kundeinfo['Fornavn']} {kundeinfo['Etternavn']}",
            'adresse': kundeinfo['Adresse'],
            'postnummer': kundeinfo['PostNr'],
            'poststed': kundeinfo['Poststed'],
            'ordre_id': ordre_id,
            'ordre_dato': ordredata['OrdreDato'],
            'ordrelinjer': ordrelinjer,
            'dato': str(ordredata['OrdreDato']),
            'fakturanummer': str(ordredata['OrdreNr'])+"-"
            +str(randint(100000, 999999)),                                      # Bruker ordrenummer med tilfeldig tall for å lage unikt fakturanummer
            'belop': belop,           
            'mva': belop  * Decimal(0.25),                                      # MVA-beløp (25% av beløp)   
            'total': int(belop) * Decimal(1.25),                                # Totalbeløp inkl. mva
            'betalingsbetingelser': 14,  
            'var_referanse': "Varelageret AS",
            'deres_referanse': f"{kundeinfo['Fornavn']} {kundeinfo['Etternavn']}",
            'betalingsinformasjon': "1234.56.78910"                             # Eksempel på kontonummer
        }

        try:
            lag_faktura(fakturadata)
        except Exception as e:
            logging.error(f"Feil ved generering av faktura: {e}")

def lag_faktura(
    fd: dict[str, Any],
    filnavn: str = "faktura.pdf"
) -> None:
    """
    Genererer en faktura i PDF-format med spesifiserte detaljer.
    Returns:
        None
    Args:
        fd (dict): En ordbok som inneholder fakturadetaljer som kunde, adresse, postnummer, poststed, ordrenummer,
                   fakturanummer, betalingsbetingelser, betalingsinformasjon, deres referanse, var referanse,
                   fakturadato og ordrelinjer.
        filnavn (str): Navnet på filen som skal lagres. Standard er "faktura.pdf".
    """
    #beregner forfallsdato
    fd['fakturadato'] = datetime.strptime(fd['dato'], "%Y-%m-%d")               # Konverter dato til datetime-objekt
    fd['forfallsdato'] = fd['fakturadato'] + timedelta(days=fd['betalingsbetingelser'])     # Legg til antall dager
    fd['forfallsdato_str'] = fd['forfallsdato'].strftime("%Y-%m-%d")            # Konverter tilbake til streng

    fd['fakturadato_str'] = fd['fakturadato'].strftime("%d.%m.%Y")              # Konverterer dato fra YYYY.MM.DD til dd.mm.yyyy
    fd['forfallsdato_str'] = fd['forfallsdato'].strftime("%d.%m.%Y")            # Konverterer dato fra YYYY.MM.DD til dd.mm.yyyy

    faktura_mappe = "fakturaer"
    if not os.path.exists(faktura_mappe):
        os.makedirs(faktura_mappe)

    filsti = os.path.join(faktura_mappe, f"{fd['fakturanummer']}.pdf")

    pdf = FPDF(format='A4')
    pdf.w = 210 
    pdf.add_font('DejaVu', '', 'assets/fonts/ttf/DejaVuSans.ttf', uni=True)
    pdf.add_font('DejaVu', 'B', 'assets/fonts/ttf/DejaVuSans-Bold.ttf', uni=True)
    pdf.add_font('DejaVu', 'I', 'assets/fonts/ttf/DejaVuSans-Oblique.ttf', uni=True)
    pdf.set_font('DejaVu', size=10)
    pdf.cell
    pdf.add_page()
    # Legger inn logoen
    logo_bredde = 30
    logo_hoyde = 30
    pdf.image("assets/logo.png", x=10, y=10, w=logo_bredde, h=logo_hoyde)       # Plasserer logoen i øverste venstre hjørne av siden

    # Legger til det unike nummeret i PDF-en øverst, i senter av fakturaen
    pdf.cell(190, 10, txt=f"Fakturanummer: {fd['fakturanummer']}", ln=True, align="C")
   
    #plassering av fakuraoverskrift og infofelt(kundeopplysninger, til venstre)
    x = pdf.w - 60
    y = 10
    # pdf.w - logo_bredde - 20
    hoyde = 60
    
    
    pdf.set_xy(x + 2, y + 5)
    pdf.set_font("DejaVu", size=14, style="B")
    pdf.cell(pdf.w - 10, 5, txt="Faktura", ln=True, align="L")
    pdf.set_xy(x + 2, y + 10)
    pdf.set_font("DejaVu", size=8)
    pdf.cell(pdf.w - 10, 5, txt="Fakt.nr.: {}".format(fd['fakturanummer']), ln=True, align="L")
    infofelt1 = [
        "Ordrenummer: {}".format(fd['ordre_id']),
        "Kundenummer: {}".format(fd['kunde_nr']),
        "Deres ref: {}".format(fd['deres_referanse']),
        "Vår ref: {}".format(fd['var_referanse']),
        "Kontonr.:{}".format(fd['betalingsinformasjon']),
        "Fakturadato: {}".format(fd['fakturadato_str']),
        "Forfallsdato: {}".format(fd['forfallsdato_str']),
    ]
    for linje in infofelt1:
        pdf.set_x(x + 2)
        pdf.cell(pdf.w - 10, 5, txt=linje, ln=True, align="L")

    #plassering av fakturainfo referanser (infofelt2, mottaker/kunde)
    x = pdf.w -200
    y = 90
    pdf.w = x + 190    
    hoyde = 60

    pdf.set_font("DejaVu", size=10, style="B")
    pdf.cell(pdf.w, 10, txt="Fakturamottaker:", ln=True, align="L")
    
    infofelt2 = [
        "{}".format(fd['kunde_navn']),                                          # Navn på kunden
        "{}".format(fd['adresse']),                                             # Adresse til kunden         
        "{}".format(fd['postnummer']),                                          # Postnummer til kunden    
        "{}".format(fd['poststed']),                                            # Poststed til kunden
    ]

    for linje in infofelt2:
        pdf.set_x(x + 4)
        pdf.cell(pdf.w - 10, 5, txt=linje, ln=True, align="L")
        
    #overskrift før tabell, ordreoversikt
    pdf.ln(10)
    pdf.cell(pdf.w, 10, txt="Fakturaoversikt for gjeldende ordre", ln=True, align="C")
    pdf.set_font("DejaVu", size=10, style="B")  
 

    #tabelloverskrifter
    pdf.cell(30, 10, txt="Varenr", border=1, align="C")
    pdf.cell(80, 10, txt="Beskrivelse", border=1, align="C")
    pdf.cell(20, 10, txt="Antall", border=1, align="C")
    pdf.cell(30, 10, txt="Pris", border=1, align="C")
    pdf.cell(30, 10, txt="Total", border=1, align="C")
    pdf.set_font("DejaVu", size=8)
    pdf.ln()
    
    #tabellinnhold, ordrelinjer
    #sjekker om ordrelinjer er tom eller har feil struktur
    if not fd['ordrelinjer'] or not all(len(linje) == 4 for linje in fd['ordrelinjer']):
        pdf.cell(
            pdf.w - 10, 10, txt="Ingen ordrelinjer tilgjengelig eller feil struktur.",
            ln=True, align="L")
    else:
        for linje in fd['ordrelinjer']:
            try:
                varenr, beskrivelse, antall, pris = linje
                antall = int(antall)
                pris = float(pris)
                totalpris = antall * pris
                pdf.cell(30, 10, txt=str(varenr), border=1, align="C")
                x, y = pdf.get_x(), pdf.get_y()
                pdf.multi_cell(80, 10, txt=beskrivelse, border=1, align="L")
                pdf.set_xy(x + 80, y)
                pdf.cell(20, 10, txt=str(antall), border=1, align="C")
                pdf.cell(30, 10, txt=f"{pris:.2f} NOK", border=1, align="R")
                pdf.cell(30, 10, txt=f"{totalpris:.2f} NOK", border=1, align="R")
                pdf.ln()
            except (IndexError, ValueError) as e:
                logging.error(f"Feil i ordrelinje: {linje}. Feilmelding: {e}")
                pdf.cell(pdf.w - 10, 10, txt="Feil i ordrelinje.", ln=True, align="L")
    
    
    #sluttsummer, eks mva, mva og total inkl. mva
    bredde = 60
    hoyde = 20
    x = pdf.w - bredde
    y = pdf.get_y()
    
    pdf.rect(x, y, bredde, hoyde)
    summer = [
        "Eks. MVA: {:.2f}".format(fd['belop']),
        "MVA: {:.2f}".format(fd['mva']),
        "Totalt inkl. MVA: {:.2f}".format(fd['total'])
    ]

    pdf.set_xy(x, y + 2)
    pdf.set_font("DejaVu", size=8, style="B") 

    for linje in summer:
        pdf.set_x(x)
        pdf.cell(bredde, 5, txt=linje, ln=True, align="R")
       
    pdf.cell(pdf.w - 10, 10, txt="", ln=True)
    pdf.cell(pdf.w - 10, 10, txt="Takk for handelen!", ln=True, align="C")
    pdf.cell(pdf.w - 10, 10, txt="Vennligst betal innen 14 dager.", ln=True, align="C")
    pdf.cell(pdf.w - 10, 10, txt="Oppgi ordrenummer ved betaling: " \
             "{}".format(fd['ordre_id']),ln=True, align="C")
    pdf.cell(pdf.w - 10, 10, txt="Betal til:" \
    " {}".format(fd['betalingsinformasjon']), ln=True, align="C")
    pdf.cell(pdf.w - 10, 10, txt="Vennligst kontakt oss ved spørsmål.", ln=True, align="C")


    pdf.output(filsti)
    if lagre_faktura(fd['fakturanummer'], str(fd['forfallsdato']), str(fd['fakturadato']), fd['ordre_id']):
        bekreft = CTkMessagebox(
            title="Faktura lagret",
            message=f"Faktura {fd['fakturanummer']} er lagret fakturamappe og i databasen.\n Ønsker du å åpne den?",
            icon="check",
            option_1="OK",
            option_2="Lukk"
        )
        if bekreft.get() == "OK":                                               # Hvis bruker velger OK, åpner vi fakturaen i standard PDF-leser
            os.startfile(filsti)
    else:
        logging.error(f"Kunne ikke lagre faktura {fd['fakturanummer']} i databasen.")
        bruker_varsel(
            melding="Kunne ikke lagre faktura i databasen.\
                  Kontakt systemadministrator.",
            icon="warning"
        )


