# Campus IT Service Desk Handover Lab
### Lab 2 — Terminal Tools · AlgoUniversity IT Support Centre

---

## Before You Begin

### Your role

You are the incoming early-morning technician at the AlgoUniversity campus
IT Support Centre. The help desk opens in 90 minutes. The outgoing night-shift
technician left three problems in the records:

1. **The handover note** has the wrong room number and the wrong start time.
   They were copied from a draft written two weeks ago.
2. **The ticket ownership log** has duplicate entries — two shift exports were
   merged and nobody ran deduplication.
3. **The task list** is the old working version. The shift supervisor sent an
   approved replacement, but the working copy was never updated.

Your job is to inspect the records, repair the working files, and validate the
result before the next technician arrives.

### What you will produce

By the end of this lab you will have seven clean files in `work/` and five
deliverable files in `work/mission/`. Run the checker at the end to confirm.

### Tools covered

| Experiment | Tool | What you learn |
|---|---|---|
| 1 | `history` | Recall, search and reuse commands |
| 2 | `nano` | Edit and create plain-text files |
| 3 | `less` | Navigate a long file and extract one line |
| 4 | `sort` | Sort lines alphabetically and numerically |
| 5 | `uniq` | Deduplicate lines; count occurrences |
| 6 | `cut` | Extract fields from delimited records |
| 7 | `diff` | Compare file versions; repair working copies |
| Mission | All 7 | Apply every skill on a fresh set of evidence |

### How to start

```bash
bash start.sh
```

Enter your instructor-assigned ID when prompted. Run the `cd` command that
setup prints. Then confirm your location and read your identity file:

```bash
pwd
cat identity.txt
```

`identity.txt` contains four lines. You will use **ROOM** and **START** in
Experiment 2. Note them down now.

```
SHIFT_ID=SHF-xxxxxx      ← your unique shift code
TECHNICIAN=              ← the technician name for this shift
ROOM=ITSD-               ← the correct room (you will need this)
START=                   ← the correct start time (you will need this)
```

> **Work only in your `lab-work/lab2-<ID>/` folder.**
> Begin every experiment from that folder. Run `pwd` if you are unsure.
> Never edit files in `evidence/` or `mission/` — they are the originals.

---

## Experiment 1 — history

### What history does

The shell keeps a numbered list of every command you run. `history` prints
that list. You can search it, reuse a command, or edit one before running it
again. This saves typing and avoids mistakes when repeating complex commands.

### Key commands and keys

| Command or key | What it does |
|---|---|
| `history` | Print the full history list |
| `history 10` | Print the last 10 entries |
| `history \| grep word` | Show only entries containing *word* |
| `Ctrl+R` | Open reverse search; type to find a match |
| `Ctrl+R` again | Jump to the next (older) match |
| `Right Arrow` | Accept the found command for editing |
| `Enter` | Accept and run the found command immediately |
| `Ctrl+G` | Cancel the search without running anything |

---

### 1A — Build a history trail

> **Starting directory:** `lab-work/lab2-<ID>/`  
> Confirm with `pwd` before running any command in this experiment.

Run these three commands. They confirm your identity and create the history
trail you will search in 1B–1D.

```bash
grep SHIFT_ID identity.txt
grep ROOM identity.txt
grep START identity.txt
```

**What do you see?** Write the values for ROOM and START — you will use them
to repair the handover note in Experiment 2.

---

### 1B — Print and filter history

```bash
history 10
```

**What do you see?** You should see the three `grep` commands from 1A near
the bottom of the list, each with a line number.

Now filter history to show only lines that contain the word `grep`:

```bash
history | grep grep
```

**Observation:** The pipe `|` sends the output of `history` into `grep`.
`grep grep` shows only the lines that contain the word "grep".
How many matches appear? What is the line number of your earliest `grep` command?

---

### 1C — Search with Ctrl+R

Press `Ctrl+R`. A search prompt appears:

