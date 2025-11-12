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

    # Keep same behaviour as Tkinter version: return the programme dict
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



def repartir_exercices_ppl(exercices_choisis, sessions_names, get_exercise_info_fn=get_exercise_info):
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
        info = get_exercise_info_fn(exercice_name)
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


def generate_workout_program(nb_jours, objectifs_muscles, exercices_choisis, pattern_muscles=None, get_exercise_info_fn=get_exercise_info):
    """Génère un programme d'entraînement (par session) basé sur la logique existante

    Retourne un dict mapping session_name -> list of exercise dicts
    """
    if pattern_muscles is None:
        pattern_muscles = {}

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
    for muscle, objectif in (objectifs_muscles or {}).items():
        volume_range = volume_objectifs.get(objectif, [5])
        volumes_hebdomadaires[muscle] = volume_range[1] if len(volume_range) > 1 else volume_range[0]

    # Générer le programme pour chaque session
    programme = {}
    sessions_names = list(split.sessions.keys())
    
    # Calculer le volume cible par session
    volumes_par_session = {s: {} for s in sessions_names}
    
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
        exercices_repartis = repartir_exercices_ppl(exercices_choisis, sessions_names, get_exercise_info_fn)
    elif split.name == "Upper/Lower":
        # Répartition spéciale pour Upper/Lower
        exercices_repartis = {session: [] for session in sessions_names}
        
        # Séparer les exercices par catégorie
        exercices_upper = []
        exercices_lower = []
        
        for exercice_name in exercices_choisis:
            info = get_exercise_info_fn(exercice_name)
            if not info:
                continue
            
            exercice_info = (exercice_name, info.get("all_muscles", []), info.get("pattern"), info.get("type"))
            
            # Classer selon la catégorie
            if info.get("category") in ["push", "pull", "core"]:  # Core (abs) va dans upper
                exercices_upper.append(exercice_info)
            elif info.get("category") == "legs":
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
            info = get_exercise_info_fn(exercice_name)
            if info:
                exercices_avec_info.append((exercice_name, info.get("all_muscles", []), info.get("pattern"), info.get("type")))
        
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
        
        volumes_session = volumes_par_session.get(session_name, {}).copy()
        
        for exercice, muscles_communs, pattern, _ in exercices_repartis.get(session_name, []):
            if exercices_ajoutes >= max_exercices_par_session:
                break
                
            muscles_session_communs = [m for m in muscles_communs if m in muscles_session]
            
            if not muscles_session_communs:
                continue
                
            volume_necessaire = max([volumes_session.get(m, 0) for m in muscles_session_communs]) if muscles_session_communs else 0
            
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
    
    # Post-processing: ensure arm isolations present and redistribute verticals if needed
    def _find_isolation_local(muscle, assigned):
        # prefer chosen exercises
        for name in exercices_choisis:
            info = get_exercise_info(name)
            if not info:
                continue
            if muscle in info.get('all_muscles', []) and info.get('type') == 'isolation' and name not in assigned:
                return name
        # fallback to DB
        for name in get_exercises_by_muscle(muscle):
            if name in assigned:
                continue
            if is_isolation(name):
                return name
        return None

    def _ensure_arm_isolations_local(programme):
        assigned = set()
        for sess in programme.values():
            for e in sess:
                assigned.add(e['exercice'])

        for muscle in ('Biceps', 'Triceps'):
            has_iso = any(
                (get_exercise_info(e['exercice']) and muscle in get_exercise_info(e['exercice']).get('all_muscles', []) and get_exercise_info(e['exercice']).get('type') == 'isolation')
                for sess in programme.values() for e in sess)
            if not has_iso:
                candidate = _find_isolation_local(muscle, assigned)
                if candidate:
                    # choose session to place the isolation: prefer sessions that already include exercises
                    # touching this muscle; among candidates pick the one with fewest exercises to distribute.
                    best_session = None
                    best_len = None
                    sessions_with_muscle = []
                    for session_name, sess_exs in programme.items():
                        for e in sess_exs:
                            info = get_exercise_info(e['exercice'])
                            if info and muscle in info.get('all_muscles', []):
                                sessions_with_muscle.append(session_name)
                                break

                    candidate_sessions = sessions_with_muscle if sessions_with_muscle else list(programme.keys())
                    for sname in candidate_sessions:
                        l = len(programme.get(sname, []))
                        if best_len is None or l < best_len:
                            best_len = l
                            best_session = sname

                    if best_session:
                        programme[best_session].append({"exercice": candidate, "series": "2-3", "muscles": [muscle]})
                        assigned.add(candidate)

    def _redistribute_verticals_local(programme):
        vertical_locations = []
        for session_name, sess_exs in programme.items():
            for idx, e in enumerate(sess_exs):
                ex_name = e['exercice']
                info = get_exercise_info(ex_name)
                if not info:
                    continue
                if 'Vertical' in info.get('pattern', ''):
                    vertical_locations.append((session_name, idx, ex_name))
        if not vertical_locations:
            return

        for session_name, sess_exs in programme.items():
            non_vertical_push_indices = []
            for idx, e in enumerate(sess_exs):
                ex_name = e['exercice']
                info = get_exercise_info(ex_name)
                if not info:
                    continue
                if info.get('category') == 'push' and info.get('type') == 'polyarticulaire' and 'Vertical' not in info.get('pattern', ''):
                    non_vertical_push_indices.append((idx, ex_name, info.get('pattern', '')))

            if len(non_vertical_push_indices) >= 2:
                target_idx = None
                for idx, name, pattern in non_vertical_push_indices:
                    if 'Incline' in pattern or 'Incline' in name:
                        target_idx = idx
                        break
                if target_idx is None:
                    target_idx = non_vertical_push_indices[-1][0]

                for v_session, v_idx, v_name in list(vertical_locations):
                    if v_session == session_name:
                        continue
                    original = sess_exs[target_idx]
                    other_sess = programme[v_session]
                    other_sess[v_idx] = original
                    sess_exs[target_idx] = {"exercice": v_name, "series": "3-5", "muscles": [m for m in get_exercise_info(v_name).get('all_muscles', [])][:1]}
                    vertical_locations = [vl for vl in vertical_locations if not (vl[0] == v_session and vl[1] == v_idx)]
                    break

    try:
        _ensure_arm_isolations_local(programme)
    except Exception:
        pass
    try:
        _redistribute_verticals_local(programme)
    except Exception:
        pass

    return programme


def create_complete_program(nb_jours, objectifs_muscles, exercices_choisis):
    """Wrapper that returns programme_by_session, split_name and sessions_order so the web app can map sessions to days."""
    split = create_prog(nb_jours)
    programme = generate_workout_program(nb_jours, objectifs_muscles, exercices_choisis, {})
    sessions_order = list(split.sessions.keys())
    return programme, split.name, sessions_order
def generate_program(days, goal, priorities):
    text = f"Programme {goal.upper()} – {days} jours/semaine\n\n"
    for muscle, priority in priorities.items():
        text += f"{muscle.capitalize()} → priorité {priority}\n"
        text += f"  Exos : [à choisir depuis ta base de données]\n\n"
    return text
