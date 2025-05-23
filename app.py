# import tk
import customtkinter
from PIL import Image

from moduler.hoved import Hovedvindu
from moduler.ordrer import Ordrer
from moduler.varelager import Varelager
from moduler.kunder import Kunder

class App(customtkinter.CTk):
    def __init__(self):
        # Oppretter hovedvinduet:
        super().__init__()
        self.title("Varelageret")                                               # Setter tittelen på vinduet
        self.minsize(1280, 720)
        customtkinter.set_default_color_theme("theme.json")                     # Henter farger fra theme.json filen, der er fargene definert.
        customtkinter.set_appearance_mode("light")                              #Tvinger programmet til å kjøre lys modus 
        self.iconbitmap("assets/icon.ico")
        self.geometry("1280x720")
        self.grid_columnconfigure(0, weight=0)                                  # Meny venstre side låser denne til 200px. weight=0 gjør at den ikke vokser.
        self.grid_columnconfigure(1, weight=1)                                  # Visningsvindu (resten av vinduet på høyre side )
        self.grid_rowconfigure(0, weight=1)                                     # Hele høyden
        # Oppretter menyen:
        self.opprett_meny()
        # Oppretter visningsruten:
        self.opprett_visningsrute()
        # Starter hovedloop:
        self.mainloop()

    
    def opprett_meny(self):
        # Oppretter menyen på venstre side: (se https://customtkinter.tomschimansky.com/documentation/widgets/frame for forklaring)
        self.meny = customtkinter.CTkFrame(
            master=self,
            fg_color="lightgrey",                                               #tvinger grå sidemeny venstre side
            corner_radius=2,
            width=200,                                                          # Setter bredden på menyen til 200px
        )
        self.meny.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.meny.grid_columnconfigure(0, weight=1)                             # Sentrerer innhold

        # Setter opp ikon her: 
        self.bilde = customtkinter.CTkImage(
            dark_image=Image.open("assets/icon.ico"), 
            light_image=Image.open("assets/icon.ico"),
            size=(140, 140)                                                     # 140x140px tilsvarer bredden på knappene.
        )
        self.bildeknapp = customtkinter.CTkButton(
            master=self.meny,
            image=self.bilde,
            width=140,
            height=140,
            fg_color="lightgrey",                                               # Endret farge til å matche grå sidemeny venstre side
            hover_color="lightgrey",                                            # Endret farge til å matche grå sidemeny venstre side
            text="",
            command=lambda: self.vis_modul(Hovedvindu)                          # Viser hovedvinduet når knappen trykkes
        ) 
        self.bildeknapp.grid(row=0, column=0, sticky="n", padx=10, pady=10) 
        # Oppretter knappene i menyen: ( se https://customtkinter.tomschimansky.com/documentation/widgets/button for forklaring )
        self.knapp = customtkinter.CTkButton(
            master=self.meny,
            text="Ordrer",
            command=lambda: self.vis_modul(Ordrer)
        )
        self.knapp.grid(row=1, column=0, sticky="n", padx=10, pady=3)
        self.knapp2 = customtkinter.CTkButton(
            master=self.meny,
            text="Varelager",
            command=lambda: self.vis_modul(Varelager)
        )
        self.knapp2.grid(row=2, column=0, sticky="n", padx=10, pady=3)
        self.knapp3 = customtkinter.CTkButton(
            master=self.meny,
            text="Kunder",
            command=lambda: self.vis_modul(Kunder)
        )
        self.knapp3.grid(row=3, column=0, sticky="n", padx=10, pady=3)

    
    # Visningsrute:
    def opprett_visningsrute(self):
        # Oppretter visningsruten: (se https://customtkinter.tomschimansky.com/documentation/widgets/frame for forklaring)
        self.visningsrute = customtkinter.CTkFrame(
            master=self,
            fg_color="white",
            corner_radius=0
            )
        self.visningsrute.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        # Setter opp grid for visningsruten og får den til å ta opp hele høyden og bredden:
        self.visningsrute.grid_rowconfigure(0, weight=1)
        self.visningsrute.grid_columnconfigure(0, weight=1)
        self.vis_modul(Hovedvindu)                                              # Viser hovedvinduet i visningsruten ved oppstart av programmet.



    def vis_modul(self, modul_klasse):
        # Funksjon for å vise en modul i visningsruten:
        for widget in self.visningsrute.winfo_children():                       # Sletter innholdet i visningsruten:
            widget.destroy()
        # Oppretter ny modul:
        modul = modul_klasse(self.visningsrute)
        modul.vis_innhold()                                                     # kaller på vis_innhold metoden i modulen for å vise innholdet i visningsruten
# Starter programmet:
if __name__ == "__main__":
    App()

