import sys
sys.path.insert(0, '/Users/alexpeirano/Desktop/personal coding/tinker_project')

from version_site.core.prog import create_complete_program

objectifs_muscles = {
    'Biceps': 'prioritised_growth',
    'Epaules': 'normal_growth',
    'Triceps': 'normal_growth',
    'Dorsaux': 'normal_growth',
    'Quadriceps': 'normal_growth',
    'Isquios-jambiers': 'normal_growth',
    'Abdominaux': 'normal_growth'
}

exercices_selectionnes = [
    'Overhead press', 'Pushdown', 'Bent over row', 'Curl',
    'Barbell squat', 'Stiff leg deadlift', 'Machine ab crunch'
]

programme, split_name, sessions_order = create_complete_program(
    nb_jours=3,
    objectifs_muscles=objectifs_muscles,
    exercices_choisis=exercices_selectionnes
)

print(f'\n=== PROGRAMME 3 JOURS ({split_name}) ===\n')
for session_name in sessions_order:
    exercices = programme[session_name]
    print(f'{session_name}:')
    for exo in exercices:
        print(f'  - {exo["exercice"]} ({exo["series"]})')
    print()

volumes = {}
for session_name in sessions_order:
    for exo in programme[session_name]:
        muscles = exo['muscles']
        series_range = exo['series']
        if '-' in series_range:
            min_s, max_s = map(int, series_range.split('-'))
            series_avg = (min_s + max_s) / 2
        else:
            series_avg = int(series_range)
        for muscle in muscles:
            volumes[muscle] = volumes.get(muscle, 0) + series_avg

print('=== VOLUMES (muscles primaires seulement) ===')
for muscle in objectifs_muscles.keys():
    vol = volumes.get(muscle, 0)
    obj = objectifs_muscles[muscle]
    if obj == 'prioritised_growth':
        cible = '11-13'
        ok = 11 <= vol <= 13
    elif obj == 'normal_growth':
        cible = '7-10'
        ok = 7 <= vol <= 10
    else:
        cible = '4-6'
        ok = 4 <= vol <= 6
    
    status = '✅' if ok else '❌'
    print(f'{status} {muscle}: {vol} séries (cible: {cible})')
