# Topic 1 — Linux Fundamentals — Filesystem, SSH, VMs

> Personal study notebook — full teaching content, commands, outputs, and explanations.
> Distinct from `progress.md` (the session log).
> Two-day topic per the roadmap — covered across two sessions, ending in the quiz.

---

## Day 1 — 2026-07-06 (heavy scaffolding, guided walkthrough)

### Today's agenda
1. The Linux filesystem — why it's laid out the way it is.
2. Permissions — reading `ls -la` output.
3. Filesystem navigation & manipulation.
4. SSH — core concepts.
5. VMs — core concepts.

### 1. The Linux filesystem — why it looks like it does

Windows gives every drive its own letter (`C:\`, `D:\`). Linux has **one single tree**, starting
at `/` ("root" — not the root *user*). Everything (disks, USB drives, network shares) gets
*mounted* somewhere into that one tree. This is why WSL exposes your Windows C: drive at `/mnt/c`
— it's mounted into the Linux tree at that point.

Key top-level directories:

| Path | What lives there |
|---|---|
| `/home/<you>` | Your personal files (like `C:\Users\<you>`) |
| `/etc` | System-wide config files (plain text, human-readable) |
| `/var` | Variable data — logs (`/var/log`), caches, things that grow over time |
| `/tmp` | Scratch space, wiped on reboot |
| `/usr/bin`, `/bin` | Installed programs/binaries |
| `/root` | The root user's home (not your home) |

Commands run: `pwd`, `whoami`, `ls -la ~`, `ls /`

**Syntax**: `ls [OPTIONS] [PATH]` — `-l` = long/detailed format, `-a` = include hidden (dotfiles)

**Output — `ls -la ~`**:
```
total 40
drwxr-x--- 6 devuser devuser 4096 Jul  6 14:28 .
drwxr-xr-x 3 root    root    4096 Mar 15 10:59 ..
lrwxrwxrwx 1 devuser devuser   25 Jun 26 07:08 .aws -> /mnt/c/Users/devuser/.aws
lrwxrwxrwx 1 devuser devuser   27 Jun 26 07:08 .azure -> /mnt/c/Users/devuser/.azure
-rw------- 1 devuser devuser   16 Apr 26 04:35 .bash_history
-rw-r--r-- 1 devuser devuser  220 Mar 15 10:59 .bash_logout
-rw-r--r-- 1 devuser devuser 3771 Mar 15 10:59 .bashrc
drwx------ 3 devuser devuser 4096 Jul  6 14:28 .cache
drwx------ 3 devuser devuser 4096 Jul  6 14:28 .copilot
drwxr-xr-x 4 devuser devuser 4096 Jun 26 07:08 .docker
-rw-rw-r-- 1 devuser devuser    0 Jul  6 13:50 .motd_shown
-rw-r--r-- 1 devuser devuser  807 Mar 15 10:59 .profile
drwxr-xr-x 5 devuser devuser 4096 Jul  6 14:28 .vscode-server
```
Note `.aws` and `.azure` are symlinks (`l`) into `/mnt/c/Users/devuser/...` — Windows integration
sharing AWS/Azure credentials between WSL and Windows tools.

**Output — `ls /`**:
```
Docker  bin.usr-is-merged  dev  home  lib                lib64       media  opt   root  sbin                snap  sys  usr  wslCPjKBG  wslHJKJEJ  wslaBBPlp  wslhenGkp  wslkoPokp
bin     boot               etc  init  lib.usr-is-merged  lost+found  mnt    proc  run   sbin.usr-is-merged  srv   tmp  var  wslGGfecp  wslMeLiEJ  wslhdaeDJ  wslkgkBIj  wslpBiAAJ
```

### 2. Permissions — reading `ls -la` output

Example output style:
```
drwx------ 3 devuser devuser 4096 Jul  6 14:28 .cache
-rw------- 1 devuser devuser   16 Apr 26 04:35 .bash_history
```

**Permission string breakdown** (`drwx------`):
| `d` | `rwx` | `---` | `---` |
|---|---|---|---|
| type (`d`=directory, `-`=file, `l`=symlink) | owner | group | others |

**Syntax**: `chmod MODE FILE`

**Octal notation** (`chmod 700`, etc.): each digit sums `read=4, write=2, execute=1`.
`7 = 4+2+1 = rwx`, `0 = ---`. So `700` = owner full access, group/others nothing.

**Why `.bash_history` defaults to `600` (owner-only)**: shell history can accidentally contain
sensitive data (a password typed after `mysql -p`, an API token pasted into a `curl` command). If
world-readable, any other user on a shared machine could read it and lift secrets out.

**Why execute doesn't matter on data files**: execute only matters for things meant to be *run*
— scripts, binaries, or (for directories) permission to `cd` into them. Irrelevant on a plain
data file like `.bash_history`.

**Syntax**: `head -N FILE` (or piped: `COMMAND | head -N`) — show only the first N lines

**Example**: `ls -la /etc | head -5` (pipe `ls` output into `head` to see only the first 5 lines)

**Output**:
```
total 820
drwxr-xr-x 88 root root       4096 Jul  6 14:31 .
drwxr-xr-x 33 root root       4096 Jul  6 14:30 ..
-rw-------  1 root root          0 Feb  9 19:54 .pwd.lock
-rw-r--r--  1 root root        862 Feb  9 19:54 .resolv.conf.systemd-resolved.bak
```
`.pwd.lock` — a permanent lock *target* used by the `lckpwdf()` mechanism (called by `passwd`,
`vipw`, `useradd`, and similar tools). It exists as an empty file on essentially every Linux
system at all times, whether or not an edit is in progress — its presence alone means nothing.
What actually indicates an in-progress edit is whether the file is held under an active advisory
lock at that moment, which a plain `ls`/`stat` can't reveal.
`.resolv.conf.systemd-resolved.bak` — a DNS resolver config backup, world-readable (not sensitive)
but root-only to modify.

**Ownership** — files in `/etc` are owned by `root`, not the regular user, because `/etc` is
system-wide config. If any user could edit it, they could reconfigure the whole machine. Root
ownership + restrictive permissions forces `sudo` for system changes — a deliberate safety gate.

**Special directory entries `.` and `..`**: every directory automatically contains these.
- `.` = "this directory itself" (e.g., in `/etc`, `.` refers to `/etc`)
- `..` = "the parent directory, one level up" (e.g., in `/etc`, `..` refers to `/`)
- Used constantly: `cd ..` (go up one level), `./script.sh` (run a script in the current dir)

**`stat` command** — deeper metadata than `ls -l`:

**Syntax**: `stat FILE`

**Example**: `stat ~/.bashrc`

**Output**:
```
  File: /home/devuser/.bashrc
  Size: 3771            Blocks: 8          IO Block: 4096   regular file
Device: 8,48    Inode: 46478       Links: 1
Access: (0644/-rw-r--r--)  Uid: ( 1000/ devuser)   Gid: ( 1000/ devuser)
Access: 2026-07-06 13:50:46.463647672 -0400
Modify: 2026-03-15 10:59:06.565696864 -0400
Change: 2026-03-15 10:59:06.565696864 -0400
 Birth: 2026-03-15 10:59:06.565696864 -0400
```
- `Inode` — the filesystem's real internal ID for a file's data; the filename is just a label
  pointing at it (why renames are instant, and how hard links work).
- Four timestamps:
  - **Access** — last time content was *read*
  - **Modify** — last time content was *changed*
  - **Change** — last time *metadata* changed (permissions, owner) — NOT content
  - **Birth** — creation time, never changes after

**Verified hands-on** — ran `chmod 700 ~/.bash_logout` then `chmod 644` back, checking `stat`
before/after each:
```
$ chmod 700 ~/.bash_logout && ls -l ~/.bash_logout
-rwx------ 1 devuser devuser 220 Mar 15 10:59 /home/devuser/.bash_logout

$ stat ~/.bash_logout
  File: /home/devuser/.bash_logout
  Size: 220             Blocks: 8          IO Block: 4096   regular file
Device: 8,48    Inode: 1236        Links: 1
Access: (0700/-rwx------)  Uid: ( 1000/ devuser)   Gid: ( 1000/ devuser)
Access: 2026-07-06 17:25:03.251284111 -0400
Modify: 2026-03-15 10:59:06.565696864 -0400
Change: 2026-07-06 17:24:37.354927872 -0400
 Birth: 2026-03-15 10:59:06.565696864 -0400

$ chmod 644 ~/.bash_logout && ls -l ~/.bash_logout
-rw-r--r-- 1 devuser devuser 220 Mar 15 10:59 /home/devuser/.bash_logout

$ stat ~/.bash_logout
  File: /home/devuser/.bash_logout
  Size: 220             Blocks: 8          IO Block: 4096   regular file
Device: 8,48    Inode: 1236        Links: 1
Access: (0644/-rw-r--r--)  Uid: ( 1000/ devuser)   Gid: ( 1000/ devuser)
Access: 2026-07-06 17:25:03.251284111 -0400
Modify: 2026-03-15 10:59:06.565696864 -0400
Change: 2026-07-06 17:26:48.552676456 -0400
 Birth: 2026-03-15 10:59:06.565696864 -0400
```
**Confirmed**: `Modify` and `Birth` stayed identical across both changes (content untouched),
`Change` updated on each `chmod` (metadata changed — exactly what `Change` tracks). Note `Access`
itself was untouched by either `chmod` too — `stat` only reads metadata, it never touches a
file's Access time. Reading a file's actual *content* (e.g. `cat`) is what can bump Access, and
even then many Linux setups mount with `relatime`/`noatime` for performance, throttling those
updates.

**WSL ↔ Windows File Explorer**: WSL's Linux filesystem is browsable from Windows at
`Linux → Ubuntu → home → <user>` in File Explorer's left sidebar (a separate top-level section,
not nested under "This PC"). It's not literally "inside C:\" — it's a separate virtual disk that
Windows can browse into via a special protocol.

### 3. Filesystem navigation & manipulation

**Syntax**: `cd [PATH]` — absolute path (starts with `/`, works from anywhere) vs relative path
(starts from wherever you currently are)

**Syntax**: `pwd` — prints the current working directory's absolute path, no arguments.

**Verified hands-on**:
```
$ cd /tmp && pwd
/tmp
$ cd ~ && pwd
/home/devuser
$ cd .. && pwd
/home
```
(third command run from `/home/devuser` — `..` correctly moved up exactly one level to `/home`)

**Syntax**: `mkdir [-p] PATH`

**Example**: `mkdir test1` creates a folder in the current directory. `mkdir -p a/b/c` creates the
whole nested chain in one shot, including missing parents, and doesn't error if directories
already exist.

**Verified hands-on**: bare `mkdir a/b/c` (no `-p`) failed since `a` didn't exist yet
(`mkdir: cannot create directory 'a/b/c': No such file or directory` — standard error shape;
exact wording not logged verbatim in-session). `mkdir -p a/b/c` then succeeded, creating all
three nested levels in one command — confirmed via `ls -la a` and `ls -la a/b` showing the
nested folders in place.

**Syntax**: `cp [-r] SOURCE DEST` — copy a file (`-r` for a directory tree)
**Syntax**: `mv SOURCE DEST` — move, and also how Linux renames a file (no separate `rename`
command)

**Verified hands-on** — filesystem manipulation sequence:
```
$ cd ~ && mkdir -p practice/subdir && cd practice
$ echo "hello linux" > file1.txt
$ cp file1.txt file2.txt
$ mv file2.txt renamed.txt
$ ls -la
total 16
drwxr-xr-x 2 devuser devuser 4096 Jul  6 18:37 .
drwxr-x--- 7 devuser devuser 4096 Jul  6 18:34 ..
-rw-r--r-- 1 devuser devuser   12 Jul  6 18:37 file1.txt
-rw-r--r-- 1 devuser devuser   12 Jul  6 18:37 renamed.txt
```
(`subdir` doesn't appear — it was separately created and removed with `rm -r subdir` to test
deletion, confirmed clean with no trace left)
**Syntax**: `rm [-r] PATH`
- **`rm file`** — deletes a file. **`rm folder` alone fails** — it refuses to delete directories
  without `-r`. **`rm -r folder`** deletes a folder and everything inside, recursively,
  permanently.
- **No recycle bin at the shell level** — `rm` immediately unlinks the filename from its inode
  and frees the disk space; no confirmation, no undo. This is true even for files that happen to
  be visible from Windows File Explorer (via WSL) — deleting through WSL's `rm` never routes
  through Windows' NTFS delete APIs, so it never touches the Windows Recycle Bin, regardless of
  visibility from Explorer.

**Syntax**: `touch FILE`
- **`touch filename`** — creates an empty file if it doesn't exist, or updates timestamps if it
  does. **`> filename`** also creates/truncates a file to empty as a side effect.

### 4. SSH — concepts (hands-on install blocked, see troubleshooting log)

**Why SSH exists**: `telnet` and similar older tools sent everything, including passwords, in
plain text over the network. SSH (**S**ecure **SH**ell) encrypts the entire session.

**Two authentication methods**:
1. Password-based — weaker, often disabled in production.
2. Key-based — the standard. A key pair: **private key** (secret, stays only on your machine) and
   **public key** (safe to share, placed on the remote server).

**Mechanism (public-key authentication, signature-based)**:
1. Your public key is placed on the server in `~/.ssh/authorized_keys`.
2. On connection attempt, the server sends a random challenge value tied to this session.
3. Your machine signs that challenge using the **private** key, sends the signature back.
4. Server verifies the signature against your known public key. Proves you hold the private
   key — the private key itself is **never transmitted**, only proof of possession via a valid
   signature.

**Why swapping public/private keys is dangerous**: the private key is what proves your identity.
Anyone who obtains it can impersonate you on every server carrying the matching public key — no
password needed, until revoked everywhere. This is a real, common incident (private keys
accidentally committed to public GitHub repos get exploited by bots within minutes). Handing out
a public key, by contrast, grants zero login ability by itself.

**Related but distinct actions**:
- Uninstall the SSH server software: `sudo apt remove openssh-server`
- Stop the server temporarily (stays installed): `sudo systemctl stop ssh`
- Disconnect one active session: client types `exit`/`Ctrl+D`, or server admin kills that
  specific connection's process

### 5. VMs — core concepts

**What is a VM**: software emulating an entire physical computer (virtual CPU, memory, disk,
network) via a **hypervisor**, which divides one physical machine's resources among isolated
guest operating systems. Each VM runs its **own full OS kernel** — this is the single fact that
distinguishes it from a container.

**Type 1 (bare-metal) vs Type 2 (hosted) hypervisors**:
- The distinction is **architecture** (does it run directly on hardware, or as an app on top of
  an already-running host OS?) — **not** "personal machine vs. data center."
- **Type 1**: runs directly on hardware, no host OS underneath (VMware ESXi; also **Hyper-V**,
  which WSL2 runs on). When Hyper-V is enabled, Windows itself becomes a "parent partition"
  running *alongside* guest VMs, with Hyper-V sitting below all of them — so even a personal
  Windows laptop can be running a genuine Type 1 hypervisor.
- **Type 2**: installs as a regular application inside an already-booted host OS (VirtualBox,
  VMware Workstation).
- **Plain-English analogy**: Type 1 = build a foundation directly on the ground, then build
  several apartments on top of it (one of those apartments is "Windows," another is the WSL2
  Ubuntu VM — neither is in charge of the other, both are residents on the same foundation).
  Type 2 = the house (Windows) is already fully built; afterward you add a shed in the backyard
  (VirtualBox), and inside the shed there's another mini-house (the VM) — added after the fact,
  inside an already-finished house.

**VM vs container — kernel sharing**:
- A VM has its **own separate kernel** — fully self-sufficient, isolated from the host and from
  other VMs.
- A container **shares the host's (or host VM's) kernel** instead of running its own — lighter,
  but less isolated.
- **Analogy**: a physical server is a plot of land. A VM is a separate apartment building built
  on that land, with its own complete utilities (kitchen, plumbing = kernel). A container is a
  room inside one apartment, sharing that apartment's utilities with other rooms (other
  containers) in the same VM.

**Reboot / blast-radius scope** (a common point of confusion, corrected during this session):
- Rebooting the **physical server** (the plot of land losing power) takes down *everything* —
  every VM and every container inside every VM. Nothing survives this; it's the ground everything
  else is built on.
- Rebooting **one specific VM** only takes down the containers inside *that* VM. Other VMs on the
  same physical host, with their own separate kernels, are unaffected. This is the real isolation
  benefit VMs provide: **protection between VMs on shared hardware**, not protection from the
  hardware itself failing.

**Speed and resource tradeoffs**:
- VMs boot slowly (minutes) — an entire OS/kernel has to start from zero, like a real computer
  powering on. VMs are heavy on memory/disk — every VM duplicates a full OS.
- Containers start almost instantly (seconds or less) — the kernel is already running; a
  container is an isolated process launching on top of it, not a machine booting. Containers are
  lightweight — only the app and its direct dependencies, no duplicated OS.

**Interview-style scenario practiced**: "explain the VM vs. container tradeoff to a non-technical
stakeholder" → *"A VM is like giving each app its own complete computer — very safe and isolated,
but slow to start and expensive. A container is like giving each app its own private room in a
computer that's already running — much faster and cheaper, with slightly less isolation."*

**Interview-style scenario practiced**: isolating two untrusted customer workloads → choose
separate VMs, because a kernel exploit in a shared-kernel container setup could let an attacker
escape into the shared kernel and reach the other workload; separate VMs mean separate kernels,
containing the blast radius.

**Interview-style scenario practiced**: a file with `777` permissions → the real risk isn't vague
"anyone can mess with it," it's specific: if the file is a script later executed automatically by
a **more privileged process** (e.g., a root cron job), and an unprivileged attacker has **write**
access (granted by `777`), they can replace the script's contents with malicious code. When root
runs it on schedule, the attacker's code executes **with root's permission** — privilege
escalation via a writable execution path, a real, common security-audit finding.

### Troubleshooting log — corporate network blocked local SSH server install

**Goal**: install `openssh-server` in WSL Ubuntu to practice an actual SSH connection.

**Command run**: `sudo apt update && sudo apt install openssh-server`
**Result**: package resolution succeeded, but the downloads failed, so the install never
completed — `Cannot initiate the connection ... Network is unreachable` (IPv6) and
`connection timed out` (IPv4 fallback addresses).

**Diagnosis steps**:
1. `which sshd` → empty, confirmed `sshd` wasn't installed yet.
2. **`curl -Is https://google.com`** (quick headers-only check) — ran first, and it just hung
   indefinitely with a blinking cursor, no output at all, until cancelled with **Ctrl+C**. This
   itself was diagnostically meaningful: a hang with no response (versus an instant "connection
   refused") is the classic signature of a **firewall silently dropping outbound packets**
   rather than actively rejecting them — an active reject would come back fast; a silent drop
   just leaves you waiting.
3. **`curl -v --max-time <n> <url>`** — ran `curl -v --max-time 10 https://google.com` and the
   `http://` variant → **DNS resolved fine**
   (got both IPv4 and IPv6 addresses back), but the actual **TCP connection timed out** on the
   IPv4 address, and IPv6 failed instantly with "Network is unreachable" (WSL has no IPv6 route
   out at all — separate, minor issue).
4. Confirmed Windows browsers (Edge/Chrome) work fine on the same network — ruling out "no
   internet at all," pointing instead at a WSL-specific gap.
5. Checked Windows proxy config: `netsh winhttp show proxy` → "Direct access (no proxy server)"
   at the system level.
6. Checked per-user Internet Settings (Settings → Network & Internet → Proxy): "Automatically
   detect settings" (WPAD-style auto-discovery) was ON; no static address to read off directly.
7. Checked `edge://net-internals/#proxy` for the browser's actual effective proxy → no
   "Effective proxy settings" section populated, suggesting the browser may be using a **direct**
   connection too, and the actual traffic control is likely a network-level
   firewall/DPI appliance (not a classic HTTP proxy), filtering non-browser traffic like `apt`
   differently from browser TLS traffic.

**Conclusion**: root cause is network-level (corporate firewall), not something fixable from
within WSL alone — likely needs an IT-provided proxy address or a policy exception. A possible
fallback mentioned but not pursued in-session: **WSL2's mirrored networking mode / the
`autoProxy` feature** — a built-in WSL capability that can automatically mirror Windows' own
proxy settings into WSL without manual configuration, worth checking if this comes up again.
**Deferred**: hands-on SSH connection will be done later against an AWS sandbox VM instead, where
`sshd` is pre-installed and this local-install problem doesn't apply.

**Key command reference from this troubleshooting session**:
| Command | Purpose |
|---|---|
| `which <program>` | Check if a program is installed and show its path, or nothing if not found |
| `sudo apt update` | Refresh the package manager's list of available packages/versions |
| `sudo apt install -y <pkg>` | Install a package, auto-confirming prompts |
| `curl -Is <url>` | Fetch only HTTP headers from a URL — quick reachability check |
| `curl -v --max-time <n> <url>` | Verbose connection attempt with a timeout, showing each stage |
| `netsh winhttp show proxy` | (Windows) show the system-wide WinHTTP proxy config |

---

## Day 2 — 2026-07-07 (harder scenarios + quiz)

### Today's agenda
1. Permission troubleshooting — solved independently.
2. Hard links vs. symbolic links — the inode model, proven hands-on.
3. `rm` and links — precision correction.
4. SSH — key generation.
5. SSH — `known_hosts` and `~/.ssh/config`.
6. VM/container isolation — real project tie-in.
7. The quiz.

### 1. Permission troubleshooting — solved independently

**Scenario**: created a script, ran it, got `Permission denied`.

```
$ echo 'echo "hello from script"' > myscript.sh
$ ./myscript.sh
bash: ./myscript.sh: Permission denied

$ ls -l myscript.sh
-rw-r--r-- 1 devuser devuser 25 Jul  7 ... myscript.sh
```

**Diagnosis**: `>` redirection creates files with default `644` (`rw-r--r--`) — read/write, no
execute for anyone. Editing/opening works (needs read/write), running fails (needs execute).

**Syntax**: `chmod OCTAL FILE` — recompute the octal digit-by-digit: `read=4, write=2, execute=1`.
Owner needed `rw-` (`6`) → add execute → `7`. Group/others stay `r--` (`4`) each, unchanged.

**Fix**: `chmod 744 myscript.sh` → `rwxr--r--` → confirmed working:
```
$ chmod 744 myscript.sh
$ ls -l myscript.sh
-rwxr--r-- 1 devuser devuser 25 Jul  7 ... myscript.sh
$ ./myscript.sh
hello from script
```
(Initial guess was `711` — rejected on review: it *does* add owner execute, but also strips
group/others' existing read and grants them execute instead, changing things that weren't asked
to change. `744` is the precise fix — add only what's missing, leave the rest untouched.)

### 2. Hard links vs. symbolic links — the inode model, proven hands-on

**The core idea**: a file's *name* and its *data* are different things. The name is a label
pointing at an **inode** (the filesystem's real internal ID for the data — see Day 1's `stat`
section). Multiple names can point at the same inode.

**Syntax**: `ln TARGET LINK_NAME` (hard link — TARGET must exist, LINK_NAME must not already
exist unless `-f` is used) · `ln -s TARGET LINK_NAME` (symlink — same rule)

**Verified hands-on — creating both**:
```
$ echo "original content" > original.txt
$ ln original.txt hardlink.txt
$ ln -s original.txt symlink.txt
$ ls -li original.txt hardlink.txt symlink.txt
50105 -rw-r--r-- 2 devuser devuser 17 Jul  7 16:09 hardlink.txt
50105 -rw-r--r-- 2 devuser devuser 17 Jul  7 16:09 original.txt
50106 lrwxrwxrwx 1 devuser devuser 12 Jul  7 16:09 symlink.txt -> original.txt
```
`original.txt` and `hardlink.txt` share inode `50105`, link count `2` — genuinely the same file,
two names. `symlink.txt` has its own separate inode `50106`, type `l`, and just stores the path
text `original.txt` (12 bytes — the length of that path string).

**Syntax**: `cat FILE [FILE...]` — prints a file's contents to the terminal, no paging.

**Verified hands-on — deleting the original**:
```
$ rm original.txt
$ cat hardlink.txt
original content
$ cat symlink.txt
cat: symlink.txt: No such file or directory
```
`hardlink.txt` survives — the data isn't freed until the link count hits `0`, and one name
(`hardlink.txt`) still points at it. `symlink.txt` breaks (**dangling symlink**) — it only ever
stored a path, and that path no longer resolves to anything.

**Real discovery — a hard link to a symlink links to the symlink itself, not its target**:
```
$ ln symlink.txt hardlink2.txt
$ ls -li symlink.txt hardlink2.txt
50106 lrwxrwxrwx 2 devuser devuser 12 Jul  7 16:09 hardlink2.txt -> original.txt
50106 lrwxrwxrwx 2 devuser devuser 12 Jul  7 16:09 symlink.txt -> original.txt
```
`ln` (no `-s`) does **not** dereference/follow a symlink source — it hard-links directly to the
symlink's own inode. Since that inode's data *is* "I am a symlink pointing at `original.txt`,"
the new name is *also* a symlink with the same broken target — proven by both showing type `l`
and the same `-> original.txt`.

**Real discovery — `ln -f` can silently destroy the last copy of real data**:
```
$ cat hardlink.txt
original content
$ ln symlink.txt hardlink.txt
ln: failed to create hard link 'hardlink.txt': File exists
$ ln -f symlink.txt hardlink.txt
$ cat hardlink.txt
cat: hardlink.txt: No such file or directory
```
At this point `hardlink.txt` (inode `50105`) was the **only** remaining name holding the real
`"original content"` data (link count `1`). `ln -f` removed that name first (to make room for the
new link), dropping the count to `0` — permanently freeing the data — then relinked `hardlink.txt`
to the symlink's inode (`50106`) instead. Net effect: identical to what `-f` was warned about
earlier — it can delete-then-recreate a name, discarding whatever the name used to point to, with
no confirmation and no recovery.

**Re-teach — the library-book analogy** (built from scratch after confusion resurfaced following
the `ln -f` experiments above): a **hard link** is like a second catalog card in the library's
card catalog, pointing at the exact same physical book on the shelf — there's still only one book
(one inode), just two cards (names) that both lead to it. A **symlink** is like a separate sticky
note that just says "go check shelf 12B" — it isn't the book and isn't even a catalog card, it's
only a pointer to where the book is supposed to be. If the actual book gets removed from shelf
12B, the sticky note is now pointing at nothing (a dangling symlink), while a second catalog card
for that same book would be unaffected as long as the book itself still physically exists
somewhere.

**Follow-up — `ln -s` (not `-f` alone) creates a genuinely new symlink, chained**:
```
$ ln -s symlink.txt hardlink.txt
ln: failed to create symbolic link 'hardlink.txt': File exists
$ ln -fs symlink.txt hardlink.txt
$ cat hardlink.txt
cat: hardlink.txt: No such file or directory
```
This created a **new, separate inode** for `hardlink.txt` (unlike the plain `ln` case above) that
stores the path `symlink.txt` — a two-hop chain: `hardlink.txt` → `symlink.txt` → `original.txt`
(missing). Broken at the final hop for the same underlying reason. `ls -li` would show a
**different** inode number for `hardlink.txt` here vs. the earlier plain-`ln` case, confirming
`-s` always creates a new file rather than reusing an existing inode.

**Key mental model, confirmed by direct test** — editing through *either* name of a hard-linked
pair changes the *one* shared file, visible via both names immediately:
```
$ echo "hello" > book.txt
$ ln book.txt card2.txt
$ echo "edited via card2" > card2.txt
$ cat book.txt
edited via card2
$ cat card2.txt
edited via card2
$ ls -li book.txt card2.txt
50107 -rw-r--r-- 2 devuser devuser 17 Jul  7 18:28 book.txt
50107 -rw-r--r-- 2 devuser devuser 17 Jul  7 18:28 card2.txt
```
(Note: `>` here *overwrote* rather than appended, replacing "hello" entirely — see `>` vs `>>`
below. The point still stands: both names show identical content because they're the same inode.)

**`>` vs `>>`**:

**Syntax**: `command > file` (overwrite — replaces all existing content) · `command >> file`
(append — adds to the end, keeping existing content)
```
echo "line 1" > file.txt      # file.txt: line 1
echo "line 2" > file.txt      # file.txt: line 2   (line 1 is gone)
echo "line 3" >> file.txt     # file.txt: line 2 / line 3
```

**Practical difference table — hard link vs. symlink**:
| | Hard link | Symlink |
|---|---|---|
| What it is | 2nd name, same inode | separate file storing a path string |
| Can it be created across filesystems/drives? | No — must stay on the same filesystem | Yes — can point across drives |
| If the target is deleted | Survives (until link count hits 0) — there's no separate "target," just another name for the same data | Breaks (dangling) — the stored path no longer resolves |
| If the target is moved | Not applicable — same inode, no separate "target" to move | Breaks (dangling) — a symlink only stores a fixed path, it doesn't track the file if it moves |

### 3. `rm` and links — precision correction

`rm` doesn't directly "delete data" — it removes **one name** and decrements that inode's link
count by 1. Data is only actually freed once the count reaches **0** (every name pointing at it
is gone). For an ordinary file with only one name, this looks identical to instant deletion — but
the mechanism underneath is always "unlink a name," which is exactly what made the `ln -f`
data-loss scenario above possible without ever running `rm` directly.

### 4. SSH — key generation (hands-on)

**Syntax**: `ssh-keygen -t TYPE -f FILEPATH`
- `-t` — key type/algorithm. Chose `ed25519` deliberately (not RSA) — smaller, faster, and the
  current best-practice recommendation over older RSA/ECDSA, unless a legacy system requires RSA.
- `-f` — output path; produces two files: `FILEPATH` (private key) and `FILEPATH.pub` (public key)

**Example**: `ssh-keygen -t ed25519 -f ~/.ssh/id_test` (passphrase skipped with Enter/Enter for
this practice run — production keys would normally set one)

**Verified hands-on**: confirmed via `ls -la ~/.ssh/` (private key contents intentionally never
pasted/viewed in chat — correct practice) — `id_test` shows `600` (`rw-------`, owner-only, as
expected for a private key) and `id_test.pub` shows `644` (`rw-r--r--`, freely readable, as
expected for a public key).

### 5. SSH — `known_hosts` and `~/.ssh/config`

**`known_hosts`** — a *file* (not a folder) inside `~/.ssh/`, created automatically the first
time you connect to any new remote server. On first connection, SSH shows the server's
fingerprint and asks for confirmation (protects against man-in-the-middle attacks); once
accepted, that server's identity is appended as a new line. Future connections are silently
checked against this — if a server's identity ever doesn't match, SSH refuses and warns loudly.

**`~/.ssh/config`** — connection shortcuts, one block per host:
```
Host myserver
    HostName 1.2.3.4
    User ec2-user
    IdentityFile ~/.ssh/id_test
```
Turns `ssh -i ~/.ssh/id_test ec2-user@1.2.3.4` into just `ssh myserver`. (Deferred full hands-on
until AWS sandbox access is ready — the value of this will click faster once actually typing the
long form repeatedly.)

**`-i` flag** (identity file): tells `ssh` which private key to use, since custom key filenames
(like `id_test`) aren't in the small set `ssh` tries automatically by default.

### 6. VM/container isolation — real project tie-in

**Scenario**: the project will run containers on Kubernetes, on EC2 (VMs), on AWS. Why not
containers directly on bare physical servers, skipping the VM layer entirely?

**Answer, reached with follow-up pushback**: AWS physical hardware is **multi-tenant** — multiple
unrelated customers' workloads can share the same physical machine. If containers ran directly on
bare metal with no VM boundary, all tenants on that machine would share **one kernel** — a kernel
exploit letting one tenant's container escape could let an attacker reach every other tenant's
containers on that same kernel (a real, documented **container escape / cross-tenant attack**
class). The VM layer gives each AWS customer their **own separate kernel** — a hard boundary that
survives even a full container compromise inside another customer's VM. Within *your own* VM, your
own containers still share *your* VM's kernel with each other, which is fine, since they're all
yours.

**Interview-answer lesson learned this session**: naming the right general concept ("privacy",
"a hardwall") isn't sufficient — an interviewer pushes for the specific mechanism. Full-credit
shape: *name the concept → trace the actual mechanism step by step → name the concrete
consequence.* E.g. "kernel-sharing" isn't enough on its own; "a kernel exploit lets an attacker
escape their container and reach the shared kernel, which other tenants' containers also run on"
is the complete answer.

---

## Topic 1 Quiz — both days combined — Attempt 1: PASS, 90/100

Interview-style, open-ended, no multiple choice. Ran ~32 minutes (over the 20-min cap — allowed
to finish in progress rather than cut mid-question). Question and full correct answer for each:

1. **Decode `-rwxr-xr-- 1 alice devs 2048 Jan 5 10:00 deploy.sh` fully.**
   The first character `-` is the file type — a regular file (`d` would mean directory, `l` a
   symlink). The next nine characters split into three groups of three: `rwx` for the **owner**,
   `r-x` for the **group**, `r--` for **others**. So the owner can read, write, and execute;
   anyone in the file's group can read and execute but not write; everyone else can only read.
   `alice` and `devs` are two separate fields, not one merged label — `alice` is the owning user,
   `devs` is the owning group. `2048` is the file's size in bytes. `Jan 5 10:00` is the **Modify**
   timestamp — the last time the file's *content* changed — not the file's creation/Birth time;
   `ls -l` shows Modify by default, while `stat` shows all four timestamps, including Birth,
   which `ls` can't show at all. `deploy.sh` is the filename.

2. **A root cron job runs `/opt/scripts/backup.sh`, permissions `777`, owned by root — what's the
   fix?**
   `777` means `rwxrwxrwx` — owner, group, and everyone else all have read, write, and execute.
   The dangerous part is that **anyone on the system can write to this file**, and it's executed
   automatically and repeatedly by root's cron job. An unprivileged attacker could overwrite the
   script's contents with malicious code; the next time cron fires, root runs that script and the
   attacker's code executes with root's own permissions — privilege escalation through a writable
   execution path. The fix is `chmod 700 /opt/scripts/backup.sh`, giving the owner (root) full
   `rwx` and stripping every permission from group and others (`---`). Root can still execute it
   because root itself owns the file and cron runs it as root. `600` is not the fix, even though
   it also locks out other users — it removes execute entirely, so cron couldn't run the script at
   all; the final mode must retain owner execute (so cron can still run it) while stripping
   group/other write (so no one else can tamper with it), not just lock everything down
   indiscriminately.

3. **Hard link `B` to `A`, then `rm A` — what happens at the filesystem level?**
   `ln A B` creates a second filename, `B`, pointing at the exact same inode as `A` — not a copy,
   the same underlying data — bringing that inode's link count to `2`. `rm A` does not delete the
   data; it only removes the name `A` and decrements the inode's link count by one, down to `1`.
   Since `B` still holds a name pointing at that inode, the actual data is untouched and fully
   readable through `B`. Data on a Linux filesystem is only actually freed once an inode's link
   count reaches `0` — i.e., once every name pointing at it is gone.

4. **Full SSH key-based auth mechanism, step by step.**
   SSH key auth relies on a key pair: a **private key**, which stays secret on your own machine
   and is never transmitted anywhere, and a **public key**, which is safe to share and gets placed
   on the remote server. The steps: (1) your public key is copied onto the server, into
   `~/.ssh/authorized_keys`. (2) When you attempt to connect, the server sends a random challenge
   value tied to this session. (3) Your machine signs that challenge using the matching
   **private** key and sends the signature back to the server. (4) The server verifies the
   signature against your known public key. Only the holder of the matching private key could
   have produced a valid signature, so this proves your identity — without the private key itself
   ever crossing the network, only proof that you possess it.

5. **Why separate VMs over separate containers for two untrusted customers on shared hardware?**
   AWS's physical hardware is multi-tenant — unrelated customers can end up sharing the same
   physical machine. Containers share the kernel of whatever they run on top of. If two untrusted
   customers' containers ran directly on bare metal with no VM boundary between them, both sets of
   containers would share **one kernel** — and a kernel exploit that lets an attacker escape their
   own container would let them reach that shared kernel, and from the kernel, reach the other
   customer's containers running on it too (a real, documented container-escape / cross-tenant
   attack class). Putting a VM layer between them gives each customer their **own separate
   kernel** — a hard boundary that still holds even if an attacker fully compromises a container,
   because their escape only ever reaches their own VM's kernel, never the other customer's.
   Within one customer's own VM, their own containers sharing that one VM's kernel with each other
   is fine, since it's all the same customer's workloads.

6. **Hard link vs. symlink: file moves to another drive / file gets deleted.**
   A hard link cannot even be *created* pointing across two different drives/filesystems in the
   first place — hard links work by referencing an inode number directly, and inode numbers are
   only unique within a single filesystem, so there's no way to hard-link to an inode on a
   different device. A symlink, by contrast, *can* be created pointing across drives, since it
   just stores a path string rather than referencing an inode — but if the target file
   subsequently *moves* (to another location, on the same or a different drive), the symlink
   breaks (dangling), because it only ever stored a fixed path and has no way to track the file if
   that path stops resolving. On deletion: a hard link survives the target being deleted, because
   it's a second name pointing at the same inode, and the data persists as long as the inode's
   link count is still above `0`. A symlink does not survive — it breaks (dangling) the moment its
   stored path no longer resolves to anything, since a symlink never held the data itself, only a
   path to it.

**How the actual quiz session went** (for context, not the answers themselves): Q1 needed a
correction on the owner/group split and Modify-vs-Birth timestamp; Q2 needed a correction from an
initial `600` answer to the correct `700`; Q3 passed cleanly, first try; Q4 passed cleanly, first
try; Q5 needed two follow-up nudges to move from "privacy"/"hardwall" to the specific shared
resource (kernel) and attack path (container escape); Q6 needed a correction on conflating
"created across drives" with "moves after creation."

**Score: 90/100**
- **Quiz 36/40** — 4 of 6 answers needed a real correction or follow-up nudge (permission
  decoding's two-field/timestamp mixup, the cron-script fix, VM-vs-container justification, hard
  link/symlink edge case), 2 passed cleanly.
- **Hands-on 27/30** — real corporate-proxy troubleshooting and independent permission fixes,
  though the actual SSH connection stayed deferred.
- **Depth 27/30** — solid VM/container isolation reasoning, though it took two full explanation
  passes to land.

**Verdict**: **Topic 1 CLEARED, attempt 1, 90/100.**
