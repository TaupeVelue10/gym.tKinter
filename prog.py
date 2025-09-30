# Imports pour les connexions avec les autres modules
from muscle import get_selected_muscle_goals
from exercise import get_selected_exercises, get_exercise_pattern
from pattern_muscles import get_muscles_from_pattern

class Split:
    def __init__(self, name, sessions):
        self.name = name
        self.sessions = sessions

def create_prog(input):
    maintenance = [4, 5, 6]
    normal_growth = [7, 8, 9]
    prioritised_growth = [10, 11, 12]
    
    # Full Body - tous les muscles dans chaque session
    full_body = Split("Full Body", {
        "session": ["Pectoraux", "Epaules", "Dorsaux", "Biceps", "Triceps", 
                   "Abdominaux", "Quadriceps", "Isquios-jambiers", "Fessiers", "Lombaires"]
    })
    
    # Upper/Lower Split
    upper_lower = Split("Upper/Lower", {
        "upper": ["Pectoraux", "Epaules", "Dorsaux", "Biceps", "Triceps", "Abdominaux", "Lombaires"],
        "lower": ["Quadriceps", "Isquios-jambiers", "Fessiers"]
    })
    
    # Push/Pull/Legs Split
    push_pull_legs = Split("Push/Pull/Legs", {
        "push": ["Epaules", "Triceps", "Pectoraux", "Abdominaux"],
        "pull": ["Dorsaux", "Biceps", "Lombaires"],
        "legs": ["Quadriceps", "Isquios-jambiers", "Fessiers"]
    })
    
    if input == 2 or input == 3:
        prog = full_body
    elif input == 4 or input == 5: 
        prog = upper_lower
    elif input == 6:
        prog = push_pull_legs
    
    return prog

# Fonction utilitaire pour obtenir le nom du split
def get_split_name(input):
    if input == 2 or input == 3:
        return "Full Body"
    elif input == 4 or input == 5:
        return "Upper/Lower"
    elif input == 6:
        return "Push/Pull/Legs"

def generate_workout_program(nb_jours, objectifs_muscles, exercices_choisis, pattern_muscles):
    """
    Génère un programme d'entraînement basé sur les objectifs et exercices choisis
    
    Args:
        nb_jours: nombre de jours d'entraînement (2-6)
        objectifs_muscles: dict {"muscle": "maintenance"/"normal_growth"/"prioritised_growth"}
        exercices_choisis: list des exercices sélectionnés
        pattern_muscles: dict qui associe chaque pattern aux muscles travaillés
    """
    
    # Définir les volumes cibles
    volume_objectifs = {
        "maintenance": [4, 5, 6],
        "normal_growth": [7, 8, 9], 
        "prioritised_growth": [10, 11, 12]
    }
    
    # Obtenir le split approprié
    split = create_prog(nb_jours)
    
    # Calculer le volume cible pour chaque muscle (prendre le milieu de la fourchette)
    volumes_cibles = {}
    for muscle, objectif in objectifs_muscles.items():
        volume_range = volume_objectifs[objectif]
        volumes_cibles[muscle] = volume_range[1]  # Prendre la valeur moyenne
    
    # Associer chaque exercice aux muscles qu'il travaille
    exercices_muscles = {}
    for exercice in exercices_choisis:
        pattern = get_exercise_pattern(exercice)
        if pattern:
            muscles = get_muscles_from_pattern(pattern)
            exercices_muscles[exercice] = muscles
        else:
            exercices_muscles[exercice] = []
    
    # Classer les exercices par type (polyarticulaire vs isolation)
    exercices_poly = []
    exercices_isolation = []
    
    for exercice, muscles in exercices_muscles.items():
        if len(muscles) > 1:
            exercices_poly.append(exercice)
        else:
            exercices_isolation.append(exercice)
    
    # Générer le programme pour chaque session
    programme = {}
    
    for session_name, muscles_session in split.sessions.items():
        programme[session_name] = []
        volumes_restants = {muscle: volumes_cibles.get(muscle, 0) for muscle in muscles_session}
        
        # Ajouter d'abord les exercices polyarticulaires
        for exercice in exercices_poly:
            muscles_exercice = exercices_muscles[exercice]
            # Vérifier si l'exercice travaille des muscles de cette session
            muscles_communs = [m for m in muscles_exercice if m in muscles_session]
            
            if muscles_communs and any(volumes_restants[m] > 0 for m in muscles_communs):
                # Calculer le nombre de séries (entre 2 et 6)
                volume_max_necessaire = max([volumes_restants[m] for m in muscles_communs])
                series = min(6, max(2, volume_max_necessaire))
                
                programme[session_name].append({
                    "exercice": exercice,
                    "series": series,
                    "muscles": muscles_communs
                })
                
                # Réduire le volume restant pour chaque muscle travaillé
                for muscle in muscles_communs:
                    volumes_restants[muscle] = max(0, volumes_restants[muscle] - series)
        
        # Ajouter ensuite les exercices d'isolation si nécessaire
        for exercice in exercices_isolation:
            muscles_exercice = exercices_muscles[exercice]
            muscles_communs = [m for m in muscles_exercice if m in muscles_session]
            
            if muscles_communs and any(volumes_restants[m] > 0 for m in muscles_communs):
                muscle_cible = muscles_communs[0]  # Pour l'isolation, un seul muscle
                series = min(6, max(2, volumes_restants[muscle_cible]))
                
                programme[session_name].append({
                    "exercice": exercice,
                    "series": series,
                    "muscles": [muscle_cible]
                })
                
                volumes_restants[muscle_cible] = max(0, volumes_restants[muscle_cible] - series)
    
    # Afficher le programme
    print_workout_program(programme, split.name, nb_jours)
    return programme

