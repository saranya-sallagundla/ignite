# Topic 2 — Linux: Top 50 Shell Commands

> Personal study notebook — full teaching content, commands, outputs, and explanations.
> Distinct from `progress.md` (tracking) and `session_notes.md` (short personal reflection).

---

## Day 1 — 2026-07-08 (file viewing, search, text processing)

Grouped thematically rather than as a random list, since that's how these get used in practice.
Skips what Topic 1 already covered: `ls`, `cd`, `mkdir`, `cp`, `mv`, `rm`, `cat`, `chmod`.

### Today's agenda
1. Viewing large files — `head`, `tail`, `less`.
2. `grep` — search text by pattern.
3. `find` — locate files by name.
4. `sort`, `uniq`, `wc`.
5. `cut` — extract columns.
6. Combined pipeline exercise.

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

**Gotcha — the `^` anchor, a real regex mix-up**: given a `numbers.txt` with lines like `9`, `19`,
`29`, `90`, `91`, ..., `99`, the initial assumption was that `grep "9" numbers.txt` (no anchor)
would only match lines *starting* with 9. That's wrong — with no anchor, `grep` matches a `9`
**anywhere** in the line, so `19` and `29` would match too, not just `9`/`90`-`99`. `^` specifically
anchors to the start of the line: `grep -n "^9"` matches only lines that *start* with `9` (`9`,
`90`, `91`, ... `99`), correctly excluding `19`/`29`/`59` where the `9` appears later in the line.

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

## Day 2 — 2026-07-09 (process/system monitoring, networking, archiving)

### Today's agenda
1. Process monitoring — `ps`, `top`, `kill`, signals.
2. System resource commands — `df`, `du`, `free`, `uptime`.
3. Networking — `ping`, `curl`, `ss`.
4. Archiving — `tar`.
5. The quiz.

### 1. Process monitoring — `ps`, `top`, `kill`, signals

**Syntax**: `ps aux` — list every process, all users, detailed format. Actually 3 flags combined:
`a` = all users' processes, `u` = user-oriented detailed columns, `x` = include processes with
no controlling terminal (background/daemon services).

**Syntax**: `top` — live-updating interactive process view (`q` to quit)

**Syntax**: `kill [-SIGNAL] PID` — send a signal to a process by PID.
- Default (`kill PID`) = **SIGTERM** (signal 15) — a polite request to stop. The process **can**
  catch this and run its own cleanup code first (close files, save state), or even ignore it.
- `kill -9 PID` = **SIGKILL** — the kernel forcibly removes the process immediately. The process
  **cannot catch, block, or ignore** SIGKILL — no cleanup chance at all. Last resort, used when a
  process is frozen/hung and won't respond to SIGTERM.

**Analogy — tenant/landlord**: SIGTERM is knocking on the door and saying "please pack up and
leave" — the tenant can take their time, grab their things, or even ignore the knock entirely.
SIGKILL is skipping the knock altogether — the landlord physically removes the tenant and
everything gets tossed out immediately, zero warning, zero chance to grab anything on the way
out.

**Verified hands-on** — full lifecycle: start a background process, find it, stop it:
```
$ sleep 300 &
$ ps aux | grep sleep
devuser   244173  0.0  0.0   3128  1792 pts/5    S    17:16   0:00 sleep 300
devuser   244225  0.0  0.0   4092  2048 pts/5    S+   17:16   0:00 grep --color=auto sleep
```
**Gotcha**: `grep`'s own process line matched the search pattern "sleep" (since its own command
line contains that text) — a very common real annoyance. Fix: bracket one letter of the pattern
so grep's own invocation no longer contains the literal substring:
```
$ ps aux | grep [s]leep
devuser   244173  0.0  0.0   3128  1792 pts/5    S    17:16   0:00 sleep 300

$ kill 244173
[1]+  Terminated              sleep 300

$ ps aux | grep [s]leep
(nothing — confirmed gone)
```

### 2. System resource commands — `df`, `du`, `free`, `uptime`

**Syntax**: `df -h` — disk free space per mounted filesystem, human-readable sizes
**Syntax**: `du -sh PATH` — disk usage of a specific path, `-s` = summary total (not every file)
**Syntax**: `free -h` — RAM usage (total/used/free/swap)
**Syntax**: `uptime` — how long since last boot, plus load average

