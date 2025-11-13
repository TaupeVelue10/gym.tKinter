"""
Générateur de programme d'entraînement basé sur une philosophie stricte :
1. Split selon jours : 2-3j=Full Body, 4-5j=Upper/Lower, 6j=Push/Pull/Legs
2. Volume hebdomadaire exact selon priorité (maintenance=4-6, normal=7-10, prioritised=11-13)
3. Les exercices peuvent être répétés plusieurs fois/semaine pour atteindre le volume
4. Le volume total est identique quel que soit le nb de jours (dépend uniquement du choix utilisateur)
5. Exercices répartis par ordre de priorité (polyarticulaires en premier)
6. Volume réparti uniformément entre les séances
7. Full Body : seulement UN tirage OU UN push par séance (pas horiz + vert)
8. N'utiliser que les exercices nécessaires pour atteindre le volume
"""
from version_site.core.exercise_database import get_exercise_info


# Volumes d'entraînement hebdomadaires selon objectif
VOLUME_OBJECTIFS = {
    "maintenance": [4, 5, 6],
    "normal_growth": [7, 8, 9, 10],
    "prioritised_growth": [11, 12, 13]
}


class Split:
    """Définit les splits d'entraînement"""
    def __init__(self, name, sessions):
        self.name = name
        self.sessions = sessions


def create_prog(nb_jours):
    """Crée le split approprié selon le nombre de jours"""
    if nb_jours in [2, 3]:
        return Split("Full Body", {
            "session_A": ["Pectoraux", "Epaules", "Dorsaux", "Biceps", "Triceps", 
                         "Abdominaux", "Quadriceps", "Isquios-jambiers", "Fessiers", "Lombaires"],
            "session_B": ["Pectoraux", "Epaules", "Dorsaux", "Biceps", "Triceps", 
                         "Abdominaux", "Quadriceps", "Isquios-jambiers", "Fessiers", "Lombaires"],
            "session_C": ["Pectoraux", "Epaules", "Dorsaux", "Biceps", "Triceps", 
                         "Abdominaux", "Quadriceps", "Isquios-jambiers", "Fessiers", "Lombaires"]
        })
    elif nb_jours in [4, 5]:
        return Split("Upper/Lower", {
            "upper_A": ["Pectoraux", "Epaules", "Dorsaux", "Biceps", "Triceps", "Abdominaux"],
            "lower_A": ["Quadriceps", "Isquios-jambiers", "Fessiers", "Lombaires"],
            "upper_B": ["Pectoraux", "Epaules", "Dorsaux", "Biceps", "Triceps", "Abdominaux"],
            "lower_B": ["Quadriceps", "Isquios-jambiers", "Fessiers", "Lombaires"]
        })
    elif nb_jours == 6:
        return Split("Push/Pull/Legs", {
            "push_A": ["Pectoraux", "Epaules", "Triceps", "Abdominaux"],
            "pull_A": ["Dorsaux", "Biceps"],
            "legs_A": ["Quadriceps", "Isquios-jambiers", "Fessiers", "Lombaires"],
            "push_B": ["Pectoraux", "Epaules", "Triceps", "Abdominaux"],
            "pull_B": ["Dorsaux", "Biceps"],
            "legs_B": ["Quadriceps", "Isquios-jambiers", "Fessiers", "Lombaires"]
        })
    else:
        raise ValueError(f"Nombre de jours non supporté: {nb_jours}")


def trier_exercices_par_priorite(exercices_choisis):
    """Trie les exercices par ordre de priorité : polys jambes, polys haut, isolations"""
    polys_jambes = []
    polys_haut = []
    isolations = []
    
    for exo_name in exercices_choisis:
        info = get_exercise_info(exo_name)
        if not info:
            continue
        
        if info['type'] == 'polyarticulaire':
            if info['category'] == 'legs':
                polys_jambes.append(exo_name)
            else:
                polys_haut.append(exo_name)
        else:
            isolations.append(exo_name)
    
    return polys_jambes + polys_haut + isolations


