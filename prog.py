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
    
    # Full Body - 2 séances différentes A et B
    full_body = Split("Full Body", {
        "session_A": ["Pectoraux", "Epaules", "Dorsaux", "Biceps", "Triceps", 
                     "Abdominaux", "Quadriceps", "Isquios-jambiers", "Fessiers", "Lombaires"],
        "session_B": ["Pectoraux", "Epaules", "Dorsaux", "Biceps", "Triceps", 
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
    nb_sessions = len(split.sessions)
    
    # Calculer le volume total hebdomadaire pour chaque muscle
    volumes_hebdomadaires = {}
    for muscle, objectif in objectifs_muscles.items():
        volume_range = volume_objectifs[objectif]
        volumes_hebdomadaires[muscle] = volume_range[1]  # Prendre la valeur moyenne
    
    # Associer chaque exercice aux muscles qu'il travaille
    exercices_muscles = {}
    for exercice in exercices_choisis:
        pattern = get_exercise_pattern(exercice)
        if pattern:
            muscles = get_muscles_from_pattern(pattern)
            exercices_muscles[exercice] = muscles
        else:
            exercices_muscles[exercice] = []
    
    # Classer les exercices par catégorie pour éviter les conflits
    exercices_par_pattern = {}
    for exercice, muscles in exercices_muscles.items():
        pattern = get_exercise_pattern(exercice)
        if pattern not in exercices_par_pattern:
            exercices_par_pattern[pattern] = []
        exercices_par_pattern[pattern].append((exercice, muscles))
    
    # Générer le programme pour chaque session
    programme = {}
    volumes_utilises = {muscle: 0 for muscle in objectifs_muscles.keys()}
    
    # Groupes d'exercices similaires à éviter dans la même session
    exercices_similaires = {
        "Bench press": ["Dips"],
        "Dips": ["Bench press"],
        "Overhead press": ["Incline press"],
        "Incline press": ["Overhead press"],
        "Machine row": ["Bent over row"],
        "Bent over row": ["Machine row"],
        "Pull up": ["Chin up", "Lat pulldown"],
        "Chin up": ["Pull up", "Lat pulldown"],
        "Lat pulldown": ["Pull up", "Chin up"],
        "Barbell squat": ["Hack squat", "Bulgarian split squat"],
        "Hack squat": ["Barbell squat", "Bulgarian split squat"],
        "Bulgarian split squat": ["Barbell squat", "Hack squat", "Split squat"],
        "Split squat": ["Bulgarian split squat"],
        "Stiff leg deadlift": ["Deadlift", "Back hyperextension"],
        "Deadlift": ["Stiff leg deadlift", "Back hyperextension"],
        "Back hyperextension": ["Stiff leg deadlift", "Deadlift"],
        "Machine ab crunch": ["Sit ups", "Hanging leg raises"],
        "Sit ups": ["Machine ab crunch", "Hanging leg raises"],
        "Hanging leg raises": ["Machine ab crunch", "Sit ups"]
    }
    
    # Répartir les exercices de manière alternée entre les sessions
    sessions_names = list(split.sessions.keys())
    exercices_repartis = {session: [] for session in sessions_names}
    exercices_utilises_globalement = []
    
    # Grouper les exercices par pattern pour une meilleure répartition
    for pattern, exercices_pattern in exercices_par_pattern.items():
        exercices_du_pattern = []
        for exercice, muscles in exercices_pattern:
            muscles_communs = [m for m in muscles if any(m in split.sessions[s] for s in sessions_names)]
            if muscles_communs:
                priorite = len(muscles_communs)
                exercices_du_pattern.append((exercice, muscles_communs, pattern, priorite))
        
        # Trier par priorité et alterner entre les sessions
        exercices_du_pattern.sort(key=lambda x: x[3], reverse=True)
        
        for i, (exercice, muscles_communs, pattern, priorite) in enumerate(exercices_du_pattern):
            session_index = i % len(sessions_names)
            session_name = sessions_names[session_index]
            exercices_repartis[session_name].append((exercice, muscles_communs, pattern, priorite))
    
    # Générer le programme pour chaque session
    for session_name, muscles_session in split.sessions.items():
        programme[session_name] = []
        exercices_utilises_session = []
        
        # Calculer le volume cible par session pour chaque muscle
        volumes_session = {}
        for muscle in muscles_session:
            if muscle in volumes_hebdomadaires:
                volume_restant = volumes_hebdomadaires[muscle] - volumes_utilises[muscle]
                volumes_session[muscle] = max(0, min(volume_restant, 6))  # Max 6 séries par muscle par session
        
        # Ajouter les exercices de cette session
        for exercice, muscles_communs, pattern, _ in exercices_repartis[session_name]:
            # Vérifier si l'exercice travaille des muscles de cette session
            muscles_session_communs = [m for m in muscles_communs if m in muscles_session]
            
            if not muscles_session_communs:
                continue
                
            # Vérifier si on a encore besoin de volume pour ces muscles
            volume_necessaire = max([volumes_session.get(m, 0) for m in muscles_session_communs])
            
            if volume_necessaire <= 0:
                continue
                
            # Vérifier si on peut ajouter cet exercice (éviter les exercices similaires)
            peut_ajouter = True
            if exercice in exercices_similaires:
                for exercice_similaire in exercices_similaires[exercice]:
                    if exercice_similaire in exercices_utilises_session:
                        peut_ajouter = False
                        break
            
            if peut_ajouter:
                # Calculer le nombre de séries (entre 2 et 4)
                series = min(4, max(2, volume_necessaire))
                
                programme[session_name].append({
                    "exercice": exercice,
                    "series": series,
                    "muscles": muscles_session_communs
                })
                
                exercices_utilises_session.append(exercice)
                
                # Mettre à jour les volumes utilisés
                for muscle in muscles_session_communs:
                    volumes_utilises[muscle] += series
                    volumes_session[muscle] = max(0, volumes_session.get(muscle, 0) - series)
    
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