**Verified hands-on**:
```
$ df -h
...
/dev/sdd       1007G  2.4G  954G   1% /
...
C:\             475G  237G  239G  50% /mnt/c
```
`C:\` mounted at `/mnt/c` is literally the Windows drive, live confirmation of Topic 1's
single-tree/mount concept — same disk, viewed from inside WSL.

```
$ du -sh ~/practice
44K     /home/devuser/practice

$ free -h
               total        used        free      shared  buff/cache   available
Mem:           7.6Gi       1.0Gi       6.6Gi       3.6Mi       193Mi       6.6Gi
Swap:          2.0Gi          0B       2.0Gi

$ uptime
 17:26:18 up 1 day, 10:20,  1 user,  load average: 0.00, 0.00, 0.00
```

**Load average** — the average number of processes actively **waiting for CPU time** (not idle)
over the last 1/5/15 minutes respectively. `0.00, 0.00, 0.00` = essentially idle system, nothing
competing for CPU. A high number relative to core count = overloaded; comparing the three values
shows whether a load spike is rising or easing off over time.

**`df` vs. `du` — practical difference, and why they can occasionally disagree**: `df` reports
at the whole-filesystem/mount level; `du` sums actual usage of specific files/paths you point it
at. They can genuinely diverge: a **deleted file still held open by a running process** still
occupies real disk space at the filesystem level (`df` counts it as used) — but since it no
longer has a directory entry/filename, `du` can't traverse to it and won't count it at all. A
disk shown as nearly full by `df`, with no `du` total anywhere close to accounting for that
space, points at exactly this — find and restart whatever process is holding a deleted file open.

### 3. Networking — `ping`, `curl` (recap), `ss`

**Syntax**: `ping -c N HOST` — send N test packets (ICMP echo) to test reachability/latency.
Without `-c`, runs forever until `Ctrl+C`. `127.0.0.1` = loopback, always "this machine itself."

**Key real-world discovery — ICMP vs. TCP are independently firewalled**:
```
$ ping -c 4 127.0.0.1        → 0% packet loss (loopback, always works)
$ ping -c 4 google.com       → 0% packet loss (!)
$ ping -c 4 claude.com       → 0% packet loss (!)
```
This initially seemed to contradict Topic 1's finding that `curl`/`apt` timed out on this same
corporate network. The resolution: **`ping` uses ICMP** (a lightweight "are you there?"
diagnostic protocol); **`curl`/web traffic uses TCP** on specific ports (80/443). A corporate
firewall commonly allows ICMP through for basic network diagnostics while still blocking or
restricting direct outbound TCP on 80/443 unless routed through an approved proxy — these are
independently controlled. This is a real, common interview/on-the-job scenario: *"ping works but
the app/website doesn't load"* — the answer is almost always exactly this distinction. `telnet`
and `curl` both rely on TCP as their transport, unlike `ping`.

**`ping` output, decoded**:
```
64 bytes from ...: icmp_seq=1 ttl=117 time=27.9 ms
--- google.com ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3005ms
rtt min/avg/max/mdev = 27.415/28.096/28.973/0.560 ms
```
- `icmp_seq` — sequence number per packet, lets you spot loss/reordering
- `ttl` (Time To Live) — hop-counter, decremented by 1 per router hop. Common OS defaults: `64`
  (Linux/Unix), `128` (Windows), `255` (older Unix/networking gear). Working backward from the
  observed value to the nearest common default gives a rough hop count and an educated (not
  certain) guess at the remote host's OS — a lightweight technique called OS fingerprinting.
  `ttl=117` → nearest default `128` → ~11 hops → likely Windows-family or Windows-mimicking config.
  Note: this TTL reflects the **remote** host's OS (the one replying), not the local machine.
- `rtt min/avg/max/mdev` — round-trip time stats; `mdev` = mean deviation (consistency of
  latency — low is stable, high suggests an unstable connection)
- packet loss % — did every sent packet get a reply back

**Syntax**: `ss -tuln` — show listening network sockets
- `-t` TCP, `-u` UDP, `-l` listening only (not active connections), `-n` numeric (skip name
  resolution)

**Verified hands-on**:
```
$ ss -tuln
...
tcp    LISTEN   0   511   127.0.0.1:38027   0.0.0.0:*
...
(no port 22 anywhere in the output)
```
**Column-by-column breakdown**:
- **`Netid`** — `tcp` or `udp`, which protocol this socket is.
- **`State`** — for TCP, `LISTEN` means actively waiting for an incoming connection; UDP entries
  show `UNCONN` instead, since UDP is connectionless — there's no "listening" state the same way,
  just a socket bound to a port ready to receive datagrams.
- **`Local Address:Port`** — `127.0.0.1:PORT` means loopback-only (only this machine can connect);
  `0.0.0.0:PORT` means accepting connections from anywhere.
- **`Peer Address:Port`** — the remote side of an established connection; `*` for a listening
  socket, since nothing's connected yet.

Multiple entries on **port 53** in the real output were identified as **`systemd-resolved`** —
Ubuntu's built-in local DNS resolver, running as its own listening service rather than something
tied to any specific app being tested.

Confirms directly what Topic 1's troubleshooting already established: `sshd` never finished
installing (blocked by the corporate proxy), since port 22 isn't listening at all — `ss -tuln` is
the tool to verify "is this service actually running," not just "did the install command exit
without error."

### 4. Archiving — `tar`

**Syntax**: `tar -czvf ARCHIVE.tar.gz PATH` — create an archive
- `-c` create, `-z` compress with gzip, `-v` verbose (print each file as added), `-f` filename
  (must immediately precede the archive name)
- Name origin: **t**ape **ar**chive, from 1970s magnetic tape backups — name stuck, tool didn't.

**Syntax**: `tar -xzvf ARCHIVE.tar.gz` — extract (`-x`, same other flags)
**Syntax**: `tar -tzvf ARCHIVE.tar.gz` — list/table of contents **without** extracting

**Verified hands-on**:
```
$ cd ~
$ tar -czvf practice-backup.tar.gz practice/
practice/
practice/app.log
...
practice/logs/
practice/logs/log2.txt
...

