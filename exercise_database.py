# filepath: /Users/alexpeirano/Desktop/personal coding/tinker_project/exercise_database.py
"""
Base de données centralisée de tous les exercices
Chaque exercice est défini une seule fois avec toutes ses propriétés
"""

EXERCISE_DATABASE = {
    # PUSH - Horizontal Push (Chest)
    "Bench press": {
        "name": "Bench press",
        "category": "push",
        "pattern": "Horizontal Push (Chest)",
        "type": "polyarticulaire",  # ou "isolation"
        "primary_muscles": ["Pectoraux"],
        "secondary_muscles": ["Triceps", "Epaules"],
        "all_muscles": ["Pectoraux", "Triceps", "Epaules"],
        "equipment": "Barbell",
        "difficulty": "intermediate",
        "image_path": "images/bench_press.jpg"
    },
    
    "Dips": {
        "name": "Dips",
        "category": "push", 
        "pattern": "Horizontal Push (Chest)",
        "type": "polyarticulaire",
        "primary_muscles": ["Pectoraux"],
        "secondary_muscles": ["Triceps", "Epaules"],
        "all_muscles": ["Pectoraux", "Triceps", "Epaules"],
        "equipment": "Bodyweight",
        "difficulty": "intermediate",
        "image_path": "images/dips.jpg"
    },
    
    # PUSH - Vertical Push
    "Overhead press": {
        "name": "Overhead press",
        "category": "push",
        "pattern": "Vertical Push", 
        "type": "polyarticulaire",
        "primary_muscles": ["Epaules"],
        "secondary_muscles": ["Triceps"],
        "all_muscles": ["Epaules", "Triceps"],
        "equipment": "Barbell",
        "difficulty": "intermediate",
        "image_path": "images/overhead_press.jpg"
    },
    
    "Incline press": {
        "name": "Incline press",
        "category": "push",
        "pattern": "Incline Push",
        "type": "polyarticulaire", 
        "primary_muscles": ["Pectoraux"],
        "secondary_muscles": ["Epaules", "Triceps"],
        "all_muscles": ["Pectoraux", "Epaules", "Triceps"],
        "equipment": "Barbell",
        "difficulty": "intermediate",
        "image_path": "images/incline_press.jpg"
    },
    
    # PUSH - Isolations
    "Lateral raises": {
        "name": "Lateral raises",
        "category": "push",
        "pattern": "Lateral Raise",
        "type": "isolation",
        "primary_muscles": ["Epaules"],
        "secondary_muscles": [],
        "all_muscles": ["Epaules"],
        "equipment": "Dumbbells",
        "difficulty": "beginner",
        "image_path": "images/lateral_raises.jpg"
    },
    
    "Front raise": {
        "name": "Front raise", 
        "category": "push",
        "pattern": "Front Raise",
        "type": "isolation",
        "primary_muscles": ["Epaules"],
        "secondary_muscles": [],
        "all_muscles": ["Epaules"],
        "equipment": "Dumbbells", 
        "difficulty": "beginner",
        "image_path": "images/front_raise.jpg"
    },
    
    "Rear delt fly": {
        "name": "Rear delt fly",
        "category": "push", 
        "pattern": "Rear Delt",
        "type": "isolation",
        "primary_muscles": ["Epaules"],
        "secondary_muscles": [],
        "all_muscles": ["Epaules"],
        "equipment": "Dumbbells",
        "difficulty": "beginner", 
        "image_path": "images/rear_delt_fly.jpg"
    },
    
    "Pushdown": {
        "name": "Pushdown",
        "category": "push",
        "pattern": "Tricep Extension", 
        "type": "isolation",
        "primary_muscles": ["Triceps"],
        "secondary_muscles": [],
        "all_muscles": ["Triceps"],
        "equipment": "Cable",
        "difficulty": "beginner",
        "image_path": "images/pushdown.jpg"
    },
    
    "Tricep extension": {
        "name": "Tricep extension",
        "category": "push",
        "pattern": "Tricep Extension",
        "type": "isolation", 
        "primary_muscles": ["Triceps"],
        "secondary_muscles": [],
        "all_muscles": ["Triceps"],
        "equipment": "Dumbbells",
        "difficulty": "beginner",
        "image_path": "images/tricep_extension.jpg"
    },
    
    # PULL - Horizontal Pull
    "Bent over row": {
        "name": "Bent over row",
        "category": "pull",
        "pattern": "Horizontal Pull",
        "type": "polyarticulaire",
        "primary_muscles": ["Dorsaux"],
        "secondary_muscles": ["Biceps", "Epaules"],
        "all_muscles": ["Dorsaux", "Biceps", "Epaules"],
        "equipment": "Barbell",
        "difficulty": "intermediate", 
        "image_path": "images/bent_over_row.jpg"
    },
    
    "Machine row": {
        "name": "Machine row",
        "category": "pull",
        "pattern": "Horizontal Pull",
        "type": "polyarticulaire",
        "primary_muscles": ["Dorsaux"],
        "secondary_muscles": ["Biceps"],
        "all_muscles": ["Dorsaux", "Biceps"],
        "equipment": "Machine",
        "difficulty": "beginner",
        "image_path": "images/machine_row.jpg"
    },
    
    # PULL - Vertical Pull  
    "Pull up": {
        "name": "Pull up",
        "category": "pull",
        "pattern": "Vertical Pull",
        "type": "polyarticulaire",
        "primary_muscles": ["Dorsaux"],
        "secondary_muscles": ["Biceps"],
        "all_muscles": ["Dorsaux", "Biceps"],
        "equipment": "Bodyweight",
        "difficulty": "advanced",
        "image_path": "images/pull_up.jpg"
    },
    
    "Chin up": {
        "name": "Chin up", 
        "category": "pull",
        "pattern": "Vertical Pull",
        "type": "polyarticulaire",
        "primary_muscles": ["Dorsaux"],
        "secondary_muscles": ["Biceps"],
        "all_muscles": ["Dorsaux", "Biceps"],
        "equipment": "Bodyweight",
        "difficulty": "advanced",
        "image_path": "images/chin_up.jpg"
    },
    
    # PULL - Isolations
    "Curl": {
        "name": "Curl",
        "category": "pull",
        "pattern": "Bicep Curl",
        "type": "isolation",
        "primary_muscles": ["Biceps"],
        "secondary_muscles": [],
        "all_muscles": ["Biceps"],
        "equipment": "Dumbbells",
        "difficulty": "beginner",
        "image_path": "images/curl.jpg"
    },
    
    "Hammer curl": {
        "name": "Hammer curl",
        "category": "pull", 
        "pattern": "Bicep Curl",
        "type": "isolation",
        "primary_muscles": ["Biceps"],
        "secondary_muscles": [],
        "all_muscles": ["Biceps"],
        "equipment": "Dumbbells",
        "difficulty": "beginner",
        "image_path": "images/hammer_curl.jpg"
    },
    
    "Preacher curl": {
        "name": "Preacher curl",
        "category": "pull",
        "pattern": "Bicep Curl",
        "type": "isolation",
        "primary_muscles": ["Biceps"],
        "secondary_muscles": [],
        "all_muscles": ["Biceps"],
        "equipment": "Barbell",
        "difficulty": "beginner", 
        "image_path": "images/preacher_curl.jpg"
    },
    
    # LEGS - Squat Pattern
    "Barbell squat": {
        "name": "Barbell squat",
        "category": "legs",
        "pattern": "Squat",
        "type": "polyarticulaire",
        "primary_muscles": ["Quadriceps"],
        "secondary_muscles": ["Fessiers", "Lombaires"],
        "all_muscles": ["Quadriceps", "Fessiers", "Lombaires"],
        "equipment": "Barbell",
        "difficulty": "intermediate",
        "image_path": "images/barbell_squat.jpg"
    },
    
    "Bulgarian split squat": {
        "name": "Bulgarian split squat",
        "category": "legs",
        "pattern": "Single Leg", 
        "type": "polyarticulaire",
        "primary_muscles": ["Quadriceps"],
        "secondary_muscles": ["Fessiers"],
        "all_muscles": ["Quadriceps", "Fessiers"],
        "equipment": "Bodyweight",
        "difficulty": "intermediate",
        "image_path": "images/bulgarian_split_squat.jpg"
    },
    
    "Hack squat": {
        "name": "Hack squat",
        "category": "legs",
        "pattern": "Squat",
        "type": "polyarticulaire",
        "primary_muscles": ["Quadriceps"],
        "secondary_muscles": ["Fessiers"],
        "all_muscles": ["Quadriceps", "Fessiers"],
        "equipment": "Machine",
        "difficulty": "beginner",
        "image_path": "images/hack_squat.jpg"
    },
    
    # LEGS - Hip Hinge Pattern
    "Stiff leg deadlift": {
        "name": "Stiff leg deadlift",
        "category": "legs",
        "pattern": "Hip Hinge",
        "type": "polyarticulaire", 
        "primary_muscles": ["Isquios-jambiers"],
        "secondary_muscles": ["Fessiers", "Lombaires"],
        "all_muscles": ["Isquios-jambiers", "Fessiers", "Lombaires"],
        "equipment": "Barbell",
        "difficulty": "intermediate",
        "image_path": "images/stiff_leg_deadlift.jpg"
    },
    
    "Back hyperextension": {
        "name": "Back hyperextension",
        "category": "legs",
        "pattern": "Hip Hinge",
        "type": "isolation",  # Plus spécifique aux lombaires
        "primary_muscles": ["Lombaires"],
        "secondary_muscles": ["Isquios-jambiers", "Fessiers"],
        "all_muscles": ["Lombaires", "Isquios-jambiers", "Fessiers"],
        "equipment": "Machine",
        "difficulty": "beginner",
        "image_path": "images/back_hyperextension.jpg"
    },
    
    # LEGS - Isolations
    "Leg extension": {
        "name": "Leg extension",
        "category": "legs",
        "pattern": "Leg Extension",
        "type": "isolation",
        "primary_muscles": ["Quadriceps"],
        "secondary_muscles": [],
        "all_muscles": ["Quadriceps"],
        "equipment": "Machine",
        "difficulty": "beginner",
        "image_path": "images/leg_extension.jpg"
    },
    
    "Sissy squat": {
        "name": "Sissy squat",
        "category": "legs", 
        "pattern": "Leg Extension",
        "type": "isolation",
        "primary_muscles": ["Quadriceps"],
        "secondary_muscles": [],
        "all_muscles": ["Quadriceps"],
        "equipment": "Bodyweight",
        "difficulty": "advanced",
        "image_path": "images/sissy_squat.jpg"
    },
    
    "Seated leg curl": {
        "name": "Seated leg curl",
        "category": "legs",
        "pattern": "Leg Curl",
        "type": "isolation",
        "primary_muscles": ["Isquios-jambiers"],
        "secondary_muscles": [],
        "all_muscles": ["Isquios-jambiers"],
        "equipment": "Machine", 
        "difficulty": "beginner",
        "image_path": "images/seated_leg_curl.jpg"
    },
    
    "Nordic curl": {
        "name": "Nordic curl",
        "category": "legs",
        "pattern": "Leg Curl", 
        "type": "isolation",
        "primary_muscles": ["Isquios-jambiers"],
        "secondary_muscles": [],
        "all_muscles": ["Isquios-jambiers"],
        "equipment": "Bodyweight",
        "difficulty": "advanced",
        "image_path": "images/nordic_curl.jpg"
    },
    
    # CORE - Abdominaux (tous isolations)
    "Machine ab crunch": {
        "name": "Machine ab crunch",
        "category": "core",
        "pattern": "Abs",
        "type": "isolation",
        "primary_muscles": ["Abdominaux"],
        "secondary_muscles": [],
        "all_muscles": ["Abdominaux"],
        "equipment": "Machine",
        "difficulty": "beginner",
        "image_path": "images/machine_ab_crunch.jpg"
    },
    
    "Hanging leg raises": {
        "name": "Hanging leg raises",
        "category": "core",
        "pattern": "Abs",
        "type": "isolation",
        "primary_muscles": ["Abdominaux"],
        "secondary_muscles": [],
        "all_muscles": ["Abdominaux"],
        "equipment": "Bodyweight", 
        "difficulty": "intermediate",
        "image_path": "images/hanging_leg_raises.jpg"
    }
}

