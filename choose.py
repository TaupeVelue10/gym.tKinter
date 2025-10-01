import tkinter as tk

selected_days = None

def main():
    """Interface tkinter pour choisir le nombre de jours d'entrainement"""
    global selected_days
    selected_days = None
    
    def select_days(days):
        global selected_days
        selected_days = days
        root.destroy()
    
    root = tk.Tk()
    root.title("Choix du nombre de jours")
    root.geometry("500x400")
    
    # Titre
    title_label = tk.Label(root, text="NOMBRE DE JOURS D'ENTRAINEMENT", font=('Arial', 16, 'bold'))
    title_label.pack(pady=20)
    
    # Boutons pour chaque nombre de jours
    for days in range(2, 7):  # 2 à 6 jours
        btn = tk.Button(
            root,
            text=f"{days}",
            font=('Arial', 17),
            width=15,
            height=2,
            command=lambda d=days: select_days(d)
        )
        btn.pack(padx=6, pady=6, fill="x")
    
    # Centrer la fenêtre
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()
    
    return selected_days

if __name__ == "__main__":
    days = main()
    if days:
        print(f"Nombre de jours selectionne: {days}")
    else:
        print("Aucune selection")
