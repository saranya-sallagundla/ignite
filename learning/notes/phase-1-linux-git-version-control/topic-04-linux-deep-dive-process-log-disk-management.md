# Topic 4 — Linux Deep Dive — Process, Log, Disk Management

> Personal study notebook — full teaching content, commands, outputs, and explanations.
> Distinct from `progress.md` (the session log).
> Two-day topic per the roadmap — covered across two sessions, ending in the quiz.

---

## Day 1 — 2026-07-12 (process states, /proc, nice/renice, log basics)

Goes deeper than Topic 2's `ps`/`top` basics.

### Today's agenda
1. Process states.
2. `awk` — column extraction and filtering.
3. The `/proc` filesystem.
4. `pstree` — visualizing parent-child relationships.
5. `nice` and `renice` — process priority.
6. Log management.
7. Analogies used.
8. Combined exercise — "the system feels slow" scenario.

### 1. Process states

Every process is always in one specific state:

| Code | State | Meaning |
|---|---|---|
| `R` | Running | Actively executing on CPU right now |
| `S` | Sleeping | Waiting for something — not using CPU |
| `D` | Uninterruptible sleep | Waiting on disk/IO — can't even be killed until it returns |
| `Z` | Zombie | Finished, but exit status not yet collected by its parent |
| `T` | Stopped | Paused (e.g. `Ctrl+Z`) |

**Modifier characters** appended to the base letter:
- `+` — in the **foreground** of its terminal
- `s` — a **session leader** (the "head" process of a group)
- `l` — **multi-threaded**
- `<` — **higher priority** than normal

### 2. `awk` — column extraction and filtering (new tool, introduced here)

**Syntax**: `awk '{print $N}'` — print column N of each line (columns are whitespace-separated
by default)
**Syntax**: `awk 'CONDITION {print ...}'` — condition comes **before** the action block; only
matching lines get the action applied
**Syntax**: `awk '$N ~ /PATTERN/ {print ...}'` — `~` means "matches"; `/^X/` = starts with X
(same `^` anchor meaning as `grep`)

**Verified hands-on — full breakdown by STAT category**:
```
$ ps aux | awk '{print $8}' | sort | uniq -c
      2 R+
      4 S
      5 S+
      1 S<s
      1 STAT          <- header row leaked through (its own text "STAT" got counted)
      2 Sl
      4 Sl+
     12 Ss
      3 Ss+
      3 Ssl
      2 Ssl+
```

**Gotcha, hit for real — condition order reversed**: first attempt was
`ps aux | awk '{print $1 $8 $11} ~ /^R/'` — the condition placed *after* the action block.
`awk` doesn't work that way: the condition always comes first, action second (matching the
syntax rule above). Corrected to `awk '$8 ~ /^R/ {print $1 $8 $11}'`.

**Verified hands-on — filtering by state/modifier** (special regex chars need escaping, e.g.
`+` → `\+`; `s`, `l`, `<` are plain, no escaping needed):
```
$ ps aux | awk '$8 ~ /^R/ {print $1 $8 $11}'          # running only
$ ps aux | awk '$8 ~ /^S/ {print $1 $8 $11}'          # sleeping only — header "STAT" leaked
                                                         # through too, since "STAT" itself
                                                         # starts with "S" — filter noise isn't
                                                         # immune to coincidental header matches
$ ps aux | awk '$8 ~ /s/ {print $1 $8 $11}'           # session leaders
$ ps aux | awk '$8 ~ /l/ {print $1 $8 $11}'           # multi-threaded
$ ps aux | awk '$8 ~ /</ {print $1 $8 $11}'           # higher priority
$ ps aux | awk '$8 ~ /\+/ {print $1 $8 $11}'          # foreground — correctly matched the exact
                                                         # commands run interactively in this
                                                         # pipeline (ps, bash, awk)
```
**Extra technique, offered as an aside (not required, but real)**: the leaking header row can be
excluded cleanly by adding a second condition — `$8 ~ /^S/ && $1 != "USER" {print $1 $8 $11}` —
"match state S, **and** the first column isn't literally the header text 'USER'."

**Counting**: `sort | uniq -c` gives grouped counts per unique value; add `| wc -l` afterward to
get the **total number of distinct groups** instead of per-group counts.

### 3. The `/proc` filesystem