```
(reverse-i-search)`':
```

Start typing `ROOM`. The shell finds the most recent command containing those
characters:

```
(reverse-i-search)`ROOM': grep ROOM identity.txt
```

Press `Ctrl+R` again to jump to the next older match. Press `Right Arrow`
to accept the command into the prompt — you can then edit it before running it.

**Try this:** Accept the `grep ROOM identity.txt` command and edit it so it
reads `grep START identity.txt`. Run it and check the output.

---

### 1D — Cancel a search

Press `Ctrl+R` and start typing `sev`. Before pressing Enter or Right Arrow,
press `Ctrl+G`.

**What happens?** The search cancels and you return to an empty prompt.
Nothing was run. `Ctrl+G` is the safe exit from Ctrl+R when you change your mind.

> **Connection to Experiment 2:** In the next experiment you will edit
> `work/handover-note.txt`. The ROOM and START values you confirmed in 1A
> are the correct replacements for the wrong values in that file.

---

## Experiment 2 — nano

### What nano does

`nano` is a terminal text editor. It opens a file in your terminal window.
You type to change the content. Named key shortcuts (shown at the bottom of
the screen) save, exit, and navigate.

### Key shortcuts

| Key | Action |
|---|---|
| `Ctrl+O` | Write (save) — then press `Enter` to confirm the filename |
| `Ctrl+X` | Exit nano |
| `Ctrl+K` | Cut the current line |
| `Ctrl+U` | Paste the last cut line |
| Arrow keys | Move the cursor |

> If the screen shows `^O` that means `Ctrl+O`. The caret `^` always means `Ctrl`.

---

### 2A — Edit an existing file

The handover note draft was copied from an old template. It has two errors:
the room number and the start time are both wrong.

Open it in nano:

```bash
nano work/handover-note.txt
```

You will see four lines. Two of them are wrong:

```
Shift: SHF-xxxxxx
Room: ITSD-00          ← wrong — use the ROOM value from identity.txt
Start: 00:00           ← wrong — use the START value from identity.txt
Bring your access card.
```

Use the arrow keys to position your cursor on the `Room:` line.
Replace `ITSD-00` with the correct value from `identity.txt`.
Move to the `Start:` line and replace `00:00` with the correct start time.

---

### 2B — Save, exit, and verify

When both lines are corrected:

1. Press `Ctrl+O` — the status bar asks for the filename
2. Press `Enter` — saves to the same filename
3. Press `Ctrl+X` — exits nano

Verify the changes were saved:

```bash
cat work/handover-note.txt
```

The file should now show the correct room and start time.
Reopen it in nano and check that both values are still correct:

```bash
nano work/handover-note.txt
```

Exit again with `Ctrl+X` (no changes needed — just checking).

---

### 2C — Create a new file

nano can create a brand new file — the same save/exit keys apply.

```bash
nano work/summary.txt
```

The file does not exist yet. nano opens an empty editor.
On the first line, type one sentence describing what the shift handover is for.
Save with `Ctrl+O` and `Enter`. Exit with `Ctrl+X`.

Verify the file was created:

```bash
cat work/summary.txt
```

**What you learned:** `nano filename` edits an existing file **or** creates a
new one if the path does not yet exist. The save and exit keys are identical
in both cases.

> **Connection to Experiment 3:** In the next experiment you will read a
> long log file to find the official shift instruction. It will confirm
> the room and start time you have just saved in the handover note.

---

## Experiment 3 — less

### What less does

`cat` prints an entire file at once. For a long file this floods the screen.
`less` shows the file one screen at a time. You navigate forward and backward,
search for text, and quit when done. The file is never changed.

### Key commands inside less

| Key | Action |
|---|---|
| `Space` | Scroll forward one screen |
| `b` | Scroll backward one screen |
| `g` | Jump to the beginning |
| `G` | Jump to the end |
| `/text` | Search forward for *text* (press `Enter` to start) |
| `n` | Jump to the next match |
| `N` | Jump to the previous match |
| `q` | Quit |

---

### 3A — Navigate the incident log

