import os
import datetime
import logging
from datetime import datetime, timedelta
from fpdf import FPDF
from moduler.hjelpere import bruker_varsel
from api.database import lagre_faktura, hent_spesifikk_kunde, hent_ordrelinjer

def generer_faktura(ordre_id, verdier):

        ordre_id = verdier[0]
        kundeinfo = hent_spesifikk_kunde(verdier[4])                            #henter kundeinfo
        ordrelinjer = hent_ordrelinjer(ordre_id)                                #henter ordrelinjer

        #forbereder innhold for faktura
        kunde = f"{kundeinfo[1]} {kundeinfo[2]}"
        adresse = kundeinfo[3]
        postnummer = kundeinfo[4]
        poststed = kundeinfo[5]
        dato = verdier[2]
        belop = sum(
            linje[2] * linje[3] 
            for linje in ordrelinjer
            )
        mva = belop / 25
        total = belop + mva
        betalingsbetingelser = 14
        fakturanummer = generer_unikt_fakturanummer(ordrenummer=str(ordre_id), dato=dato)
        ordrenummer = ordre_id
        kundenummer = kundeinfo[0]
        var_referanse = "Varelageret AS"
        deres_referanse = kunde
        betalingsinformasjon = "1234.56.78910"
        kommentar = " "
        vedlegg = "Ingen"

        # Generer faktura
        try:
            lag_faktura(
                kunde=kunde,
                adresse=adresse,
                postnummer=postnummer,
                poststed=poststed,
                dato=dato,
                belop=belop,
                mva=mva,
                total=total,
                betalingsbetingelser=betalingsbetingelser,
                fakturanummer=fakturanummer,
                ordrenummer=ordrenummer,
                kundenummer=kundenummer,
                var_referanse=var_referanse,
                deres_referanse=deres_referanse,
                betalingsinformasjon=betalingsinformasjon,
                ordrelinjer=ordrelinjer,
                kommentar=kommentar,
                vedlegg=vedlegg,
                unikt_nummer=fakturanummer,
                filnavn=f"{fakturanummer}.pdf",
                )
            print(f"Faktura generert:{fakturanummer}.pdf")
        except Exception as e:
            logging.error(f"Feil ved generering av faktura: {e}")

def generer_unikt_fakturanummer(ordrenummer: str, dato: str) -> str:
    """Genererer et unikt fakturanummer basert på dato og tid."""
    tidstempel = datetime.now().strftime("%Y%m%d%H%M%S")                        # ÅÅÅÅMMDDHHMMSS
    dato_renset = dato.replace("-", "")                                         # Fjern bindestreker fra dato
    return f"{ordrenummer}-{dato_renset}{tidstempel[:6]}" 