def print_workout_program(programme, split_name, nb_jours):
    """Affiche le programme d'entraînement dans le terminal"""
    
    print(f"\n=== PROGRAMME D'ENTRAINEMENT ===")
    print(f"Split: {split_name}")
    print(f"Nombre de jours: {nb_jours}")
    print("=" * 40)
    
    for session_name, exercices in programme.items():
        print(f"\nSESSION: {session_name.upper()}")
        print("-" * 30)
        
        if not exercices:
            print("Aucun exercice pour cette session")
            continue
            
        for i, exercice_info in enumerate(exercices, 1):
            exercice = exercice_info["exercice"]
            series = exercice_info["series"]
            muscles = ", ".join(exercice_info["muscles"])
            
            print(f"{i}. {exercice}")
            print(f"   Series: {series}")
            print(f"   Muscles: {muscles}")
            print()
    
    print("=" * 40)

def create_complete_program(nb_jours):
    """
    Fonction principale qui génère un programme complet en utilisant
    les données sélectionnées dans muscle.py et exercise.py
    """
    
    # Récupérer les objectifs sélectionnés pour chaque muscle
    objectifs_muscles = get_selected_muscle_goals()
    
    # Récupérer les exercices sélectionnés
    exercices_choisis = get_selected_exercises()
    
    if not objectifs_muscles:
        print("Aucun objectif muscle defini. Veuillez d'abord selectionner vos objectifs dans muscle.py")
        return None
        
    if not exercices_choisis:
        print("Aucun exercice selectionne. Veuillez d'abord choisir vos exercices dans exercise.py")
        return None
    
    print(f"Objectifs recuperes: {len(objectifs_muscles)} muscles")
    print(f"Exercices recuperes: {len(exercices_choisis)} exercices")
    
    # Générer le programme complet
    programme = generate_workout_program(nb_jours, objectifs_muscles, exercices_choisis, {})
    
    return programme

# Exemple d'utilisation simple
def exemple_usage():
    """Exemple avec données simulées pour tester l'algorithme"""
    objectifs = {
        "Pectoraux": "normal_growth",
        "Epaules": "maintenance", 
        "Dorsaux": "prioritised_growth",
        "Biceps": "maintenance",
        "Triceps": "maintenance",
        "Quadriceps": "normal_growth",
        "Isquios-jambiers": "maintenance",
        "Fessiers": "normal_growth"
    }
    
    exercices = ["Développé couché", "Tractions", "Squats", "Curls biceps"]
    
    generate_workout_program(4, objectifs, exercices, {})

# Fonction de test complète
def test_complete_system():
    """
    Teste le système complet avec toutes les connexions
    """
    print("🧪 TEST DU SYSTÈME COMPLET")
    print("=" * 50)
    
    # 1. Configuration des objectifs muscles (simule les sélections utilisateur)
    from muscle import setup_example_goals, print_current_goals
    setup_example_goals()
    
    # 2. Configuration des exercices (simule les sélections utilisateur)
    from exercise import setup_example_exercises, print_selected_exercises
    setup_example_exercises()
    
    print("\n" + "=" * 50)
    print("📊 DONNÉES CONFIGURÉES:")
    print_current_goals()
    print_selected_exercises()
    
    print("\n" + "=" * 50)
    print("🏗️ GÉNÉRATION DU PROGRAMME...")
    
    # 3. Générer le programme avec 4 jours d'entraînement
    programme = create_complete_program(4)
    
    return programme

# Ce fichier contient toute la logique de génération de programme
# Pour lancer le système, exécutez main.py
