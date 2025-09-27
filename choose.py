import tkinter as tk

# fonction qui restreint l'input
def valider(input):
    n = ["2","3","4","5","6"]
    if input == ""  or input in n:
        return True
    return False 
# fonction qui récupère l'input
def afficher():
    input = text_box.get()
    print(input)

def run_choose() -> None :
    number_of_days = 0
    global text_box
    window = tk.Tk()
    window.title("nombre de jours/semaine")

    window.geometry("300x300")

    vcmd = (window.register(valider), "%P")

    text_box = tk.Entry(window, validate="key", validatecommand=vcmd)
    text_box.pack()

    bouton = tk.Button(window, text="Valider", command=afficher).pack(pady=10)
    

    tk.mainloop()

run_choose()