The shift log is 110 lines — too long to read with `cat`. Open it:

```bash
less evidence/incident-log.txt
```

Practice navigation:

1. Press `Space` several times to scroll forward.
2. Press `b` to scroll backward.
3. Press `G` to jump to the last line.
4. Press `g` to return to the first line.
5. Press `q` to quit.

---

### 3B — Search for your shift section

The log contains three sections tagged `SHIFT LOG`. Only one is current.
Open the log again:

```bash
less evidence/incident-log.txt
```

Search for the tag:

```
/SHIFT LOG
```

Press `Enter`. The first match is **SHIFT LOG - ARCHIVED** — this is an
outdated record. Do not use it.

Press `n` to jump to the next match. You should now see:

```
SHIFT LOG - ACTIVE SHF-xxxxxx
```

Check that the shift code matches **your** shift code from `identity.txt`.
The line immediately below this heading is your shift instruction.

Press `n` once more. You reach **SHIFT LOG - OTHER SHIFT** — this is for a
different shift. Press `N` to go back to **ACTIVE**.

Read the instruction line carefully. Press `q` to quit.

---

### 3C — Save the shift instruction

Create the file `work/shift-instruction.txt` using nano. On the first and only
line, type the exact sentence from the **SHIFT LOG - ACTIVE** section of the
incident log. Save and exit.

Verify it:

```bash
cat work/shift-instruction.txt
```

**Observation:** Compare the room and time in the shift instruction with the
values you saved in `work/handover-note.txt`. They should match. If they do
not, recheck Experiment 2.

> **Connection to Experiments 4 and 5:** Next you will sort and deduplicate
> the ticket ownership log. The names it contains are the technicians who
> currently hold open tickets.

---

## Experiment 4 — sort

### What sort does

`sort` reads lines from a file and writes them in sorted order to the terminal.
By default, sorting is alphabetical (text sort). Flags change the sort order.
The `>` operator saves the output to a file.

### Flags

| Flag | Meaning |
|---|---|
| *(none)* | Alphabetical (text) sort, ascending |
| `-n` | Numeric sort (treats values as numbers, not text) |
| `-r` | Reverse order (descending) |
| `-nr` | Numeric + reverse (largest number first) |

---

### 4A — Sort names alphabetically

> **Starting directory:** `lab-work/lab2-<ID>/`

```bash
sort evidence/ticket-owners.txt
```

The names appear in alphabetical order. Each name appears as many times as
it occurs in the original file — sort does not remove duplicates.

Save the result:

```bash
sort evidence/ticket-owners.txt > work/owners-sorted.txt
cat work/owners-sorted.txt
```

How many lines does the sorted file have? How many unique names do you see?

> **Safe redirect rule:** Always redirect to a *different* file from the one
> you are reading. Never run `sort file > file` — that empties the file
> before sort can read it, destroying the contents.

---

### 4B — Text sort vs numeric sort

The file `evidence/severity-scores.txt` contains five numeric scores.
Print it first:

```bash
cat evidence/severity-scores.txt
```

Now sort it as text (the default):

```bash
sort evidence/severity-scores.txt
```

Then sort it numerically:

```bash
sort -n evidence/severity-scores.txt
```

**Observation:** What is the order in the text sort? What is the order in
the numeric sort? Why does text sort put 100 before 2?

> **Hint:** Text sort compares character by character, left to right.
> The character '1' comes before '2' in the alphabet, so '100' sorts
> before '2' — even though 100 is much larger as a number.

---

### 4C — Numeric descending sort

Sort the severity scores from highest to lowest and save the result:

```bash
sort -nr evidence/severity-scores.txt > work/scores-desc.txt
cat work/scores-desc.txt
```

**Check:** The first line should be `100`. The last line should be `2`.

> **Connection to Experiment 5:** The sorted names from 4A (all duplicates
> included) are the starting point for the deduplication you will do next.

---

## Experiment 5 — uniq

### What uniq does

