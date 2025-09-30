# Association pattern <-> muscles
pattern_to_muscles = {
    "Press horizontale": ["Pectoraux", "Epaules"],
    "press verticale": ["Epaules"],
    "tirage verticale": ["Dorsaux"],
    "tirage vertical": ["Dorsaux"],
    "squat pattern": ["Quadriceps", "Fessiers"],
    "hinge pattern": ["Lombaires", "Isquios-jambiers"],
    "spine flexion": ["Abdominaux"],
    "quad iso": ["Quadriceps"],
    "hamstring isolation": ["Isquios-jambiers"],
    "bicep isolation": ["Biceps"],
    "tricep isolation": ["Triceps"],
    "delt isolation": ["Epaules"]
}

# Association muscle <-> patterns (inverse mapping)
muscle_to_patterns = {}
for pattern, muscles in pattern_to_muscles.items():
    for muscle in muscles:
        if muscle not in muscle_to_patterns:
            muscle_to_patterns[muscle] = []
        muscle_to_patterns[muscle].append(pattern)

# Liste des noms de muscles (pour correspondre à muscle.py)
muscle_names = [
    "Pectoraux", "Epaules", "Biceps", "Triceps", "Abdominaux", 
    "Quadriceps", "Dorsaux", "Trapèze", "Lombaires", "Fessiers", "Isquios-jambiers"
]

# Fonction utilitaire pour obtenir les patterns d'un muscle
def get_patterns_for_muscle(muscle_name):
    """Retourne la liste des patterns d'exercices pour un muscle donné"""
    return muscle_to_patterns.get(muscle_name, [])

# Fonction utilitaire pour obtenir les muscles d'un pattern
def get_muscles_for_pattern(pattern_name):
    """Retourne la liste des muscles travaillés par un pattern d'exercices"""
    return pattern_to_muscles.get(pattern_name, [])