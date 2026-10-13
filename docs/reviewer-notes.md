# Reviewer Notes — Campus IT Service Desk Handover Lab
<!-- For examiner use only. Not included in the student lab book. -->

---

## 1. Expected Results (Reference Solution)

All expected outputs are generated deterministically from the student's
assigned ID. The checker at `validation/check.py` computes these at runtime
using `setup.py:make_data(student_id)`. Fixed outputs (same for every ID)
are stored as auditable fixture files in `validation/expected/`.

### Fixed fixtures (identical for all IDs)

| File | Content |
|---|---|
| `validation/expected/scores-desc.txt` | `100`, `35`, `12`, `7`, `2` |
| `validation/expected/tasklist-approved.txt` | 4-line approved task list |
| `validation/expected/mission-schedule-approved.txt` | 4-line mission schedule |
| `validation/expected/mission-tasklist-diff.txt` | `3d2` / `4a4` block |

### ID-seeded outputs (vary per student)

| Output file | Derived from |
|---|---|
| `work/handover-note.txt` | `SHIFT_ID`, `ROOM`, `START` from `identity.txt` |
| `work/shift-instruction.txt` | `SHIFT LOG - ACTIVE` line in `evidence/incident-log.txt` |
| `work/owners-sorted.txt` | `evidence/ticket-owners.txt` sorted alphabetically |
| `work/unique-owners.txt` | Same, deduplicated with `sort \| uniq` |
| `work/owner-counts.txt` | Same, with occurrence counts via `sort \| uniq -c` |
| `work/ticket-owners-list.txt` | Field 2 of `evidence/tickets.txt` (cut) |
| `work/id-category.txt` | Fields 1,3 of `evidence/tickets.txt` (cut) |
| `work/category-counts.txt` | Field 3 categories counted via `cut \| sort \| uniq -c` |
| `work/mission/handover-note.txt` | Same values as main handover note |
| `work/mission/open-tickets.txt` | Field 2 of `mission/tickets.txt`, sorted + deduped |
| `work/mission/category-counts.txt` | Field 3 of `mission/tickets.txt` counted |

### Reference values for local-test ID

```
SHIFT_ID=SHF-A9A3F0   TECHNICIAN=Cris   ROOM=ITSD-6   START=09:30
```

Evidence ticket-owners.txt: Cris, Elan, Elan, Juno, Cris, Bea, Cris, Elan
Sorted unique: Bea, Cris, Elan, Juno
Owner counts: 1 Bea, 3 Cris, 3 Elan, 1 Juno (sum = 8)
Category counts: 1 Access, 2 Hardware, 3 Network, 2 Software (sum = 8)
Mission unique owners: Kofi, Priya, Sona
Mission category counts: 2 Hardware, 3 Network, 3 Software (sum = 8)

---

## 2. Tool-to-Experiment Mapping

| Tool | Experiment | Behaviours covered |
|---|---|---|
| `history` | 1, Mission Step 7 | `history 10`; `history \| grep`; `Ctrl+R`; repeated `Ctrl+R`; `Right Arrow` to edit; execute; `Ctrl+G` to cancel |
| `nano` | 2, 3C, 7C, Mission 2, Mission 6 | Edit existing; create new; `Ctrl+O` + Enter; `Ctrl+X`; reopen to verify |
| `less` | 3, Mission Step 1 | `Space`, `b`, `g`, `G`; `/search`, `n`, `N`, `q`; distinguish 3 tagged sections |
| `sort` | 4 | Text (default); `-n` numeric; `-nr` descending; redirect `>`; explain text vs numeric difference |
| `uniq` | 5 | Adjacent-only demo; `sort \| uniq` correct vs `uniq \| sort` wrong; `-c` counts; sum reconciliation |
| `cut` | 6 | `-d "\|"` quoting required; `-f 2` single field; `-f 1,3` multiple fields; row-order preservation |
| `diff` | 7, Mission 5/6 | Identical files; before vs approved; `c`, `d`, `a` markers explained; save diff; repair with nano; verify with empty diff |

---

## 3. Three Improvements Over the Reference Lab

### Improvement 1 — Explicit wrong-order comparison for uniq (Experiment 5C)

