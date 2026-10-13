# Codespace Acceptance Report
**Repository:** https://github.com/AdDeR55/TA-Tech-Lab-2-Assignment  
**Branch:** main  
**Commit:** d93a0275c71bde22591fe37d6668a7f70cae09bf  
**Tested by:** [your name]  
**Date:** [fill in]  

---

## Check Results

| # | Check | Command | Expected | Actual | Status |
|---|---|---|---|---|---|
| 1 | Codespace opens | *(launch from GitHub)* | VS Code loads, no error | [fill] | |
| 2 | Working directory | `pwd` | `/workspaces/TA-Tech-Lab-2-Assignment` | [fill] | |
| 3 | All 7 tools available | `which sort uniq cut diff nano less python3` | 7 paths printed | [fill] | |
| 4 | history builtin | `history` | Lists recent commands | [fill] | |
| 5 | start.sh runs | `bash start.sh` → `codespace-test` | Shift details table printed | [fill] | |
| 6 | Lab folder created | `cd lab-work/lab2-codespace-test && ls` | evidence/ identity.txt mission/ work/ | [fill] | |
| 7 | identity.txt readable | `cat identity.txt` | SHIFT_ID ROOM START visible | [fill] | |
| 8 | Checker before work | `python3 ../../validation/check.py` | 4/20, 16 FAIL with hints | [fill] | |
| 9 | sort | `sort evidence/ticket-owners.txt > work/owners-sorted.txt` | 8 alphabetical lines | [fill] | |
| 10 | sort -nr | `sort -nr evidence/severity-scores.txt > work/scores-desc.txt` | 100 first, 2 last | [fill] | |
| 11 | uniq pipeline | `sort evidence/ticket-owners.txt \| uniq > work/unique-owners.txt` | 4 names | [fill] | |
| 12 | uniq -c | `sort evidence/ticket-owners.txt \| uniq -c > work/owner-counts.txt` | counts sum to 8 | [fill] | |
| 13 | cut field 2 | `cut -d "\|" -f 2 evidence/tickets.txt > work/ticket-owners-list.txt` | 8 names | [fill] | |
| 14 | cut fields 1,3 + pipeline | `cut -d "\|" -f 3 evidence/tickets.txt \| sort \| uniq -c > work/category-counts.txt` | category counts | [fill] | |
| 15 | diff | `diff evidence/tasklist-before.txt evidence/tasklist-approved.txt` | 3,4c3,4 block | [fill] | |
| 16 | diff repair | `cp evidence/tasklist-approved.txt work/tasklist.txt && diff work/tasklist.txt evidence/tasklist-approved.txt` | no output | [fill] | |
| 17 | nano (edit) | `nano work/handover-note.txt` fix room/start, Ctrl+O Enter Ctrl+X | file saved | [fill] | |
| 18 | nano (create) | `nano work/summary.txt` type text, save | file created | [fill] | |
| 19 | less navigation | `less evidence/incident-log.txt` Space g G /SHIFT LOG n q | navigation works | [fill] | |
| 20 | Ctrl+R search | `grep ROOM identity.txt` then Ctrl+R type ROOM Right Arrow | match found | [fill] | |
| 21 | Ctrl+G cancel | Ctrl+R type sev Ctrl+G | search cancelled | [fill] | |
| 22 | Mission outputs | all 5 work/mission/ files produced | files present | [fill] | |
| 23 | **Final checker** | `python3 ../../validation/check.py` | **20/20 checks passed** | [fill] | |
| 24 | Deliberate fail | `echo "wrong" > work/scores-desc.txt && python3 ../../validation/check.py` | FAIL detected with fix hint | [fill] | |
| 25 | Fix restores pass | `sort -nr evidence/severity-scores.txt > work/scores-desc.txt && python3 ../../validation/check.py` | 20/20 restored | [fill] | |
| 26 | Evidence preserved | `git diff HEAD -- .` shows no changes to evidence/ | no diff output | [fill] | |
| 27 | Reset script | `bash ../../scripts/reset_work.sh codespace-test` → yes | work/ reset, evidence intact | [fill] | |
| 28 | PDF accessible | download docs/student-lab-book.pdf from GitHub | opens, 8 pages, readable | [fill] | |
| 29 | README badge | click badge on repo homepage | Codespace launches | [fill] | |

---

## Issue Log

| # | Description | Cause | Fix | Re-tested |
|---|---|---|---|---|
| — | None | — | — | — |

---

## Summary verdict

**Overall:** [PASS / FAIL]  
**Signed:** [your name / student ID]  
**Date:** [fill in]