def calculer_volume_hebdomadaire(objectifs_muscles):
    """Calcule le volume hebdomadaire cible pour chaque muscle"""
    volumes = {}
    for muscle, objectif in objectifs_muscles.items():
        volume_range = VOLUME_OBJECTIFS[objectif]
        volumes[muscle] = volume_range[len(volume_range) // 2]
    return volumes


def selectionner_exercices_necessaires(exercices_choisis, volumes_hebdo, split):
    """Sélectionne uniquement les exercices nécessaires pour atteindre le volume"""
    exercices_tries = trier_exercices_par_priorite(exercices_choisis)
    allocation = {}
    
    for muscle, volume_cible in volumes_hebdo.items():
        allocation[muscle] = []
        
        # Trouver exercices avec ce muscle comme primaire
        exercices_muscle = []
        for exo_name in exercices_tries:
            info = get_exercise_info(exo_name)
            if info and muscle in info.get('primary_muscles', []):
                exercices_muscle.append(exo_name)
        
        if not exercices_muscle:
            continue
        
        # Calculer combien d'apparitions totales nécessaires
        # Avec des séries de 2-4, moyenne = 3 séries par apparition
        series_par_apparition = 3.0
        total_apparitions_necessaires = int(volume_cible / series_par_apparition + 0.99)  # Arrondir vers le haut
        
        # Limiter le nombre d'apparitions selon le nombre de sessions disponibles
        # Pour Full Body 2j: max 2 apparitions, 3j: max 3, etc.
        nb_sessions = len(split.sessions)
        total_apparitions_necessaires = min(total_apparitions_necessaires, nb_sessions)
        
        # Distribuer les apparitions sur les exercices disponibles
        nb_exercices = len(exercices_muscle)
        
        if nb_exercices == 0:
            continue
        
        # Stratégie : répartir équitablement sur les exercices, max 3 apparitions par exercice
        apparitions_restantes = total_apparitions_necessaires
        
        for i, exo_name in enumerate(exercices_muscle):
            if apparitions_restantes <= 0:
                break
            
            # Calculer combien d'apparitions pour cet exercice
            exos_restants = nb_exercices - i
            # Distribuer équitablement le reste, max 3 par exercice
            nb_apparitions = min(3, max(1, int((apparitions_restantes + exos_restants - 1) / exos_restants)))
            
            if nb_apparitions > 0:
                allocation[muscle].append((exo_name, nb_apparitions))
                apparitions_restantes -= nb_apparitions
    
    return allocation


def repartir_exercices_full_body(allocation_exercices, volumes_hebdo, nb_jours):
    """Répartit les exercices sur les séances Full Body"""
    nb_sessions = min(nb_jours, 3)
    sessions = {f"session_{chr(65+i)}": [] for i in range(nb_sessions)}
    volumes_par_session = {s: 0 for s in sessions.keys()}
    patterns_utilises = {s: set() for s in sessions.keys()}
    exercices_par_session = {s: set() for s in sessions.keys()}
    
    # Créer une file d'attente de toutes les "apparitions" d'exercices
    apparitions = []
    for muscle, exercices_list in allocation_exercices.items():
        for exo_name, nb_apparitions in exercices_list:
            info = get_exercise_info(exo_name)
            if not info:
                continue
            
            # Ajouter chaque apparition séparément
            for _ in range(nb_apparitions):
                apparitions.append((exo_name, muscle, info))
    
    # Trier les apparitions (polyarticulaires jambes en premier)
    apparitions.sort(key=lambda x: (
        0 if x[2]['type'] == 'polyarticulaire' and x[2]['category'] == 'legs' else
        1 if x[2]['type'] == 'polyarticulaire' else 2
    ))
    
    # Distribuer chaque apparition
    for exo_name, muscle, info in apparitions:
        pattern = info['pattern']
        session_choisie = None
        min_volume = float('inf')
        
        for session_name in sessions.keys():
            # RÈGLE 1: Ne jamais répéter un exercice dans la même session
            if exo_name in exercices_par_session[session_name]:
                continue
            
            # RÈGLE 2: Contrainte Full Body - UN SEUL mouvement de push ET UN SEUL mouvement de pull
            # On peut avoir 1 push + 1 pull dans la même séance
            # Mais PAS 2 push différents (ex: pas Horizontal Push + Vertical Push)
            # Et PAS 2 pull différents (ex: pas Horizontal Pull + Vertical Pull)
            if pattern in ['Horizontal Push (Chest)', 'Vertical Push', 'Incline Push']:
                # C'est un push - vérifier qu'il n'y a pas déjà un AUTRE pattern de push
                push_patterns = {'Horizontal Push (Chest)', 'Vertical Push', 'Incline Push'}
                patterns_push_dans_session = push_patterns & patterns_utilises[session_name]
                if patterns_push_dans_session and pattern not in patterns_push_dans_session:
                    # Il y a déjà un push différent dans cette session
                    continue
            elif pattern in ['Horizontal Pull', 'Vertical Pull']:
                # C'est un pull - vérifier qu'il n'y a pas déjà un AUTRE pattern de pull
                pull_patterns = {'Horizontal Pull', 'Vertical Pull'}
                patterns_pull_dans_session = pull_patterns & patterns_utilises[session_name]
                if patterns_pull_dans_session and pattern not in patterns_pull_dans_session:
                    # Il y a déjà un pull différent dans cette session
                    continue
            
            # Choisir session avec moins de volume
            if volumes_par_session[session_name] < min_volume:
                min_volume = volumes_par_session[session_name]
                session_choisie = session_name
        
        # Si aucune session ne respecte les contraintes, ignorer cette apparition
        # (cela peut arriver si on demande trop d'apparitions pour le nb de jours)
        if session_choisie is None:
            continue
        
        # Ajouter l'exercice
        series = "3-4" if info['type'] == 'polyarticulaire' else "2-3"
        sessions[session_choisie].append({
            "exercice": exo_name,
            "series": series,
            "muscles": [muscle]
        })
        
        patterns_utilises[session_choisie].add(pattern)
        exercices_par_session[session_choisie].add(exo_name)
        volumes_par_session[session_choisie] += 3.5
    
    # Trier (polyarticulaires en premier)
    for session_name in sessions.keys():
        sessions[session_name].sort(key=lambda x: (
            0 if get_exercise_info(x['exercice'])['type'] == 'polyarticulaire' else 1,
            0 if get_exercise_info(x['exercice'])['category'] == 'legs' else 1
        ))
    
    return sessions


def repartir_exercices_upper_lower(allocation_exercices, volumes_hebdo, nb_jours):
    """Répartit les exercices sur les séances Upper/Lower"""
    sessions = {
        "upper_A": [],
        "lower_A": [],
        "upper_B": [],
        "lower_B": []
    }
    volumes_par_session = {s: 0 for s in sessions.keys()}
    exercices_par_session = {s: set() for s in sessions.keys()}
    
    # Créer une file d'attente de toutes les apparitions
    apparitions = []
    for muscle, exercices_list in allocation_exercices.items():
        for exo_name, nb_apparitions in exercices_list:
            info = get_exercise_info(exo_name)
            if not info:
                continue
            
            # Ajouter chaque apparition séparément
            for _ in range(nb_apparitions):
                apparitions.append((exo_name, muscle, info))
    
    # Trier les apparitions (polyarticulaires en premier)
    apparitions.sort(key=lambda x: (
        0 if x[2]['type'] == 'polyarticulaire' and x[2]['category'] == 'legs' else
        1 if x[2]['type'] == 'polyarticulaire' else 2
    ))
    
    # Distribuer chaque apparition
    for exo_name, muscle, info in apparitions:
        if info['category'] in ['push', 'pull', 'core']:
            sessions_cibles = ['upper_A', 'upper_B']
        else:
            sessions_cibles = ['lower_A', 'lower_B']
        
        # Trouver session qui n'a pas encore cet exercice et a le moins de volume
        session_choisie = None
        min_volume = float('inf')
        
        for s in sessions_cibles:
            if exo_name not in exercices_par_session[s]:
                if volumes_par_session[s] < min_volume:
                    min_volume = volumes_par_session[s]
                    session_choisie = s
        
        # Si l'exercice est déjà dans toutes les sessions, ignorer cette apparition
        if session_choisie is None:
            continue
        
        series = "3-4" if info['type'] == 'polyarticulaire' else "2-3"
        sessions[session_choisie].append({
            "exercice": exo_name,
            "series": series,
            "muscles": [muscle]
        })
        
        exercices_par_session[session_choisie].add(exo_name)
        volumes_par_session[session_choisie] += 3.5
    
    for session_name in sessions.keys():
        sessions[session_name].sort(key=lambda x: (
            0 if get_exercise_info(x['exercice'])['type'] == 'polyarticulaire' else 1
        ))
    
    return sessions


def repartir_exercices_ppl(allocation_exercices, volumes_hebdo):
    """Répartit les exercices sur les séances Push/Pull/Legs"""
    sessions = {
        "push_A": [],
        "pull_A": [],
        "legs_A": [],
        "push_B": [],
        "pull_B": [],
        "legs_B": []
    }
    volumes_par_session = {s: 0 for s in sessions.keys()}
    exercices_par_session = {s: set() for s in sessions.keys()}
    
    # Créer une file d'attente de toutes les apparitions
    apparitions = []
    for muscle, exercices_list in allocation_exercices.items():
        for exo_name, nb_apparitions in exercices_list:
            info = get_exercise_info(exo_name)
            if not info:
                continue
            
            # Ajouter chaque apparition séparément
            for _ in range(nb_apparitions):
                apparitions.append((exo_name, muscle, info))
    
    # Trier les apparitions (polyarticulaires en premier)
    apparitions.sort(key=lambda x: (
        0 if x[2]['type'] == 'polyarticulaire' and x[2]['category'] == 'legs' else
        1 if x[2]['type'] == 'polyarticulaire' else 2
    ))
    
    # Distribuer chaque apparition
    for exo_name, muscle, info in apparitions:
        if info['category'] == 'push' or info['category'] == 'core':
            sessions_cibles = ['push_A', 'push_B']
        elif info['category'] == 'pull':
            sessions_cibles = ['pull_A', 'pull_B']
        else:
            sessions_cibles = ['legs_A', 'legs_B']
        
        # Trouver session qui n'a pas encore cet exercice et a le moins de volume
        session_choisie = None
        min_volume = float('inf')
        
        for s in sessions_cibles:
            if exo_name not in exercices_par_session[s]:
                if volumes_par_session[s] < min_volume:
                    min_volume = volumes_par_session[s]
                    session_choisie = s
        
        # Si l'exercice est déjà dans toutes les sessions, ignorer cette apparition
        if session_choisie is None:
            continue
        
        series = "3-4" if info['type'] == 'polyarticulaire' else "2-3"
        sessions[session_choisie].append({
            "exercice": exo_name,
            "series": series,
            "muscles": [muscle]
        })
        
        exercices_par_session[session_choisie].add(exo_name)
        volumes_par_session[session_choisie] += 3.5
    
    for session_name in sessions.keys():
        sessions[session_name].sort(key=lambda x: (
            0 if get_exercise_info(x['exercice'])['type'] == 'polyarticulaire' else 1
        ))
    
    return sessions


def ajuster_volumes_exacts(programme, volumes_hebdo):
    """Ajuste les séries pour atteindre exactement les volumes cibles"""
    MAX_ITERATIONS = 10
    
    for iteration in range(MAX_ITERATIONS):
        # Calculer volume actuel par muscle
        volumes_actuels = {}
        exercices_par_muscle = {}
        
        for session_name, exercices in programme.items():
            for exo in exercices:
                muscle = exo['muscles'][0]
                series_str = exo['series']
                
                if '-' in series_str:
                    min_s, max_s = map(int, series_str.split('-'))
                    avg = (min_s + max_s) / 2.0
                else:
                    avg = float(series_str)
                
                volumes_actuels[muscle] = volumes_actuels.get(muscle, 0) + avg
                
                if muscle not in exercices_par_muscle:
                    exercices_par_muscle[muscle] = []
                exercices_par_muscle[muscle].append((session_name, exo))
        
        # Vérifier convergence
        tout_bon = True
        
        # Ajuster chaque muscle
        for muscle, volume_cible in volumes_hebdo.items():
            volume_actuel = volumes_actuels.get(muscle, 0)
            diff = volume_cible - volume_actuel
            
            if abs(diff) < 0.1:
                continue
            
            tout_bon = False
            
            if muscle not in exercices_par_muscle:
                continue
            
            exos = exercices_par_muscle[muscle]
            nb_exos = len(exos)
            
            # Calculer l'ajustement total nécessaire
            series_totales_a_ajuster = abs(diff)
            
            # Distribuer l'ajustement sur tous les exercices
            for idx, (session_name, exo) in enumerate(exos):
                series_str = exo['series']
                
                if '-' in series_str:
                    min_s, max_s = map(int, series_str.split('-'))
                else:
                    min_s = max_s = int(series_str)
                
                # Part de l'ajustement pour cet exercice
                ajustement = series_totales_a_ajuster / nb_exos
                
                if diff > 0:
                    # Augmenter
                    # Stratégie: augmenter le max et parfois le min
                    if ajustement >= 1.5:
                        # Grosse augmentation nécessaire
                        new_max = 5
                        new_min = min(5, max(2, min_s + int(ajustement / 2)))
                    elif ajustement >= 0.8:
                        # Augmentation moyenne
                        new_max = min(5, max_s + 1)
                        new_min = max(2, min(new_max, min_s))
                    else:
                        # Petite augmentation
                        new_max = min(5, max_s + 1)
                        new_min = min_s
                else:
                    # Diminuer
                    # Stratégie: diminuer le min et parfois le max
                    if ajustement >= 1.5:
                        new_min = 2
                        new_max = max(2, min(5, max_s - int(ajustement / 2)))
                    elif ajustement >= 0.8:
                        new_min = max(2, min_s - 1)
                        new_max = max(new_min, min(5, max_s))
                    else:
                        new_min = max(2, min_s - 1)
                        new_max = max_s
                
                # Mettre à jour
                if new_min == new_max:
                    exo['series'] = str(new_max)
                else:
                    exo['series'] = f"{new_min}-{new_max}"
        
        if tout_bon:
            break


def generate_workout_program(nb_jours, objectifs_muscles, exercices_choisis, pattern_muscles=None):
    """Génère un programme d'entraînement complet"""
    split = create_prog(nb_jours)
    volumes_hebdo = calculer_volume_hebdomadaire(objectifs_muscles)
    allocation = selectionner_exercices_necessaires(exercices_choisis, volumes_hebdo, split)
    
    if split.name == "Full Body":
        programme = repartir_exercices_full_body(allocation, volumes_hebdo, nb_jours)
    elif split.name == "Upper/Lower":
        programme = repartir_exercices_upper_lower(allocation, volumes_hebdo, nb_jours)
    else:
        programme = repartir_exercices_ppl(allocation, volumes_hebdo)
    
    ajuster_volumes_exacts(programme, volumes_hebdo)
    
    return programme


def create_complete_program(nb_jours, objectifs_muscles, exercices_choisis):
    """Fonction wrapper pour l'application web"""
    split = create_prog(nb_jours)
    programme = generate_workout_program(nb_jours, objectifs_muscles, exercices_choisis)
    sessions_order = list(split.sessions.keys())
    
    return programme, split.name, sessions_order


if __name__ == "__main__":
    print("Test du générateur de programme\n")
    
    sample_exercices = [
        'Bench press', 'Overhead press', 'Bent over row', 'Pull up',
        'Barbell squat', 'Stiff leg deadlift', 'Curl', 'Pushdown',
        'Lateral raises', 'Machine ab crunch'
    ]
    
    sample_objectifs = {
        'Pectoraux': 'normal_growth',
        'Epaules': 'normal_growth',
        'Dorsaux': 'normal_growth',
        'Biceps': 'prioritised_growth',
        'Triceps': 'normal_growth',
        'Quadriceps': 'normal_growth',
        'Isquios-jambiers': 'maintenance',
        'Abdominaux': 'maintenance'
    }
    
    for jours in [2, 3, 4, 5, 6]:
        print(f"\n{'='*60}")
        print(f"Programme {jours} jours/semaine")
        print('='*60)
        
        prog, split_name, order = create_complete_program(jours, sample_objectifs, sample_exercices)
        
        print(f"Split: {split_name}")
        print(f"Sessions: {order}\n")
        
        for session_name in order:
            if session_name not in prog or not prog[session_name]:
                continue
            print(f"\n{session_name.upper()}:")
            for exo in prog[session_name]:
                print(f"  - {exo['exercice']}: {exo['series']} séries ({exo['muscles']})")
        
        print("\nVérification volumes hebdomadaires:")
        volumes = {}
        for session_name, exercices in prog.items():
            for exo in exercices:
                muscle = exo['muscles'][0]
                series = exo['series']
                if '-' in series:
                    min_s, max_s = map(int, series.split('-'))
                    avg = (min_s + max_s) / 2
                else:
                    avg = float(series)
                volumes[muscle] = volumes.get(muscle, 0) + avg
        
        for muscle, vol in sorted(volumes.items()):
            objectif = sample_objectifs.get(muscle, 'N/A')
            if objectif != 'N/A':
                cible = calculer_volume_hebdomadaire({muscle: objectif})[muscle]
                print(f"  {muscle}: {vol:.1f} séries (cible: {cible})")
