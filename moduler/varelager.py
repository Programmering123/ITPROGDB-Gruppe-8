# TODO: Lage oversikt over varelager, i tillegg mulighet for å legge til og fjerne ting?
# Oppgaveteksten:
# Vise en liste over hvilke varer som er på varelageret, inkludert varenummer, navn på varen, antall og pris.  
# I tillegg til å vise varelageret i selv Python programmet skal dere ved bruk av en API vise varelageret i en nettleser.
import customtkinter
from tkinter import ttk
from api.database import hent_varelager # Importer databasen fra api/database.py
class VarelagerModul:
    def __init__(self, master):
        self.master = master
        self.aktuell_side = 1 # Setter aktuell side til 1
        self.antall_sider = 1 # Setter antall sider til 1
    def vis(self):
        # Setter opp grunndata:
        self.data = hent_varelager() # Henter varelager fra databasen
        self.vist_data = self.data # Henter de første 20 radene fra varelageret // kanskje denne bare trenger å være hvor vi fyller inn data i tabellen?
        self.antall_sider = len(self.data) // 20 + 1 # Beregner antall sider basert på antall rader i varelageret
        kolonner = ["Varenummer", "Betegnelse", "Antall", "Pris"] # Kolonnenavnene som vi skal vise

        # Setter opp øvre meny:
        meny_ramme = customtkinter.CTkFrame(master=self.master, fg_color="lightgrey") # Lager en ramme for øvre meny
        meny_ramme.grid(row=0, column=0, sticky="nwe", padx=10, pady=10) # Plassering av ramme

        # Søkefelt i øvre meny:
        leteord = customtkinter.CTkEntry(
            master=meny_ramme,
            width=300,
            height=30,
            corner_radius=5,
            fg_color="lightgrey",
            text_color="black",
            bg_color="white",
            placeholder_text="Søk i varelager...",
            placeholder_text_color="grey",
        )
        leteord.grid(row=0, column=0, sticky="nw", padx=10, pady=10)
        leteord.bind("<Return>", lambda event: self.søk_i_data(leteord.get(), tree)) # Binder Enter-tasten til søkefunksjonen
        # Søkeknapp i øvre meny:
        knapp_søk = customtkinter.CTkButton(
            master=meny_ramme,
            text="Søk",
            command=lambda: self.søk_i_data(leteord.get(), tree), 
        )
        knapp_søk.grid(row=0, column=1, sticky="nw", padx=10, pady=10) 

        # # Oppretter en ramme for tabellen:
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
        tree = ttk.Treeview(master=tabell_ramme, columns=kolonner, show="headings", height="100")
        #customtkinter.CTkTreeview(master=self.master, columns=kolonner, show="headings", height=20)
        tree.grid(row=0, column=0, sticky="new", padx=10, pady=10)
        
        

        # Setter opp kolonneoverskriftene:
        for kolonne in kolonner:
            tree.heading(kolonne, text=kolonne)
            tree.column(kolonne, anchor="center", width=100)
        # Setter opp scrollbar:
        scrollbar = ttk.Scrollbar(master=tabell_ramme, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Navigasjonsrute i bunn:
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
            command=lambda x: self.oppdater_tabell(
                tree,
                ),
            variable=self.knapp_antall_var,
        )
        knapp_nav_bak = customtkinter.CTkButton(
            master=navigasjon_ramme,
            text="<<",
            command=lambda: self.endre_side(-1, tree),
            width=30,
        )
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
            command=lambda: self.endre_side(1, tree),
            width=30,
        )
        self.oppdater_tabell(tree) # Kaller oppdater_tabell for å vise første side av dataene i tabellen
        # Plassering av komponenter:
        navigasjon_ramme.grid(row=2, column=0, sticky="sew", padx=10, pady=10)
        knapp_antall_tekst.grid(row=0, column=0, sticky="nw", padx=10, pady=10)
        knapp_antall.grid(row=0, column=1, sticky="nw", padx=10, pady=10)
        knapp_nav_bak.grid(row=0, column=2, sticky="e", padx=10, pady=10)
        self.side_indikator.grid(row=0, column=3, sticky="ew", padx=10, pady=10)
        knapp_nav_frem.grid(row=0, column=4, sticky="w", padx=10, pady=10)
    # Her oppdaterer vi tabellen i egen funksjon:
    def oppdater_tabell(self, tree):
        for rad in tree.get_children():
            tree.delete(rad)
        fra = int(self.aktuell_side) * int(self.knapp_antall_var.get()) - int(self.knapp_antall_var.get())
        til = int(self.aktuell_side) * int(self.knapp_antall_var.get())
        print("Fra:", fra, "Til:", til)
        for rad in self.vist_data[fra:til]:
            tree.insert("", "end", values=rad) 
        self.antall_sider = len(self.vist_data) // int(self.knapp_antall_var.get()) + 1 # Beregner antall sider på nytt
        self.side_indikator.configure(text=f"{self.aktuell_side}/{self.antall_sider}") # Oppdaterer sideindikatoren
        

    # Søkefunksjon: 
    def søk_i_data(self, søk, tree):
        self.vist_data = [
            rad for rad in self.data if søk.lower() in str(rad).lower()
        ]
        self.aktuell_side = 1 # Resetter aktuell side til 1
        self.antall_sider = len(self.vist_data) // int(self.knapp_antall_var.get()) + 1 # Beregner antall sider på ny
        self.oppdater_tabell(tree)
    # Funksjon for å endre side la oss se.... 
    def endre_side(self, retning, tree):
        # Funksjon for å endre side i tabellen:
        print("Endrer side", retning)
        ny_side = self.aktuell_side + retning
        print("Ny side:", ny_side)
        # Sjekker om ny side er innenfor gyldig område:
        if ny_side < 1:
            ny_side = 1
        elif ny_side > self.antall_sider:
            ny_side = self.antall_sider
        self.aktuell_side = ny_side
        self.oppdater_tabell(tree)
        

     #   self.oppda