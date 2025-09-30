# Base de données des exercices avec leurs patterns de mouvement
EXERCISES_DB = {
    # Exercices de poussée
    "Développé couché": "Horizontal Push (Chest)",
    "Développé incliné": "Incline Push",
    "Développé décliné": "Decline Push",
    "Développé militaire": "Vertical Push",
    "Développé haltères": "Horizontal Push (Chest)",
    "Pompes": "Horizontal Push (Chest)",
    
    # Exercices de tirage
    "Tractions": "Vertical Pull",
    "Tirage horizontal": "Horizontal Pull",
    "Rowing barre": "Row",
    "Rowing haltère": "Row",
    "Lat pulldown": "Vertical Pull",
    
    # Exercices de jambes
    "Squats": "Squat",
    "Soulevé de terre": "Deadlift",
    "Fentes": "Lunge",
    "Hip thrust": "Hip Hinge",
    "Leg press": "Squat",
    "Bulgarian split squat": "Single Leg",
    
    # Exercices d'isolation
    "Curls biceps": "Bicep Curl",
    "Extensions triceps": "Tricep Extension",
    "Élévations latérales": "Lateral Raise",
    "Oiseau": "Rear Delt",
    "Écarté couché": "Chest Fly",
    "Leg extension": "Leg Extension",
    "Leg curl": "Leg Curl",
    "Mollets debout": "Calf Raise",
    "Crunch": "Abs",
    "Extensions lombaires": "Lower Back",
}

# Stockage des exercices sélectionnés
selected_exercises = []

def add_exercise(exercise_name):
    """Ajouter un exercice à la sélection"""
    if exercise_name in EXERCISES_DB and exercise_name not in selected_exercises:
        selected_exercises.append(exercise_name)
        print(f"✅ Exercice ajouté: {exercise_name}")
    elif exercise_name in selected_exercises:
        print(f"⚠️ Exercice déjà sélectionné: {exercise_name}")
    else:
        print(f"❌ Exercice inconnu: {exercise_name}")

def remove_exercise(exercise_name):
    """Retirer un exercice de la sélection"""
    if exercise_name in selected_exercises:
        selected_exercises.remove(exercise_name)
        print(f"🗑️ Exercice retiré: {exercise_name}")
    else:
        print(f"❌ Exercice non trouvé dans la sélection: {exercise_name}")

def get_selected_exercises():
    """Retourne la liste des exercices sélectionnés"""
    return selected_exercises.copy()

def get_exercise_pattern(exercise_name):
    """Retourne le pattern de mouvement d'un exercice"""
    return EXERCISES_DB.get(exercise_name)

def get_all_exercises():
    """Retourne tous les exercices disponibles"""
    return list(EXERCISES_DB.keys())

def reset_selected_exercises():
    """Remet à zéro la sélection d'exercices"""
    global selected_exercises
    selected_exercises = []
    print("🔄 Sélection d'exercices remise à zéro")

def print_selected_exercises():
    """Affiche les exercices actuellement sélectionnés"""
    if not selected_exercises:
        print("Aucun exercice sélectionné")
    else:
        print("\n🏋️ EXERCICES SÉLECTIONNÉS:")
        for exercise in selected_exercises:
            pattern = get_exercise_pattern(exercise)
            print(f"  {exercise} - Pattern: {pattern}")

def print_available_exercises():
    """Affiche tous les exercices disponibles"""
    print("\n📋 EXERCICES DISPONIBLES:")
    for exercise, pattern in EXERCISES_DB.items():
        selected = "✓" if exercise in selected_exercises else " "
        print(f"  [{selected}] {exercise} - {pattern}")

# Exemple de sélection d'exercices
def setup_example_exercises():
    """Configure une sélection d'exercices d'exemple"""
    exercises_to_add = [
        "Développé couché", "Tractions", "Squats", "Soulevé de terre",
        "Développé militaire", "Rowing barre", "Curls biceps", 
        "Extensions triceps", "Fentes", "Élévations latérales"
    ]
    
    for exercise in exercises_to_add:
        add_exercise(exercise)

# Interface tkinter originale restaurée
import tkinter as tk

