import tk
import customtkinter
# Temp
# Antar vi skal ha noe her..
def vis_ordrer():
    return print("vise ordrer!")
def vis_varelager():
    return print("vise varelager")
def vis_kunder():
    return print("vise kunder")

# Hovedvindu:
vindu = customtkinter.CTk(fg_color="white")
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
        border_color="red", # TODO: Denne er midlertidig, kun får å se rammen.
        border_width=2) # Oppretter et meny felt i form av en frame. 
vindu.meny.grid(row=0, 
                column=0, 
                sticky="nsw", 
                padx=10, 
                pady=(10,0)) # Oppsett av en grid for å få plassert komponenter riktig


# Knapper i menyen: se https://customtkinter.tomschimansky.com/documentation/widgets/button for forklaring 
# TODO: Opprett riktige knapper her.
vindu.knapp = customtkinter.CTkButton(master=vindu.meny, # Definerer hvilket objekt denne skal ligge under
                                      text="Ordrer", # Hva teksten skal vise
                                      command=vis_ordrer # Definerer hva slags kommando som skal kjøres
                                      ) 
vindu.knapp.grid(column=0, row=0, sticky="nw", padx=10, pady=3)

vindu.knapp2 = customtkinter.CTkButton(master=vindu.meny, 
                                       text="Varelager",
                                       command=vis_varelager
                                       ) #definerer andre knappen
vindu.knapp2.grid(column=0, row=1, sticky="nw", padx=10, pady=(0,5)) # TROR dette definerer at knapp skal "limes" til "North East"

vindu.knapp2 = customtkinter.CTkButton(master=vindu.meny, text="Varebeholdning") #definerer andre knappen
vindu.knapp2.grid(column=0, row=2, sticky="nw", padx=10, pady=(0,5)) # TROR dette definerer at knapp skal "limes" til "North East"

vindu.knapp3 = customtkinter.CTkButton(master=vindu.meny, text="Kunder", command=vis_kunder)#definerer knapp tre
vindu.knapp3.grid(column=0, row=3, sticky="nw", padx=10, pady=(0,5))

vindu.mainloop()