`uniq` removes **adjacent** duplicate lines. If identical lines are next to
each other, it keeps only the first. Lines that repeat but are not adjacent
are left unchanged.

This means order matters: you usually need to sort before deduplicating.

### Flags

| Flag | Meaning |
|---|---|
| *(none)* | Remove adjacent duplicates |
| `-c` | Count occurrences; prefix each unique line with its count |

---

### 5A — Adjacent duplicates only

```bash
uniq evidence/ticket-owners.txt
```

**Observation:** How many lines are in the output? Is it fewer than the
original? Did all duplicates disappear, or only some?

Look at the original file again:

```bash
cat evidence/ticket-owners.txt
```

Find any two identical names that appear on consecutive lines — these are
**adjacent duplicates**. Find any identical names that appear with other
names in between — these are **separated duplicates**.

`uniq` removes only the adjacent ones. Separated duplicates survive.

---

### 5B — Sort first, then uniq (correct order)

To eliminate all duplicates, sort first so that identical names become adjacent:

```bash
sort evidence/ticket-owners.txt | uniq
```

Save the result:

```bash
sort evidence/ticket-owners.txt | uniq > work/unique-owners.txt
cat work/unique-owners.txt
```

How many lines does this file have?

---

### 5C — Wrong order: what happens if you uniq first?

**Predict:** What do you expect if you run `uniq` before `sort`?

Try it:

```bash
uniq evidence/ticket-owners.txt | sort
```

**Compare the line counts:**

| Command | Lines in output | Duplicates remain? |
|---|---|---|
| `uniq \| sort` (wrong) | **7** | Yes — three names still repeat |
| `sort \| uniq` (correct) | **4** | No |

The wrong order produces 7 lines because `uniq` only removed the one adjacent
duplicate pair before sorting. The three separated duplicates survived into
the sorted output, where they are now adjacent — but `uniq` has already finished.

> **Explanation:** `uniq | sort` removes only the adjacent duplicates first,
> then sorts the remaining lines — but separated duplicates are now sorted
> next to each other without being removed. `sort | uniq` groups all identical
> names first, then removes the adjacent groups.
> **The correct order is always `sort | uniq`.**

---

### 5D — Count occurrences

```bash
sort evidence/ticket-owners.txt | uniq -c
```

Save the result:

```bash
sort evidence/ticket-owners.txt | uniq -c > work/owner-counts.txt
cat work/owner-counts.txt
```

Each line shows a count and a name. The counts should add up to 8
(the total number of lines in the original file).

**Check:** Add the counts. Do they sum to 8?

> **Connection to Experiment 6:** In the next experiment you will extract
> names directly from `evidence/tickets.txt`. You will find that those names
> match the file you have been working with here.

---

## Experiment 6 — cut

### What cut does

`cut` extracts specific fields (columns) from each line of a delimited file.
You tell it the delimiter character and which field numbers to keep.
`cut` preserves the original line order — it does not sort.

### Flags

| Flag | Meaning |
|---|---|
| `-d "char"` | Set the field delimiter to *char* |
| `-f N` | Extract field N (1-indexed) |
| `-f M,N` | Extract fields M and N |

---

### 6A — Extract the owner names from ticket records

The file `evidence/tickets.txt` contains pipe-separated records:

```
T01|Name|Category
T02|Name|Category
...
```

Preview the file:

```bash
cat evidence/tickets.txt
```

Field 1 is the ticket ID. Field 2 is the owner name. Field 3 is the category.
The delimiter is `|`. Because `|` is special in the shell (it creates a pipe),
you must quote it.

Extract field 2 (owner names):

```bash
cut -d "|" -f 2 evidence/tickets.txt
```

Save the result:

```bash
cut -d "|" -f 2 evidence/tickets.txt > work/ticket-owners-list.txt
cat work/ticket-owners-list.txt
```

**Observation:** Compare `work/ticket-owners-list.txt` with
`evidence/ticket-owners.txt` (from Experiments 4 and 5).

```bash
cat evidence/ticket-owners.txt
```