A **virtual (pseudo) filesystem** — nothing in it is real data on disk; the kernel generates its
contents **live**, the instant you read them. `ps`, `top`, and `free` are really just reading and
formatting `/proc` under the hood (per-process info, `/proc/meminfo`). `df` is the one exception —
it queries the kernel more directly via `statfs()`/`statvfs()` against each mounted filesystem,
using `/proc/mounts` only to enumerate which filesystems exist.

**Kernel recap**: the core part of the OS that directly manages hardware (CPU, memory, disk) and
mediates between hardware and every other program — deciding CPU time allocation, memory,
disk IO, and process lifecycle. `/proc` is the kernel exposing its own internal bookkeeping as a
readable filesystem.

**Structure**:
- `/proc/<PID>/` — one folder per running process: `status` (summary), `cmdline` (exact start
  command), `environ`, `fd/` (open file descriptors)
- `/proc/cpuinfo`, `/proc/meminfo` — system-wide info (literally what `free`/`lscpu` read from)

**Verified hands-on**:
```
$ echo $$
44720
$ cat /proc/44720/status | head -10
Name:   bash
State:  S (sleeping)
Pid:    44720
PPid:   44675
...
$ cat /proc/44720/cmdline
/bin/bash--init-file/home/.../shellIntegration-bash.sh
$ cat /proc/meminfo | head -5
MemTotal:        7971040 kB
...
```
- `PPid` (parent PID) — every process except PID 1 has a parent. Directly tied to the **Zombie**
  state: a zombie is a finished child whose exit status the parent hasn't collected yet.
- `cmdline` prints with no spaces between arguments — it actually stores them separated by
  **null bytes**, which `cat` doesn't render as visible spaces; the real command had normal
  spacing, just not shown that way here.
- `meminfo`'s `MemTotal: 7971040 kB` matches exactly what `free -h` reported in Topic 2 (`7.6Gi`)
  — direct confirmation `free` reads this same file.

**File descriptors** — `/proc/<PID>/fd/` is a directory, not a file (needs `ls`, not `cat`):
```
$ ls -l /proc/44720/fd/
lrwx------ 1 devuser devuser 64 ... 0 -> /dev/pts/5
lrwx------ 1 devuser devuser 64 ... 1 -> /dev/pts/5
lrwx------ 1 devuser devuser 64 ... 2 -> /dev/pts/5
lrwx------ 1 devuser devuser 64 ... 255 -> /dev/pts/5
```
Every process gets three standard file descriptors: **`0` = stdin**, **`1` = stdout**,
**`2` = stderr**. **This directly explains Topic 3's `2>&1` syntax**: it means "redirect file
descriptor 2 (stderr) to wherever file descriptor 1 (stdout) currently points" — merging error
output into the normal output stream. (`255` is bash's own internal bookkeeping fd, not something
to manage directly.)

### 4. `pstree` — visualizing parent-child relationships

**Syntax**: `pstree [-p]` — `-p` shows PIDs alongside each process name (not "parent" — the tree
*shape itself* is what shows parent-child relationships, regardless of any flag)

**Verified hands-on**: confirmed the exact chain `systemd(1)` → ... → `MainThread(44675)` →
`bash(44720)` → `pstree(...)`, matching precisely the `PPid: 44675` seen in `/proc/44720/status`
— `ps`'s STAT column, `/proc`, and `pstree` all confirmed as different views of the identical
underlying process relationships.

### 5. `nice` and `renice` — process priority

Niceness ranges **-20** (highest priority) to **19** (lowest priority, most "nice" to others),
default `0`.

**Syntax**: `nice -n VALUE COMMAND` — start a new command with a given niceness
**Syntax**: `renice VALUE -p PID` — change niceness of an already-running process

**First attempt, hit a real mixup**: ran `nice -n 10 sleep 60 &`, but an extra command run in
between backgrounding it and checking `ps -o pid,ni,cmd -p $!` overwrote `$!` with a different
job's PID, so the lookup pointed at the wrong process and nothing relevant printed. Fixed by
switching to `sleep 300` and reading `$!` immediately after backgrounding it, with nothing run
in between, to avoid the mixup entirely.

**Repeated PID typo, hit for real**: practicing `renice` against a background process
(PID `68890`), the actual PID got mistyped as `68990` — a single digit swapped (`8`→`9`) in the
middle — three separate times in a row (`renice 5 -p 68990`, `renice 10 -p 68990`, ...), each
attempt failing with "No such process," before the typo was spotted and corrected to the real
`68890`.

