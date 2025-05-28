"""
Tabell.py
Dette er en klasse for å lage en tabellvisning i et GUI-program.
Den er laget for å være en baseklasse som kan brukes av andre moduler.
"""
import logging
from typing import Any, Literal
from tkinter import ttk
import customtkinter

class Tabell:
    def __init__(self, master):
        self.master = master
        self.aktuell_side = 1
        self.antall_sider = 1
        self.data = []                                                          # Tom liste. Settes av subklasse.
        self.kolonner = []                                                      # Tom liste. Settes av subklasse.
        self.detalj_visning_ramme:customtkinter.CTkFrame
        self.tabell_visning_ramme:customtkinter.CTkFrame
        self.tabell:ttk.Treeview
        self.knapp_detaljer:customtkinter.CTkButton
        self.knapp_detaljer_betinget = False                                    # Setter knapp til False, for å sjekke om den er opprettet i subklasse

    def vis_innhold(self):
        """Funksjon for å vise innholdet i tabellen."""
        # Setter opp grunndata:
        self.data = self.hent_data()                                            # Henter data fra databasen 
        self.vist_data = self.data                                              # Kopierer dataene til vist_data
        self.antall_sider = len(self.data) // 20 + 1                            # Beregner antall sider basert på antall rader i varelageret
    
        self.opprett_rammer()

        self._opprett_meny_topp()

        self._opprett_tabell()

        self._opprett_meny_bunn()
        
        self.oppdater_tabell()                                                  # Kaller oppdater_tabell for å vise første side av dataene i tabellen



    def knapp_detaljer_opprett(self, _master):
        """
        Dette er en tom funksjon som skal overstyres av submoduler.
        Kopier funksjonen til submodulene, fjern kommentering og tilpass den der.
        Args:
            _master (customtkinter.CTkFrame): Ramme der knappen skal opprettes.
        """
        # self.knapp_detaljer = customtkinter.CTkButton(
        #     master=_master, 
        #     text="",
        #     command="", 
        #     state="normal",                     
        #     width=140,
        # )
        # self.knapp_detaljer.grid(row=0, column=3, sticky="ne", padx=10, pady=10)

    def valg_filter_boks(self):
        """
        Dette er en tom funksjon som skal overstyres av submoduler.
        Kopier funksjonen til submodulene, fjern kommentering og tilpass den der.
        """

    def knapp_oppdater_tilstand(self, knapp:customtkinter.CTkButton):
        """
        Oppdaterer tilstand til <knapp> basert på valg i tabellen.
        state "disabled" eller "normal".
        Args: 
            knapp (customtkinter.CTkButton): Knappen som skal oppdateres.
        """
        if self.tabell.selection():
            knapp.configure(state="normal")                                     # Aktiverer detaljknappen hvis det er valgt en ordrelinje
        else:
            knapp.configure(state="disabled")

    def opprett_rammer(self):
        """Funksjon for å opprette rammer for visning av tabell eller detaljer."""
        self.tabell_visning_ramme = customtkinter.CTkFrame(
            master=self.master, 
            corner_radius=0
            )                                                                   # Lager en ramme for tabellvisning
        self.tabell_visning_ramme.grid(row=0, column=0, sticky="nsew")          # Plassering av ramme
        self.detalj_visning_ramme = customtkinter.CTkFrame(
            master=self.master, 
            corner_radius=0
            )                                                                   # Lager en ramme for detaljvisning
        self.detalj_visning_ramme.grid(row=0, column=0, sticky="nsew")          # Plassering av ramme
        self.detalj_visning_ramme.lower(self.tabell_visning_ramme)              # Setter detaljvisningrammen i bakgrunnen
        # Setter opp grid for tabellen og får den til å ta opp hele høyden og bredden:
        self.tabell_visning_ramme.grid_rowconfigure(0, weight=0)                # Låser ramme_meny
        self.tabell_visning_ramme.grid_rowconfigure(1, weight=1)                # Fleksibel høyde for tabellen
        self.tabell_visning_ramme.grid_columnconfigure(0, weight=1)             # Fleksibel bredde for tabellen

    def _opprett_meny_topp(self):
        """Intern funksjon for å opprette topp meny."""
        self.meny_ramme = customtkinter.CTkFrame(
            master=self.tabell_visning_ramme, 
        ) 
        self.meny_ramme.grid(row=0, column=0, sticky="new", padx=10, pady=10)   # Plassering av ramme
        self.meny_ramme.grid_columnconfigure(0, weight=0)                       # Søkefeltet
        self.meny_ramme.grid_columnconfigure(1, weight=0)                       # Søkeknappen
        self.meny_ramme.grid_columnconfigure(2, weight=1)                       # Generelt plassopptak weigh=1
        self.meny_ramme.grid_columnconfigure(3, weight=0)                       # Opprett ny kunde

        # Søkefelt:
        self.leteord = customtkinter.CTkEntry(
            master=self.meny_ramme,
            width=300,
            height=30,
            corner_radius=5,
            placeholder_text="Søk i tabellen...",
            placeholder_text_color="grey",
        )
        self.leteord.grid(row=0, column=0, sticky="nw", padx=10, pady=10)            # Plassering av søkefelt
        self.leteord.bind("<KeyRelease>", lambda event: self.let_i_data(self.leteord.get())) # Binder tastetrykk til søkefunksjonen for live søk
        self.leteord.bind("<Return>", lambda event: self.let_i_data(self.leteord.get()))  # Binder Enter-tasten til søkefunksjonen
        # Søkeknapp:
        knapp_søk = customtkinter.CTkButton(
            master=self.meny_ramme,
            text="Søk",
            command=lambda: self.let_i_data(self.leteord.get()), 
        )
        knapp_søk.grid(row=0, column=1, sticky="nw", padx=10, pady=10)          # Plassering av søkeknapp
        # valgfri filterboks:
        self.valg_filter_boks()                                                 # Kaller på funksjon for å opprette filterboks
        # valgfri vis detaljer:
        self.knapp_detaljer_opprett(self.meny_ramme)                            # Oppretter detaljknappen i menyen basert på evt subclass

    def _opprett_tabell(self):
        """Intern funksjon for å opprette tabellen."""
        tabell_ramme = customtkinter.CTkFrame(
            master=self.tabell_visning_ramme, 
            corner_radius=5
            )
        tabell_ramme.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Setter opp grid for tabellen og får den til å ta opp hele høyden og bredden:
        tabell_ramme.grid_rowconfigure(0, weight=1)
        tabell_ramme.grid_columnconfigure(0, weight=1)

        # Velger å bruke Tkinter sin Treeview for å lage tabellen, da den er vesentlig raskere enn Ctk sin.
        # Pynter litt på tabellen:
        stil = ttk.Style()
        stil.configure("Treeview", font=("Roboto", 12), background="white", foreground="black", highlightthickness=1, bordercolor="grey")
        stil.configure("Treeview.Heading", font=("Roboto", 14, "bold"), background="white", foreground="black")
        # Setter opp kolonnene i tabellen:
        self.tabell = ttk.Treeview(master=tabell_ramme, columns=self.kolonner, show="headings", height=100)
        self.tabell.grid(row=0, column=0, sticky="new", padx=10, pady=10)
        self.tabell.bind(
            "<Double-1>",                                                       # Binder dobbeltklikk
            lambda event: (
                self.vis_detaljer(                                              # Bruker en lambda funksjon som peker til funksjon
                    self.tabell.item(self.tabell.focus())['values'],            # Sende verdiene til valgt rad som argument
                    )
                )
                if self.tabell.focus() and self.tabell.identify_region(
                    event.x, event.y == "cell"
                )                                                               # Sjekker om det er valgt en rad og at det er en celle som er klikket på
                else None
            )
               
        
        if self.knapp_detaljer_betinget and self.knapp_detaljer != None:        # Sjekker om detaljknappen er opprettet og at den er betinget
            self.knapp_detaljer.configure(state="disabled")
            self.tabell.bind(
                "<<TreeviewSelect>>",                                           # Binder valg av rad i tabellen til funksjon for oppdatering av knapp
                lambda event: self.knapp_oppdater_tilstand(self.knapp_detaljer) # Sender verdiene til knapp som argument
            )

        # Setter opp kolonneoverskriftene:
        for kolonne in self.kolonner:
            self.tabell.heading(kolonne, text=kolonne)
            self.tabell.column(kolonne, anchor="center", width=100)
        # Setter opp scrollbar:
        scrollbar = ttk.Scrollbar(master=tabell_ramme, orient="vertical", command=self.tabell.yview)
        self.tabell.configure(yscroll=scrollbar.set)                            # type: ignore
        scrollbar.grid(row=0, column=1, sticky="ns")

    def _opprett_meny_bunn(self):
        """Intern funksjon for å opprette bunn meny."""
        # Bunn meny, oppsett:
        navigasjon_ramme = customtkinter.CTkFrame(
            master=self.tabell_visning_ramme, 
            corner_radius=5
        )
        # Valg av antall rader : Her skal vi sende antall viste sider til oppdater_tabell funksjonen.
        knapp_antall_tekst = customtkinter.CTkLabel(
            master=navigasjon_ramme,
            text="Vis antall:",
            text_color="black",
        )
        self.knapp_antall_var = customtkinter.StringVar(value="20")             # Setter standard sidevisningsverdi til 20
        knapp_antall = customtkinter.CTkOptionMenu(
            master=navigasjon_ramme,
            values=["20", "50", "100"],
            command=lambda x: self.oppdater_tabell(),
            variable=self.knapp_antall_var,
        )
        knapp_nav_bak = customtkinter.CTkButton(
            master=navigasjon_ramme,
            text="<<",
            command=lambda: self.endre_side(-1),
            width=30,
        )
        # Sideindikator:
        self.side_indikator = customtkinter.CTkLabel(
            master=navigasjon_ramme,
            text=f"{self.aktuell_side}/{self.antall_sider}",
            text_color=customtkinter.ThemeManager.theme["CTkButton"]["text_color"],
            fg_color=customtkinter.ThemeManager.theme["CTkButton"]["fg_color"],
            corner_radius=6
        )
        knapp_nav_frem = customtkinter.CTkButton(
            master=navigasjon_ramme,
            text=">>",
            command=lambda: self.endre_side(1),
            width=30,
        )
        navigasjon_ramme.grid(row=2, column=0, sticky="sew", padx=10, pady=10)
        knapp_antall_tekst.grid(row=0, column=0, sticky="nw", padx=10, pady=10)
        knapp_antall.grid(row=0, column=1, sticky="nw", padx=10, pady=10)
        knapp_nav_bak.grid(row=0, column=2, sticky="e", padx=10, pady=10)
        self.side_indikator.grid(row=0, column=3, sticky="ew", padx=10, pady=10)
        knapp_nav_frem.grid(row=0, column=4, sticky="w", padx=10, pady=10)


    def hent_data(self):
        """Henter data fra databasen. Denne funksjonen må implementeres i SubClass."""
        raise NotImplementedError("Denne funksjonen må implementeres i SubClass.")
    
    # Blank definering av detaljvisning, må implementeres i SubClass:
    def vis_detaljer(self, data:list[Any]|Literal['']=[]):
        """Viser detaljer for valgt rad. Denne funksjonen må implementeres i SubClass."""
        raise NotImplementedError("Denne funksjonen må implementeres i SubClass.")

    # Søkefunksjon: 
    def let_i_data(self, sok: str):
        self.vist_data = [
            rad for rad in self.data if sok.lower() in str(rad).lower()
        ]
        self.oppdater_tabell()
    
    # Her oppdaterer vi tabellen i egen funksjon:
    def oppdater_tabell(self):

        self.antall_sider = max(
             1, (
                  len(self.vist_data) 
                  +int(self.knapp_antall_var.get()) 
                  -1
                ) 
                // int(self.knapp_antall_var.get())
             )                                                                  # Beregner antall sider basert på antall rader i varelageret og antall viste rader  
        # Oppdaterer tabellen med dataene:  

        if      self.aktuell_side > self.antall_sider:                          # Hvis aktuell side er større enn antall sider, så setter vi den til antall sider
                self.aktuell_side = self.antall_sider
        elif    self.aktuell_side < 1:                                          # Hvis aktuell side er mindre enn 1, så setter vi den til 1
                self.aktuell_side = 1   

        # Slette eksisterende rader i tabellen:
        for rad in self.tabell.get_children():
            self.tabell.delete(rad)

        # Beregning av hvilke rader som skal vises basert på aktuell side og antall viste rader:
        fra = (
             int(self.aktuell_side)
             *int(self.knapp_antall_var.get())
             -int(self.knapp_antall_var.get())
             )                                                                  # Beregner fra hvilken rad vi skal begynne å vise dataene
        til =  fra + int(self.knapp_antall_var.get())                           # Beregner til hvilken rad vi skal slutte å vise dataene
        # Legger til nye rader i tabellen:
        for rad in self.vist_data[fra:til]:                                     # Går gjennom dataene tilgjengelig, begrenset til sidevisning
            self.tabell.insert("", "end", values=[str(verdi) for verdi in rad])                           # Legger de inn i tabell
        self.antall_sider = len(self.vist_data) // int(self.knapp_antall_var.get()) + 1     # Beregner antall sider på nytt
        self.side_indikator.configure(text=f"{self.aktuell_side}/{self.antall_sider}")      # Oppdaterer sideindikatoren

    # Funksjon for å endre side la oss se.... 
    def endre_side(self, retning):
        ny_side = self.aktuell_side + retning # Ønsket side
        # Sjekker om ny side er innenfor gyldig område:
        if ny_side < 1:                                                         # Hvis det blir valgt mindre tall enn 1, så setter vi det til 1
            ny_side = 1
        elif ny_side > self.antall_sider:                                       # Hvis det blir valgt større tall enn antall sider, så setter vi det til antall sider
            ny_side = self.antall_sider
        self.aktuell_side = ny_side
        self.oppdater_tabell()