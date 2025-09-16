#imports
import tkinter as tk

# liste des différents exo par pattern de mouvement
## press horizontale
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

#Imbeded list
pattern_liste = [press_horizontale, press_verticale, tirage_horizontal, tirage_vertical, squat_pattern, hinge_pattern, spine_flexion, quad_iso, ham_iso, bicep_iso, tricep_iso, delt_iso]

# méthodes
## Retiens en mémoire les exos choisis 
def choose_exercise() -> None : 
    pattern_liste[i][j] = (exercise_name, exercise_photo_path, 1)

def not_chosen_exercise() -> None :
    pattern_liste[i][j] = (exercise_name, exercise_photo_path, 0)

class Exercises:   # template de classe, a modif 

    def __init__(self, exercise_name, exercise_photo_path):
        self._restart = False
        self.window = tk.Tk()
        self.window.state("zoomed")
        self.window.title("MyFitnessPal de l'entrainement")
        
        self.exercise_name = exercise_name

        self.exercise_photo = tk.PhotoImage(file=exercise_photo_path)

        self.label_b_1 = tk.Label(self.window, text = pattern_name, font=('Arial', 25))
        self.label_b_1.pack(padx=10)

        self.label_b_2 = tk.Label(self.window, text = "Quel exercice préférez-vous")
        self.label_b_2.pack()
        
        #button frame
        self.buttonframe = tk.Frame(self.window)
        self.buttonframe.columnconfigure(0, weight= 1)
        self.buttonframe.columnconfigure(1, weight=1)

        self.bouton_p_1 = tk.Button(self.buttonframe, text=self.exercise_name, image= self.exercise_photo)
        self.bouton_p_1.grid(row=0, column=0, sticky=tk.W+tk.E)

        self.bouton_p_2 = tk.Button(self.buttonframe, text=self.exercise_name, image= self.exercise_photo)
        self.bouton_p_2.grid(row=0, column=1, sticky=tk.W+tk.E)

        self.bouton_p_3 = tk.Button(self.buttonframe, text=self.exercise_name, image= self.exercise_photo)
        self.bouton_p_3.grid(row=1, column=0, sticky=tk.W+tk.E)

        self.bouton_p_4 = tk.Button(self.buttonframe, text=self.exercise_name, image= self.exercise_photo)
        self.bouton_p_4.grid(row=1, column=1, sticky=tk.W+tk.E)

        self.buttonframe.pack()

    def create_new_window(self):
        self._restart = True
        self.window.destroy()
    # pour afficher l'ensemble des exos d'un pattern, il faut faire ca pour exphoto et pour exname : je n'ai pas tester la fonction
    def show_exercises(self):
        exo = ""
        for i in range(len(pattern_liste)):
            for j in range(len(pattern_liste[i])):   
                exo = pattern_liste[i][j]
i = 0
while i < len(pattern_liste):
    for j in range(len(pattern_liste[i])):
        pattern_name = pattern_liste[i]
        exercise_name = pattern_liste[i][j][0]
        exercise_photo_path = pattern_liste[i][j][1]
        app_1 = Exercises(exercise_name, exercise_photo_path)
        app_1.window.mainloop()
    
    if app_1._restart:
        continue
    else:
        break

