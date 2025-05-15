     
import customtkinter
from PIL import Image

class Hovedvindu:
    def __init__(self, master):
        self.master = master
        self.visningsrute = None  # Initialiserer visningsruten

    def vis_innhold(self):

       # Setter opp en label i visningsruten som viser en velkomstmelding:
        self.bakgrunnsbilde = customtkinter.CTkImage(
            dark_image=Image.open("assets/bakgrunn5.png"),  # Legg til bildet ditt her
            light_image=Image.open("assets/bakgrunn5.png"),
            size=(1280, 720)  # Tilpass størrelsen på bildet til vinduet
        )
        self.bakgrunn_label = customtkinter.CTkLabel(
            master=self.master,
            image=self.bakgrunnsbilde,
            text="",  # Ingen tekst, kun bilde
        )
        self.bakgrunn_label.grid(row=0, column=0, sticky="nsew")
        #oppretter ny label med velkomstmelding:
        # Setter opp en label i visningsruten som viser en velkomstmelding:
        self.tekst_startvindu = customtkinter.CTkLabel(
            master=self.master,
            text="Velkommen til startsiden for Varelageret! \n" \
            "For å navigere videre må du trykke på en knapp i menyen.",
            text_color="black",
            font=("Arial", 20, "bold"),
            corner_radius=6,
        )
        # Setter opp en label i visningsruten som viser en velkomstmelding:
        self.tekst_startvindu.grid(row=0, column=0, padx=20, pady=20)