def get_exercise_info(exercise_name):
    """Récupère toutes les informations d'un exercice"""
    return EXERCISE_DATABASE.get(exercise_name, None)

def get_all_exercises():
    """Récupère tous les noms d'exercices"""
    return list(EXERCISE_DATABASE.keys())

def get_exercises_by_category(category):
    """Récupère tous les exercices d'une catégorie (push, pull, legs, core)"""
    return [name for name, info in EXERCISE_DATABASE.items() if info["category"] == category]

def get_exercises_by_type(exercise_type):
    """Récupère tous les exercices d'un type (polyarticulaire, isolation)"""
    return [name for name, info in EXERCISE_DATABASE.items() if info["type"] == exercise_type]

def get_exercises_by_pattern(pattern):
    """Récupère tous les exercices d'un pattern donné"""
    return [name for name, info in EXERCISE_DATABASE.items() if info["pattern"] == pattern]

def get_exercises_by_muscle(muscle):
    """Récupère tous les exercices qui travaillent un muscle donné"""
    return [name for name, info in EXERCISE_DATABASE.items() if muscle in info["all_muscles"]]

def is_polyarticular(exercise_name):
    """Vérifie si un exercice est polyarticulaire"""
    info = get_exercise_info(exercise_name)
    return info["type"] == "polyarticulaire" if info else False

def is_isolation(exercise_name):
    """Vérifie si un exercice est d'isolation"""
    info = get_exercise_info(exercise_name)  
    return info["type"] == "isolation" if info else False