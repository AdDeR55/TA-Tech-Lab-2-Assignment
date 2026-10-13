#!/usr/bin/env python3
"""
setup.py  —  Campus IT Service Desk Handover Lab
Generates deterministic, ID-seeded lab data in lab-work/lab2-<ID>/.
An existing attempt folder is never overwritten (same ID = work preserved).
Use --reset-work <ID> to regenerate only the work/ files.

Datasets and expected outputs are documented in docs/data-design.md.
"""
import hashlib
import os
import re
import shlex
import sys
from pathlib import Path

def _bash_path(p):
    """Return a shell-safe cd argument.

    Under Git Bash on Windows (MSYSTEM is set), convert Windows paths like
    E:\\Foo\\Bar to /e/Foo/Bar so the printed cd command works without quoting.
    Elsewhere (Linux, macOS, Codespace) use shlex.quote as before.
    """
    if os.environ.get('MSYSTEM'):
        posix = str(p).replace('\\', '/')
        if len(posix) >= 2 and posix[1] == ':':
            posix = '/' + posix[0].lower() + posix[2:]
        return posix
    return shlex.quote(str(p))

def valid_id(value):
    """1–24 ASCII letters/digits/hyphens/underscores, starting with letter/digit."""
    return re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,23}', value) is not None

def make_data(student_id):
    """Return a dict of {relative_path: text_content} for the given student ID.

    All values are deterministic: the same ID always produces the same files.
    Raises ValueError for invalid IDs.
    """
    if not valid_id(student_id):
        raise ValueError(
            'Use 1–24 letters/digits, hyphens or underscores; begin with a letter/digit.'
        )

    digest = hashlib.sha256(student_id.encode()).hexdigest()
    seed   = int(digest[:8], 16)

    shift_code = 'SHF-' + digest[:6].upper()
    room       = 'ITSD-' + str(1 + seed % 6)
    start_time = ['08:30', '09:00', '09:30'][seed % 3]
    desk       = 'Desk-' + str(1 + seed % 6)
    instruction = (
        f'Report to {desk} in {room} at {start_time} for the shift briefing.'
    )

    exp_base = ['Bea', 'Cris', 'Elan', 'Juno']
    e_off    = seed % 4
    N        = exp_base[e_off:] + exp_base[:e_off]
    technician = N[0]

    miss_base = ['Kofi', 'Priya', 'Sona']
    m_off     = seed % 3
    M         = miss_base[m_off:] + miss_base[:m_off]

    owners = [N[0], N[1], N[1], N[2], N[0], N[3], N[0], N[1]]

    ticket_cats = [
        'Network', 'Hardware', 'Network', 'Access',
        'Software', 'Hardware', 'Network', 'Software',
    ]
    tickets = [
        f'T{i+1:02d}|{owners[i]}|{ticket_cats[i]}' for i in range(len(owners))
    ]

    scores = ['35', '100', '2', '12', '7']

    tasklist_before   = (
        '08:00 System checks\n'
        '09:00 Help desk open\n'
        '09:30 Ticket triage\n'
        '10:00 Lunch cover\n'
    )
    tasklist_approved = (
        '08:00 System checks\n'
        '09:00 Help desk open\n'
        '10:00 Ticket triage\n'
        '11:00 Shift handover\n'
    )

    log = [f'{i:03d} Routine IT support log entry {i}.' for i in range(1, 111)]
    log[12:15] = [
        'SHIFT LOG - ARCHIVED',
        'Report to Desk-0 in ITSD-00 at 00:00 for the shift briefing.',
        'This record is outdated. Do not use.',
    ]
    log[57:60] = [
        f'SHIFT LOG - ACTIVE {shift_code}',
        instruction,
        'This is the current instruction for your shift.',
    ]
    log[92:95] = [
        'SHIFT LOG - OTHER SHIFT',
        'Report to Desk-9 in ITSD-09 at 16:00 for the shift briefing.',
        'This record applies to a different shift.',
    ]

    handover_draft = (
        f'Shift: {shift_code}\n'
        f'Room: ITSD-00\n'
        f'Start: 00:00\n'
        f'Bring your access card.\n'
    )

    m_owners = [M[1], M[0], M[1], M[2], M[0], M[1], M[2], M[0]]
    m_cats   = [
        'Software', 'Network', 'Hardware', 'Software',
        'Network',  'Network', 'Hardware', 'Software',
    ]
    mission_tickets = [
        f'R{i+1:02d}|{m_owners[i]}|{m_cats[i]}' for i in range(len(m_owners))
    ]

    schedule_before   = (
        '10:00 Briefing\n'
        '10:30 Account setup\n'
        '11:00 Coffee break\n'
        '11:30 Hardware check\n'
    )
    schedule_approved = (
        '10:00 Briefing\n'
        '10:30 Account setup\n'
        '11:30 Hardware check\n'
        '12:00 Sign-off\n'
    )

    brief = [
        f'{i:03d} Shift handover preparation note {i}.' for i in range(1, 91)
    ]
    brief[15:20] = [
        'HANDOVER - OLD',
        'Shift: SHF-000000',
        'Room: ITSD-00',
        'Start: 00:00',
        'Do not use this archived notice.',
    ]
    brief[62:68] = [
        f'HANDOVER - APPROVED {shift_code}',
        'Use these four lines for the final handover note:',
        f'Shift: {shift_code}',
        f'Room: {room}',
        f'Start: {start_time}',
        'Bring your access card.',
    ]

    files = {
        'identity.txt': (
            f'SHIFT_ID={shift_code}\n'
            f'TECHNICIAN={technician}\n'
            f'ROOM={room}\n'
            f'START={start_time}\n'
        ),
        'evidence/ticket-owners.txt':    '\n'.join(owners) + '\n',
        'evidence/severity-scores.txt':  '\n'.join(scores) + '\n',
        'evidence/tickets.txt':          '\n'.join(tickets) + '\n',
        'evidence/tasklist-before.txt':  tasklist_before,
        'evidence/tasklist-approved.txt': tasklist_approved,
        'evidence/incident-log.txt':     '\n'.join(log) + '\n',
        'mission/brief.txt':             '\n'.join(brief) + '\n',
        'mission/handover-draft.txt':    handover_draft,
        'mission/tickets.txt':           '\n'.join(mission_tickets) + '\n',
        'mission/schedule-before.txt':   schedule_before,
        'mission/schedule-approved.txt': schedule_approved,
        'work/handover-note.txt':         handover_draft,
        'work/tasklist.txt':              tasklist_before,
        'work/mission/handover-note.txt': handover_draft,
        'work/mission/tasklist.txt':      schedule_before,
    }
    return files