The reference booklet mentions that `sort | uniq` is correct but does not
make learners run the wrong order and compare. This lab requires running
`uniq | sort` and shows a concrete table: 7 lines (wrong) vs 4 lines (correct).
Processing-order awareness becomes observable, not just stated.

### Improvement 2 — nano creates a new file, not only edits (Experiment 2C)

The reference booklet only demonstrates editing an existing file.
This lab adds `nano work/summary.txt` on a non-existent path, proving that
nano's create behaviour uses identical save/exit keys. The learner verifies
with `cat` — covering the full create-save-exit-verify cycle.

### Improvement 3 — All three diff markers shown across the lab (Exp 7B + Mission 5)

The reference booklet's diff examples use only one marker type (`c`).
This lab ensures learners see all three: `c` in Experiment 7B (replace),
`d` and `a` in Mission Step 5 (delete + add). The mission explicitly prompts
learners to compare the markers and understand why they differ.

---

## 4. Timing Estimates

| Audience | Estimated completion |
|---|---|
| Confident beginner | 60–75 minutes |
| Average beginner | 75–100 minutes |
| Learner needing support | Up to 120 minutes |

Experiments 1–7: approx. 8–10 minutes each.
Independent Mission: approx. 20–25 minutes.
Validation run: under 2 minutes.

---

## 5. Actual Time Spent

> **[PLACEHOLDER — fill in honestly before submission]**

| Activity | Time |
|---|---|
| Scenario design and data creation | [X] hours |
| Lab book writing and editing | [X] hours |
| Implementation (setup.py, check.py) | [X] hours |
| Testing and debugging | [X] hours |
| Documentation and reviewer notes | [X] hours |
| Recording walkthrough | [X] hours |
| **Total** | **[X] hours** |

---

## 6. Blockers and Assumptions

| Item | Detail |
|---|---|
| Line endings | `setup.py` uses `write_bytes` to force LF. `check.py` normalises CRLF before comparison. Without this, all checks fail on Windows. |
| No pandoc on Windows | PDF built via browser print locally. Pandoc PDF is produced in the Codespace (Phase 7). |
| Interactive tools | `history`, `nano`, `less` cannot be statically checked. Checker marks them OK (interactive) and reminds student at every run. |
| Codespace not yet verified | Full devcontainer test deferred to Phase 7. |
| `valid_id()` guard | Prevents accidental checker runs from wrong directories. |

---

## 7. AI-Use Disclosure

This project was developed with AI assistance (Google Antigravity IDE).

**What the AI did:**
- Generated the fictional scenario, names, rooms and schedule content.
- Produced first drafts of all Python scripts and Markdown documents.
- Suggested the three improvements over the reference lab.
- Wrote the HTML builder, CSS stylesheet and validation system.

**What I personally reviewed, rewrote or tested:**

> [PLACEHOLDER — replace these examples with your honest account]
>
> - Read every section of the lab book and verified it made sense as a beginner.
> - Ran `bash start.sh` and worked through each experiment in a real terminal.
> - Verified checker output against my own manually produced results.
> - Rewrote [X] sections for clarity or correctness.
> - Changed [Y] for originality reasons.
> - Confirmed the reset script does not delete evidence files.

**What was not done by AI:**
- The live interactive demonstration of `history`, `nano` and `less`.
- Final editorial and submission decisions.

> This disclosure is honest. The project required personal judgment, testing
> and editorial decisions at every phase.

---

## 8. Validation System Summary

| Checker | Invocation | Checks |
|---|---|---|
| `validation/check.py` | `python3 ../../validation/check.py` | 20 checks, grouped, actionable messages |
| `check.py` (root) | `python3 ../../check.py` | 17 checks, plain PASS/CHECK |

Exit `0` = all pass. Exit `1` = one or more failures. Neither modifies any file.

---

## 9. Outstanding Items Before Submission

| Item | Status |
|---|---|
| Codespace launch button in README | Needs GitHub repo URL (Phase 7) |
| pandoc PDF in Codespace | Phase 7 |
| Full Codespace walkthrough | Phase 7 |
| Live demonstration recording | Student to record / instructor to witness |
| Section 5 actual time | Student to fill in |
| Section 7 personal AI-use narrative | Student to fill in |