$ tar -tzvf practice-backup.tar.gz | head -5
drwxr-xr-x devuser/devuser   0 2026-07-08 20:07 practice/
-rw-r--r-- devuser/devuser 125 2026-07-08 18:17 practice/app.log
lrwxrwxrwx devuser/devuser   0 2026-07-07 16:09 practice/hardlink2.txt -> original.txt
...

$ ls -lh practice-backup.tar.gz
-rw-r--r-- 1 devuser devuser 1014 Jul  9 19:23 practice-backup.tar.gz
```
Confirms: archiving is recursive (includes the `logs/` subfolder), symlinks are preserved as
symlinks inside the archive (not copied as regular files — the `->` arrow notation survives),
and the original `practice/` folder is completely untouched — `tar` only reads to build the new
archive file, placed whichever directory you ran the command from (here, `~`, since `-f` was
given a bare filename with no path prefix). Compression is real: `1014` bytes vs. `44K`
uncompressed (`du -sh` earlier) — text compresses very well due to repeated patterns.

---

## Topic 2 Quiz — both days combined — Attempt 1: PASS, 84/100

Interview-style, open-ended, no multiple choice. Ran ~28 minutes (over the 20-min cap — allowed
to finish in progress).

1. **Find the memory-heavy process, then force-kill a hung one by name.**
   `ps aux` lists every process on the system, for all users, in a detailed columnar format —
   this is where you'd look to spot which process is consuming the most memory. Once a specific
   named process needs to be targeted, searching for it directly (e.g. `ps aux | grep
   "stuck-service"`) runs into a self-match gotcha: `grep`'s own process line also contains the
   literal search text, so it shows up as a false match against itself. The fix is bracketing one
   letter of the pattern — `ps aux | grep "[s]tuck-service"` — which still matches the real target
   process but no longer matches grep's own command-line text (since `[s]tuck-service` isn't the
   literal substring `stuck-service`). Once the correct PID is identified, force-killing a hung
   process — one that isn't responding and needs to be stopped immediately — means `kill -9 PID`:
   this sends SIGKILL (signal 9), which the kernel enforces right away and which the target
   process cannot catch, block, or ignore. This is different from the default `kill PID`, which
   sends SIGTERM (signal 15) — a polite request the process could catch and clean up after, or
   simply ignore — and is why SIGKILL is the right call specifically when a process is frozen and
   unresponsive to that polite request.
2. **"Ping works, so the app must be reachable" — true or false?**
   False. `ping` tests reachability using ICMP, a lightweight "are you there?" diagnostic
   protocol — it says nothing about whether actual application traffic can get through. Web
   traffic (`curl`, browsers, `telnet`) relies on TCP, on specific ports (80/443 for
   web/HTTPS), which is a completely separate protocol from ICMP. A corporate firewall commonly
   allows ICMP through for basic network diagnostics while still blocking or restricting direct
   outbound TCP on those ports unless traffic is routed through an approved proxy — the two are
   controlled independently, so one working proves nothing about the other. This was directly
   confirmed hands-on: `ping -c 4 google.com` and `ping -c 4 claude.com` both came back at 0%
   packet loss on the same corporate network where `curl`/`apt` (TCP-based) had already been found
   to time out. "Ping works but the app/website doesn't load" is a common real troubleshooting
   scenario, and the answer is almost always this exact ICMP-vs-TCP distinction.
3. **`uniq` isn't removing visible duplicates in a file — why?**
   `uniq` only removes **adjacent** (consecutive) duplicate lines — it compares each line only to
   the line immediately before it, and has no awareness of duplicates anywhere else in the file.
   If identical lines are scattered rather than next to each other (e.g. `banana, apple, cherry,
   apple, banana, apple` — the three `apple` lines aren't consecutive), `uniq` removes nothing,
   because none of the matching lines are adjacent. The fix is to `sort` the file first, which
   groups all identical lines together, so a subsequent `uniq` (or `uniq -c` to also get a count
   of how many times each line occurred) actually catches every duplicate: `sort file.txt | uniq
   -c`. Separately, `uniq` also only ever compares whole lines to each other, never text within a
   single line — `"apple apple"` on one line is untouched by `uniq` entirely, since it never looks
   inside a line, only at adjacent whole lines.
4. **`grep` for content vs. `find` for filename, scoped to `/var/log`.**
   `grep` searches file **contents** for a text pattern; `find` locates files by **name** (or other
   attributes) — they answer fundamentally different questions and aren't interchangeable. To
   search file contents recursively under `/var/log`: `grep -r "PATTERN" /var/log` — `-r` is the
   proper recursive flag (not some other syntax), and giving `/var/log` explicitly as the path
   scopes the search to that directory tree specifically, rather than defaulting to the current
   directory or searching the whole filesystem. To locate a file by name within the same
   directory: `find /var/log -name "FILENAME"` (`-iname` for case-insensitive, wildcards like
   `"*.log"` supported) — scoped to `/var/log` rather than the much slower and noisier `find /`
   from the filesystem root. The core distinction: `find` answers "which file has this **name**,
   and where is it?"; `grep -r` answers "which file **contains** this **text**, and where?"
5. **`df` vs. `du` disagreement — why can they differ?**
   `df` reports free/used space at the whole-filesystem (mount) level; `du` sums the actual disk
   usage of specific files or paths you point it at (`-s` gives one summary total rather than
   listing every file). They usually agree, but can genuinely diverge in one specific scenario: a
   file that has been **deleted** but is still held open by a running process still occupies real
   disk space at the filesystem level — `df` counts that space as used, since the underlying data
   blocks haven't actually been freed yet. But because the file no longer has a directory
   entry/filename, `du` has no path to traverse to it and won't count it in any total at all. So a
   disk that `df` shows as nearly full, with no `du` total anywhere close to accounting for that
   space, points at exactly this: some process is holding a deleted file open, and the fix is
   finding and restarting that process to actually reclaim the space.

**How the actual quiz session went** (for context, not the answers themselves): Q1 needed two
nudges (exact `kill -9 PID` form, and the `ps aux | grep` bracket self-match trick); Q2 passed
cleanly after one nudge to name the ICMP-vs-TCP mechanism itself; Q3 passed cleanly, first try;
Q4 needed two corrections (invalid `-/var/log` syntax fixed to proper `-r`, and `find /` narrowed
to `find /var/log`); Q5 was correct on the basic distinction, with the deleted-open-file edge
case explained directly rather than pushed on, since it went beyond what was explicitly taught
this session.

**Score: 84/100**
- **Quiz 34/40** — 3 of 5 answers needed a correction (`kill` syntax precision, `grep`/`find`
  flag and scope fixes), 2 passed cleanly.
- **Hands-on 26/30** — more syntax slips than Topic 1 (`grep -r` placement, `find` scope).
- **Depth 24/30** — strong independent reasoning on the ICMP-vs-TCP firewall discovery.

**Verdict**: **Topic 2 CLEARED, attempt 1, 84/100.**