**Key rule — stated first as a simplification, then genuinely refined live**: the first pass at
the rule was just "a regular user can't decrease niceness below 0." That turned out to be
under-stated — testing `renice 5 -p` against a process already at niceness `10` (a `10→5`
decrease, both values positive) *also* failed with Permission denied, which shouldn't happen
under the "below 0" framing alone. The corrected, complete rule: a regular user can only
**increase** niceness (lower priority — e.g. `0→10`, `10→19`), never **decrease** it (raise
priority — e.g. `10→5`), **regardless of starting point** — not just "can't go below 0."
Decreasing requires `sudo`/root, full stop.

**Verified hands-on**:
```
$ nice -n 10 sleep 300 &
$ ps -o pid,ni,cmd -p 70478
    PID  NI CMD
  70478  10 sleep 300

$ renice 19 -p 70478                    # increase, no sudo needed — succeeded
70478 (process ID) old priority 10, new priority 19

$ sudo renice 0 -p 70478                # decrease, sudo required — succeeded
70478 (process ID) old priority 19, new priority 0

$ renice -5 -p 70478                    # decrease, no sudo — failed as expected
renice: failed to set priority for 70478 (process ID): Permission denied
```
`$!` — special variable holding the PID of the most recently backgrounded process, a shortcut
for checking a process you just started with `&` without needing to look up its number manually.

**Syntax**: `wsl -u USER` — launches a WSL session as the given user, bypassing normal login;
`passwd USER` — sets/resets that user's password.

**Forgot sudo password mid-session** — resolved via WSL-specific recovery (run from Windows
PowerShell, not WSL bash): `wsl -u root` (opens a root session bypassing sudo/password entirely,
since WSL trusts the launching Windows account) → `passwd <username>` to set a new password.
Confirmed: resetting the password only changes the login credential — zero effect on files,
permissions, installed packages, or any other settings.

### 6. Log management

**`/var/log`** — traditional plain-text logs, one (or more) file per service/subsystem. Recall
Topic 1: `/var` holds data that grows over time.

**Verified hands-on — log rotation, seen for real**:
```
$ ls -l /var/log | head -10
...
-rw-r--r--  1 root   root    178 Jul 10 13:44 alternatives.log
-rw-r--r--  1 root   root  29315 Jun 27 06:04 alternatives.log.1
...
-rw-r-----  1 syslog adm    5310 Jul 12 15:17 auth.log
-rw-r-----  1 syslog adm   21120 Jul 11 23:17 auth.log.1
-rw-r-----  1 syslog adm    2673 Jul  6 13:50 auth.log.2.gz
```
Current log, previous rotation (`.1`), and an older one already compressed (`.2.gz`, using
gzip from Topic 2) — log rotation happening for real, not just a described concept.

**`journalctl`** — the modern, unified, structured systemd log (`journald`), covering most of
what used to be scattered across separate plain-text files.

**Syntax**: `journalctl [-n N] [-f] [-u SERVICE_NAME]`
- `journalctl -n N` — last N entries
- `journalctl -f` — follow live (like `tail -f`)
- `journalctl -u SERVICE_NAME` — filter to one service

**Verified hands-on — real entries recognized from earlier work**:
```
$ journalctl -n 10
Jul 12 15:15:35 ... sudo[70805]: pam_unix(sudo:session): session closed for user root
Jul 12 15:17:01 ... CRON[71176]: pam_unix(cron:session): session opened for user root...
Jul 12 15:17:01 ... CRON[71177]: (root) CMD (cd / && run-parts --report /etc/cron.hourly)
Jul 12 15:20:35 ... systemd-timesyncd[114]: Timed out waiting for reply from ... (ntp.ubuntu.com)
```
- The `sudo` entry is literally the `renice` command from earlier, showing up in the real log.
- **`cron(175)` vs. `CRON[71176]`**: `cron(175)` (an illustrative PID, not from the `pstree` run
  above) is the persistent background **daemon** always watching the clock; `CRON[71176]` is a **short-lived child
  process** spawned each time a scheduled task actually runs, exiting once done. One watcher,
  many temporary instances.
- **`systemd-timesyncd` timeout messages** — the system failing to reach an NTP time server.
  Almost certainly the **same corporate network/firewall block** from Topic 1's SSH
  troubleshooting, now showing up in a completely different context (system logs vs. a failed
  `apt install`) — same root cause, different symptom.

