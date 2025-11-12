# Programme d'entraînement - Version propre
from muscle import get_selected_muscle_goals
from exercise import get_selected_exercises
from exercise_database import get_exercise_info, is_polyarticular

class Split:
    def __init__(self, name, sessions):
        self.name = name
        self.sessions = sessions

def create_prog(input):
    # Full Body - 3 séances distinctes A, B et C
    full_body = Split("Full Body", {
        "session_A": ["Pectoraux", "Epaules", "Dorsaux", "Biceps", "Triceps", 
                     "Abdominaux", "Quadriceps", "Isquios-jambiers", "Fessiers", "Lombaires"],
        "session_B": ["Pectoraux", "Epaules", "Dorsaux", "Biceps", "Triceps", 
                     "Abdominaux", "Quadriceps", "Isquios-jambiers", "Fessiers", "Lombaires"],
        "session_C": ["Pectoraux", "Epaules", "Dorsaux", "Biceps", "Triceps", 
                     "Abdominaux", "Quadriceps", "Isquios-jambiers", "Fessiers", "Lombaires"]
    })
    
    # Upper/Lower Split - 4 séances distinctes pour 4-5 jours
    upper_lower = Split("Upper/Lower", {
        "upper_A": ["Pectoraux", "Epaules", "Dorsaux", "Biceps", "Triceps", "Abdominaux"],
        "lower_A": ["Quadriceps", "Isquios-jambiers", "Fessiers", "Lombaires"],
        "upper_B": ["Pectoraux", "Epaules", "Dorsaux", "Biceps", "Triceps", "Abdominaux"],
        "lower_B": ["Quadriceps", "Isquios-jambiers", "Fessiers", "Lombaires"]
    })
    
    # Push/Pull/Legs Split - 6 séances distinctes
    push_pull_legs = Split("Push/Pull/Legs", {
        "push_A": ["Pectoraux", "Epaules", "Triceps", "Abdominaux"],
        "pull_A": ["Dorsaux", "Biceps"],
        "legs_A": ["Quadriceps", "Isquios-jambiers", "Fessiers", "Lombaires"],
        "push_B": ["Pectoraux", "Epaules", "Triceps", "Abdominaux"],
        "pull_B": ["Dorsaux", "Biceps"],
        "legs_B": ["Quadriceps", "Isquios-jambiers", "Fessiers", "Lombaires"]
    })
    
    if input == 2 or input == 3:
        prog = full_body
    elif input == 4 or input == 5: 
        prog = upper_lower
    elif input == 6:
        prog = push_pull_legs
    
    return prog

def repartir_exercices_ppl(exercices_choisis, sessions_names):
    """Répartit les exercices pour PPL en utilisant la base de données centralisée"""
    exercices_repartis = {session: [] for session in sessions_names}
    
    # Identifier les sessions par type
    sessions_push = [s for s in sessions_names if 'push' in s.lower()]
    sessions_pull = [s for s in sessions_names if 'pull' in s.lower()]
    sessions_legs = [s for s in sessions_names if 'legs' in s.lower()]
    
    # Classer les exercices par catégorie en utilisant la base de données
    exercices_push = []
    exercices_pull = []
    exercices_legs = []
    
    for exercice_name in exercices_choisis:
        info = get_exercise_info(exercice_name)
        if not info:
            continue
            
        exercice_info = (exercice_name, info["all_muscles"], info["pattern"], info["type"])
        
        if info["category"] == "push" or info["category"] == "core":
            exercices_push.append(exercice_info)
        elif info["category"] == "pull":
            exercices_pull.append(exercice_info)
        elif info["category"] == "legs":
            exercices_legs.append(exercice_info)
    
    # Trier : polyarticulaires d'abord
    def sort_by_priority(exercice_info):
        return 2 if exercice_info[3] == "polyarticulaire" else 1
    
    exercices_push.sort(key=sort_by_priority, reverse=True)
    exercices_pull.sort(key=sort_by_priority, reverse=True)
    exercices_legs.sort(key=sort_by_priority, reverse=True)
    
    # Distribuer alternativement entre sessions A et B
    for i, exercice_info in enumerate(exercices_push):
        if sessions_push and i < len(exercices_push):
            session_index = i % len(sessions_push)
            exercices_repartis[sessions_push[session_index]].append(exercice_info)
    
    for i, exercice_info in enumerate(exercices_pull):
        if sessions_pull and i < len(exercices_pull):
            session_index = i % len(sessions_pull)
            exercices_repartis[sessions_pull[session_index]].append(exercice_info)
    
    for i, exercice_info in enumerate(exercices_legs):
        if sessions_legs and i < len(exercices_legs):
            session_index = i % len(sessions_legs)
            exercices_repartis[sessions_legs[session_index]].append(exercice_info)
    
    return exercices_repartis

