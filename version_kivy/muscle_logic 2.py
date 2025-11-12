from exercise_database import get_all_muscles, get_muscle_list_with_images, VOLUME_TARGETS

Liste_muscles = get_muscle_list_with_images()
MUSCLES = get_all_muscles()
selected_goals = {}

def set_muscle_goal(muscle, goal):
    valid_goals = list(VOLUME_TARGETS.keys())
    if muscle in MUSCLES and goal in valid_goals:
        selected_goals[muscle] = goal

def get_selected_muscle_goals():
    return selected_goals.copy()

def reset_all_goals():
    global selected_goals
    selected_goals = {}

