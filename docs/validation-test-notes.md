# Validation Test Notes — Campus IT Service Desk Handover Lab
<!-- Phase 5 evidence. All tests run 2026-10-13 on Windows (local-test ID). -->

---

## Validation System Overview

| File | Role |
|---|---|
| `validation/check.py` | Comprehensive checker — 20 checks, grouped by experiment, actionable feedback |
| `validation/expected/scores-desc.txt` | Fixture: numeric descending sort of severity scores (all IDs) |
| `validation/expected/tasklist-approved.txt` | Fixture: approved task list (all IDs) |
| `validation/expected/mission-schedule-approved.txt` | Fixture: approved mission schedule (all IDs) |
| `validation/expected/mission-tasklist-diff.txt` | Fixture: expected diff of mission schedule pair (all IDs) |
| `check.py` (root) | Legacy student-facing checker — 17 checks (plain PASS/CHECK) |

**Invocation (from lab folder):**
```bash
python3 ../../validation/check.py
```

---

## Tests Completed Locally

### TEST 1 — Fresh attempt; no result files written

**Condition:** `lab-work/lab2-local-test/` created fresh. No `work/` files produced yet.

**Command:**
```bash
cd lab-work/lab2-local-test
python3 ../../validation/check.py
```

**Key output (abridged):**
```
Experiment 2  nano
  FAIL  work/handover-note.txt
        -> Line 2 is wrong. Expected: 'Room: ITSD-6'  Got: 'Room: ITSD-00'
  FAIL  work/summary.txt
        -> File not found. Create it with  nano work/summary.txt  then Ctrl+O, Enter, Ctrl+X.

Experiment 4  sort
  FAIL  work/owners-sorted.txt
        -> File not found. Run:  sort evidence/ticket-owners.txt > work/owners-sorted.txt
  FAIL  work/scores-desc.txt
        -> File not found. Create it with the correct command. Fixture: validation/expected/scores-desc.txt

Experiment 6  cut
  FAIL  work/ticket-owners-list.txt
        -> File not found. Run  cut -d "|" -f 2 evidence/tickets.txt > work/ticket-owners-list.txt

Result : 4/20 checks passed
```
**Exit code:** `1` ✅  
**Verdict:** All missing-file FAILs show the exact corrective command. Evidence integrity PASS (nothing tampered).

---

### TEST 2 — All correct results written programmatically

**Condition:** `write_correct_results.py` writes all 16 correct result files for `local-test` ID.

**Command:**
```bash
python3 ../../validation/check.py
```

**Output:**
```
Result : 20/20 checks passed
All automated checks passed.
```
**Exit code:** `0` ✅  
**Verdict:** Full pass achieved. Both checkers agree (root `check.py` 17/17, `validation/check.py` 20/20).

---

### TEST 3A — Wrong sort order in `work/owners-sorted.txt`

**Condition:** File written in original (unsorted) row order instead of alphabetical.

**Detection:**
```
  FAIL  work/owners-sorted.txt
        -> Lines are not in ascending alphabetical order: 'Cris' should come before ...
```
**Exit code:** `1` ✅  
**Restored and re-verified:** 20/20 ✅

---

### TEST 3B — Duplicate entries in `work/unique-owners.txt` (simulating `uniq|sort` wrong order)

**Condition:** File contains 7 lines with Cris and Elan repeated (simulates wrong pipeline order).

**Detection:**
```
  FAIL  work/unique-owners.txt
        -> Contains duplicate: 'Cris'. Use  sort evidence/ticket-owners.txt | uniq  (not  uniq | sort ).
```
**Exit code:** `1` ✅  
**Restored:** 20/20 ✅

---

### TEST 3C — Bad counter format in `work/owner-counts.txt`

**Condition:** File written as `Bea-1`, `Cris-3`... (hyphen separator instead of `COUNT NAME` space format).

**Detection:**
```
  FAIL  work/owner-counts.txt
        -> Format error: line 'Bea-1' is not in COUNT NAME format. Each line must be:  COUNT NAME
```
**Exit code:** `1` ✅  
**Restored:** 20/20 ✅

---

### TEST 3D — Diff files compared in wrong order (swapped)

**Condition:** `work/mission/tasklist-diff.txt` written as if `diff approved before` (reverse order).

**Detection:**
```
  FAIL  work/mission/tasklist-diff.txt
        -> Files were compared in the wrong order. Put the OLDER file first:
           diff mission/schedule-before.txt mission/schedule-approved.txt
```
**Exit code:** `1` ✅  
**Verdict:** Checker correctly identifies file-order swap and names the correct command.  
**Restored:** 20/20 ✅

---

### TEST 3E — Repaired `work/tasklist.txt` still contains old content

**Condition:** `work/tasklist.txt` left as `tasklist-before.txt` content (not repaired).

**Detection:**
```
  FAIL  work/tasklist.txt
        -> Line 3 is wrong. Expected: '10:00 Ticket triage'  Got: '09:30 Ticket triage'
```
**Exit code:** `1` ✅  
**Restored:** 20/20 ✅

---

### TEST 3F — Counter sum wrong (one group undercounted)

**Condition:** `work/owner-counts.txt` has `2 Cris` instead of `3 Cris` — sum becomes 7 instead of 8.

**Detection:**
```
  FAIL  work/owner-counts.txt
        -> Counts sum to 7, expected 8. Did you use the correct source file (evidence/ticket-owners.txt)?
```
**Exit code:** `1` ✅  
**Restored:** 20/20 ✅