def generate_workout_program(nb_jours, objectifs_muscles, exercices_choisis, pattern_muscles):
    """Génère un programme d'entraînement basé sur la base de données centralisée"""
    
    # Volumes d'entraînement
    volume_objectifs = {
        "maintenance": [4, 5, 6],
        "normal_growth": [7, 8, 9, 10], 
        "prioritised_growth": [11, 12, 13]
    }
    
    # Obtenir le split approprié
    split = create_prog(nb_jours)
    
    # Calculer le volume à la semaine pour chaque muscle
    volumes_hebdomadaires = {}
    for muscle, objectif in objectifs_muscles.items():
        volume_range = volume_objectifs[objectif]
        volumes_hebdomadaires[muscle] = volume_range[1]  
    
    # Générer le programme pour chaque session
    programme = {}
    sessions_names = list(split.sessions.keys())
    
    # Calculer le volume cible par session
    volumes_par_session = {}
    for session_name in sessions_names:
        volumes_par_session[session_name] = {}
    
    # Calculer combien de fois chaque session sera exécutée dans la semaine
    repetitions_par_session = {}
    if split.name == "Upper/Lower" and nb_jours == 5:
        for session_name in sessions_names:
            if "upper_a" in session_name.lower():
                repetitions_par_session[session_name] = 2
            else:
                repetitions_par_session[session_name] = 1
    else:
        for session_name in sessions_names:
            repetitions_par_session[session_name] = 1
        
    for muscle, volume_hebdo in volumes_hebdomadaires.items():
        sessions_avec_muscle = [s for s in sessions_names if muscle in split.sessions[s]]
        if sessions_avec_muscle:
            total_repetitions = sum(repetitions_par_session[s] for s in sessions_avec_muscle)
            
            if total_repetitions > 0:
                volume_base_par_session = volume_hebdo // total_repetitions
                volume_restant = volume_hebdo % total_repetitions
                
                for i, session_name in enumerate(sessions_avec_muscle):
                    volumes_par_session[session_name][muscle] = volume_base_par_session
                    if i < volume_restant:
                        volumes_par_session[session_name][muscle] += 1
    
    # Répartition des exercices selon le type de split
    if split.name == "Push/Pull/Legs":
        exercices_repartis = repartir_exercices_ppl(exercices_choisis, sessions_names)
    elif split.name == "Upper/Lower":
        # Répartition spéciale pour Upper/Lower
        exercices_repartis = {session: [] for session in sessions_names}
        
        # Séparer les exercices par catégorie
        exercices_upper = []
        exercices_lower = []
        
        for exercice_name in exercices_choisis:
            info = get_exercise_info(exercice_name)
            if not info:
                continue
            
            exercice_info = (exercice_name, info["all_muscles"], info["pattern"], info["type"])
            
            # Classer selon la catégorie
            if info["category"] in ["push", "pull", "core"]:  # Core (abs) va dans upper
                exercices_upper.append(exercice_info)
            elif info["category"] == "legs":
                exercices_lower.append(exercice_info)
        
        # Trier par priorité (polyarticulaires d'abord)
        exercices_upper.sort(key=lambda x: 2 if x[3] == "polyarticulaire" else 1, reverse=True)
        exercices_lower.sort(key=lambda x: 2 if x[3] == "polyarticulaire" else 1, reverse=True)
        
        # Distribuer alternativement entre A et B
        sessions_upper = [s for s in sessions_names if 'upper' in s.lower()]
        sessions_lower = [s for s in sessions_names if 'lower' in s.lower()]
        
        for i, exercice_info in enumerate(exercices_upper):
            if sessions_upper:
                session_index = i % len(sessions_upper)
                exercices_repartis[sessions_upper[session_index]].append(exercice_info)
        
        for i, exercice_info in enumerate(exercices_lower):
            if sessions_lower:
                session_index = i % len(sessions_lower)
                exercices_repartis[sessions_lower[session_index]].append(exercice_info)
    else:
        # Pour Full Body, répartition simple
        exercices_repartis = {session: [] for session in sessions_names}
        
        # Trier tous les exercices par priorité
        exercices_avec_info = []
        for exercice_name in exercices_choisis:
            info = get_exercise_info(exercice_name)
            if info:
                exercices_avec_info.append((exercice_name, info["all_muscles"], info["pattern"], info["type"]))
        
        # Trier par type (polyarticulaires d'abord)
        exercices_avec_info.sort(key=lambda x: 2 if x[3] == "polyarticulaire" else 1, reverse=True)
        
        # Distribuer alternativement
        for i, exercice_info in enumerate(exercices_avec_info):
            session_index = i % len(sessions_names)
            session_name = sessions_names[session_index]
            exercices_repartis[session_name].append(exercice_info)
    
    # Déterminer l'approche selon le nombre de jours
    approche_minimaliste = nb_jours <= 4
    max_exercices_par_session = 5 if approche_minimaliste else 6
    
    # Générer le programme pour chaque session
    for session_name, muscles_session in split.sessions.items():
        programme[session_name] = []
        exercices_ajoutes = 0
        
        volumes_session = volumes_par_session[session_name].copy()
        
        for exercice, muscles_communs, pattern, _ in exercices_repartis[session_name]:
            if exercices_ajoutes >= max_exercices_par_session:
                break
                
            muscles_session_communs = [m for m in muscles_communs if m in muscles_session]
            
            if not muscles_session_communs:
                continue
                
            volume_necessaire = max([volumes_session.get(m, 0) for m in muscles_session_communs])
            
            if volume_necessaire <= 0:
                continue
            
            # Adapter les séries selon l'approche
            if approche_minimaliste:
                volume_max_possible = min(4, max(3, volume_necessaire))
                volume_min = max(3, volume_max_possible - 1)
            else:
                volume_max_possible = min(3, max(2, volume_necessaire))
                volume_min = max(2, volume_max_possible - 1)
            
            volume_min = max(2, int(volume_min))
            volume_max_possible = max(volume_min, int(volume_max_possible))
            
            if volume_min == volume_max_possible:
                series_intervalle = str(volume_min)
            else:
                series_intervalle = f"{volume_min}-{volume_max_possible}"
            
            muscle_principal = muscles_session_communs[0] if muscles_session_communs else ""
            
            programme[session_name].append({
                "exercice": exercice,
                "series": series_intervalle,
                "muscles": [muscle_principal]
            })
            
            exercices_ajoutes += 1
            
            # Mettre à jour les volumes utilisés
            for muscle in muscles_session_communs:
                volumes_session[muscle] = max(0, volumes_session.get(muscle, 0) - volume_min)
    
    # Afficher le programme
    print_workout_program(programme, split.name, nb_jours)
    return programme

