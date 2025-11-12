import sys, os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from version_site.app import app as flask_app
from version_site.core.prog import create_complete_program

selected = ['Bench press', 'Dips', 'Overhead press', 'Incline press', 'Front raise', 'Lateral raises', 'Pushdown', 'Tricep extension', 'Bent over row', 'Machine row', 'Pull up', 'Chin up', 'Hammer curl', 'Curl', 'Barbell squat', 'Bulgarian split squat', 'Stiff leg deadlift', 'Back hyperextension', 'Leg extension', 'Sissy squat', 'Seated leg curl', 'Nordic curl', 'Machine ab crunch', 'Hanging leg raises']
objectifs = {'Pectoraux':'normal_growth','Epaules':'normal_growth','Dorsaux':'normal_growth','Biceps':'normal_growth','Triceps':'normal_growth','Quadriceps':'maintenance'}
days = 3

with flask_app.app_context():
    programme_by_session, split_name, sessions_order = create_complete_program(days, objectifs, selected)
    from version_site.core.exercise_database import get_exercise_info
    # Map sessions to day numbers (same logic as app.generate)
    program_days = {d+1: [] for d in range(days)}
    for day in range(1, days+1):
        session_name = sessions_order[(day-1) % len(sessions_order)] if sessions_order else None
        if session_name and session_name in programme_by_session:
            exs = []
            seen = set()
            for item in programme_by_session[session_name]:
                name = item.get('exercice') if isinstance(item, dict) else (item[0] if isinstance(item, tuple) else str(item))
                if name in seen:
                    continue
                seen.add(name)
                info = get_exercise_info(name)
                path = info.get('image_path') if info else None
                exs.append((name, path))
            program_days[day] = exs
        else:
            program_days[day] = []

    total = sum(len(v) for v in program_days.values())
    names = [n for d in sorted(program_days.keys()) for n,_ in program_days[d]]
    print('TOTAL_EXERCISES:', total)
    print('NAMES:', names)
