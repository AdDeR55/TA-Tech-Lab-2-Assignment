#!/usr/bin/env python3
"""
validation/check.py  —  Campus IT Service Desk Handover Lab
Comprehensive validator with actionable feedback.

Run from your lab-work/lab2-<ID>/ folder:

    python3 ../../validation/check.py

Produces 17 checks grouped by experiment.
Exits 0 if ALL pass; exits 1 if any fail.
Never modifies, uploads or solves any learner file.

Fixture files (trusted expected results) live in:
    ../../validation/expected/

ID-seeded expected values are computed from setup.py.
"""
import difflib
import sys
from collections import Counter
from pathlib import Path

# ── Locate project root and import setup ──────────────────────────────────────

_HERE     = Path(__file__).resolve().parent          # .../validation/
_ROOT     = _HERE.parent                              # .../campus-it-handover-lab/
_FIXTURES = _HERE / 'expected'

sys.path.insert(0, str(_ROOT))
try:
    from setup import make_data, valid_id
except ImportError:
    sys.exit(
        'Cannot find setup.py. Is this file in the validation/ folder of\n'
        'campus-it-handover-lab? Run from lab-work/lab2-<ID>/ as shown above.'
    )


# ── Helpers ───────────────────────────────────────────────────────────────────

def norm(text):
    """Normalise CRLF -> LF for cross-platform comparison."""
    return text.replace('\r\n', '\n').replace('\r', '\n')


def read(path):
    """Read a file, return normalised text or None on error."""
    try:
        return norm(path.read_bytes().decode('utf-8'))
    except (OSError, UnicodeError):
        return None


def fixture(name):
    """Read a fixture file and return normalised text. Abort if missing."""
    p = _FIXTURES / name
    content = read(p)
    if content is None:
        sys.exit(
            f'Fixture file missing: {p}\n'
            'The validation/expected/ folder must be present in the repository.'
        )
    return content


def parse_counter(text):
    """
    Parse a uniq -c style block.
    Returns (dict of name->count, error_message).
    Accepts any leading whitespace before the count.
    """
    result = {}
    if text is None:
        return None, 'file is missing'
    for raw in text.splitlines():
        stripped = raw.strip()
        if not stripped:
            continue
        parts = stripped.split(None, 1)
        if len(parts) != 2:
            return None, f"line '{raw.strip()}' is not in COUNT NAME format"
        count_str, name = parts
        try:
            count = int(count_str)
        except ValueError:
            return None, f"count '{count_str}' is not a whole number"
        if count < 1:
            return None, f"count for '{name}' is {count} (must be >= 1)"
        if name in result:
            return None, f"name '{name}' appears in two separate groups"
        result[name] = count
    return result, None


def is_sorted(lst, key=str.lower, reverse=False):
    """Return (True, None) if sorted; (False, message) otherwise."""
    for i in range(len(lst) - 1):
        a, b = key(lst[i]), key(lst[i + 1])
        if reverse:
            if a < b:
                return False, f"'{lst[i]}' should come after '{lst[i+1]}'"
        else:
            if a > b:
                return False, f"'{lst[i]}' should come before '{lst[i+1]}'"
    return True, None


def has_duplicates(lst):
    seen = set()
    for item in lst:
        if item in seen:
            return item
        seen.add(item)
    return None


def normal_diff(a, b):
    """Generate GNU-style normal diff output from two line lists."""
    out = []
    span = lambda s, e: str(s + 1) if e - s == 1 else f'{s + 1},{e}'
    for kind, i, j, k, l in difflib.SequenceMatcher(
            None, a, b, autojunk=False).get_opcodes():
        if kind == 'equal':
            continue
        if kind == 'replace':
            out += (
                [span(i, j) + 'c' + span(k, l)]
                + ['< ' + v for v in a[i:j]]
                + ['---']
                + ['> ' + v for v in b[k:l]]
            )
        elif kind == 'delete':
            out += [span(i, j) + 'd' + str(k)] + ['< ' + v for v in a[i:j]]
        else:
            out += [str(i) + 'a' + span(k, l)] + ['> ' + v for v in b[k:l]]
    return '\n'.join(out) + '\n' if out else ''


# ── Result collector ──────────────────────────────────────────────────────────

class Results:
    def __init__(self):
        self._items = []

    def ok(self, label, detail=''):
        self._items.append(('PASS', label, detail))

    def fail(self, label, detail):
        self._items.append(('FAIL', label, detail))

    def all_passed(self):
        return all(s == 'PASS' for s, _, _ in self._items)

    def print_group(self, title):
        print(f'\n{title}')
        print('-' * min(len(title), 50))
        for status, label, detail in self._items:
            marker = 'OK  ' if status == 'PASS' else 'FAIL'
            print(f'  {marker}  {label}')
            if detail and status == 'FAIL':
                print(f'        -> {detail}')

    def summary(self):
        passed = sum(1 for s, _, _ in self._items if s == 'PASS')
        total  = len(self._items)
        return passed, total