Are they the same? This is not a coincidence — the ticket log and the
ownership register were exported from the same source. Knowing this, you can
trust that the deduplication you did in Experiment 5 covers all open tickets.

---

### 6B — Extract ticket ID and category (skip owner)

Extract fields 1 and 3 together:

```bash
cut -d "|" -f 1,3 evidence/tickets.txt > work/id-category.txt
cat work/id-category.txt
```

**Observation:** The output still uses `|` as the separator between the two
extracted fields. `cut` does not let you change the output delimiter —
it keeps the same one.

---

### 6C — Count tickets per category

Extract just the category field, then count how many tickets belong to each category:

```bash
cut -d "|" -f 3 evidence/tickets.txt | sort | uniq -c
```

Save the result:

```bash
cut -d "|" -f 3 evidence/tickets.txt | sort | uniq -c > work/category-counts.txt
cat work/category-counts.txt
```

**Check:** The counts should add up to 8 (one per ticket). Do they?

**Observation:** This pipeline uses three tools in sequence. Explain in your
own words what each step does:

- `cut -d "|" -f 3 evidence/tickets.txt` →
- `| sort` →
- `| uniq -c` →

> **Connection to Experiment 7:** The task list you have been working toward
> has two versions — before and after supervisor approval. Next you will
> compare them and repair the working copy.

---

## Experiment 7 — diff

### What diff does

`diff` compares two files line by line. If the files are identical, it
produces no output. If they differ, it shows which lines changed and how.
The `>` operator saves the comparison to a file.

### Reading diff output

A diff result uses three kinds of markers:

| Marker | Meaning |
|---|---|
| `Nc,Nd` | Lines N–N in the **first** file **c**hanged or were **d**eleted |
| `<` | A line from the **first** file (the older/left version) |
| `---` | Separates the two sides of a change |
| `>` | A line from the **second** file (the newer/right version) |
| `NaN` | A line was **a**dded to the second file after line N |

The first argument is always the older (before) file.
The second argument is always the newer (after) file.

---

### 7A — Identical files produce no output

**Predict:** What do you think `diff` will print if the two files are the same?

Test it:

```bash
diff evidence/tasklist-approved.txt evidence/tasklist-approved.txt
```

**What do you see?** No output means the files are identical. This matters
for Experiment 7C: after you repair the working copy, running diff should
produce no output.

---

### 7B — Compare the before and after task lists

> **Starting directory:** `lab-work/lab2-<ID>/`

The working copy `work/tasklist.txt` currently contains the old task list.
The file `evidence/tasklist-approved.txt` is the version the supervisor approved.

First, look at both:

```bash
cat evidence/tasklist-before.txt
cat evidence/tasklist-approved.txt
```

Now compare them with diff. Put the older file **first**:

```bash
diff evidence/tasklist-before.txt evidence/tasklist-approved.txt
```

You will see output like this:

```
3,4c3,4
< 09:30 Ticket triage
< 10:00 Lunch cover
---
> 10:00 Ticket triage
> 11:00 Shift handover
```

Reading this output:

| Part | Meaning |
|---|---|
| `3,4` (before `c`) | Lines 3–4 of the **first** (before) file changed |
| `c` | **c**hanged — lines were replaced |
| `3,4` (after `c`) | Lines 3–4 of the **second** (approved) file |
| `<` lines | What the before file had |
| `---` | Separator between old and new |
| `>` lines | What the approved file has |

> `c` means both sides changed. `d` means a line was deleted (no `>` side).
> `a` means a line was added (no `<` side). You will see all three markers
> in the independent mission.

**Questions:**

1. How many lines changed between the two files?
2. Which task had its time shifted? (Look at the `>` lines.)
3. Which task was replaced entirely?

---

### 7C — Repair the working copy

`work/tasklist.txt` currently matches the old (before) version. You need to
update it to match the approved version.

Open it in nano:

```bash
nano work/tasklist.txt
```

Use the diff output from 7B as your guide. Edit the lines that need changing.
Save with `Ctrl+O` and `Enter`. Exit with `Ctrl+X`.