**Log rotation, the concept**: logs would grow forever and eventually fill the disk if left
unchecked (ties to Topic 2's `df`/disk-usage concerns). `logrotate` (config in
`/etc/logrotate.d/`) periodically archives/compresses old logs automatically.

### 7. Analogies used

- **`systemd`** = hotel general manager — starts every department in order, watches over them,
  restarts anything that fails, shuts everything down properly at close.
- **`journalctl`** = the hotel's unified digital logbook — search/filter everything centrally,
  instead of hunting through each department's own separate paper logbook.
- **`/var/log`** = each department's own separate paper logbook (the pre-unified-system state) —
  still coexists alongside the journal, since some software still writes its own plain-text files.

### 8. Combined exercise — "the system feels slow" troubleshooting scenario

**Step 1** — find active (`R`-state) processes:
```
$ ps aux | awk '$8 ~ /^R/'
devuser 75904  0.0  0.0  8284  4224 pts/5  R+  15:39  0:00 ps aux
```
Only match: `ps aux` itself — makes sense, since running `ps` briefly *is* the actively-executing
process capturing this exact snapshot. Confirms a healthy, non-slow system at that moment — no
actual CPU hog found.

**Step 2** — check recent logs for explicit errors/failures:

**Syntax**: `grep -iE "PATTERN1|PATTERN2"` — `-E` enables extended regex, where `|` means
**OR** between patterns (plain `grep -i "error fail"` would search for that exact literal phrase
as one string, not either word independently).
```
$ journalctl -n 50 | grep -iE "error|fail"
(no output)
```

**Real lesson, confirmed by testing directly**: this empty result initially looked like "nothing
wrong," but the `systemd-timesyncd` timeout messages from earlier are a genuine real problem —
they just don't contain the literal words "error" or "fail," they say "Timed out" instead:
```
$ journalctl -n 50 | grep "Time"
Jul 12 15:20:35 ... systemd-timesyncd[114]: Timed out waiting for reply from ...
Jul 12 15:20:45 ... systemd-timesyncd[114]: Timed out waiting for reply from ...
...
```
**Takeaway**: log searching is only as good as the keywords chosen — a real issue can exist in
logs without matching the specific words guessed first. Real troubleshooting often searches
multiple related terms at once (`"error|fail|timeout|denied|refused"`), precisely because you
don't always know in advance how a problem will be phrased.

---

## Day 2 — 2026-07-13 (disk management: partitions, mounting)

### Today's agenda
1. The land/lot/driveway analogy.
2. `lsblk` and UUIDs.
3. `fdisk` — listing partitions (creation deferred to the loop-disk exercise, #5).
4. Attempting to mount an "unused" disk.
5. Practicing safely with a loop-mounted virtual disk.
6. `fsck` — the filesystem checker.
7. `/etc/fstab` — persistent mounts.
8. Combined scenario — inode vs. block exhaustion.
9. The quiz.

### 1. The land/lot/driveway analogy

- **Partition** = drawing boundaries on raw land into separate lots (`/dev/sda1`, etc.)
- **Filesystem (`mkfs`)** = pouring a foundation with a specific blueprint on a lot, so files can
  be organized on it at all
- **Mount** = building the driveway connecting a lot to the existing road network (attaching it
  to a folder in the existing filesystem tree) — without this, a partition/filesystem exists but
  is completely invisible; you can't `cd` into it or see its files through the normal tree.

### 2. `lsblk` and UUIDs

**Syntax**: `lsblk [-f] [-a]` — `-f` shows filesystem type + UUID; `-a` includes empty devices.
Read-only, safe.

**UUID** — a permanent, randomly-generated ID stamped onto a filesystem at creation time
(`mkfs`). Device names (`/dev/sda1`) can shift if disks are added/removed; the UUID never
changes for that filesystem's life. Analogy: device name = parking spot number (can be
reassigned); UUID = the car's VIN (permanently tied to that one filesystem). This is exactly what
`/etc/fstab` uses for persistent mounts, instead of device names.

