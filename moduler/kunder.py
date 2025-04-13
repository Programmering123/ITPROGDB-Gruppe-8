# TODO: Lage visning og behandling av kunder Her går det ann å leke seg med customktinker. 
# Jeg tenker vi kan leke oss litt her først. Husk at riktig moduler må være importert ført. 
import customtkinter
class KunderModul:
    def __init__(self, master):
        self.master = master

    def vis(self):
        etikett = customtkinter.CTkLabel(master=self.master, text="Kunder-modul", text_color="black", bg_color="white")
        etikett.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)