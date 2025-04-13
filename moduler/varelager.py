# TODO: Lage oversikt over varelager, i tillegg mulighet for å legge til og fjerne ting?
import customtkinter
class VarelagerModul:
    def __init__(self, master):
        self.master = master

    def vis(self):
        etikett = customtkinter.CTkLabel(master=self.master, text="Varelager-modul", text_color="black", bg_color="white")
        etikett.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)