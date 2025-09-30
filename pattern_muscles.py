# Association entre les patterns de mouvement et les muscles travaillés

PATTERN_MUSCLES = {
    # Patterns de poussée
    "Horizontal Push (Chest)": ["Pectoraux", "Triceps", "Epaules"],
    "Incline Push": ["Pectoraux", "Epaules", "Triceps"],
    "Decline Push": ["Pectoraux", "Triceps"],
    "Vertical Push": ["Epaules", "Triceps"],
    "Overhead Press": ["Epaules", "Triceps"],
    
    # Patterns de tirage
    "Horizontal Pull": ["Dorsaux", "Biceps", "Lombaires"],
    "Vertical Pull": ["Dorsaux", "Biceps"],
    "Row": ["Dorsaux", "Biceps", "Lombaires"],
    
    # Patterns de jambes
    "Squat": ["Quadriceps", "Fessiers", "Isquios-jambiers"],
    "Deadlift": ["Isquios-jambiers", "Fessiers", "Lombaires", "Dorsaux"],
    "Hip Hinge": ["Isquios-jambiers", "Fessiers", "Lombaires"],
    "Lunge": ["Quadriceps", "Fessiers", "Isquios-jambiers"],
    "Single Leg": ["Quadriceps", "Fessiers", "Isquios-jambiers"],
    
    # Patterns d'isolation
    "Bicep Curl": ["Biceps"],
    "Tricep Extension": ["Triceps"],
    "Lateral Raise": ["Epaules"],
    "Rear Delt": ["Epaules"],
    "Chest Fly": ["Pectoraux"],
    "Leg Extension": ["Quadriceps"],
    "Leg Curl": ["Isquios-jambiers"],
    "Calf Raise": ["Mollets"],
    "Abs": ["Abdominaux"],
    "Lower Back": ["Lombaires"],
    
    # Patterns fonctionnels
    "Carry": ["Lombaires", "Abdominaux", "Dorsaux"],
    "Core": ["Abdominaux", "Lombaires"],
}

def get_muscles_from_pattern(pattern):
    """Retourne la liste des muscles travaillés par un pattern donné"""
    return PATTERN_MUSCLES.get(pattern, [])

def get_all_patterns():
    """Retourne tous les patterns disponibles"""
    return list(PATTERN_MUSCLES.keys())