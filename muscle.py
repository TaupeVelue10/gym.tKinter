import tkinter as tk

# counters
maintenance = 0
normal_growth = 0
prioritised_growth = 0
                               # cree liste des muscles # cree boucle 
# liste des muscles et images sous forme de tuple
Liste_muscles = [("Pectoraux", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png/pec1.png"), ("Epaules", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png/epaule1.png"), ("Biceps", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/biceps.png"), ("Triceps", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png/tricep1.png"), ("Abdominaux", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png/ab1.png"), ("Quadriceps", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png/quad1.png"), ("Dorsaux", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/lat1.png"), ("Trapèze", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png/trap1.png"), ("Lombaires", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png/lb1.png"), ("Fessiers", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png/glute1.png"), ("Isquios-jambiers", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png/ham1.png")]


# Fonctions
## Fonctions updates
def update_maintenance() -> None:
    global maintenance
    maintenance += 1
    Liste_muscles[i] = (Liste_muscles[i][0], Liste_muscles[i][1], 1)

def update_normal_growth() -> None:
    global normal_growth
    normal_growth += 1
    Liste_muscles[i] = (Liste_muscles[i][0], Liste_muscles[i][1], 2)

def update_prioritised_growth() -> None:
    global prioritised_growth
    prioritised_growth += 1
    Liste_muscles[i] = (Liste_muscles[i][0], Liste_muscles[i][1], 3)


# choix des priorités pour les muscles 
class Muscle:

    def __init__(self, muscle_name, muscle_photo_path):
        self._restart = False
        self.window = tk.Tk()
        self.window.geometry("500x500+100+100")
        """self.window.state("zoomed")"""
        self.window.title(muscle_name)
        
        self.muscle_name = muscle_name

        self.muscle_photo = tk.PhotoImage(file=muscle_photo_path)

        """self.label_b_1 = tk.Label(self.window, text = muscle_name, font=('Arial', 25))
        self.label_b_1.pack()"""

        self.label_b_2 = tk.Label(self.window, image= self.muscle_photo).pack(fill="both")
        """self.label_b_2.place(anchor="nw")"""

        self.button_maintenance = tk.Button(self.window, text= "Maintenance", font=('Arial', 50), fg='green', command= lambda: (update_maintenance(), self.create_new_window()))
        self.button_maintenance.pack(padx=6, pady=6, fill="x")

        self.button_normal_growth = tk.Button(self.window, text="Normal Growth", font=('Arial', 50), fg='blue', command=lambda: (update_normal_growth(), self.create_new_window()))
        self.button_normal_growth.pack(padx=6, pady=6, fill="x")

        self.button_prioritised_growth = tk.Button(self.window, text="Prioritised Growth", font=('Arial', 50), fg='red', command=lambda: (update_prioritised_growth(), self.create_new_window()))
        self.button_prioritised_growth.pack(padx=6, pady=6, fill="x")
        
        """self.label_maintenace = tk.Label(self.window, text=maintenance)      #bien placer les labels counters (avec une box?)
        self.label_maintenace.pack()

        self.label_normal_growth = tk.Label(self.window, text=normal_growth)
        self.label_normal_growth.pack()

        self.label_prioritised_growth = tk.Label(self.window, text=prioritised_growth)
        self.label_prioritised_growth.pack()"""
    def create_new_window(self):
        self._restart = True
        self.window.destroy()

# controleur, quand un bouton est cliqué -> on appelle la methode create_new_window qui update self._restart comme True
## a chaque itération i += 1 pour changer de muscle 
i = 0
while i < len(Liste_muscles):                              # ya une couille avec la boucle genre index out of range
    muscle_name = Liste_muscles[i][0]
    muscle_photo_path = Liste_muscles[i][1]
    app = Muscle(muscle_name, muscle_photo_path)
    app.window.mainloop()
    
    if app._restart:
        i += 1
        continue
    break