def print_workout_program(programme, split_name, nb_jours):
    """Affiche le programme d'entraînement dans le terminal"""
    
    print(f"\n=== PROGRAMME D'ENTRAINEMENT ===")
    print(f"Split: {split_name}")
    print(f"Nombre de jours: {nb_jours}")
    
    # Afficher l'organisation hebdomadaire selon le split
    if split_name == "Full Body" and nb_jours == 2:
        print("Organisation: Jour 1: Session A | Jour 2: Session B")
    elif split_name == "Full Body" and nb_jours == 3:
        print("Organisation: Jour 1: Session A | Jour 2: Session B | Jour 3: Session C")
    elif split_name == "Upper/Lower" and nb_jours == 4:
        print("Organisation: Jour 1: Upper A | Jour 2: Lower A | Jour 3: Upper B | Jour 4: Lower B")
    elif split_name == "Upper/Lower" and nb_jours == 5:
        print("Organisation: Jour 1: Upper A | Jour 2: Lower A | Jour 3: Upper B | Jour 4: Lower B | Jour 5: Upper A")
    elif split_name == "Push/Pull/Legs" and nb_jours == 6:
        print("Organisation: Jour 1: Push A | Jour 2: Pull A | Jour 3: Legs A | Jour 4: Push B | Jour 5: Pull B | Jour 6: Legs B")
    
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
            print(f"   Séries: {series}")
            print(f"   Muscles: {muscles}")
            print()
    
    print("=" * 40)

def create_complete_program(nb_jours):
    """Fonction principale utilisant la base de données centralisée"""
    
    objectifs_muscles = get_selected_muscle_goals()
    exercices_choisis = get_selected_exercises()
    
    if not objectifs_muscles:
        print("Aucun objectif muscle defini. Veuillez d'abord selectionner vos objectifs dans muscle.py")
        return None
        
    if not exercices_choisis:
        print("Aucun exercice selectionne. Veuillez d'abord choisir vos exercices dans exercise.py")
        return None
    
    # Générer le programme complet
    programme = generate_workout_program(nb_jours, objectifs_muscles, exercices_choisis, {})
    
    return programme