# ── Per-file check functions ──────────────────────────────────────────────────

def check_exact(r, root, relative, expected_text, hint=''):
    path   = root / relative
    actual = read(path)
    label  = relative
    if actual is None:
        r.fail(label, f'File not found. Create it with the correct command.{" "+hint if hint else ""}')
        return
    if actual == expected_text:
        r.ok(label)
        return
    exp_lines = expected_text.splitlines()
    act_lines = actual.splitlines()
    for i, (e, a) in enumerate(zip(exp_lines, act_lines)):
        if e != a:
            r.fail(label, f'Line {i+1} is wrong. Expected: {repr(e)}  Got: {repr(a)}')
            return
    if len(act_lines) != len(exp_lines):
        r.fail(label, f'Expected {len(exp_lines)} line(s), got {len(act_lines)}. '
                      f'Check for extra blank lines or missing content.')
        return
    r.fail(label, 'Content differs from expected.')


def check_nonempty(r, root, relative):
    path   = root / relative
    actual = read(path)
    label  = relative
    if actual is None:
        r.fail(label, 'File not found. Create it with  nano work/summary.txt  then Ctrl+O, Enter, Ctrl+X.')
        return
    if actual.strip():
        r.ok(label)
    else:
        r.fail(label, 'File exists but is empty. Open with nano and write at least one sentence.')


def check_sorted_names(r, root, relative, expected_sorted, source_file):
    path   = root / relative
    actual = read(path)
    label  = relative
    if actual is None:
        r.fail(label, f'File not found. Run:  sort {source_file} > {relative}')
        return
    act = [l for l in actual.splitlines() if l]
    exp = expected_sorted
    if len(act) != len(exp):
        r.fail(label, f'Expected {len(exp)} lines, got {len(act)}. '
                      f'Did you save the full sort output with  > ?')
        return
    if sorted(act) != sorted(exp):
        r.fail(label, f'Names do not match {source_file}. '
                      f'Check you read the correct source file.')
        return
    ok, msg = is_sorted(act)
    if not ok:
        r.fail(label, f'Lines are not in ascending alphabetical order: {msg}')
        return
    r.ok(label)


def check_unique_sorted(r, root, relative, expected_unique, source_file):
    path   = root / relative
    actual = read(path)
    label  = relative
    if actual is None:
        r.fail(label, f'File not found. Run:  sort {source_file} | uniq > {relative}')
        return
    act = [l for l in actual.splitlines() if l]
    dup = has_duplicates(act)
    if dup:
        r.fail(label, f"Contains duplicate: '{dup}'. "
                      f"Use  sort {source_file} | uniq  (not  uniq | sort ).")
        return
    ok, msg = is_sorted(act)
    if not ok:
        r.fail(label, f'Lines are not in ascending order: {msg}. '
                      f'Sort before piping to uniq.')
        return
    if sorted(act) != sorted(expected_unique):
        r.fail(label, f'Wrong set of names. Check source file and pipeline.')
        return
    r.ok(label)


def check_counter(r, root, relative, expected_counter, total, source_file, field=None):
    path   = root / relative
    actual = read(path)
    label  = relative
    if actual is None:
        cmd = f'sort {source_file}'
        if field:
            cmd = f'cut -d "|" -f {field} {source_file} | sort'
        r.fail(label, f'File not found. Run:  {cmd} | uniq -c > {relative}')
        return
    parsed, err = parse_counter(actual)
    if err:
        r.fail(label, f'Format error: {err}. Each line must be:  COUNT NAME')
        return
    actual_sum = sum(parsed.values())
    if actual_sum != total:
        r.fail(label, f'Counts sum to {actual_sum}, expected {total}. '
                      f'Did you use the correct source file ({source_file})?')
        return
    if Counter(parsed) != Counter(expected_counter):
        exp_str = ', '.join(f'{v} {k}' for k, v in sorted(expected_counter.items()))
        r.fail(label, f'Wrong groups or counts. Expected: {exp_str}')
        return
    r.ok(label)


def check_cut_ordered(r, root, relative, expected_rows, source_file, field_desc):
    path   = root / relative
    actual = read(path)
    label  = relative
    if actual is None:
        r.fail(label, f'File not found. Run  cut -d "|" -f {field_desc} {source_file} > {relative}')
        return
    act = [l for l in actual.splitlines() if l]
    exp = expected_rows
    if len(act) != len(exp):
        r.fail(label, f'Expected {len(exp)} rows (one per ticket), got {len(act)}.')
        return
    for i, (e, a) in enumerate(zip(exp, act)):
        if e != a:
            r.fail(label, f'Row {i+1} wrong. Expected: {repr(e)}  Got: {repr(a)}. '
                          f'Check field number (-f) and source file.')
            return
    r.ok(label)