def write_files(files, destination):
    """Write all files to destination directory. Parent dirs created as needed.

    Files are written in binary mode so that \n line endings are preserved
    exactly on all platforms (no \r\n translation on Windows).
    """
    destination = Path(destination)
    for relative, content in files.items():
        path = destination / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content.encode('utf-8'))

def work_files(files):
    """Return only the work/ subset of a files dict."""
    return {k: v for k, v in files.items() if k.startswith('work/')}

def create_attempt(student_id, lab_root):
    """Create a new attempt folder. Raises FileExistsError if it already exists."""
    files       = make_data(student_id)
    destination = Path(lab_root) / ('lab2-' + student_id)
    if destination.is_symlink():
        raise OSError('This path is a symbolic link. Ask your instructor for a new ID.')
    destination.mkdir(parents=True, exist_ok=False)
    write_files(files, destination)
    return destination

def reset_work_only(student_id, lab_root):
    """Delete and regenerate only work/ inside an existing attempt."""
    destination = Path(lab_root) / ('lab2-' + student_id)
    if not destination.is_dir():
        raise FileNotFoundError(f'No attempt found at {destination}')
    work_dir = destination / 'work'
    if work_dir.exists():
        import shutil
        shutil.rmtree(work_dir)
    files = make_data(student_id)
    write_files(work_files(files), destination)
    return destination

def lab_root_from_script():
    """lab-work/ sibling to the directory containing this script."""
    return Path(__file__).resolve().parent / 'lab-work'

def main():
    lab_root = lab_root_from_script()

    if len(sys.argv) == 3 and sys.argv[1] == '--reset-work':
        student_id = sys.argv[2].strip()
        if not valid_id(student_id):
            sys.exit('Invalid ID.')
        destination = Path(lab_root) / ('lab2-' + student_id)
        if not destination.is_dir():
            sys.exit(f'No attempt found at {destination}\nRun setup normally first.')
        print(f'\nThis will delete and regenerate  {destination / "work"}')
        print('Evidence and mission files will NOT be changed.')
        answer = input('Type  yes  to continue, anything else to cancel: ').strip().lower()
        if answer != 'yes':
            sys.exit('Reset cancelled. No files were changed.')
        try:
            dest = reset_work_only(student_id, lab_root)
            print(f'\nwork/ reset for {dest.name}.')
            print(f'cd {_bash_path(dest)}')
        except Exception as exc:
            sys.exit(f'Reset failed: {exc}')
        return

    student_id = input(
        'Enter your instructor-assigned lab ID (not your email): '
    ).strip()
    if not valid_id(student_id):
        sys.exit(
            'Invalid ID. Use 1–24 letters/digits, hyphens or underscores; '
            'begin with a letter/digit.'
        )

    destination = Path(lab_root) / ('lab2-' + student_id)
    if destination.is_symlink():
        sys.exit('This attempt path is a symbolic link. Ask your instructor for a new ID.')

    try:
        dest = create_attempt(student_id, lab_root)
    except FileExistsError:
        if not destination.is_dir():
            sys.exit('The attempt path is not a folder. Ask your instructor for a new ID.')
        print('\nThis attempt already exists. Your work has been preserved.')
        dest = destination
    else:
        print('\nLab files created.')

    print('\nMove into your lab folder with this exact command:')
    print('  cd ' + _bash_path(dest))

    id_path = dest / 'identity.txt'
    if id_path.exists():
        id_data = dict(
            line.split('=', 1)
            for line in id_path.read_text(encoding='utf-8').splitlines()
            if '=' in line
        )
        print('\n  Your shift details:')
        print('  ' + '-' * 34)
        for key in ('SHIFT_ID', 'TECHNICIAN', 'ROOM', 'START'):
            val = id_data.get(key, '?')
            print(f'  {key:<12} {val}')
        print('  ' + '-' * 34)
        print('  Write down ROOM and START — you need them in Experiment 2.')

    print('\nThen run:')
    print('  pwd')
    print('\nFollow the student lab book. No commands have been added to your shell history.')

if __name__ == '__main__':
    main()