def lag_faktura(
    kunde: str,
    adresse: str,
    postnummer: float,
    poststed: str,
    dato: str,
    belop: float,
    mva: float,
    total: float,
    betalingsbetingelser: int,
    fakturanummer: str,
    ordrenummer: str,
    kundenummer: str,
    var_referanse: str,
    deres_referanse: str,
    betalingsinformasjon: str,
    ordrelinjer: list,
    unikt_nummer: str,
    kommentar: str,
    vedlegg: str,
    filnavn: str = "faktura.pdf"
) -> None:
    """
    Genererer en faktura i PDF-format med spesifiserte detaljer.
    Returns:
        None
    Args:
        kunde (str): Navn på kunden.
        adresse (str): Adresse til kunden.
        postnummer (float): Postnummer til kunden.
        poststed (str): Poststed til kunden.
        dato (str): Fakturadato i formatet "YYYY-MM-DD".
        belop (float): Beløp eks. mva.
        mva (float): MVA-beløp.
        total (float): Totalt beløp inkl. mva.
        betalingsbetingelser (int): Antall dager for betalingsbetingelser.
        fakturanummer (str): Fakturanummer.
        ordrenummer (str): Ordrenummer.
        kundenummer (str): Kundenummer.
        var_referanse (str): Vår referanse.
        deres_referanse (str): Deres referanse.
        betalingsinformasjon (str): Betalingsinformasjon.
        ordrelinjer (list): Liste med ordrelinjer, hver linje er en liste med varenr, beskrivelse, antall og pris.
    """
    #beregner forfallsdato
    fakturadato = datetime.strptime(dato, "%Y-%m-%d")                           # Konverter dato til datetime-objekt
    forfallsdato = fakturadato + timedelta(days=betalingsbetingelser)           # Legg til antall dager
    forfallsdato_str = forfallsdato.strftime("%Y-%m-%d")                        # Konverter tilbake til streng

    fakturadato_str = fakturadato.strftime("%d.%m.%Y")                          #konverterer dato fra YYYY.MM.DD til dd.mm.yyyy
    forfallsdato_str = forfallsdato.strftime("%d.%m.%Y")                        #konverterer dato fra YYYY.MM.DD til dd.mm.yyyy

    faktura_mappe = "fakturaer"
    if not os.path.exists(faktura_mappe):
        os.makedirs(faktura_mappe)

    filsti = os.path.join(faktura_mappe, f"{fakturanummer}.pdf")
    print(f"Fakturamappe: {faktura_mappe}")

    pdf = FPDF(format='A4')
    pdf.w = 210 
    pdf.add_font('DejaVu', '', 'assets/fonts/ttf/DejaVuSans.ttf', uni=True)
    pdf.add_font('DejaVu', 'B', 'assets/fonts/ttf/DejaVuSans-Bold.ttf', uni=True)
    pdf.add_font('DejaVu', 'I', 'assets/fonts/ttf/DejaVuSans-Oblique.ttf', uni=True)
    pdf.set_font('DejaVu', size=10)
    pdf.cell
    pdf.add_page()
    #legger inn logoen
    logo_bredde = 30
    logo_hoyde = 30
    pdf.image("assets/logo.png", x=10, y=10, w=logo_bredde, h=logo_hoyde)       #plasserer logoen i øverste venstre hjørne av siden
    unikt_nummer = generer_unikt_fakturanummer(ordrenummer, dato)

    #legger til det unike nummeret i PDF-en øverst, i senter av fakturaen
    pdf.cell(190, 10, txt=f"Fakturanummer: {unikt_nummer}", ln=True, align="C")
   
    #plassering av fakuraoverskrift og infofelt(kundeopplysninger, til venstre)
    x = pdf.w - 60
    y = 10
    pdf.w - logo_bredde - 20
    hoyde = 60
    
    
    pdf.set_xy(x + 2, y + 5)
    pdf.set_font("DejaVu", size=14, style="B")
    pdf.cell(pdf.w - 10, 5, txt="Faktura", ln=True, align="L")
    pdf.set_xy(x + 2, y + 10)
    pdf.set_font("DejaVu", size=8)
    pdf.cell(pdf.w - 10, 5, txt="Fakt.nr.: {}".format(unikt_nummer), ln=True, align="L")
    infofelt1 = [
        "Ordrenummer: {}".format(ordrenummer),
        "Kundenummer: {}".format(kundenummer),
        "Deres ref: {}".format(deres_referanse),
        "Vår ref: {}".format(var_referanse),
        "Kontonr.:{}".format(betalingsinformasjon),
        "Fakturadato: {}".format(fakturadato_str),
        "Forfallsdato: {}".format(forfallsdato_str),
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
        "{}".format(kunde),                                                     #navn på kunden
        "{}".format(adresse),                                                   #adresse til kunden         
        "{}".format(postnummer),                                                #postnummer til kunden    
        "{}".format(poststed),                                                  #poststed til kunden
    ]

    for linje in infofelt2:
        pdf.set_x(x + 4)
        pdf.cell(pdf.w - 10, 5, txt=linje, ln=True, align="L")
        
    #overskrift før tabell, ordreoversikt
    pdf.ln(10)
    pdf.cell(pdf.w, 10, txt="Fakturaoversikt for gjeldende ordre", ln=True, align="C"),
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
    if not ordrelinjer or not all(len(linje) == 4 for linje in ordrelinjer):
        pdf.cell(
            pdf.w - 10, 10, txt="Ingen ordrelinjer tilgjengelig eller feil struktur.",
            ln=True, align="L")
    else:
        for linje in ordrelinjer:
            print("Linje:", linje, "Lengde:", len(linje))
            try:
                varenr, beskrivelse, antall, pris = linje
                print(f"Varenr: {varenr}, Beskrivelse: {beskrivelse}, Antall: {antall}, Pris: {pris}")
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
                print(f"Feil i ordrelinje: {linje}. Feilmelding: {e}")
                pdf.cell(pdf.w - 10, 10, txt="Feil i ordrelinje.", ln=True, align="L")
    
    
    #sluttsummer, eks mva, mva og total inkl. mva
    bredde = 60
    hoyde = 20
    x = pdf.w - bredde
    y = pdf.get_y()
    
    pdf.rect(x, y, bredde, hoyde)
    summer = [
        "Eks. mva: {:.2f}".format(belop),
        "MVA: {:.2f}".format(mva),
        "Totalt inkl. mva: {:.2f}".format(total)
    ]

    pdf.set_xy(x, y + 2)
    pdf.set_font("DejaVu", size=8, style="B") 

    for linje in summer:
        pdf.set_x(x)
        pdf.cell(bredde, 5, txt=linje, ln=True, align="R")
       
    pdf.cell(pdf.w - 10, 10, txt="", ln=True)
    pdf.cell(pdf.w - 10, 10, txt="Takk for handelen!", ln=True, align="C")
    pdf.cell(pdf.w - 10, 10, txt="Vennligst betal innen 14 dager.", ln=True, align="C")
    pdf.cell(pdf.w - 10, 10, txt="Oppgi ordrenummer ved betaling:" \
             "{}".format(ordrenummer),ln=True, align="C")
    pdf.cell(pdf.w - 10, 10, txt="Betal til:" \
    " {}".format(betalingsinformasjon), ln=True, align="C")
    pdf.cell(pdf.w - 10, 10, txt="Vennligst kontakt oss ved spørsmål.", ln=True, align="C")


    pdf.output(filsti)
    if lagre_faktura(fakturanummer, forfallsdato, fakturadato, ordrenummer):
        bruker_varsel(
            melding="Faktura er lagret i databasen.",
            icon="check"
        )

    print (ordrelinjer)