**Verified hands-on**:
```
$ lsblk -f
NAME  FSTYPE FSVER LABEL UUID                                 FSAVAIL FSUSE% MOUNTPOINTS
sda   ext4   1.0
sdb   ext4   1.0
sdc   swap   1           e614c30d-6feb-4222-95a0-6de3c2a2befc                [SWAP]
sdd   ext4   1.0         b33832f5-02a1-439b-ba34-78a309a1d7e6  953.2G     0% /mnt/wslg/distro
                                                                              /
```
- No `sda1`/`sda2` sub-entries under `sda`/`sdb` — WSL2's virtual disks aren't partitioned in the
  traditional sense; each whole disk *is* one pre-made filesystem, no partition table on top.
- `sdd` shows **two mountpoints on wrapped lines** (`/mnt/wslg/distro` and `/`) — a single
  filesystem genuinely can be mounted at more than one path at once (a bind mount). First read
  looked like a contradiction against `df -h`; re-reading the raw wrapped output resolved it —
  another real "verify, don't just trust the first read" moment.

**Cross-checked with `df -h`**: confirmed `sdd` is the actual root filesystem (`/`), `sdc` is
swap, and `sda`/`sdb` are genuinely unmounted — not attached anywhere in the visible folder tree.

### 3. `fdisk` — listing partitions (creation deferred to §5)

**Syntax**: `fdisk -l [device]` — list partitions (safe, read-only)
**Syntax**: `fdisk [device]` — interactive mode, create/delete/modify partitions (destructive)

Not run destructively this session — WSL2's real disks (`sda`/`sdb`/`sdd`) aren't safe to
experiment on directly (see below), so partition creation itself was deferred to a virtual
practice disk instead.

### 4. Attempting to mount an "unused" disk — real permission and busy errors

**Syntax**: `mount DEVICE MOUNTPOINT` (or `mount -a` to mount everything listed in `/etc/fstab`)

```
$ mount /dev/sda /mnt/test
```
Predicted correctly beforehand that `/mnt/test` must already exist (`mount` never creates the
folder itself) — but hit real errors in sequence:
```
$ mkdir -p /mnt/test
mkdir: cannot create directory '/mnt/test': Permission denied      # needed sudo — self-diagnosed
$ sudo mkdir -p /mnt/test
$ sudo mount /dev/sda /mnt/test
mount: /mnt/test: /dev/sda already mounted or mount point busy.
```
Investigated with `sudo dmesg | tail -20` instead of guessing:
```
[ 1969.447667] sda: Can't mount, would change RO state
```
**Real lesson**: the kernel already considers `sda` "busy" — mounted somewhere in a namespace
not visible via `lsblk`/`df -h` (almost certainly WSL2 using it internally, e.g. as a read-only
base disk image for another installed distro or utility-VM internals). Attempting to mount it
read-write was rejected because that would change a read-only state something else depends on.
Same *shape* of lesson as Topic 1's corporate-proxy discovery: a tool reporting "busy"/blocked
doesn't mean the cause is visible to you — another process/namespace can hold a resource you
can't see directly.

### 5. Practicing safely with a loop-mounted virtual disk

Since the real spare disks weren't safe to experiment on, used the standard technique for
practicing partition/filesystem/mount work without a spare physical disk: back a loop device
with an ordinary file.

**Syntax and why, each command**:
- `fallocate -l <size> <path>` — creates a file of a given size instantly; stands in for raw
  disk space ("blank land").
- `losetup -fP <path>` — attaches a regular file to a loop device (`/dev/loop0`), making the
  kernel treat the file as if it were a real block device (`-f` = auto-pick free loop device,
  `-P` = scan for partitions on it).
- `mkfs.ext4 <device>` — formats the device with ext4 (pours the foundation).
- `mkdir -p` + `mount` — as before.

**Verified hands-on, full pipeline**:
```
$ sudo fallocate -l 100M /root/practice.img
$ sudo losetup -fP /root/practice.img
$ losetup -a
/dev/loop0: []: (/root/practice.img)

$ sudo mkfs.ext4 /dev/loop0
mke2fs 1.47.0 (5-Feb-2023)
Creating filesystem with 25600 4k blocks and 25600 inodes
Creating journal (1024 blocks): done
Writing superblocks and filesystem accounting information: done

$ sudo mkdir -p /mnt/test
$ sudo mount /dev/loop0 /mnt/test

$ df -h /mnt/test
Filesystem      Size  Used Avail Use% Mounted on
/dev/loop0       90M   24K   83M   1% /mnt/test

$ lsblk -f
loop0 ext4   1.0         57ea35a9-50ee-422f-b798-7cd4e839274f   82.7M     0% /mnt/test

$ sudo touch /mnt/test/hello.txt
$ ls -l /mnt/test
-rw-r--r-- 1 root root     0 Jul 13 17:54 hello.txt
drwx------ 2 root root 16384 Jul 13 17:51 lost+found
```
Fully verified end-to-end: file → loop device → formatted filesystem → mounted → usable (created
a real file on it), not just cosmetically attached.

