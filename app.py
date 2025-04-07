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
vindu.grid_columnconfigure(2, weight=1) # Konfigurasjon av kolonne grid
vindu.grid_rowconfigure(0, weight=1) # konfigurasjon av rad grid

# Meny på venstre side: se https://customtkinter.tomschimansky.com/documentation/widgets/frame for forklaring
meny = customtkinter.CTkFrame(master=vindu, bg_color="grey", fg_color="white", corner_radius=0) # Oppretter et meny felt i form av en frame. 
meny.grid(row=0, column=0, sticky="nsw", padx=10) # Oppsett av en grid for å få plassert komponenter riktig
meny.grid_rowconfigure(0, weight=2) # plassering av rader
meny.grid_columnconfigure(0, weight=1) # plassering av kolonner

# Knapper i menyen: se https://customtkinter.tomschimansky.com/documentation/widgets/button for forklaring 
knapp = customtkinter.CTkButton(master=meny, text="Ordre", command=vis_ordre()) # definerer første knappen. 
knapp.grid(sticky="nw")

knapp2 = customtkinter.CTkButton(master=meny, text="Varebeholdning", command=vis_ordre()) #definerer andre knappen
knapp2.grid(sticky="nw") # TROR dette definerer at knapp skal "limes" til "North East"

vindu.mainloop()