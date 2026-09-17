# Topic 2 — Linux: Top 50 Shell Commands

> Personal study notebook — full teaching content, commands, outputs, and explanations.
> Distinct from `progress.md` (tracking) and `session_notes.md` (short personal reflection).

---

## Day 1 — 2026-07-08 (file viewing, search, text processing)

Grouped thematically rather than as a random list, since that's how these get used in practice.
Skips what Topic 1 already covered: `ls`, `cd`, `mkdir`, `cp`, `mv`, `rm`, `cat`, `chmod`.

### 1. Viewing large files — `head`, `tail`, `less`

**Syntax**: `head [-n LINES] FILE` — first N lines (default 10)
**Syntax**: `tail [-n LINES] FILE` — last N lines (default 10)

**Verified hands-on**:
```
$ seq 1 100 > numbers.txt
$ head numbers.txt
1
2
3
4
5
6
7
8
9
10
$ tail -n 2 numbers.txt
99
100
```
(`seq 1 100` generates numbers 1–100, one per line — quick way to make test data)

**Syntax**: `less FILE` — interactive scrollable pager (vs. dumping the whole file at once)

Controls: `↓`/`j` scroll down, `↑`/`k` scroll up, `Space` next page, `b` previous page,
`/searchterm` + `Enter` to search forward, `n` for next match, `q` to quit.

**Verified hands-on**: `less numbers.txt`, then `/50` + Enter correctly jumped to and highlighted
the first occurrence of "50" in the file.

### 2. `grep` — search text by pattern (content, not filename)

**Syntax**: `grep [OPTIONS] "PATTERN" FILE`

Flags: `-i` case-insensitive, `-n` show line numbers, `-v` invert match (show non-matching
lines), `-r` recursive (search all files in a directory tree).

**Gotcha — case sensitivity, proven hands-on**:
```
$ echo "Error: disk full" > log1.txt
$ echo "warning: low memory" >> log1.txt
$ echo "ERROR: network down" >> log1.txt

$ grep "error" log1.txt
(no output — case-sensitive by default, no lowercase "error" exists in the file)

$ grep -i "error" log1.txt
Error: disk full
ERROR: network down

$ grep "ERROR" log1.txt
ERROR: network down
```

**Recursive search, and default-path behavior**:
```
$ mkdir logs
$ echo "error: timeout" > logs/log2.txt

$ grep "error" log2.txt
grep: log2.txt: No such file or directory   # wrong path — file is at logs/log2.txt, not here

$ grep -r "error"
logs/log2.txt:error: timeout
```
`grep -r` with **no path given** defaults to searching the current directory (`.`) recursively.
Output format for recursive/multi-file search is `filename:matching-line`.

**Gotcha — `-v` on a pattern that matches nothing does nothing useful, proven hands-on**:
```
$ printf "INFO: server started\nERROR: disk full\nINFO: user login\nWARNING: low memory\nERROR: connection refused\nINFO: request processed\n" > app.log

$ grep -vn "info" app.log      # WRONG — pattern is lowercase, file has uppercase INFO
1:INFO: server started
2:ERROR: disk full
3:INFO: user login
4:WARNING: low memory
5:ERROR: connection refused
6:INFO: request processed
```
`"info"` (lowercase) matched **zero** lines to begin with (file has `INFO`, uppercase). `-v`
("show lines that DON'T match") had nothing to exclude, so it showed *everything* back — not a
bug, but a common real debugging trap: check case-sensitivity first when `-v` "isn't filtering."

```
$ grep -ivn "info" app.log      # CORRECT — added -i
2:ERROR: disk full
4:WARNING: low memory
5:ERROR: connection refused
```

### 3. `find` — locate files by name (different from `grep`, which searches content)

**Syntax**: `find PATH -name "FILENAME"`

- `PATH` — where to start (`.` = here, recursively)
- `-name` — exact filename (supports wildcards, e.g. `"*.txt"`)
- `-iname` — case-insensitive version
- `find / -name "FILE" 2>/dev/null` — search whole filesystem from root, suppressing permission
  errors

**Key distinction, reinforced with a real mix-up**: `find` answers "which file has this **name**,
and where is it?" `grep -r` answers "which file **contains** this **text**, and where?" Trying to
use `find`-style thinking for a content search (or vice versa) doesn't work — they search
completely different things.

### 4. `sort`, `uniq`, `wc`