---

### TEST 4 — Missing output file

**Condition:** `work/scores-desc.txt` deleted after being correctly produced.

**Detection:**
```
  FAIL  work/scores-desc.txt
        -> File not found. Create it with the correct command. Fixture: validation/expected/scores-desc.txt
```
**Exit code:** `1` ✅  
**Restored:** 20/20 ✅

---

### TEST 5 — Tampered evidence file

**Condition:** `evidence/ticket-owners.txt` modified (last name changed to `Xxx`).

**Detection:**
```
Evidence integrity
  FAIL  Original evidence files preserved
        -> Modified files: evidence/ticket-owners.txt (modified). Evidence files must not be edited.
           Ask instructor for a new attempt.
```
**Exit code:** `1` ✅  
**Verdict:** Evidence preservation check fires correctly. Message tells student what to do.  
**Restored:** 20/20 ✅

---

### TEST 6 — Final confirmation after all restorations

**Command:** `python3 ../../validation/check.py`

**Output:**
```
Result : 20/20 checks passed
All automated checks passed.
```
**Exit code:** `0` ✅

---

### TEST 7 — Backward compatibility: root `check.py`

**Command:** `python3 ../../check.py`

**Output:**
```
PASS  work/handover-note.txt
...
PASS  Original evidence files preserved
17/17 checks passed. No files were changed or submitted.
```
**Exit code:** `0` ✅  
**Verdict:** Root checker continues to work. Both checkers may be used interchangeably.

---

### TEST 8 — Fixture files unchanged after all tests

All four fixture files verified byte-for-byte after completing the test suite:

| Fixture | Size | Content verified |
|---|---|---|
| `scores-desc.txt` | 14 B | `100\n35\n12\n7\n2` |
| `tasklist-approved.txt` | 82 B | 4 task lines |
| `mission-schedule-approved.txt` | 71 B | 4 schedule lines |
| `mission-tasklist-diff.txt` | 46 B | `3d2`, `< 11:00 Coffee break`, `4a4`, `> 12:00 Sign-off` |

✅ No fixture was modified by any test.

---

## What the Checker Does NOT Verify (Requires Live Demo)

| Tool | Why it cannot be statically checked |
|---|---|
| `history 10` | Shell history is session-specific; no file is produced |
| `history \| grep grep` | Output depends on in-session command sequence |
| `Ctrl+R` / `Right Arrow` / `Ctrl+G` | Interactive keystroke sequences; no file evidence |
| `nano` open/edit/save/exit | Editing in nano produces a file but the process cannot be observed |
| `nano` reopen-to-verify | Second open produces no file evidence |
| `less` navigation (`Space`, `b`, `g`, `G`) | No output to file |
| `less` search (`/`, `n`, `N`, `q`) | No output to file |

> The checker reports these as **PASS (interactive)** with a note that they must be demonstrated live.
> A full 20/20 score alone does not substitute for the instructor walkthrough.

---

## Tests Still Requiring a GitHub Codespace

The following cannot be verified locally on Windows:

| Test | Reason |
|---|---|
| PDF build via `python3 build_booklet.py` | Requires `pandoc` on Ubuntu; HTML fallback tested locally |
| `bash start.sh` line-ending correctness on Linux | Windows uses CRLF; LF behaviour confirmed in `setup.py` write_bytes logic |
| `less` rendering with proper terminal dimensions | Requires a real terminal, not a Windows console emulator |
| `bash scripts/reset_work.sh` interactive `yes` prompt | Requires Bash; tested conceptually, not run end-to-end |
| `bash scripts/verify_environment.sh` tool smoke tests | Requires Linux tools (`diff --version`, etc.) |
| `python3 ../../validation/check.py` from Codespace shell | Path resolution tested locally; to confirm on Ubuntu |

These will be recorded in `REVIEWER_NOTES.md` after the Codespace walkthrough in Phase 7.

---

## Summary Table

| Test | Condition | Expected | Actual | Pass? |
|---|---|---|---|---|
| T1 | Fresh attempt, no results | FAIL + actionable messages, exit 1 | 4/20, exit 1 | ✅ |
| T2 | All correct results | 20/20, exit 0 | 20/20, exit 0 | ✅ |
| T3A | Sort order wrong | FAIL + ordering message | FAIL detected | ✅ |
| T3B | Duplicates in unique file | FAIL + duplicate + pipeline hint | FAIL detected | ✅ |
| T3C | Bad counter format | FAIL + format error | FAIL detected | ✅ |
| T3D | Diff files swapped | FAIL + "Put OLDER file first" + correct command | FAIL detected | ✅ |
| T3E | Repaired file still old | FAIL + line number + expected vs got | FAIL detected | ✅ |
| T3F | Counter sum wrong | FAIL + "sum to 7, expected 8" | FAIL detected | ✅ |
| T4 | Missing output file | FAIL + corrective command | FAIL detected | ✅ |
| T5 | Tampered evidence | FAIL + filename + instructor advice | FAIL detected | ✅ |
| T6 | All restored | 20/20, exit 0 | 20/20, exit 0 | ✅ |
| T7 | Root `check.py` compat | 17/17, exit 0 | 17/17, exit 0 | ✅ |
| T8 | Fixture integrity | No fixture modified | All unchanged | ✅ |
