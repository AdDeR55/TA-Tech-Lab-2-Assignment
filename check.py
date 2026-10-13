#!/usr/bin/env python3
"""
check.py  —  Campus IT Service Desk Handover Lab validator
Run from your lab-work/lab2-<ID> folder:

    python3 ../../check.py

Reads 16 result files and verifies that all original evidence is unchanged:
17 checks in total. Does not upload, repair or delete any files.

The checker is visible source code and not an exam security mechanism.
A passing score alone does not prove how you worked; interactive
demonstrations of history, nano and less are also required.
"""
import difflib
import sys
from collections import Counter
from pathlib import Path

# ── Import make_data from setup.py two levels up ──────────────────────────────
_script_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(_script_dir))
try:
    from setup import make_data, valid_id
except ImportError:
    sys.exit('Cannot find setup.py. Run this checker from lab-work/lab2-ID/ as shown.')


# ── Normal diff (Python reimplementation — same output on all platforms) ───────

def normal_diff(before_lines, after_lines):
    """Produce GNU/BSD normal diff output for simple line sequences."""
    a, b   = before_lines, after_lines
    output = []
    span   = lambda s, e: str(s + 1) if e - s == 1 else f'{s + 1},{e}'
    for kind, i, j, k, l in difflib.SequenceMatcher(
            None, a, b, autojunk=False).get_opcodes():
        if kind == 'equal':
            continue
        if kind == 'replace':
            output += (
                [span(i, j) + 'c' + span(k, l)]
                + ['< ' + v for v in a[i:j]]
                + ['---']
                + ['> ' + v for v in b[k:l]]
            )
        elif kind == 'delete':
            output += [span(i, j) + 'd' + str(k)] + ['< ' + v for v in a[i:j]]
        else:  # insert
            output += [str(i) + 'a' + span(k, l)] + ['> ' + v for v in b[k:l]]
    return '\n'.join(output) + '\n' if output else ''


# ── Counter matching (flexible — accepts any padding and line order) ───────────

def counts_match(actual_text, expected_counter):
    """Return True if actual_text is a valid uniq -c style report for expected_counter."""
    parsed = {}
    try:
        for line in actual_text.splitlines():
            line = line.strip()
            if not line:
                continue
            parts = line.split(None, 1)
            if len(parts) != 2:
                return False
            count_str, value = parts
            if value in parsed or int(count_str) < 1:
                return False
            parsed[value] = int(count_str)
    except (ValueError, TypeError):
        return False
    return parsed == dict(expected_counter)


# ── Expected results ───────────────────────────────────────────────────────────