**Syntax**: `sort [-n] FILE` — alphabetical sort by default, `-n` for numeric sort (without it,
`"10"` sorts before `"2"` — character-by-character comparison, not numeric value)
**Syntax**: `uniq FILE` — removes only **adjacent** (consecutive) duplicate lines; add `-c` to
also show a count per unique line
**Syntax**: `wc -l FILE` — count lines (`-w` words, `-c` bytes; plain `wc` shows all three)

**Corrected misconception**: `uniq` compares whole **lines** to the next whole line — it has no
concept of "words within one line." `"apple\napple"` (two separate lines) *is* what `uniq` would
catch (adjacent, identical lines); `"apple apple"` (one line, space-separated) is untouched by
`uniq` entirely, since it never looks inside a single line.

**Verified hands-on — why `sort` before `uniq` matters**:
```
$ printf "banana\napple\ncherry\napple\nbanana\napple\n" > fruits.txt

$ uniq fruits.txt              # duplicates NOT adjacent in original order — removes nothing
banana
apple
cherry
apple
banana
apple

$ sort fruits.txt              # groups identical lines together
apple
apple
apple
banana
banana
cherry

$ sort fruits.txt | uniq -c    # now uniq can catch every duplicate, with counts
      3 apple
      2 banana
      1 cherry

$ wc -l fruits.txt
6 fruits.txt
```
`sort | uniq -c` is a very common real one-liner: bring identical lines together first, then
count them — used constantly for "how many times does each distinct value appear" questions
(e.g., log analysis).

### 5. `cut` — extract specific columns from delimited text

**Syntax**: `cut -d 'DELIMITER' -f FIELD_NUMBER(S) FILE` — fields counted from `1`, not `0`

**Verified hands-on — `/etc/passwd`** (colon-delimited, one line per user account; ties back to
Topic 1's `/etc` coverage):
```
$ cut -d ':' -f 1 /etc/passwd | head -5
root
daemon
bin
sys
sync
```

**Gotcha — field 2 is always `x`, and that's correct, not broken**:
```
$ cut -d ':' -f 2 /etc/passwd | head -5
x
x
x
x
x
```
Field 2 is historically the password field, but real password hashes moved to the more
restricted `/etc/shadow` file long ago (`/etc/passwd` is world-readable; `/etc/shadow` isn't).
`x` is a placeholder meaning "see `/etc/shadow`" — identical for every account, by design.

**Verified hands-on — custom CSV**:
```
$ printf "name,age,city\nAlice,30,NY\nBob,25,LA\n" > people.csv
$ cut -d ',' -f 2 people.csv
age
30
25
```

### 6. Combined pipeline exercise — "which error happens most often?"

A realistic one-liner combining everything from today, built step by step:

**Setup**:
```
$ printf "10:01 ERROR DiskFull\n10:02 INFO Started\n10:03 ERROR Timeout\n10:04 ERROR DiskFull\n10:05 WARNING LowMemory\n10:06 ERROR DiskFull\n10:07 ERROR Timeout\n10:08 INFO Started\n" > server.log
```

**Built incrementally**:
```
$ grep "ERROR" server.log
10:01 ERROR DiskFull
10:03 ERROR Timeout
10:04 ERROR DiskFull
10:06 ERROR DiskFull
10:07 ERROR Timeout

$ grep "ERROR" server.log | cut -d " " -f 3
DiskFull
Timeout
DiskFull
DiskFull
Timeout

$ grep "ERROR" server.log | cut -d " " -f 3 | sort | uniq -c
      3 DiskFull
      2 Timeout
```

**Final pieces — `sort -nr` (numeric, descending) and `head -1` (top result only)**:

**Syntax**: `sort -nr` — numeric sort, reversed (largest first) · `head -1` — first line only
```
$ grep "ERROR" server.log | cut -d " " -f 3 | sort | uniq -c | sort -nr | head -1
      3 DiskFull
```

**Full pipeline, the complete real-world idiom**:
```
grep "PATTERN" file | cut -d "DELIM" -f N | sort | uniq -c | sort -nr | head -N
```
"Filter to relevant lines → extract the field that matters → count occurrences of each distinct
value → rank by frequency → take the top result." One of the most useful log-analysis one-liners
in real DevOps/SRE work.

**Clarified distinction — `grep -n` vs. `sort | uniq -c`**: these answer different questions.
`grep -n "X" file` = "**where** does X occur" (filter + locate, shows matching lines with their
original line numbers). `sort | uniq -c` = "**how many** of each distinct value" (aggregate +
count, no concept of original line position at all).

---

## Day 2 — TBD

_To be filled in as Day 2 progresses._