Now verify the repair:

```bash
diff work/tasklist.txt evidence/tasklist-approved.txt
```

**Expected result:** No output. Empty diff means the working copy now matches
the approved version exactly.

If there is output, read it to find what still differs. Open nano again,
make the correction, save, exit, and re-run diff.

---

## Independent Mission

You have now used all seven tools in a guided setting.

The independent mission gives you a fresh set of evidence with the same
scenario — a different batch of records that need the same treatment. No
step-by-step instructions are provided. Apply the skills you practised
in Experiments 1–7.

### Your mission

The night shift left five things incomplete. Produce these five files
in `work/mission/`:

| File | What it must contain |
|---|---|
| `handover-note.txt` | The corrected four-line handover note |
| `open-tickets.txt` | Alphabetical list of distinct ticket owners (one per line) |
| `category-counts.txt` | Count of tickets per category (`sort \| uniq -c` format) |
| `tasklist-diff.txt` | The saved normal diff comparing the old and approved schedule |
| `tasklist.txt` | The working schedule updated to match the approved version |

---

### Mission files

All mission evidence is in `mission/`. Do not edit these files.

| File | Description |
|---|---|
| `mission/brief.txt` | Long briefing document — contains the handover-note content |
| `mission/handover-draft.txt` | The original draft (for reference only) |
| `mission/tickets.txt` | Pipe-delimited records: `ID\|owner\|category` |
| `mission/schedule-before.txt` | Old task schedule |
| `mission/schedule-approved.txt` | Approved task schedule |

Your working copies are already in `work/mission/`:

| File | Starting state |
|---|---|
| `work/mission/handover-note.txt` | Draft with wrong room and start time |
| `work/mission/tasklist.txt` | Copy of schedule-before |

---

### Step 0 — Check your history (history)

Before starting the mission, take stock of what commands you have already run:

```bash
history 10
```

You should see `diff`, `cut`, `sort`, `uniq` and `nano` commands from
Experiments 1–7. In Step 6 you will use `Ctrl+R` to recall a `diff` command
from this list.

---

### Step 1 — Find the approved handover note (less)

> **Starting directory:** `lab-work/lab2-<ID>/`

Open `mission/brief.txt` in `less`. Search for the section heading
**HANDOVER - APPROVED**.

The brief contains two `HANDOVER` sections. The first one is labelled
`HANDOVER - OLD` — do not use it. Press `n` to jump to the next match.
Check that the shift code in the heading matches **your** shift code from
`identity.txt`.

Below the heading you will see a line that says:

```
Use these four lines for the final handover note:
```

The **four lines that follow that instruction line** (not the instruction line
itself) are the exact content you need for `work/mission/handover-note.txt`:

```
Shift: SHF-xxxxxx
Room: ITSD-x
Start: HH:MM
Bring your access card.
```

Note these four lines. Quit less when you have them.

---

### Step 2 — Repair the handover note (nano)

Open `work/mission/handover-note.txt` in nano. Correct the Room and Start
values using the lines you found in Step 1. Save and exit. Verify with `cat`.

---

### Step 3 — List open ticket owners (cut, sort, uniq)

Use `mission/tickets.txt`. Extract the owner field. Produce a list of
distinct owners in alphabetical order. Save it to `work/mission/open-tickets.txt`.

The field delimiter and field number are the same as in Experiment 6.

---

### Step 4 — Count tickets by category (cut, sort, uniq)

Using `mission/tickets.txt`, count how many tickets belong to each category.
Save the result to `work/mission/category-counts.txt`.

---

### Step 5 — Save the schedule comparison (diff)

Compare `mission/schedule-before.txt` and `mission/schedule-approved.txt`
using diff. Put the older file first. Save the diff output to
`work/mission/tasklist-diff.txt`.

```bash
diff mission/schedule-before.txt mission/schedule-approved.txt > work/mission/tasklist-diff.txt
cat work/mission/tasklist-diff.txt
```

