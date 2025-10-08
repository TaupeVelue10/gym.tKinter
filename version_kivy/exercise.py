# Interface tkinter pour la sélection d'exercices - VERSION FINALE
# Utilise exercise_database.py comme source unique pour TOUT
from exercise_database import get_exercise_info, get_pattern_list_for_interface
import tkinter as tk

# Variables globales
selected_exercises = []

def choose_exercise(selected_indices, i, j):
    if j not in selected_indices:
        selected_indices.append(j)

class Exercises:
    def __init__(self, i):
        self.i = i
        self.chosen_count = 0
        self.selected_indices = []
        self.window = tk.Tk()
        nom_pattern, exercises = pattern_liste[i]
        self.window.title(f"{nom_pattern} - choisissez 2 exercices")

        self.info = tk.Label(self.window, text="Selections : 0/2", font=("Arial", 14))
        self.info.pack(pady=8)

        self._imgs = []

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
        self.info.config(text=f"Selections : {self.chosen_count}/2")

        if self.chosen_count >= 2:
            self.window.destroy()

    def filter_exercises(self):
        nom_pattern, exercises = pattern_liste[self.i]
        pattern_liste[self.i] = (nom_pattern, [exercises[j] for j in self.selected_indices])

def main():
    """Fonction principale de sélection d'exercices"""
    global pattern_liste, selected_exercises
    
    selected_exercises = []
    
    for i in range(len(pattern_liste)):
        app = Exercises(i)
        app.window.mainloop()
        app.filter_exercises()

    # Collecter tous les exercices sélectionnés
    for nom_pattern, exercises in pattern_liste:
        for exercise_name, path in exercises:
            if exercise_name not in selected_exercises:
                selected_exercises.append(exercise_name)

# Fonctions de compatibilité
def get_selected_exercises():
    """Retourne la liste des exercices sélectionnés"""
    return selected_exercises.copy()

def get_exercise_pattern(exercise_name):
    """Retourne le pattern d'un exercice depuis la base centralisée"""
    info = get_exercise_info(exercise_name)
    return info["pattern"] if info else None

# Générer la liste au démarrage depuis la base centralisée
pattern_liste = get_pattern_list_for_interface()

if __name__ == "__main__":
    main()