def check_diff_file(r, root, relative, expected_diff, before_path, after_path):
    """Verify the student captured a valid diff from before_path -> after_path."""
    path   = root / relative
    actual = read(path)
    label  = relative
    if actual is None:
        r.fail(label, f'File not found. Run:  diff {before_path} {after_path} > {relative}')
        return
    if not actual.strip():
        r.fail(label, f'File is empty. Did you use  >  to save the diff output?')
        return

    b_lines = [l for l in (read(root / before_path) or '').splitlines() if l.strip()]
    a_lines = [l for l in (read(root / after_path) or '').splitlines() if l.strip()]

    # Reject: swapped order
    if actual.strip() == norm(normal_diff(a_lines, b_lines)).strip():
        r.fail(label, f'Files were compared in the wrong order. '
                      f'Put the OLDER file first:  diff {before_path} {after_path}')
        return

    # Accept any recognised diff format: normal (< >), unified (--- +++), context (*** ---)
    lines = actual.splitlines()
    has_markers = any(
        l.startswith('< ') or l.startswith('> ')   # normal format
        or l.startswith('--- ') or l.startswith('+++ ')  # unified format
        or l.startswith('*** ')                     # context format
        or (l and l[0] in '0123456789')             # hunk header line
        for l in lines
    )
    if not has_markers:
        r.fail(label, f'No diff output found. Run:  diff {before_path} {after_path} > {relative}')
        return

    # The outcome (work/mission/tasklist.txt) is verified separately by check_exact.
    r.ok(label)




def check_evidence_preserved(r, root, source):
    failed = []
    for relative, content in source.items():
        if relative.startswith('work/'):
            continue
        path   = root / relative
        actual = read(path)
        if actual is None:
            failed.append(f'{relative} (missing)')
        elif actual != norm(content):
            failed.append(f'{relative} (modified)')
    if failed:
        r.fail('Original evidence files preserved',
               'Modified files: ' + '; '.join(failed[:3]) +
               '. Evidence files must not be edited. Ask instructor for a new attempt.')
    else:
        r.ok('Original evidence files preserved')


# ── Main validation ───────────────────────────────────────────────────────────

