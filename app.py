import tk
import customtkinter
# Temp
# Antar vi skal ha noe her..
def vis_ordre():
    print("vise ordre!!")

# Hovedvindu:
vindu = customtkinter.CTk()
vindu.title("Testing") #Her er tittelen på ruta
vindu.geometry("1280x720") #Definerer størrelsen på vinduet 
vindu.grid_columnconfigure(0, weight=1) # Konfigurasjon av kolonne grid
vindu.grid_rowconfigure(0, weight=1) # konfigurasjon av rad grid

# Meny på venstre side: se https://customtkinter.tomschimansky.com/documentation/widgets/frame for forklaring
vindu.meny = customtkinter.CTkFrame(
        master=vindu, 
        bg_color="grey", 
        fg_color="white", 
        corner_radius=2, 
        border_color="red", 
        border_width=2) # Oppretter et meny felt i form av en frame. 
vindu.meny.grid(row=0, column=0, sticky="nsw", padx=10, pady=(10,0)) # Oppsett av en grid for å få plassert komponenter riktig
# TODO: Lage flere knapper
# FIXME: Få plassert knapp2 riktig

# Knapper i menyen: se https://customtkinter.tomschimansky.com/documentation/widgets/button for forklaring 
vindu.knapp = customtkinter.CTkButton(master=vindu.meny, text="Ordrer") # definerer første knappen. 
vindu.knapp.grid(column=0, row=0, sticky="nw", padx=10, pady=(0,5))

vindu.knapp2 = customtkinter.CTkButton(master=vindu.meny, text="Varelager") #definerer andre knappen
vindu.knapp2.grid(column=0, row=1, sticky="nw", padx=10, pady=(0,5)) # TROR dette definerer at knapp skal "limes" til "North East"

vindu.knapp2 = customtkinter.CTkButton(master=vindu.meny, text="Varebeholdning") #definerer andre knappen
vindu.knapp2.grid(column=0, row=2, sticky="nw", padx=10, pady=(0,5)) # TROR dette definerer at knapp skal "limes" til "North East"

vindu.knappen = customtkinter.CTkButton(vindu, text="En test")
vindu.knappen.grid(row=3, column=0, pady=10, sticky="ew")

vindu.mainloop()