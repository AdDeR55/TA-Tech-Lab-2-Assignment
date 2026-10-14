# Campus IT Service Desk Handover Lab

> **Lab 2 — Terminal Tools**  
> Scenario: AlgoUniversity campus IT Support Centre  
> Tools: history · nano · less · sort · uniq · cut · diff

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=AdDeR55%2FTA-Tech-Lab-2-Assignment)


---

## What this lab is

You are the incoming early-morning technician at the campus IT support desk.
The outgoing technician left imperfect records: a handover note with the wrong
room and start time, a ticket log with duplicate entries, and two conflicting
versions of today's task list.

You will use seven terminal tools to investigate, repair and validate the
records before the help desk opens.

**Tools covered:** `history`, `nano`, `less`, `sort`, `uniq`, `cut`, `diff`  
**Expected time:** 90–100 minutes  
**Student lab book:** `lab-book/campus-it-handover-lab.pdf`

---

## Quick start (local or Codespace)

### 1. Prerequisites

The lab requires Bash, Python 3, and the standard Unix tools listed above.
On Ubuntu/Debian these are already installed. Verify with:

```bash
bash scripts/verify_environment.sh
```

### 2. Create your lab attempt

Run from the repository root:

```bash
bash start.sh
```

Enter your instructor-assigned ID when prompted.  
Run the exact `cd` command that setup prints.  
Then run `pwd` and `cat identity.txt` to confirm.

**Reusing an ID preserves your existing work.**  
To start a completely fresh attempt, ask your instructor for a new ID.

### 3. Follow the student lab book

Open `lab-book/campus-it-handover-lab.pdf` and work through the seven
experiments and the independent mission in order.

Begin every experiment from your lab root — the folder printed by `pwd`
after setup.

### 4. Check your work

From your lab root (`lab-work/lab2-<ID>/`):

```bash
python3 ../../check.py
```

The checker reads 16 result files and verifies that original evidence is
unchanged (17 checks total).  
**It does not upload, repair or submit your work.**

- `PASS` — file matches the expected result  
- `CHECK` — file is missing, empty, or incorrect

Fix any `CHECK` items, then run the checker again.

---

## Folder layout (inside your lab attempt)

```
lab-work/lab2-<ID>/
  identity.txt          Your shift code, room, start time and technician name.

  evidence/             Original records — never edit these files.
    incident-log.txt    Long shift log; read with less.
    ticket-owners.txt   Names with duplicates; used with sort and uniq.
    severity-scores.txt Numeric scores; used with sort -n.
    tickets.txt         Pipe-delimited records; used with cut.
    tasklist-before.txt Old task list; used with diff.
    tasklist-approved.txt Approved task list.

  mission/              Fresh evidence for the independent mission — never edit.
    brief.txt           Long briefing; read with less to find HANDOVER-APPROVED.
    handover-draft.txt  Original draft (do not edit — use work/mission/ copy).
    tickets.txt         Mission ticket records.
    schedule-before.txt Mission old schedule.
    schedule-approved.txt Mission approved schedule.

  work/                 Your working files — edit only files in here.
    handover-note.txt   Starts as a draft with errors; repair with nano.
    tasklist.txt        Starts as the old task list; repair with nano.
    shift-instruction.txt   You create this in Experiment 3.
    owners-sorted.txt       You create this in Experiment 4.
    scores-desc.txt         You create this in Experiment 4.
    unique-owners.txt       You create this in Experiment 5.
    owner-counts.txt        You create this in Experiment 5.
    ticket-owners-list.txt  You create this in Experiment 6.
    id-category.txt         You create this in Experiment 6.
    category-counts.txt     You create this in Experiment 6.
    summary.txt             You create this in Experiment 2.
    mission/                Your mission deliverables.
      handover-note.txt     Starts as draft; repair with nano.
      tasklist.txt          Starts as old schedule; repair with nano.
      open-tickets.txt      You create in Mission step 3.
      category-counts.txt   You create in Mission step 4.
      tasklist-diff.txt     You create in Mission step 5.
```

---

## Safe reset

**Resetting your work/ folder** regenerates only the initial working copies.
Evidence and mission files are never touched.  
**Confirmation is required before anything is deleted.**

```bash
bash scripts/reset_work.sh <your-ID>
```

To start completely fresh, ask your instructor for a new ID and run setup again.

---

## For instructors / reviewers

- **Reviewer notes, tool mapping and improvements:** `REVIEWER_NOTES.md`
- **Data design and expected outputs:** `docs/data-design.md`
- **Requirement coverage matrix:** `docs/requirement-matrix.md`
- **Originality plan:** `docs/originality-plan.md`

Verify the environment in a fresh Codespace with:

```bash
bash scripts/verify_environment.sh
```

The checker source (`check.py`) and generator (`setup.py`) are visible
practice materials, not exam-security mechanisms.
