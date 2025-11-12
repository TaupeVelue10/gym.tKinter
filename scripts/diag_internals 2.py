import sys, os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from version_site.core.prog import create_prog, repartir_exercices_ppl
from version_site.core.exercise_database import get_exercise_info, get_exercises_by_muscle

nb_jours = 2
objectifs_muscles = {
    'Pectoraux': 'normal_growth',
    'Epaules': 'normal_growth',
    'Dorsaux': 'normal_growth',
    'Biceps': 'normal_growth',
    'Triceps': 'normal_growth',
    'Quadriceps': 'maintenance'
}
exercices_choisis = [
    'Bench press', 'Incline press', 'Overhead press', 'Dips',
    'Pushdown', 'Curl', 'Bent over row', 'Barbell squat'
]

split = create_prog(nb_jours)
sessions_names = list(split.sessions.keys())
print('split.name=', split.name)
print('sessions_names=', sessions_names)

# compute volumes_hebdomadaires as in module
volume_objectifs = {
    'maintenance': [4,5,6],
    'normal_growth': [7,8,9,10],
    'prioritised_growth': [11,12,13]
}
volumes_hebdomadaires = {}
for muscle, objectif in (objectifs_muscles or {}).items():
    vr = volume_objectifs.get(objectif, [5])
    volumes_hebdomadaires[muscle] = vr[1] if len(vr)>1 else vr[0]
print('\nvolumes_hebdomadaires:')
print(volumes_hebdomadaires)

# repetitions_par_session
repetitions_par_session = {s:1 for s in sessions_names}
print('\nrepetitions_par_session:')
print(repetitions_par_session)

# volumes_par_session
volumes_par_session = {s: {} for s in sessions_names}
for muscle, volume_hebdo in volumes_hebdomadaires.items():
    sessions_avec_muscle = [s for s in sessions_names if muscle in split.sessions[s]]
    if sessions_avec_muscle:
        total_repetitions = sum(repetitions_par_session[s] for s in sessions_avec_muscle)
        if total_repetitions>0:
            base = volume_hebdo // total_repetitions
            rest = volume_hebdo % total_repetitions
            for i, sname in enumerate(sessions_avec_muscle):
                volumes_par_session[sname][muscle] = base
                if i < rest:
                    volumes_par_session[sname][muscle] += 1

print('\nvolumes_par_session:')
from pprint import pprint
pprint(volumes_par_session)

# compute exercices_repartis for full body path
# replicate the else branch
exercices_avec_info = []
for exercice_name in exercices_choisis:
    info = get_exercise_info(exercice_name)
    if info:
        exercices_avec_info.append((exercice_name, info.get('all_muscles', []), info.get('pattern'), info.get('type')))

exercices_avec_info.sort(key=lambda x: 2 if x[3]=='polyarticulaire' else 1, reverse=True)
print('\nexercices_avec_info sorted:')
for e in exercices_avec_info:
    print(e)

exercices_repartis = {session: [] for session in sessions_names}
for i, exercice_info in enumerate(exercices_avec_info):
    session_index = i % len(sessions_names)
    session_name = sessions_names[session_index]
    exercices_repartis[session_name].append(exercice_info)

print('\nexercices_repartis:')
for k,v in exercices_repartis.items():
    print(k, '->', [x[0] for x in v])

# Now compute which exercises would be kept by volume_necessaire
programme = {s: [] for s in sessions_names}
for session_name, muscles_session in split.sessions.items():
    volumes_session = volumes_par_session.get(session_name, {}).copy()
    added = 0
    for exercice, muscles_communs, pattern, _ in exercices_repartis.get(session_name, []):
        if added>=5:
            break
        muscles_session_communs = [m for m in muscles_communs if m in muscles_session]
        if not muscles_session_communs:
            continue
        volume_necessaire = max([volumes_session.get(m,0) for m in muscles_session_communs]) if muscles_session_communs else 0
        print(f'Checking {exercice} in {session_name}: muscles_common={muscles_session_communs}, volume_necessaire={volume_necessaire}')
        if volume_necessaire<=0:
            continue
        programme[session_name].append(exercice)
        added+=1
        for m in muscles_session_communs:
            volumes_session[m] = max(0, volumes_session.get(m,0)-2)

print('\nResulting programme (kept exercises per session):')
for k,v in programme.items():
    print(k,'->',v)
