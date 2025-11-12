from pprint import pprint
import sys, os
# ensure project root is on sys.path so version_site can be imported
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from version_site.core.prog import create_complete_program
from version_site.core.exercise_database import get_exercise_info

# Representative input that previously caused issues
nb_jours = 2
objectifs_muscles = {
    'Pectoraux': 'normal_growth',
    'Epaules': 'normal_growth',
    'Dorsaux': 'normal_growth',
    'Biceps': 'normal_growth',
    'Triceps': 'normal_growth',
    'Quadriceps': 'maintenance'
}
# include bench, incline and overhead plus some isolations
exercices_choisis = [
    'Bench press', 'Incline press', 'Overhead press', 'Dips',
    'Pushdown', 'Curl', 'Bent over row', 'Barbell squat'
]

programme, split_name, sessions_order = create_complete_program(nb_jours, objectifs_muscles, exercices_choisis)
print('\nSPLIT:', split_name)
print('SESSIONS ORDER:', sessions_order)
print('\nPROGRAMME:')
print('\nRAW programme_by_session repr:')
print(repr(programme))
for s in sessions_order:
    print('\n==', s, '==')
    sess = programme.get(s, [])
    if not sess:
        print('  (no exercises)')
        continue
    for ex in sess:
        name = ex['exercice']
        info = get_exercise_info(name)
        print(f" - {name}: pattern={info.get('pattern') if info else '??'}, type={info.get('type') if info else '??'}, series={ex.get('series')}")

# Summarize presence of isolations
print('\nIsolation summary:')
for muscle in ('Biceps','Triceps'):
    found = False
    for s in sessions_order:
        for ex in programme.get(s, []):
            info = get_exercise_info(ex['exercice'])
            if info and muscle in info.get('all_muscles',[]) and info.get('type') == 'isolation':
                print(f"Found {muscle} isolation: {ex['exercice']} in {s}")
                found = True
    if not found:
        print(f"No {muscle} isolation found")
