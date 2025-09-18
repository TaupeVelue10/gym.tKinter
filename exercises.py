import tkinter as tk

# liste d'exos
press_horizontale = [("Bench press", "images/jpg2png-2/bench1.png"), ("Dips", "images/jpg2png-2/dips.png")]
press_verticale = [("Overhead press", "images/jpg2png-2/jpg2png-3/overheadpress1.png"), ("Incline press", "images/jpg2png-2/incline_press_1.png")]
tirage_horizontal = [("Bent over row", "images/jpg2png-2/bent_over_row_1.png"), ("Machine row", "images/jpg2png-2/jpg2png-3/machine row.png")]
tirage_vertical = [("Pull up", "images/jpg2png-2/jpg2png-3/pull_up_1.png"), ("Chin up", "images/jpg2png-2/chin_up_1.png"), ("Lat pulldown", "images/jpg2png-2/lat_pulldown_1.png")]
squat_pattern = [("Barbell squat", "images/jpg2png-2/barbell_squat_1.png"), ("Bulgarian split squat", "images/jpg2png-2/bulgarian_split_squat_1.png"), ("Hack squat", "images/jpg2png-2/hack_squat_1.png"), ("Split squat", "images/jpg2png-2/jpg2png-3/split_squat.png")]
hinge_pattern = [("Stiff leg deadlift", "images/jpg2png-2/jpg2png-3/SLDL_1.png"), ("Back hyperextension", "images/jpg2png-2/back_hyper.png"), ("Deadlift", "images/jpg2png-2/deadlift.png")]
spine_flexion = [("Machine ab crunch", "images/jpg2png-2/jpg2png-3/machinecrunch.png"), ("Hanging leg raises", "images/jpg2png-2/hanginglegraises.png"), ("Sit ups", "images/jpg2png-2/jpg2png-3/situps.png")]
quad_iso = [("Leg extension", "images/jpg2png-2/jpg2png-3/legextension.png"), ("Sissy squat", "images/jpg2png-2/jpg2png-3/sissysquat.png")]
ham_iso = [("Seated leg curl", "images/jpg2png-2/jpg2png-3/seatedlegcurl.png"), ("Nordic curl", "images/jpg2png-2/jpg2png-3/nordic_curl.png"), ("Laying leg curl", "images/jpg2png-2/jpg2png-3/layinglegcurl.png")]
bicep_iso = [("Curl", "images/jpg2png-2/curl.png"), ("Preacher curl", "images/jpg2png-2/jpg2png-3/preachercurl.png"), ("Hammer curl", "images/jpg2png-2/hammercurl.png")]
tricep_iso = [("Pushdown", "images/jpg2png-2/jpg2png-3/pushdown.png"), ("Tricep extension", "images/jpg2png-2/extension tricep.png"), ("Skull crushers", "images/jpg2png-2/jpg2png-3/skullcrushers.png")]
delt_iso = [("Lateral raises", "images/jpg2png-2/jpg2png-3/lateral raises.png"), ("Front raise", "images/jpg2png-2/front raises.png"), ("Rear delt fly", "images/jpg2png-2/jpg2png-3/rear delt fly.png")]

#liste de pattern
pattern_liste = [("Press horizontale", press_horizontale), ("press verticale", press_verticale), ("tirage verticale", tirage_horizontal), ("tirage vertical", tirage_vertical),
                 ("squat pattern", squat_pattern),("hinge pattern", hinge_pattern), ("spine flexion", spine_flexion), ("quad iso", quad_iso), ("hamstring isolation", ham_iso),
                 ("bicep isolation", bicep_iso), ("tricep isolation", tricep_iso), ("delt isolation", delt_iso)]

# fonctions
def choose_exercise(i, j):
    # i = index du pattern, j = index de l'exercice dans ce pattern
    nom_pattern, exercises = pattern_liste[i]
    name, path = exercises[j][0], exercises[j][1]
    exercises[j] = (name, path, 1) # rajoute un 1 au tuple si il est choisit

class Exercises:
    def __init__(self, i):
        self.i = i
        self.chosen_count = 0
        self.window = tk.Tk()
        nom_pattern, exercises = pattern_liste[i]
        self.window.title(f"{nom_pattern}- choisissez 2 exercices")

        self.info = tk.Label(self.window, text="Sélections : 0/2", font=("Arial", 14))
        self.info.pack(pady=8)

        self._imgs = []  # garder les images en mémoire

        # un bouton par exercice
        for j in range(len(exercises)):
            name = exercises[j][0]
            path = exercises[j][1]

            # image si disponible
            try:
                img = tk.PhotoImage(file=path)
            except Exception:
                img = None
            self._imgs.append(img)

            btn = tk.Button(
                self.window,
                text=name,
                image=img,
                compound="top",
                command=lambda j=j: self.on_click(j)
            )
            btn.image = img
            btn.pack(padx=6, pady=6, fill="x")
        
        tk.Button(self.window, text="Fermer", command=self.window.destroy).pack(pady=10)

    def on_click(self, j):
        # choisir l'exercice, update le counter
        choose_exercise(self.i, j)
        self.chosen_count += 1
        # config permet de changer le label existant
        self.info.config(text=f"Sélections : {self.chosen_count}/2")

        # quand 2 choisis -> fermer la fenêtre => on passe au pattern suivant
        if self.chosen_count >= 2:
            self.window.destroy()

for i in range(len(pattern_liste)):
    app = Exercises(i)
    app.window.mainloop()


print(pattern_liste)
