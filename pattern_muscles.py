# Association entre les patterns de mouvement et les muscles travaillés

PATTERN_MUSCLES = {
    # Patterns de poussée (seulement muscles primaires)
    "Horizontal Push (Chest)": ["Pectoraux"],
    "Incline Push": ["Pectoraux"],  
    "Decline Push": ["Pectoraux"],
    "Vertical Push": ["Epaules"],
    
    # Patterns de tirage (seulement muscles primaires)
    "Horizontal Pull": ["Dorsaux"],
    "Vertical Pull": ["Dorsaux"],
    "Row": ["Dorsaux"],
    
    # Patterns de jambes
    "Squat": ["Quadriceps", "Fessiers", "Isquios-jambiers"],
    "Deadlift": ["Isquios-jambiers", "Fessiers", "Lombaires", "Dorsaux"],
    "Hip Hinge": ["Isquios-jambiers", "Fessiers", "Lombaires"],
    "Single Leg": ["Quadriceps", "Fessiers", "Isquios-jambiers"],
    
    # Patterns d'isolation
    "Bicep Curl": ["Biceps"],
    "Tricep Extension": ["Triceps"],
    "Lateral Raise": ["Epaules"],
    "Rear Delt": ["Epaules"],
    "Leg Extension": ["Quadriceps"],
    "Leg Curl": ["Isquios-jambiers"],
    "Abs": ["Abdominaux"],
    
    # Patterns fonctionnels
    "Core": ["Abdominaux", "Lombaires"],
}

def get_muscles_from_pattern(pattern):
    """Retourne la liste des muscles travaillés par un pattern donné"""
    return PATTERN_MUSCLES.get(pattern, [])