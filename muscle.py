import tkinter as tk

# Liste des muscles et images sous forme de tuple
Liste_muscles = [
    ("Pectoraux", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png/pec1.png"), 
    ("Epaules", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png/epaule1.png"), 
    ("Biceps", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/biceps.png"), 
    ("Triceps", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png/tricep1.png"), 
    ("Abdominaux", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png/ab1.png"), 
    ("Quadriceps", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png/quad1.png"), 
    ("Dorsaux", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/lat1.png"), 
    ("Lombaires", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png/lb1.png"), 
    ("Fessiers", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png/glute1.png"), 
    ("Isquios-jambiers", "/Users/alexpeirano/Desktop/personal coding/tinker_project/images/jpg2png/ham1.png")
]

# Liste des muscles disponibles (définie à partir de Liste_muscles)
MUSCLES = [muscle[0] for muscle in Liste_muscles]

# Stockage des objectifs sélectionnés
selected_goals = {}

def set_muscle_goal(muscle, goal):
    """
    Définir l'objectif pour un muscle donné
    
    Args:
        muscle: nom du muscle
        goal: "maintenance", "normal_growth", ou "prioritised_growth"
    """
    if muscle in MUSCLES and goal in ["maintenance", "normal_growth", "prioritised_growth"]:
        selected_goals[muscle] = goal
    else:
        print(f"Muscle ou objectif invalide: {muscle}, {goal}")

def get_selected_muscle_goals():
    """Retourne les objectifs sélectionnés pour tous les muscles"""
    return selected_goals.copy()

def reset_all_goals():
    """Remet à zéro tous les objectifs"""
    global selected_goals
    selected_goals = {}
    print("Tous les objectifs ont été remis à zéro")

def print_current_goals():
    """Affiche les objectifs actuellement définis"""
    if not selected_goals:
        print("Aucun objectif défini")
    else:
        print("\nOBJECTIFS ACTUELS:")
        for muscle, goal in selected_goals.items():
            print(f"  {muscle}: {goal}")

# Compteurs
maintenance = 0
normal_growth = 0
prioritised_growth = 0

# Variables globales pour l'interface
current_muscle_index = 0

# Classe pour l'interface tkinter
class Muscle:
    def __init__(self, muscle_name, muscle_photo_path):
        self._restart = False
        self.window = tk.Tk()
        self.window.geometry("500x500+100+100")
        self.window.title(muscle_name)
        
        self.muscle_name = muscle_name

        try:
            self.muscle_photo = tk.PhotoImage(file=muscle_photo_path)
            self.label_b_2 = tk.Label(self.window, image=self.muscle_photo)
            self.label_b_2.pack(fill="both")
        except tk.TclError:
            # Si l'image ne peut pas être chargée
            self.label_b_1 = tk.Label(self.window, text=muscle_name, font=('Arial', 25, 'bold'))
            self.label_b_1.pack()

        self.button_maintenance = tk.Button(
            self.window, 
            text="Maintenance", 
            font=('Arial', 50, 'bold'),   
            fg='black',  
            command=lambda: self.select_goal("maintenance")
        )
        self.button_maintenance.pack(padx=6, pady=6, fill="x")

        self.button_normal_growth = tk.Button(
            self.window, 
            text="Normal Growth", 
            font=('Arial', 50, 'bold'), 
            fg='blue', 
            command=lambda: self.select_goal("normal_growth")
        )
        self.button_normal_growth.pack(padx=6, pady=6, fill="x")

        self.button_prioritised_growth = tk.Button(
            self.window, 
            text="Prioritised Growth", 
            font=('Arial', 50, 'bold'), 
            fg='red', 
            command=lambda: self.select_goal("prioritised_growth")
        )
        self.button_prioritised_growth.pack(padx=6, pady=6, fill="x")
    
    def select_goal(self, goal):
        """Sélectionne l'objectif pour le muscle actuel et passe au suivant"""
        set_muscle_goal(self.muscle_name, goal)
        
        # Mettre à jour les compteurs globaux
        global maintenance, normal_growth, prioritised_growth
        if goal == "maintenance":
            maintenance += 1
        elif goal == "normal_growth":
            normal_growth += 1
        elif goal == "prioritised_growth":
            prioritised_growth += 1
            
        self.create_new_window()
    
    def create_new_window(self):
        self._restart = True
        self.window.destroy()

def main():
    """Fonction principale pour lancer l'interface de sélection des objectifs musculaires"""
    global current_muscle_index
    current_muscle_index = 0
    
    while current_muscle_index < len(Liste_muscles):
        muscle_name, muscle_photo_path = Liste_muscles[current_muscle_index]
        
        try:
            app = Muscle(muscle_name, muscle_photo_path)
            app.window.mainloop()
            
            if app._restart:
                current_muscle_index += 1
                continue
            break
        except Exception as e:
            print(f"Erreur avec le muscle {muscle_name}: {e}")
            current_muscle_index += 1
            continue
    
    pass  # Selection terminée silencieusement

def run_muscle_selection_gui():
    """Fonction pour compatibilité - appelle main()"""
    main()

if __name__ == "__main__":
    # Lance l'interface si exécuté directement
    main()
