import customtkinter
from tkinter import ttk

class TabellModul:
    def __init__(self, master):
        self.master = master
        self.aktuell_side = 1
        self.antall_sider = 1
        self.data = []  # Tom liste. Settes av SubClass.
        self.kolonner = []  # Tom liste. Settes av SubClass.

    def vis(self):
        # Setter opp grunndata:
        self.data = self.hent_data() # Henter data fra databasen
        self.vist_data = self.data # Kopierer dataene til vist_data
        self.antall_sider = len(self.data) // 20 + 1 # Beregner antall sider basert på antall rader i varelageret

        # Øvre meny, Oppsett:
        meny_ramme = customtkinter.CTkFrame(master=self.master, fg_color="lightgrey") # Lager en ramme for øvre meny
        meny_ramme.grid(row=0, column=0, sticky="nwe", padx=10, pady=10) # Plassering av ramme

        # Øvre meny, Søkefelt:
        leteord = customtkinter.CTkEntry(
            master=meny_ramme,
            width=300,
            height=30,
            corner_radius=5,
            fg_color="lightgrey",
            text_color="black",
            bg_color="white",
            placeholder_text="Søk i tabellen...",
            placeholder_text_color="grey",
        )
        leteord.grid(row=0, column=0, sticky="nw", padx=10, pady=10) # Plassering av søkefelt
        leteord.bind("<Return>", lambda event: self.søk_i_data(leteord.get())) # Binder Enter-tasten til søkefunksjonen
        # Øvre meny, Søkeknapp:
        knapp_søk = customtkinter.CTkButton(
            master=meny_ramme,
            text="Søk",
            command=lambda: self.søk_i_data(leteord.get()), 
        )
        knapp_søk.grid(row=0, column=1, sticky="nw", padx=10, pady=10) # Plassering av søkeknapp

        # Tabell ramme, Oppsett:
        tabell_ramme = customtkinter.CTkFrame(master=self.master, fg_color="lightgrey", corner_radius=5)
        tabell_ramme.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # # Setter opp grid for tabellen og får den til å ta opp hele høyden og bredden:# TODO: Liker ikke helt denne. Se om vi kan gjøre denne på annen metode
        self.master.grid_rowconfigure(0, weight=0) # Låser ramme_meny
        self.master.grid_rowconfigure(1, weight=1)  # Fleksibel høyde for tabellen
        self.master.grid_columnconfigure(0, weight=1) # Fleksibel bredde for tabellen
        # Setter opp grid for tabellen og får den til å ta opp hele høyden og bredden:
        tabell_ramme.grid_rowconfigure(0, weight=1)
        tabell_ramme.grid_columnconfigure(0, weight=1)

        # Velger å bruke Tkinter sin Treeview for å lage tabellen, da den er vesentlig raskere enn Ctk sin.
        # Pynter litt på tabellen:
        stil = ttk.Style()
        stil.configure("Treeview", font=("Helvetica", 12), background="white", foreground="black", highlightthickness=1, bordercolor="grey")
        stil.configure("Treeview.Heading", font=("Helvetica", 14, "bold"), background="white", foreground="black")
        # Setter opp kolonnene i tabellen:
        self.tree = ttk.Treeview(master=tabell_ramme, columns=self.kolonner, show="headings", height="100")
        #customtkinter.CTkTreeview(master=self.master, columns=kolonner, show="headings", height=20)
        self.tree.grid(row=0, column=0, sticky="new", padx=10, pady=10)
        
        

        # Setter opp kolonneoverskriftene:
        for kolonne in self.kolonner:
            self.tree.heading(kolonne, text=kolonne)
            self.tree.column(kolonne, anchor="center", width=100)
        # Setter opp scrollbar:
        scrollbar = ttk.Scrollbar(master=tabell_ramme, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Bunn meny, oppsett:
        navigasjon_ramme = customtkinter.CTkFrame(
            master=self.master, 
            fg_color="lightgrey", 
            corner_radius=5
        )
        # Valg av antall rader : Her skal vi sende antall viste sider til oppdater_tabell funksjonen.
        knapp_antall_tekst = customtkinter.CTkLabel(
            master=navigasjon_ramme,
            text="Vis antall:",
            text_color="black",
            bg_color="lightgrey",
        )
        self.knapp_antall_var = customtkinter.StringVar(value="20") # Setter default verdi til 10
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
        # TODO: Få denne til å oppdateres ved endring av antall viste rader
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
        self.oppdater_tabell() # Kaller oppdater_tabell for å vise første side av dataene i tabellen
        # Plassering av komponenter:
        navigasjon_ramme.grid(row=2, column=0, sticky="sew", padx=10, pady=10)
        knapp_antall_tekst.grid(row=0, column=0, sticky="nw", padx=10, pady=10)
        knapp_antall.grid(row=0, column=1, sticky="nw", padx=10, pady=10)
        knapp_nav_bak.grid(row=0, column=2, sticky="e", padx=10, pady=10)
        self.side_indikator.grid(row=0, column=3, sticky="ew", padx=10, pady=10)
        knapp_nav_frem.grid(row=0, column=4, sticky="w", padx=10, pady=10)
    
    def hent_data(self):
        """Henter data fra databasen. Denne funksjonen må implementeres i SubClass."""
        raise NotImplementedError("Denne funksjonen må implementeres i SubClass.")

    # Søkefunksjon: 
    def søk_i_data(self, søk):
        self.vist_data = [
            rad for rad in self.data if søk.lower() in str(rad).lower()
        ]
        self.aktuell_side = 1 # Resetter aktuell side til 1
        self.antall_sider = len(self.vist_data) // int(self.knapp_antall_var.get()) + 1 # Beregner antall sider på ny
        self.oppdater_tabell()
    
    # Her oppdaterer vi tabellen i egen funksjon:
    def oppdater_tabell(self):
        for rad in self.tree.get_children():
            self.tree.delete(rad)
        fra = int(self.aktuell_side) * int(self.knapp_antall_var.get()) - int(self.knapp_antall_var.get())
        til = int(self.aktuell_side) * int(self.knapp_antall_var.get())
        for rad in self.vist_data[fra:til]: #går gjennom dataene tilgjengelig, begrenset til sidevisning
            self.tree.insert("", "end", values=rad) #legger de inn i tree
        self.antall_sider = len(self.vist_data) // int(self.knapp_antall_var.get()) + 1 # Beregner antall sider på nytt
        self.side_indikator.configure(text=f"{self.aktuell_side}/{self.antall_sider}") # Oppdaterer sideindikatoren

    # Funksjon for å endre side la oss se.... 
    def endre_side(self, retning):
        # Funksjon for å endre side i tabellen:
        print("Endrer side", retning)
        ny_side = self.aktuell_side + retning
        print("Ny side:", ny_side)
        # Sjekker om ny side er innenfor gyldig område:
        if ny_side < 1: # Hvis det blir valgt mindre tall enn 1, så setter vi det til 1
            ny_side = 1
        elif ny_side > self.antall_sider: # Hvis det blir valgt større tall enn antall sider, så setter vi det til antall sider
            ny_side = self.antall_sider
        self.aktuell_side = ny_side
        self.oppdater_tabell()