def expected_results(student_id):
    """Return (source_files, result_dict) for the given student ID."""
    source   = make_data(student_id)
    identity = dict(
        line.split('=', 1) for line in source['identity.txt'].splitlines()
    )
    shift_code = identity['SHIFT_ID']
    room       = identity['ROOM']
    start_time = identity['START']

    # Helpers
    lines = lambda key: source[key].splitlines()
    text  = lambda values: '\n'.join(values) + '\n'

    # 1. work/handover-note.txt
    handover_correct = (
        f'Shift: {shift_code}\nRoom: {room}\n'
        f'Start: {start_time}\nBring your access card.\n'
    )

    # 2. work/shift-instruction.txt (sentence below SHIFT LOG - ACTIVE)
    log_lines  = lines('evidence/incident-log.txt')
    active_idx = next(
        i for i, l in enumerate(log_lines) if l.startswith('SHIFT LOG - ACTIVE')
    )
    shift_instruction = log_lines[active_idx + 1] + '\n'

    # 3. work/owners-sorted.txt
    owners         = lines('evidence/ticket-owners.txt')
    owners_sorted  = text(sorted(owners))

    # 4. work/scores-desc.txt
    scores      = lines('evidence/severity-scores.txt')
    scores_desc = text(sorted(scores, key=int, reverse=True))

    # 5. work/unique-owners.txt
    unique_owners = text(sorted(set(owners)))

    # 6. work/owner-counts.txt  (Counter — flexible match)
    owner_counts = Counter(owners)

    # 7. work/ticket-owners-list.txt (cut -f 2, preserves order)
    ticket_rows       = lines('evidence/tickets.txt')
    ticket_owner_list = text(r.split('|')[1] for r in ticket_rows)

    # 8. work/id-category.txt (cut -f 1,3, preserves order)
    id_category = text(
        '|'.join([r.split('|')[0], r.split('|')[2]]) for r in ticket_rows
    )

    # 9. work/category-counts.txt  (Counter — flexible match)
    category_counts = Counter(r.split('|')[2] for r in ticket_rows)

    # 10. work/tasklist.txt (must match approved)
    tasklist_correct = source['evidence/tasklist-approved.txt']

    # 11. work/summary.txt  — non-empty existence check (open content)
    #     Handled separately in the check loop below.

    # 12. work/mission/handover-note.txt (same correct text as #1)

    # 13. work/mission/open-tickets.txt (cut f2 | sort | uniq)
    m_rows       = lines('mission/tickets.txt')
    m_names      = [r.split('|')[1] for r in m_rows]
    open_tickets = text(sorted(set(m_names)))

    # 14. work/mission/category-counts.txt  (Counter — flexible match)
    m_cat_counts = Counter(r.split('|')[2] for r in m_rows)

    # 15. work/mission/tasklist-diff.txt (normal diff of schedule pair)
    sched_before   = source['mission/schedule-before.txt'].splitlines()
    sched_approved = source['mission/schedule-approved.txt'].splitlines()
    tasklist_diff  = normal_diff(sched_before, sched_approved)

    # 16. work/mission/tasklist.txt (must match approved schedule)
    mission_tasklist = source['mission/schedule-approved.txt']

    results = {
        'work/handover-note.txt':         handover_correct,
        'work/shift-instruction.txt':     shift_instruction,
        'work/owners-sorted.txt':         owners_sorted,
        'work/scores-desc.txt':           scores_desc,
        'work/unique-owners.txt':         unique_owners,
        'work/owner-counts.txt':          owner_counts,          # Counter
        'work/ticket-owners-list.txt':    ticket_owner_list,
        'work/id-category.txt':           id_category,
        'work/category-counts.txt':       category_counts,       # Counter
        'work/tasklist.txt':              tasklist_correct,
        'work/summary.txt':               'NON_EMPTY',           # special marker
        'work/mission/handover-note.txt': handover_correct,
        'work/mission/open-tickets.txt':  open_tickets,
        'work/mission/category-counts.txt': m_cat_counts,        # Counter
        'work/mission/tasklist-diff.txt': tasklist_diff,
        'work/mission/tasklist.txt':      mission_tasklist,
    }
    return source, results


# ── Main check logic ───────────────────────────────────────────────────────────

def check(root, student_id):
    """Return list of (label, passed_bool) for all checks."""
    root     = Path(root)
    source, expected = expected_results(student_id)
    results  = []

    for relative, wanted in expected.items():
        path = root / relative
        label = relative
        try:
            if path.is_symlink():
                ok = False
            else:
                # Normalise CRLF→LF so the checker works on Windows and Linux
                actual = path.read_bytes().decode('utf-8').replace('\r\n', '\n')
                if isinstance(wanted, Counter):
                    ok = counts_match(actual, wanted)
                elif wanted == 'NON_EMPTY':
                    ok = bool(actual.strip())
                else:
                    ok = (actual == wanted)
        except (OSError, UnicodeError):
            ok = False
        results.append((label, bool(ok)))

    # Evidence preservation check
    preserved = True
    evidence_keys = [
        k for k in source
        if not k.startswith('work/')
    ]
    for relative in evidence_keys:
        path = root / relative
        try:
            # Normalise CRLF→LF on both sides for cross-platform safety
            actual_norm   = path.read_bytes().decode('utf-8').replace('\r\n', '\n')
            expected_norm = source[relative].replace('\r\n', '\n')
            preserved &= (
                not path.is_symlink()
                and actual_norm == expected_norm
            )
        except OSError:
            preserved = False
    results.append(('Original evidence files preserved', bool(preserved)))

    return results


# ── CLI ────────────────────────────────────────────────────────────────────────

def main():
    root = Path.cwd()

    # Must be run from lab-work/lab2-<ID>/
    if not root.name.startswith('lab2-') or not valid_id(root.name[5:]):
        sys.exit(
            'Run this checker from your lab-work/lab2-ID folder:\n'
            '  cd lab-work/lab2-<your-ID>\n'
            '  python3 ../../check.py'
        )

    student_id = root.name[5:]
    results    = check(root, student_id)

    total  = len(results)
    passed = sum(ok for _, ok in results)

    for label, ok in results:
        print(('PASS  ' if ok else 'CHECK ') + label)

    print(f'\n{passed}/{total} checks passed. No files were changed or submitted.')
    print(
        'Also complete your written answers and demonstrate '
        'history, nano and less to your instructor.'
    )
    return 0 if passed == total else 1


if __name__ == '__main__':
    sys.exit(main())
