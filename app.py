import tk
import customtkinter
# Temp
# Antar vi skal ha noe her..
def vis_ordre():
    print("vise ordre!!")

vindu = customtkinter.CTk()
vindu.title("Testing")
vindu.geometry("800x600")
vindu.grid_columnconfigure(2, weight=1)
vindu.grid_rowconfigure(0, weight=1)

meny = customtkinter.CTkFrame(master=vindu, bg_color="grey", fg_color="white", corner_radius=0)
meny.grid(row=0, column=0, sticky="nsw", padx=10)
meny.grid_rowconfigure(0, weight=2)
meny.grid_columnconfigure(0, weight=1)

knapp = customtkinter.CTkButton(meny, text="Ordre", command=vis_ordre())
knapp.grid(sticky="ne")

vindu.mainloop()