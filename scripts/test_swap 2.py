import sys, os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from version_site.core.exercise_database import get_exercise_info

# Construct a contrived programme where bench and incline are on the same session and overhead is on another
programme = {
    'session_A': [
        {"exercice": 'Bench press', "series": '3', "muscles": ['Pectoraux']},
        {"exercice": 'Incline press', "series": '3', "muscles": ['Pectoraux']},
        {"exercice": 'Pushdown', "series": '2-3', "muscles": ['Triceps']}
    ],
    'session_B': [
        {"exercice": 'Overhead press', "series": '3', "muscles": ['Epaules']}
    ]
}

print('Before:')
for s, exs in programme.items():
    print(s)
    for e in exs:
        info = get_exercise_info(e['exercice'])
        print('  ', e['exercice'], 'pattern=', info.get('pattern') if info else '')

# Apply redistribution algorithm (same logic as in prog.py)
vertical_locations = []
for session_name, sess_exs in programme.items():
    for idx, e in enumerate(sess_exs):
        ex_name = e['exercice']
        info = get_exercise_info(ex_name)
        if not info:
            continue
        if 'Vertical' in info.get('pattern', ''):
            vertical_locations.append((session_name, idx, ex_name))

for session_name, sess_exs in programme.items():
    non_vertical_push_indices = []
    for idx, e in enumerate(sess_exs):
        ex_name = e['exercice']
        info = get_exercise_info(ex_name)
        if not info:
            continue
        if info.get('category') == 'push' and info.get('type') == 'polyarticulaire' and 'Vertical' not in info.get('pattern', ''):
            non_vertical_push_indices.append((idx, ex_name, info.get('pattern', '')))

    if len(non_vertical_push_indices) >= 2:
        target_idx = None
        for idx, name, pattern in non_vertical_push_indices:
            if 'Incline' in pattern or 'Incline' in name:
                target_idx = idx
                break
        if target_idx is None:
            target_idx = non_vertical_push_indices[-1][0]

        for v_session, v_idx, v_name in list(vertical_locations):
            if v_session == session_name:
                continue
            original = sess_exs[target_idx]
            other_sess = programme[v_session]
            other_sess[v_idx] = original
            sess_exs[target_idx] = {"exercice": v_name, "series": "3-5", "muscles": [m for m in get_exercise_info(v_name).get('all_muscles', [])][:1]}
            vertical_locations = [vl for vl in vertical_locations if not (vl[0] == v_session and vl[1] == v_idx)]
            break

print('\nAfter:')
for s, exs in programme.items():
    print(s)
    for e in exs:
        info = get_exercise_info(e['exercice'])
        print('  ', e['exercice'], 'pattern=', info.get('pattern') if info else '')