**`mkfs.ext4` output explained**:
- **4k blocks** — disk space divided into 4KB chunks, the basic storage unit. Analogy: a hotel
  only rents out whole rooms, never half a room — even a file that only needs 1KB of actual data
  still occupies one full 4KB block, with the leftover space inside that block unusable by
  anything else. This wasted leftover space is called **internal fragmentation**. Math check
  against the real output: `25600 blocks × 4K = 100MB` — matching exactly the `fallocate -l 100M`
  size requested, confirming the whole 100MB was carved into 4KB blocks with none left over.
- **inodes** — max number of files/directories the filesystem can ever hold; each file needs one
  inode for its metadata (permissions, timestamps, pointers to data blocks) — ties back to
  Topic 1's `stat` discussion.
- **journal** — reserved area logging pending writes before committing, so a power loss mid-write
  doesn't corrupt the filesystem; this is what makes ext4 a *journaling* filesystem.

**`lost+found`** — created automatically by `mkfs.ext4` on every ext4 filesystem, not something
created manually. Reserved space where `fsck` puts recovered file fragments if the filesystem
gets corrupted and files need reattaching to a name.

### 6. `fsck` — the actual filesystem checker

Analogy: filesystem metadata (inodes, block pointers, directory entries) is like a library card
catalog — every card should point to exactly one real book, every book should have exactly one
card. `fsck` walks the whole structure checking for mismatches (orphaned data, double-allocated
blocks, missing entries) and repairs what it can.

- Runs automatically at boot if a filesystem was marked "unclean" (crash/power loss instead of
  clean shutdown), or manually: `fsck <device>` — **never on a mounted filesystem**, unmount
  first, since checking something actively being written to gives false results.
- Journaling (above) exists specifically to reduce how often a *full* `fsck` scan is needed —
  normally just replaying the journal is enough after a crash; full scans are the fallback.

**`df` vs `fsck` — genuinely different checks**:
- `df` = liveness/reachability + usage stats. Reads cached metadata almost instantly. Says
  nothing about internal structural integrity — a structurally corrupted filesystem can still
  show up fine in `df` as long as it's mounted and superficially responding.
- `fsck` = structural integrity. The only way to verify the metadata itself is consistent.

**Production tie-in (real team context, not textbook)**: an alert like *"CRITICAL: filesystem
checker timed out: df took more than 60 sec to complete"* is **not actually running `fsck`**
despite the name — it's a monitoring plugin (e.g. Nagios/Icinga `check_disk`) timing a plain
`df`/`statfs()` call. `df` normally returns near-instantly since it reads cached metadata; a
60+ second hang means the call itself is stuck — almost always a **stale NFS/network mount**
(remote server unreachable but the mount still "there"), a **failing/overloaded disk**, or a
kernel-level I/O deadlock. This is a **liveness/responsiveness** problem, not a structural
corruption one — the practical next step is checking for a stale network mount or hardware I/O
errors (`dmesg`), not jumping to `fsck` (which usually can't even run cleanly against a hung
mount without a force-unmount or reboot first).

### 7. `/etc/fstab` — persistent mounts