def validate(lab_root, student_id):
    lab_root = Path(lab_root)
    source   = make_data(student_id)

    identity = dict(
        line.split('=', 1)
        for line in source['identity.txt'].splitlines()
        if '=' in line
    )
    shift_id   = identity['SHIFT_ID']
    room       = identity['ROOM']
    start_time = identity['START']

    owners   = [l for l in source['evidence/ticket-owners.txt'].splitlines() if l]
    tickets  = [l for l in source['evidence/tickets.txt'].splitlines() if l]
    m_rows   = [l for l in source['mission/tickets.txt'].splitlines() if l]

    log_lines  = source['evidence/incident-log.txt'].splitlines()
    active_idx = next(
        i for i, l in enumerate(log_lines) if l.startswith('SHIFT LOG - ACTIVE')
    )
    shift_instruction = log_lines[active_idx + 1] + '\n'

    handover_correct = (
        f'Shift: {shift_id}\nRoom: {room}\nStart: {start_time}\nBring your access card.\n'
    )

    owners_sorted     = sorted(owners)
    unique_owners     = sorted(set(owners))
    owner_counts      = Counter(owners)
    ticket_owner_list = [row.split('|')[1] for row in tickets]
    id_cat_list       = [row.split('|')[0] + '|' + row.split('|')[2] for row in tickets]
    cat_counts        = Counter(row.split('|')[2] for row in tickets)
    m_names           = [row.split('|')[1] for row in m_rows]
    m_cats            = [row.split('|')[2] for row in m_rows]
    m_unique          = sorted(set(m_names))
    m_cat_counts      = Counter(m_cats)

    fix_scores_desc   = fixture('scores-desc.txt')
    fix_tasklist_appr = fixture('tasklist-approved.txt')
    fix_mission_sched = fixture('mission-schedule-approved.txt')
    fix_mission_diff  = fixture('mission-tasklist-diff.txt')

    groups = []

    # Exp 1 — history (interactive)
    r = Results()
    r.ok('history', 'interactive — demonstrate live (history 10, pipe|grep, Ctrl+R, Ctrl+G)')
    groups.append(('Experiment 1  history [interactive]', r))

    # Exp 2 — nano
    r = Results()
    check_exact(r, lab_root, 'work/handover-note.txt', handover_correct)
    check_nonempty(r, lab_root, 'work/summary.txt')
    groups.append(('Experiment 2  nano', r))

    # Exp 3 — less
    r = Results()
    r.ok('less navigation', 'interactive — demonstrate live (Space, b, g, G, /search, n, N, q)')
    check_exact(r, lab_root, 'work/shift-instruction.txt', shift_instruction)
    groups.append(('Experiment 3  less [interactive + file]', r))

    # Exp 4 — sort
    r = Results()
    check_sorted_names(r, lab_root, 'work/owners-sorted.txt', owners_sorted,
                       'evidence/ticket-owners.txt')
    check_exact(r, lab_root, 'work/scores-desc.txt', fix_scores_desc,
                'Fixture: validation/expected/scores-desc.txt')
    groups.append(('Experiment 4  sort', r))

    # Exp 5 — uniq
    r = Results()
    check_unique_sorted(r, lab_root, 'work/unique-owners.txt', unique_owners,
                        'evidence/ticket-owners.txt')
    check_counter(r, lab_root, 'work/owner-counts.txt', owner_counts, len(owners),
                  'evidence/ticket-owners.txt')
    groups.append(('Experiment 5  uniq', r))

    # Exp 6 — cut
    r = Results()
    check_cut_ordered(r, lab_root, 'work/ticket-owners-list.txt',
                      ticket_owner_list, 'evidence/tickets.txt', '2')
    check_cut_ordered(r, lab_root, 'work/id-category.txt',
                      id_cat_list, 'evidence/tickets.txt', '1,3')
    check_counter(r, lab_root, 'work/category-counts.txt', cat_counts, len(tickets),
                  'evidence/tickets.txt', field='3')
    groups.append(('Experiment 6  cut', r))

    # Exp 7 — diff
    r = Results()
    check_exact(r, lab_root, 'work/tasklist.txt', fix_tasklist_appr,
                'Fixture: validation/expected/tasklist-approved.txt')
    groups.append(('Experiment 7  diff', r))

    # Mission
    r = Results()
    r.ok('less (mission/brief.txt)', 'interactive — verify live: find HANDOVER-APPROVED, skip HANDOVER-OLD')
    check_exact(r, lab_root, 'work/mission/handover-note.txt', handover_correct)
    check_unique_sorted(r, lab_root, 'work/mission/open-tickets.txt', m_unique,
                        'mission/tickets.txt')
    check_counter(r, lab_root, 'work/mission/category-counts.txt', m_cat_counts,
                  len(m_rows), 'mission/tickets.txt', field='3')
    check_diff_file(r, lab_root, 'work/mission/tasklist-diff.txt', fix_mission_diff,
                    'mission/schedule-before.txt', 'mission/schedule-approved.txt')
    check_exact(r, lab_root, 'work/mission/tasklist.txt', fix_mission_sched,
                'Fixture: validation/expected/mission-schedule-approved.txt')
    groups.append(('Independent Mission', r))

    # Evidence integrity
    r = Results()
    check_evidence_preserved(r, lab_root, source)
    groups.append(('Evidence integrity', r))

    return groups


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    lab_root = Path.cwd()

    if not lab_root.name.startswith('lab2-') or not valid_id(lab_root.name[5:]):
        sys.exit(
            'Run from your lab-work/lab2-<ID>/ folder:\n'
            '  cd lab-work/lab2-<your-ID>\n'
            '  python3 ../../validation/check.py'
        )

    student_id = lab_root.name[5:]
    data = make_data(student_id)
    shift_id = next(
        l.split('=')[1] for l in data['identity.txt'].splitlines()
        if l.startswith('SHIFT_ID')
    )

    print('Campus IT Service Desk Handover Lab  --  Validation Report')
    print('=' * 57)
    print(f'Attempt : {lab_root.name}')
    print(f'Shift   : {shift_id}')
    print(f'Checker : validation/check.py  [read-only]')

    groups = validate(lab_root, student_id)

    total_pass  = 0
    total_items = 0
    any_fail    = False

    for title, r in groups:
        p, t = r.summary()
        total_pass  += p
        total_items += t
        if not r.all_passed():
            any_fail = True
        r.print_group(title)

    print(f'\n{"=" * 57}')
    print(f'Result : {total_pass}/{total_items} checks passed')

    if any_fail:
        print('\nFix the FAIL items shown above and run this checker again.')
    else:
        print('\nAll automated checks passed.')

    print('\n[!] history, nano and less require a live interactive demonstration.')
    print('    A full pass here does not replace the instructor walkthrough.')
    print()

    return 0 if not any_fail else 1


if __name__ == '__main__':
    sys.exit(main())