# liste d'exos
press_horizontale = [("Bench press", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png-2/bench1.png"), ("Dips", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png-2/dips.png")]
press_verticale = [("Overhead press", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png-2/jpg2png-3/overheadpress1.png"), ("Incline press", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png-2/incline_press_1.png")]
tirage_horizontal = [("Bent over row", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png-2/bent_over_row_1.png"), ("Machine row", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png-2/jpg2png-3/machine row.png")]
tirage_vertical = [("Pull up", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png-2/jpg2png-3/pull_up_1.png"), ("Chin up", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png-2/chin_up_1.png"), ("Lat pulldown", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png-2/lat_pulldown_1.png")]
squat_pattern = [("Barbell squat", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png-2/barbell_squat_1.png"), ("Bulgarian split squat", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png-2/bulgarian_split_squat_1.png"), ("Hack squat", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png-2/hack_squat_1.png"), ("Split squat", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png-2/jpg2png-3/split_squat.png")]
hinge_pattern = [("Stiff leg deadlift", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png-2/jpg2png-3/SLDL_1.png"), ("Back hyperextension", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png-2/back_hyper.png"), ("Deadlift", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png-2/deadlift.png")]
spine_flexion = [("Machine ab crunch", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png-2/jpg2png-3/machinecrunch.png"), ("Hanging leg raises", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png-2/hanginglegraises.png"), ("Sit ups", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png-2/jpg2png-3/situps.png")]
quad_iso = [("Leg extension", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png-2/jpg2png-3/legextension.png"), ("Sissy squat", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png-2/jpg2png-3/sissysquat.png")]
ham_iso = [("Seated leg curl", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png-2/jpg2png-3/seatedlegcurl.png"), ("Nordic curl", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png-2/jpg2png-3/nordic_curl.png"), ("Laying leg curl", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png-2/jpg2png-3/layinglegcurl.png")]
bicep_iso = [("Curl", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png-2/curl.png"), ("Preacher curl", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png-2/jpg2png-3/preachercurl.png"), ("Hammer curl", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png-2/hammercurl.png")]
tricep_iso = [("Pushdown", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png-2/jpg2png-3/pushdown.png"), ("Tricep extension", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png-2/extension tricep.png"), ("Skull crushers", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png-2/jpg2png-3/skullcrushers.png")]
delt_iso = [("Lateral raises", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png-2/jpg2png-3/lateral raises.png"), ("Front raise", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png-2/front raises.png"), ("Rear delt fly", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png-2/jpg2png-3/rear delt fly.png")]

#liste de pattern
pattern_liste = [("Press horizontale", press_horizontale), ("press verticale", press_verticale), ("tirage verticale", tirage_horizontal), ("tirage vertical", tirage_vertical),
                 ("squat pattern", squat_pattern),("hinge pattern", hinge_pattern), ("spine flexion", spine_flexion), ("quad iso", quad_iso), ("hamstring isolation", ham_iso),
                 ("bicep isolation", bicep_iso), ("tricep isolation", tricep_iso), ("delt isolation", delt_iso)]

# fonctions
def choose_exercise(selected_indices, i, j):
    # Ajoute l'index sélectionné à la liste
    if j not in selected_indices:
        selected_indices.append(j)

class Exercises:
    def __init__(self, i):
        self.i = i
        self.chosen_count = 0
        self.selected_indices = []
        self.window = tk.Tk()
        nom_pattern, exercises = pattern_liste[i]
        self.window.title(f"{nom_pattern}- choisissez 2 exercices")

        self.info = tk.Label(self.window, text="Selections : 0/2", font=("Arial", 14))
        self.info.pack(pady=8)

        self._imgs = []

        # un bouton par exercice
        for j in range(len(exercises)):
            name = exercises[j][0]
            path = exercises[j][1]
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
        choose_exercise(self.selected_indices, self.i, j)
        self.chosen_count += 1
        # config permet de changer le label existant
        self.info.config(text=f"Selections : {self.chosen_count}/2")

        # quand 2 choisis -> fermer la fenêtre => on passe au pattern suivant
        if self.chosen_count >= 2:
            self.window.destroy()

    def filter_exercises(self):
        # Garde seulement les exercices sélectionnés
        nom_pattern, exercises = pattern_liste[self.i]
        pattern_liste[self.i] = (nom_pattern, [exercises[j] for j in self.selected_indices])

def main():
    """Fonction principale qui lance l'interface de sélection des exercices"""
    global pattern_liste, selected_exercises
    
    # Réinitialiser la liste des exercices sélectionnés
    selected_exercises = []
    
    for i in range(len(pattern_liste)):
        app = Exercises(i)
        app.window.mainloop()
        app.filter_exercises()  # Filtrer après la sélection

    # Ajouter tous les exercices sélectionnés à la liste globale
    for nom_pattern, exercises in pattern_liste:
        for exercise_name, path in exercises:
            if exercise_name not in selected_exercises:
                selected_exercises.append(exercise_name)

    print("Selection des exercices terminee")
    print("Exercices selectionnes par pattern:")
    for nom_pattern, exercises in pattern_liste:
        print(f"{nom_pattern}: {[ex[0] for ex in exercises]}")
    
    print(f"\nTotal des exercices selectionnes: {len(selected_exercises)}")
    for exercise in selected_exercises:
        print(f"  - {exercise}")

# Base de données des exercices avec leurs patterns de mouvement (pour compatibilité)
EXERCISES_DB = {
    # Press horizontale
    "Bench press": "Horizontal Push (Chest)",
    "Dips": "Horizontal Push (Chest)",
    
    # Press verticale  
    "Overhead press": "Vertical Push",
    "Incline press": "Incline Push",
    
    # Tirage horizontal
    "Bent over row": "Row",
    "Machine row": "Row",
    
    # Tirage vertical
    "Pull up": "Vertical Pull",
    "Chin up": "Vertical Pull", 
    "Lat pulldown": "Vertical Pull",
    
    # Squat pattern
    "Barbell squat": "Squat",
    "Bulgarian split squat": "Single Leg",
    "Hack squat": "Squat",
    "Split squat": "Single Leg",
    
    # Hinge pattern
    "Stiff leg deadlift": "Hip Hinge",
    "Back hyperextension": "Hip Hinge",
    "Deadlift": "Deadlift",
    
    # Spine flexion
    "Machine ab crunch": "Abs",
    "Hanging leg raises": "Abs",
    "Sit ups": "Abs",
    
    # Isolations
    "Leg extension": "Leg Extension",
    "Sissy squat": "Leg Extension",
    "Seated leg curl": "Leg Curl",
    "Nordic curl": "Leg Curl",
    "Laying leg curl": "Leg Curl",
    "Curl": "Bicep Curl",
    "Preacher curl": "Bicep Curl",
    "Hammer curl": "Bicep Curl",
    "Pushdown": "Tricep Extension",
    "Tricep extension": "Tricep Extension",
    "Skull crushers": "Tricep Extension",
    "Lateral raises": "Lateral Raise",
    "Front raise": "Lateral Raise",
    "Rear delt fly": "Rear Delt"
}

# Variables pour compatibilité
selected_exercises = []

# Fonctions de compatibilité avec le système existant
def get_selected_exercises():
    """Retourne la liste de tous les exercices sélectionnés"""
    # Utiliser la liste globale mise à jour
    return selected_exercises.copy()

def get_exercise_pattern(exercise_name):
    """Retourne le pattern d'un exercice donné"""
    # D'abord chercher dans la liste des patterns sélectionnés
    for nom_pattern, exercises in pattern_liste:
        for ex_name, path in exercises:
            if ex_name == exercise_name:
                # Convertir le nom du pattern vers la nomenclature du système
                pattern_mapping = {
                    "Press horizontale": "Horizontal Push (Chest)",
                    "press verticale": "Vertical Push", 
                    "tirage verticale": "Row",
                    "tirage vertical": "Vertical Pull",
                    "squat pattern": "Squat",
                    "hinge pattern": "Hip Hinge", 
                    "spine flexion": "Abs",
                    "quad iso": "Leg Extension",
                    "hamstring isolation": "Leg Curl",
                    "bicep isolation": "Bicep Curl",
                    "tricep isolation": "Tricep Extension",
                    "delt isolation": "Lateral Raise"
                }
                return pattern_mapping.get(nom_pattern, nom_pattern)
    
    # Sinon utiliser la base de données de compatibilité
    return EXERCISES_DB.get(exercise_name)

def add_exercise(exercise_name):
    """Ajoute un exercice à la sélection (pour compatibilité)"""
    if exercise_name not in selected_exercises:
        selected_exercises.append(exercise_name)

def remove_exercise(exercise_name):
    """Retire un exercice de la sélection (pour compatibilité)"""
    if exercise_name in selected_exercises:
        selected_exercises.remove(exercise_name)

def reset_selected_exercises():
    """Remet à zéro la sélection (pour compatibilité)"""
    global selected_exercises
    selected_exercises = []

def print_selected_exercises():
    """Affiche les exercices sélectionnés (pour compatibilité)"""
    selected = get_selected_exercises()
    if selected:
        print("Exercices selectionnes:")
        for exercise in selected:
            print(f"  - {exercise}")
    else:
        print("Aucun exercice selectionne")

def setup_example_exercises():
    """Configure des exercices d'exemple (pour compatibilité)"""
    pass  # Pas nécessaire avec l'interface originale

def run_exercise_selection_gui():
    """Fonction pour compatibilité - appelle main()"""
    main()

def run_exercise_selection_gui():
    """Fonction pour compatibilité - appelle main()"""
    main()

if __name__ == "__main__":
    # Lance l'interface si exécuté directement
    main()