A manual `mount` is runtime-only — it does not survive a reboot. `/etc/fstab` ("filesystem
table") is what the init system (systemd, via its fstab generator) reads at boot to remount
things automatically.

**General syntax**, 6 fields per line:
```
<device or UUID>   <mount point>   <filesystem type>   <options>   <dump>   <pass>
```
- device/UUID — prefer UUID (see §2) since device names can shift
- mount point — where to attach it
- fs type — ext4, swap, etc.
- options — `defaults` is the common case
- dump — legacy backup flag, almost always `0`
- pass — `fsck` order at boot: `0` = skip, `1` = check first (root), `2` = check after root

**Note**: `cat /etc/fstab` on this WSL2 system showed only `# UNCONFIGURED FSTAB FOR BASE
SYSTEM` — WSL2 doesn't rely on the traditional boot-time `fstab` process for its own drives
(`/mnt/c`, etc. are handled by its own `wsl.conf`/automount mechanism instead), so the real file
is left essentially untouched. On a real server/VM this file would normally have real entries.

**Verified hands-on — writing and testing a real entry, without rebooting**:

**Syntax**: `blkid [DEVICE]` — show a device's UUID/type (or every device if none given)
```
$ sudo blkid /dev/loop0
/dev/loop0: UUID="57ea35a9-50ee-422f-b798-7cd4e839274f" BLOCK_SIZE="4096" TYPE="ext4"

$ echo 'UUID=57ea35a9-50ee-422f-b798-7cd4e839274f /mnt/test ext4 defaults 0 2' | sudo tee -a /etc/fstab

$ sudo umount /mnt/test
$ sudo mount -a
mount: (hint) your fstab has been modified, but systemd still uses
       the old version; use 'systemctl daemon-reload' to reload.

$ df -h /mnt/test
Filesystem      Size  Used Avail Use% Mounted on
/dev/loop0       90M   24K   83M   1% /mnt/test
```
Wrote the full 6-field line independently and correctly on the first attempt (`defaults 0 2`).
`mount -a` reads every entry in `/etc/fstab` and mounts anything not already mounted — exactly
what happens automatically at boot, so a successful `mount -a` proves the entry is correct
without needing an actual reboot to test it. The systemd hint was a harmless cache-staleness
warning, not a failure — confirmed by `df -h` showing the mount genuinely active.

**Real confusion, fully resolved**: after the sequence above, said directly "still it's
confusing" about how `umount` → (optionally `fsck`) → editing `/etc/fstab` → `mount -a` all fit
together. Walked through each command's actual effect on filesystem *state*, one at a time:
`umount` detaches the device, making it safe to inspect/repair; `fsck` (not run here, since the
filesystem was healthy) would check/repair the filesystem while it's detached; editing
`/etc/fstab` only changes what the *next* `mount`/boot will do, it has no effect on anything
already mounted; `mount -a` is the step that actually re-attaches everything listed in
`/etc/fstab`, reading the file fresh at that moment. Each command touches a different point in
that timeline, not overlapping responsibilities.

**Cleanup, tied directly to Q3's own boot-failure warning below**: this loop device
(`/dev/loop0`, backed by `/root/practice.img`) doesn't persist across a reboot, so leaving its
test entry in `/etc/fstab` permanently would eventually hang boot exactly the way Q3 describes —
this test entry was removed from `/etc/fstab` afterward — **Syntax**: `sed -i 'PATTERN d' FILE`
deletes lines matching PATTERN in place — via `sudo sed -i '\|/mnt/test|d' /etc/fstab`, once the
exercise was done, rather than left in place.

### 8. Combined scenario — inode exhaustion vs. block exhaustion

**Scenario posed**: an application team reports their service crashed with `"No space left on
device,"` but `df -h /` shows only 40% used. What explains a disk-full error despite `df`
showing plenty of free space?

**Reasoned through correctly, with one hint** (pointed back to `mkfs.ext4`'s own output listing
both blocks *and* inodes as separate fixed quantities): the filesystem can run out of **inodes**
independently of running out of **blocks** — `df -h` only reports block/space usage, not inode
usage. Root cause named correctly: millions of tiny files (e.g. a logging bug writing one file
per request instead of appending, an uncleaned cache/session-file directory) each consume one
inode regardless of size, and inode count was fixed permanently at `mkfs` time.

**Diagnostic command**: `df -i` — shows `IUsed`/`IFree`/`IUse%` per filesystem; `IUse%` at 100%
while `df -h`'s `Use%` stays low confirms this exact scenario.

---

## Topic 4 Quiz — both days combined — Attempt 1: PASS, 88/100

Interview-style, open-ended, 5 questions covering Day 1 and Day 2 material together. Question and
full correct answer for each:

1. **Zombie process — what it is, and what cleans it up.**
   A zombie (state code `Z`) is a process that has already finished executing but still has an
   entry in the process table because its parent hasn't collected its exit status yet. The
   specific mechanism that cleans it up is the parent calling the `wait()` system call — that's
   what actually collects the exit status and lets the kernel remove the zombie's table entry. If
   the original parent dies before ever calling `wait()`, the orphaned zombie gets reparented to
   `init` (PID 1), which automatically reaps zombies reparented to it — so a zombie doesn't linger
   forever just because its real parent is gone.

2. **Inode vs. block exhaustion** ("no space left on device" despite `df -h /` showing only 40%
   used).
   `df -h` only reports block/space usage — it says nothing about inode usage, which is a
   separate, independently exhaustible resource. Every filesystem gets a fixed number of inodes
   permanently set at `mkfs` time (seen directly in `mkfs.ext4`'s own output listing "blocks" and
   "inodes" as two separate quantities), and every file consumes exactly one inode for its
   metadata regardless of the file's size. So a filesystem can run completely out of inodes while
   still having plenty of free block space, producing a genuine "No space left on device" error
   that `df -h` alone won't explain. The real-world cause is typically millions of tiny files —
   e.g. a logging bug writing one file per request instead of appending to one file, or an
   uncleaned cache/session-file directory. The diagnostic command to confirm it is `df -i`, which
   shows `IUsed`/`IFree`/`IUse%`; seeing `IUse%` at 100% while `df -h`'s `Use%` stays low is the
   signature of this exact scenario.

3. **`fstab`/UUID persistence, including boot-failure consequences.**
   A manual `mount` command only affects the running system — it does not survive a reboot.
   `/etc/fstab` is what the init system (systemd) reads at boot time to remount filesystems
   automatically, so persistence requires an `fstab` entry, not just a one-off `mount`. Within
   that entry, a UUID is preferred over a device name (e.g. `/dev/sda1`) because device names can
   shift if disks are added or removed, while the UUID is a permanent ID stamped onto the
   filesystem at creation time and never changes for that filesystem's life. Consequence of a bad
   entry: a wrong UUID or device name in `fstab` isn't silently skipped — it can hang the boot
   process entirely and require manual intervention through an emergency/maintenance shell to
   fix, since systemd expects that entry to be mountable during boot.

4. **`nice`/`renice` — why regular users can only increase niceness, never decrease it.**
   Niceness ranges from `-20` (highest priority) to `19` (lowest priority), default `0`. A regular
   user is permitted to raise their own niceness value (lower their process's priority — e.g.
   `0→10`, `10→19`) but is blocked from lowering it (raising priority — e.g. `10→5`), even moving
   between two positive numbers; only `sudo`/root can decrease niceness, regardless of the
   starting point. The reasoning is fairness on a shared system: if any regular user could freely
   decrease their own niceness, everyone would have an incentive to keep bumping their own
   processes to maximum priority, and the result would be every user's processes racing to starve
   everyone else's — not one process literally hanging the CPU, but a fairness/resource-starvation
   problem across all users sharing the machine.

5. **Production `df`-timeout alert** ("CRITICAL: filesystem checker timed out: df took more than
   60 sec to complete") **— what it does/doesn't tell you, and first diagnostic steps.**
   Despite the alert's wording ("filesystem checker"), this is not `fsck` running — it's a
   monitoring plugin (e.g. Nagios/Icinga `check_disk`) timing a plain `df`/`statfs()` call. `df`
   normally returns almost instantly because it reads cached metadata; a 60+ second hang means the
   call itself got stuck. This points to a liveness/responsiveness problem, not structural
   corruption — `df` can't detect corruption either way, since it doesn't walk filesystem
   structure the way `fsck` does. The most likely causes are a stale NFS/network mount (remote
   server unreachable but the mount entry still present), a failing or overloaded disk, or a
   kernel-level I/O deadlock. The correct first diagnostic steps are checking for a stale network
   mount and checking `dmesg` for hardware I/O errors — not jumping to `fsck`, which usually can't
   even run cleanly against a hung mount without a force-unmount or reboot first.

**How the actual quiz session went** (for context, not the answers themselves): Q1 needed two
follow-ups to reach `wait()` and reparenting-to-init; Q2 passed cleanly on both halves; Q3 passed
cleanly; Q4 needed a follow-up to sharpen "the CPU might hang" into the correct fairness framing;
Q5 passed cleanly and completely.

**Score: 88/100**
- **Quiz 34/40** — 2 of 5 answers needed a follow-up nudge for full precision but were ultimately
  correct.
- **Hands-on 28/30** — real, independently-diagnosed errors throughout, not just guided steps.
- **Depth 26/30** — strong production tie-in, correct reasoning through the combined scenario
  with minimal hinting.

**Verdict**: **Topic 4 CLEARED, attempt 1, 88/100.**
