# Reviewer Notes — Campus IT Service Desk Handover Lab

> These notes sit outside the 5–10-page student lab book page limit.

---

## 1. Tool-to-Experiment Mapping

| Experiment | Tool(s) | Activity |
|---|---|---|
| 1 | history | history 10; pipe+grep filter; Ctrl+R search (repeat); Right Arrow to edit; Ctrl+G to cancel |
| 2 | nano | Edit work/handover-note.txt (existing file); create work/summary.txt (new file); Ctrl+O/Enter/Ctrl+X |
| 3 | less | Navigate evidence/incident-log.txt (110 lines); Space/b/g/G; search /SHIFT LOG; n/N between sections; q |
| 4 | sort | Text sort (ticket-owners.txt); numeric sort -n (severity-scores.txt); reverse -nr; save with > |
| 5 | uniq | Adjacent-only removal demo; sort-before-uniq for distinct; -c count groups; processing-order comparison |
| 6 | cut | Extract field 2 (owner names); extract fields 1,3 (ID+category); quote delimiter; preserve row order |
| 7 | diff | Compare identical files (no output); compare changed files; explain markers; save with >; nano repair; verify |
| Mission | All 7 | less (find HANDOVER-APPROVED); nano (repair note + tasklist); cut+sort+uniq (open-tickets + counts); diff (save + repair) |

---

## 2. Three Specific Improvements Over the Reference

### Improvement 1 — Explicit processing-order comparison with visible wrong output
The reference mentions processing order but shows only the correct pipeline.
This lab adds a side-by-side exercise in Experiment 5B: learners run BOTH
`uniq | sort` (wrong) and `sort | uniq` (correct) on the same input.
The wrong output has 7 lines; the correct output has 4.
The error is visually unmistakable, making the teaching point concrete.

### Improvement 2 — nano covers creating a new file, not only editing
The reference edits only an existing file (work/notice.txt).
Experiment 2C adds an explicit task: create work/summary.txt from scratch using nano.
The lab book explains that nano creates a new file when the path does not yet exist
and uses the same Ctrl+O/Enter/Ctrl+X keys — covering both required nano behaviours.

### Improvement 3 — diff prediction step before the repair
The reference jumps directly from diff output to repair.
Experiment 7A adds a prediction question: "Run diff on two identical files.
What do you observe? What does no output tell you about the two files?"
This anchors the meaning of empty diff output before the learner sees a non-empty diff,
so the final empty-diff verification of the repair has clear meaning.

---

## 3. Expected Results (Reference Solution)

Expected outputs are generated deterministically by check.py using the same seed
as setup.py. Run the checker on a fresh attempt to see PASS/CHECK for each file.

### Base-case values (ID = local-test, for illustration only)

```
SHIFT_ID  : SHF-2D9F44  (varies by ID)
TECHNICIAN: Elan
ROOM      : ITSD-5
START     : 09:00
```

Key outputs are documented with field-by-field verification in `docs/data-design.md`.

The following are **fixed for all students** (not ID-seeded):

| File | Value |
|---|---|
| evidence/severity-scores.txt | 35 / 100 / 2 / 12 / 7 |
| work/scores-desc.txt | 100 / 35 / 12 / 7 / 2 |
| evidence/tasklist-before.txt | 4 fixed lines |
| evidence/tasklist-approved.txt | 4 fixed lines |
| Exp 7 diff output | 3,4c3,4 block |
| mission/schedule-before.txt | 4 fixed lines |
| mission/schedule-approved.txt | 4 fixed lines |
| Mission diff (tasklist-diff.txt) | 3d2 / 4a4 block |

---

## 4. Checker Tests

17 checks: 16 result files + 1 evidence-preservation check.

| # | File | Match type |
|---|---|---|
| 1 | work/handover-note.txt | Exact (4 lines) |
| 2 | work/shift-instruction.txt | Exact (1 line) |
| 3 | work/owners-sorted.txt | Exact (8 lines) |
| 4 | work/scores-desc.txt | Exact (5 lines) |
| 5 | work/unique-owners.txt | Exact (4 lines) |
| 6 | work/owner-counts.txt | Flexible counter |
| 7 | work/ticket-owners-list.txt | Exact (8 lines) |
| 8 | work/id-category.txt | Exact (8 lines) |
| 9 | work/category-counts.txt | Flexible counter |
| 10 | work/tasklist.txt | Exact (4 lines) |
| 11 | work/summary.txt | Non-empty |
| 12 | work/mission/handover-note.txt | Exact (4 lines) |
| 13 | work/mission/open-tickets.txt | Exact (3 lines) |
| 14 | work/mission/category-counts.txt | Flexible counter |
| 15 | work/mission/tasklist-diff.txt | Exact (normal diff) |
| 16 | work/mission/tasklist.txt | Exact (4 lines) |
| 17 | Original evidence files preserved | Byte comparison |

---

## 5. Timing

| Section | Estimated time |
|---|---|
| Setup + identity check | 5 min |
| Experiment 1 — history | 8 min |
| Experiment 2 — nano | 10 min |
| Experiment 3 — less | 8 min |
| Experiment 4 — sort | 10 min |
| Experiment 5 — uniq | 10 min |
| Experiment 6 — cut | 10 min |
| Experiment 7 — diff | 10 min |
| Independent mission | 17 min |
| Checker + exit questions | 10 min |
| **Total** | **98 min (~100 min)** |

**Expected learner completion time:** 90–100 minutes

**Actual time spent (TA):** _to be filled after walkthrough recording_

---

## 6. Blockers and Assumptions

| Item | Detail |
|---|---|
| Windows dev environment | Project developed locally on Windows using Antigravity IDE. All scripts written for Bash (Linux/Codespace). Python scripts tested locally with Windows Python. |
| Fresh Codespace verification | Not yet run — scheduled for Phase 7 after GitHub publication. |
| history interactive demo | Cannot be automated. Requires live instructor observation or walkthrough recording. |
| nano/less interactive demo | Same as above. Checker prints a reminder. |
| PDF build | Requires Phase 4 (build_booklet.py). Lab book source (.md) is complete. |

---

## 7. AI-Use Disclosure

This project was developed with Antigravity IDE (AI coding assistant) as
implementation partner.

**What the AI did:**
- Read and summarised the assignment PDFs
- Proposed the scenario, folder structure, and experiment dependency chain
- Drafted setup.py, check.py, README.md, REVIEWER_NOTES.md, and all docs/
- Drafted the student lab book source (lab-book/campus-it-handover-lab.md)
- Verified all expected outputs independently via Python scripts

**What the TA personally did / must do:**
- Reviewed and approved all design decisions phase by phase
- Will run setup.py and every experiment in the terminal before recording
- Will verify all 17 checker results against actual outputs
- Will record the teaching walkthrough independently (face, voice, explanations)
- Will explain every command in their own words during the walkthrough

**What is not AI-generated:**
- The teaching walkthrough recording
- The written observation answers in the student booklet
- Any live demonstration during class

All datasets are original. Scenario, file names, staff names, categories and
exercise wording differ substantially from the reference booklet. See
`docs/originality-plan.md` for a full comparison.