**Observation:** Read the saved file carefully.

- What marker letter do you see? `c`, `d`, or `a`?
- Is it the same as the `c` marker you saw in Experiment 7B?

> **Explanation:** The mission schedule changed differently from the task list.
> In Experiment 7B both sides had changed content (lines were *replaced*), so
> diff used `c`. In this schedule, one line was *deleted* from the first file
> (`d`) and one line was *added* to the second file (`a`) — these appear as
> two separate hunks. Recognising `c`, `d` and `a` in real diff output is a
> key skill; the markers tell you exactly what kind of repair is needed.

---

### Step 6 — Repair the working schedule (nano, diff)

Edit `work/mission/tasklist.txt` so it matches `mission/schedule-approved.txt`.
Use the diff output from Step 5 as your guide.

Verify your repair:

```bash
diff work/mission/tasklist.txt mission/schedule-approved.txt
```

No output means the repair is complete.

---

### Step 7 — Recall a command from history (history, Ctrl+R)

You have just run a `diff` command in Step 6 that verified your repair
(it produced no output). Use `Ctrl+R` to find it:

1. Press `Ctrl+R` and type `diff`.
2. The most recent `diff` command appears. If it is not the verification
   command, press `Ctrl+R` again to step back through older matches.
3. Press `Right Arrow` to bring the command to the prompt.
4. Edit the filenames to compare `mission/schedule-before.txt` and
   `mission/schedule-approved.txt` again (to confirm you can produce the same
   diff output as the file you saved in Step 5).
5. Run it. The output should match the contents of `work/mission/tasklist-diff.txt`.

This demonstrates that the `Ctrl+R` and `Right Arrow` skills from
Experiment 1 carry forward into real multi-step work.

---

## Validation

Run the checker from your lab root:

```bash
python3 ../../check.py
```

The checker reads 16 result files and verifies that original evidence is
unchanged (17 checks total). It does not upload, modify or submit anything.

### Reading the output

| Prefix | Meaning |
|---|---|
| `PASS` | This file matches the expected result exactly |
| `CHECK` | This file is missing, has wrong content, or was not created |

### If you see CHECK

For a result file (e.g. `work/owners-sorted.txt`):
- Check that you ran the correct command and used the correct file.
- Re-run the command and check the output with `cat`.
- If the output looks right, save it again with `>`.

For `Original evidence files preserved`:
- You edited a file in `evidence/` or `mission/` by mistake.
- Ask your instructor — you may need a fresh attempt with a new ID.

Run the checker again after each fix. The goal is **17/17**.

---

## Command Quick Reference

```bash
# Setup
bash start.sh                          # create your attempt
cat identity.txt                       # show your shift details

# history
history 10                             # last 10 commands
history | grep word                    # commands containing 'word'
Ctrl+R  (then type)                    # reverse search
Right Arrow                            # accept to edit
Ctrl+G                                 # cancel search

# nano
nano filename                          # open or create file
Ctrl+O  Enter                          # save
Ctrl+X                                 # exit

# less
less filename                          # open for reading
Space / b                              # forward / backward one screen
g / G                                  # jump to start / end
/text  Enter                           # search
n / N                                  # next / previous match
q                                      # quit

# sort
sort file                              # alphabetical sort
sort -n file                           # numeric sort
sort -nr file                          # numeric, descending
sort file > output                     # save sorted output

# uniq
uniq file                              # remove adjacent duplicates
sort file | uniq                       # remove all duplicates (correct order)
sort file | uniq -c                    # count each unique value

# cut
cut -d "|" -f 2 file                  # extract field 2 (pipe-delimited)
cut -d "|" -f 1,3 file               # extract fields 1 and 3

# diff
diff before.txt after.txt             # compare two files
diff file1 file2 > comparison.txt     # save diff output

# checker
python3 ../../check.py                 # run from lab-work/lab2-<ID>/

# reset (only if you need to start work/ over)
bash ../../scripts/reset_work.sh <ID> # asks for confirmation; never touches evidence/
```
