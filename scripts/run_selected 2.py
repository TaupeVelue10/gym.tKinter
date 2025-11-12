import sys, os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from version_site.core.prog import create_complete_program
from version_site.core.exercise_database import get_exercise_info

selected = ['Bench press', 'Dips', 'Overhead press', 'Incline press', 'Front raise', 'Rear delt fly', 'Pushdown', 'Tricep extension', 'Bent over row', 'Machine row', 'Pull up', 'Chin up', 'Hammer curl', 'Curl', 'Barbell squat', 'Bulgarian split squat', 'Stiff leg deadlift', 'Back hyperextension', 'Leg extension', 'Sissy squat', 'Seated leg curl', 'Nordic curl', 'Machine ab crunch', 'Hanging leg raises']

days = 3
objectifs = {'Pectoraux':'normal_growth','Epaules':'normal_growth','Dorsaux':'normal_growth','Biceps':'normal_growth','Triceps':'normal_growth','Quadriceps':'maintenance'}

programme_by_session, split_name, sessions_order = create_complete_program(days, objectifs, selected)
print('split_name=', split_name)
print('sessions_order=', sessions_order)
print('\nprogramme_by_session:')
from pprint import pprint
pprint(programme_by_session)

# Map sessions to days (same logic as app.py)
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

print('\nprogram_days mapping:')
for k,v in program_days.items():
    print(k, '->', [x[0] for x in v])
