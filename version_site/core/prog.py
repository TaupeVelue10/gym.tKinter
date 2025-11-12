"""
Port of the Tkinter `prog.py` logic adapted for the web app.
Exposes create_complete_program(nb_jours, objectifs_muscles, exercices_choisis)
which returns (programme_by_session, split_name, sessions_order).
"""
from version_site.core.exercise_database import get_exercise_info, get_exercises_by_muscle, is_isolation


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
    else:
        prog = full_body
    
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
            
        exercice_info = (exercice_name, info.get("all_muscles", []), info.get("pattern"), info.get("type"))
        
        if info.get("category") == "push" or info.get("category") == "core":
            exercices_push.append(exercice_info)
        elif info.get("category") == "pull":
            exercices_pull.append(exercice_info)
        elif info.get("category") == "legs":
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
    """Génère un programme d'entraînement basé sur la base de données centralisée (port exact du Tkinter)
    Retourne un dict mapping session_name -> list of exercise dicts
    """
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
                # Diviser le volume entre les sessions
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
        # Pour Full Body, répartition intelligente avec priorité aux gros mouvements jambes
        exercices_repartis = {session: [] for session in sessions_names}
        
        # Séparer les exercices par catégorie
        exercices_legs_poly = []  # Polyarticulaires jambes (squat, deadlift, etc.)
        exercices_upper_poly = []  # Polyarticulaires haut du corps
        exercices_isolation = []   # Tous les exercices d'isolation
        
        for exercice_name in exercices_choisis:
            info = get_exercise_info(exercice_name)
            if info:
                exercice_info = (exercice_name, info["all_muscles"], info["pattern"], info["type"])
                category = info.get("category", "")
                ex_type = info.get("type", "")
                
                # Classifier les exercices
                if category == "legs" and ex_type == "polyarticulaire":
                    exercices_legs_poly.append(exercice_info)
                elif ex_type == "polyarticulaire":
                    exercices_upper_poly.append(exercice_info)
                else:
                    exercices_isolation.append(exercice_info)
        
        # Combiner dans l'ordre optimal : legs poly d'abord, puis upper poly, puis isolation
        exercices_avec_info = exercices_legs_poly + exercices_upper_poly + exercices_isolation
        
        # Distribuer alternativement entre les sessions
        for i, exercice_info in enumerate(exercices_avec_info):
            session_index = i % len(sessions_names)
            session_name = sessions_names[session_index]
            exercices_repartis[session_name].append(exercice_info)
    
    # Déterminer l'approche selon le nombre de jours
    approche_minimaliste = nb_jours <= 4
    # Pour Full Body (2-3 jours), limiter les exercices par session pour forcer la distribution
    if nb_jours <= 3:
        max_exercices_par_session = 5  # Réduit de 7 à 5 pour forcer variation entre sessions
    elif approche_minimaliste:
        max_exercices_par_session = 6
    else:
        max_exercices_par_session = 6
    
    # Générer le programme pour chaque session
    # tracker d'utilisation globale des exercices pour éviter de dupliquer les mêmes exercices
    exercices_usage = {name: 0 for name in exercices_choisis}
    # Tracker du volume total déjà assigné pour chaque muscle (toutes sessions confondues)
    volumes_assignes_total = {muscle: 0 for muscle in volumes_hebdomadaires.keys()}

    for session_name, muscles_session in split.sessions.items():
        programme[session_name] = []
        exercices_ajoutes = 0
        
        volumes_session = volumes_par_session[session_name].copy()
        
        # Première passe: identifier quels exercices peuvent être utilisés dans cette session
        exercices_disponibles = []
        for exercice_name in exercices_choisis:
            info = get_exercise_info(exercice_name)
            if not info:
                continue
            # IMPORTANT: Utiliser uniquement les muscles PRIMAIRES pour le volume
            muscles_primaires = info.get("primary_muscles", [])
            muscles_communs = [m for m in muscles_primaires if m in muscles_session]
            if muscles_communs:
                exercices_disponibles.append((exercice_name, muscles_communs, info["pattern"], info["type"]))
        
        # Trier par priorité (polyarticulaires d'abord, puis par catégorie pour Full Body)
        if split.name == "Full Body":
            def sort_key(ex_info):
                ex_name, muscles, pattern, ex_type = ex_info
                info = get_exercise_info(ex_name)
                category = info.get("category", "")
                # Ordre: legs poly (3), upper poly (2), isolation (1)
                if category == "legs" and ex_type == "polyarticulaire":
                    return 3
                elif ex_type == "polyarticulaire":
                    return 2
                else:
                    return 1
            exercices_disponibles.sort(key=sort_key, reverse=True)
        elif split.name == "Upper/Lower":
            # Pour Upper/Lower: legs en premier dans sessions lower, polyarticulaires d'abord partout
            def sort_key_ul(ex_info):
                ex_name, muscles, pattern, ex_type = ex_info
                info = get_exercise_info(ex_name)
                category = info.get("category", "")
                is_lower_session = "lower" in session_name.lower()
                
                # Dans sessions lower: legs poly (4), legs iso (3), autres (1-2)
                # Dans sessions upper: upper poly (3), upper iso (2), legs (1)
                if is_lower_session:
                    if category == "legs" and ex_type == "polyarticulaire":
                        return 4
                    elif category == "legs":
                        return 3
                    elif ex_type == "polyarticulaire":
                        return 2
                    else:
                        return 1
                else:
                    if ex_type == "polyarticulaire" and category != "legs":
                        return 3
                    elif category != "legs":
                        return 2
                    else:
                        return 1
            exercices_disponibles.sort(key=sort_key_ul, reverse=True)
        else:
            # Pour autres splits, polyarticulaires d'abord
            exercices_disponibles.sort(key=lambda x: 2 if x[3] == "polyarticulaire" else 1, reverse=True)
        
        # Deuxième passe: ajouter des exercices jusqu'à atteindre les volumes cibles
        exercices_utilises_dans_session = set()
        
        while exercices_ajoutes < max_exercices_par_session:
            meilleur_exercice = None
            meilleur_score = -float('inf')
            meilleur_muscle = None
            
            # Trouver le meilleur exercice à ajouter pour combler les volumes manquants
            for exercice_name, muscles_communs, pattern, ex_type in exercices_disponibles:
                # Calculer le score de cet exercice (basé sur le volume manquant des muscles qu'il travaille)
                muscle_principal = muscles_communs[0] if muscles_communs else None
                if not muscle_principal:
                    continue
                
                volume_manquant = volumes_session.get(muscle_principal, 0)
                
                # Pour Full Body: éviter la répétition sauf si nécessaire
                if split.name == "Full Body":
                    # Si l'exercice a déjà été utilisé cette semaine
                    usage_count = exercices_usage.get(exercice_name, 0)
                    if usage_count > 0:
                        # Calculer le volume hebdomadaire total nécessaire pour ce muscle
                        volume_hebdo_muscle = volumes_hebdomadaires.get(muscle_principal, 0)
                        
                        # Simple: limiter à 2 utilisations max pour muscles normaux, 3 pour prioritaires
                        if volume_hebdo_muscle > 10:  # Muscle prioritaire
                            if usage_count >= 3:
                                continue  # Max 3 utilisations pour prioritaires
                        else:  # Muscle normal
                            if usage_count >= 2:
                                continue  # Max 2 utilisations pour normaux
                
                # Bonus si l'exercice n'a pas encore été utilisé dans cette session
                bonus = 2 if exercice_name not in exercices_utilises_dans_session else 0
                # Pénalité si l'exercice a déjà été assigné cette semaine
                if split.name == "Full Body":
                    # Pénalité calibrée pour volumes_par_session divisés (ex: ~2.67 pour 3 jours)
                    # Avec volume_manquant ~2-3 et bonus 2:
                    # - usage=0: score = 2-3 + 0-2 = 0-3 (bon)
                    # - usage=1: score = 2-3 + 0-2 - 3 = -3 à -1 (bloqué dans la plupart des cas)
                    # Cela force la variation sauf quand absolument nécessaire
                    usage_penalty = exercices_usage.get(exercice_name, 0) * 3
                else:
                    usage_penalty = exercices_usage.get(exercice_name, 0) * 3
                
                # Score combine volume manquant, bonus pour nouveauté et pénalité d'usage
                score = max(0, volume_manquant) + bonus - usage_penalty
                
                if score > meilleur_score and volume_manquant > 0:
                    meilleur_score = score
                    meilleur_exercice = (exercice_name, muscles_communs, pattern, ex_type)
                    meilleur_muscle = muscle_principal
            
            # Si aucun exercice n'est trouvé, on arrête
            if not meilleur_exercice:
                break
            
            exercice_name, muscles_communs, pattern, ex_type = meilleur_exercice
            muscle_principal = meilleur_muscle
            
            # Calculer le nombre de séries pour cet exercice
            volume_muscle_principal = volumes_session.get(muscle_principal, 0)
            
            # IMPORTANT: Limiter les séries par exercice pour forcer la répartition sur plusieurs jours
            # Maximum 4 séries par exercice dans une session (au lieu de 6)
            max_series_par_exercice = 4
            
            # Jusqu'à 4 séries par exercice pour forcer répartition, avec calcul intelligent
            if approche_minimaliste:
                # Pour 2-4 jours: 3-4 séries par exercice max
                if volume_muscle_principal > 3.5:
                    volume_max_possible = min(max_series_par_exercice, max(3, int(volume_muscle_principal + 0.5)))
                    volume_min = max(3, min(volume_max_possible, int(volume_muscle_principal * 0.90)))
                else:
                    volume_max_possible = min(max_series_par_exercice, max(2, int(volume_muscle_principal + 0.9)))
                    volume_min = max(2, min(volume_max_possible - 1, int(volume_muscle_principal * 0.85)))
            else:
                # Pour 5-6 jours: 2-4 séries par exercice max
                if volume_muscle_principal > 3:
                    volume_max_possible = min(max_series_par_exercice, max(3, int(volume_muscle_principal + 0.5)))
                    volume_min = max(2, min(volume_max_possible, int(volume_muscle_principal * 0.90)))
                else:
                    volume_max_possible = min(max_series_par_exercice, max(2, int(volume_muscle_principal + 0.9)))
                    volume_min = max(2, min(volume_max_possible - 1, int(volume_muscle_principal * 0.85)))
            
            # S'assurer que min <= max
            volume_min = max(2, min(volume_min, volume_max_possible))
            volume_max_possible = max(volume_min, volume_max_possible)
            
            if volume_min == volume_max_possible:
                series_intervalle = str(volume_min)
            else:
                series_intervalle = f"{volume_min}-{volume_max_possible}"
            
            programme[session_name].append({
                "exercice": exercice_name,
                "series": series_intervalle,
                "muscles": [muscle_principal]
            })
            
            # marquer l'exercice comme utilisé cette semaine
            exercices_usage[exercice_name] = exercices_usage.get(exercice_name, 0) + 1

            exercices_ajoutes += 1
            exercices_utilises_dans_session.add(exercice_name)
            
            # Mettre à jour les volumes utilisés
            series_utilisees = (volume_min + volume_max_possible) / 2
            for muscle in muscles_communs:
                volumes_session[muscle] = max(0, volumes_session.get(muscle, 0) - series_utilisees)
                # Mettre à jour le volume total assigné pour ce muscle (global)
                volumes_assignes_total[muscle] = volumes_assignes_total.get(muscle, 0) + series_utilisees
    
    # Post-processing adjustments
    def _ensure_arm_isolations(programme, exercices_choisis):
        """Ensure at least one isolation for Biceps/Triceps is present in the week's programme
        if the user selected such muscles with a non-zero volume. This tries to insert an
        available isolation exercise if it wasn't allocated by the main distribution.
        """
        # collect assigned exercises
        assigned = set()
        for sess_exs in programme.values():
            for e in sess_exs:
                assigned.add(e["exercice"]) if isinstance(e, dict) else assigned.add(e[0])

        # helper to find available isolation for a muscle from user's chosen pool
        def find_isolation(muscle):
            # prefer chosen exercises
            for name in exercices_choisis:
                info = get_exercise_info(name)
                if not info:
                    continue
                if muscle in info.get('all_muscles', []) and info.get('type') == 'isolation' and name not in assigned:
                    return name
            # fallback: search DB for an isolation for this muscle
            for name in get_exercises_by_muscle(muscle):
                if name in assigned:
                    continue
                if is_isolation(name):
                    return name
            return None

        # ensure for each session that targets biceps/triceps we have an isolation at least once per week
        needs = ['Biceps', 'Triceps']
        for muscle in needs:
            # check if muscle has any isolation already assigned
            has_iso = any((get_exercise_info(e['exercice']) and muscle in get_exercise_info(e['exercice']).get('all_muscles', []) and get_exercise_info(e['exercice']).get('type') == 'isolation')
                          for sess in programme.values() for e in sess)
            if not has_iso:
                candidate = find_isolation(muscle)
                if candidate:
                    # place candidate into the session that targets this muscle and has room, else replace last
                    placed = False
                    for session_name, sess_exs in programme.items():
                        # find session muscles from split is not available here; try to detect by checking muscles in exercises
                        # prefer sessions that already include poly exercises for same muscle
                        for i, e in enumerate(sess_exs):
                            info = get_exercise_info(e['exercice']) if isinstance(e, dict) else get_exercise_info(e[0])
                            if not info:
                                continue
                            if muscle in info.get('all_muscles', []):
                                # insert candidate after this exercise
                                sess_exs.insert(i+1, {"exercice": candidate, "series": "2-3", "muscles": [muscle]})
                                placed = True
                                break
                        if placed:
                            break
                    if not placed:
                        # fallback: append to the first session
                        first = next(iter(programme))
                        programme[first].append({"exercice": candidate, "series": "2-3", "muscles": [muscle]})

    def _balance_vertical_push_for_two_days(programme, nb_jours, exercices_choisis):
        """If nb_jours == 2, ensure there is at least one Vertical Push in the two sessions.
        If both sessions use Horizontal Push (e.g., Bench + Dips), try to replace one by an
        available Vertical Push (prefer from user choices, else from DB).
        """
        if nb_jours != 2:
            return

        # detect if any vertical push already present
        def is_vertical_push(ex):
            info = get_exercise_info(ex['exercice']) if isinstance(ex, dict) else get_exercise_info(ex[0])
            return info and info.get('pattern') == 'Vertical Push'

        any_vertical = any(is_vertical_push(e) for sess in programme.values() for e in sess)
        if any_vertical:
            return

        # find candidate vertical push: prefer chosen exercises
        candidate = None
        for name in exercices_choisis:
            info = get_exercise_info(name)
            if info and info.get('pattern') == 'Vertical Push':
                candidate = name
                break
        # else search DB for common vertical push
        if not candidate:
            # common vertical push exercise name
            for name in ('Overhead press', 'Seated overhead press', 'Push press'):
                info = get_exercise_info(name)
                if info and info.get('pattern') == 'Vertical Push':
                    candidate = name
                    break

        if not candidate:
            return

        # find a horizontal push to replace: look for exercise with pattern containing 'Horizontal Push' or 'Chest'
        replaced = False
        for session_name, sess_exs in programme.items():
            for i, e in enumerate(sess_exs):
                info = get_exercise_info(e['exercice']) if isinstance(e, dict) else get_exercise_info(e[0])
                if not info:
                    continue
                if info.get('pattern') and ('Horizontal Push' in info.get('pattern') or 'Chest' in info.get('pattern')):
                    # replace this exercise with candidate
                    sess_exs[i] = {"exercice": candidate, "series": "3-5", "muscles": [m for m in get_exercise_info(candidate).get('all_muscles', [])][:1]}
                    replaced = True
                    break
            if replaced:
                break

    def _redistribute_verticals(programme):
        """If a session contains multiple non-vertical push poly exercises (e.g., Bench + Incline)
        and another session contains a Vertical Push, swap one non-vertical with that Vertical Push
        so vertical pressing is distributed across days.
        """
        # collect verticals and their locations
        vertical_locations = []  # list of (session_name, index, ex_name)
        for session_name, sess_exs in programme.items():
            for idx, e in enumerate(sess_exs):
                ex_name = e['exercice'] if isinstance(e, dict) else e[0]
                info = get_exercise_info(ex_name)
                if not info:
                    continue
                pattern = info.get('pattern', '')
                if 'Vertical' in pattern:
                    vertical_locations.append((session_name, idx, ex_name))

        if not vertical_locations:
            return

        # for each session, detect non-vertical push polys
        for session_name, sess_exs in programme.items():
            non_vertical_push_indices = []
            for idx, e in enumerate(sess_exs):
                ex_name = e['exercice'] if isinstance(e, dict) else e[0]
                info = get_exercise_info(ex_name)
                if not info:
                    continue
                if info.get('category') == 'push' and info.get('type') == 'polyarticulaire' and 'Vertical' not in info.get('pattern', ''):
                    non_vertical_push_indices.append((idx, ex_name, info.get('pattern', '')))

            # if the session has 2 or more non-vertical push polys, try to swap one with a vertical from another session
            if len(non_vertical_push_indices) >= 2:
                # prefer to replace an Incline pattern if present
                target_idx = None
                for idx, name, pattern in non_vertical_push_indices:
                    if 'Incline' in pattern or 'Incline' in name:
                        target_idx = idx
                        break
                if target_idx is None:
                    # just pick the later push (to preserve primary exercise order)
                    target_idx = non_vertical_push_indices[-1][0]

                # find a vertical in a different session
                for v_session, v_idx, v_name in vertical_locations:
                    if v_session == session_name:
                        continue
                    # perform swap: replace target in current session with vertical, and replace vertical in other session with the original
                    original = sess_exs[target_idx]
                    # find and replace the vertical in its session
                    other_sess = programme[v_session]
                    other_sess[v_idx] = original
                    sess_exs[target_idx] = {"exercice": v_name, "series": "3-5", "muscles": [m for m in get_exercise_info(v_name).get('all_muscles', [])][:1]}
                    # update vertical_locations so we don't reuse same vertical
                    vertical_locations = [vl for vl in vertical_locations if not (vl[0] == v_session and vl[1] == v_idx)]
                    break

    # Run post-processing
    try:
        _ensure_arm_isolations(programme, exercices_choisis)
    except Exception:
        pass
    try:
        _balance_vertical_push_for_two_days(programme, nb_jours, exercices_choisis)
    except Exception:
        pass

    # Final safeguard: remove duplicate exercises within each session (preserve order)
    for session_name, sess_exs in programme.items():
        seen_names = set()
        new_list = []
        for e in sess_exs:
            name = e.get('exercice') if isinstance(e, dict) else (e[0] if isinstance(e, tuple) else str(e))
            if name in seen_names:
                continue
            seen_names.add(name)
            new_list.append(e)
        programme[session_name] = new_list
    
    # NOUVEAU: Ajuster les volumes pour garantir l'atteinte des objectifs hebdomadaires
    def _adjust_volumes_to_targets(programme, objectifs_muscles, volumes_hebdomadaires, exercices_choisis, split):
        """Ajuste les séries pour garantir que le volume total hebdomadaire atteint exactement la cible."""
        # Calculer le volume réel actuel pour chaque muscle
        volumes_actuels = {}
        exercices_par_muscle = {}  # Pour savoir quels exercices travaillent quel muscle
        
        for session_name, exercices in programme.items():
            for exo in exercices:
                muscles = exo.get('muscles', [])
                series_range = exo.get('series', '3')
                
                # Calculer le volume moyen
                if '-' in str(series_range):
                    min_s, max_s = map(int, series_range.split('-'))
                    series_avg = (min_s + max_s) / 2
                else:
                    series_avg = float(series_range)
                
                for muscle in muscles:
                    volumes_actuels[muscle] = volumes_actuels.get(muscle, 0) + series_avg
                    if muscle not in exercices_par_muscle:
                        exercices_par_muscle[muscle] = []
                    exercices_par_muscle[muscle].append((session_name, exo))
        
        # Pour chaque muscle avec un objectif, ajuster les séries si nécessaire
        for muscle, volume_cible in volumes_hebdomadaires.items():
            volume_actuel = volumes_actuels.get(muscle, 0)
            diff = volume_cible - volume_actuel
            
            # Toujours ajuster pour atteindre exactement la cible (ou très proche)
            if abs(diff) < 0.3:
                # Volume quasi parfait, on laisse
                continue
            
            # Ajuster les séries des exercices qui travaillent ce muscle
            if muscle not in exercices_par_muscle:
                continue
            
            exos_a_ajuster = exercices_par_muscle[muscle]
            if not exos_a_ajuster:
                continue
            
            # Répartir l'ajustement sur tous les exercices du muscle
            ajustement_par_exo = diff / len(exos_a_ajuster)
            
            for session_name, exo in exos_a_ajuster:
                series_range = exo.get('series', '3')
                
                # Extraire min et max
                if '-' in str(series_range):
                    min_s, max_s = map(int, series_range.split('-'))
                else:
                    min_s = max_s = int(series_range)
                
                # Ajuster (arrondir intelligemment), mais LIMITER à 4 séries max par exercice
                import math
                new_min = max(2, min(4, int(math.ceil(min_s + ajustement_par_exo - 0.3))))
                new_max = max(new_min, min(4, int(math.ceil(max_s + ajustement_par_exo))))
                
                # Mettre à jour
                if new_min == new_max:
                    exo['series'] = str(new_min)
                else:
                    exo['series'] = f"{new_min}-{new_max}"
    
    try:
        _adjust_volumes_to_targets(programme, objectifs_muscles, volumes_hebdomadaires, exercices_choisis, split)
    except Exception as e:
        # En cas d'erreur, continuer quand même
        pass

    # Keep same behaviour as Tkinter version: return the programme dict
    return programme


def create_complete_program(nb_jours, objectifs_muscles, exercices_choisis):
    """Wrapper to return (programme_by_session, split_name, sessions_order) for the web app."""
    split = create_prog(nb_jours)
    programme = generate_workout_program(nb_jours, objectifs_muscles, exercices_choisis, {})
    sessions_order = list(split.sessions.keys())
    return programme, split.name, sessions_order


if __name__ == "__main__":
    # Quick smoke test when running as a module: python -m version_site.core.prog
    print("Running version_site.core.prog quick check")
    sample_selected = ['Bench press', 'Incline press', 'Overhead press', 'Curl', 'Pushdown']
    sample_objectifs = {'Pectoraux': 'normal_growth', 'Epaules': 'normal_growth', 'Biceps': 'normal_growth', 'Triceps': 'normal_growth', 'Quadriceps': 'maintenance'}
    prog, split_name, order = create_complete_program(3, sample_objectifs, sample_selected)
    print('split_name=', split_name)
    print('sessions_order=', order)
    print('programme keys=', list(prog.keys()))
    for k, v in prog.items():
        print(k, '->', [e['exercice'] for e in v])
