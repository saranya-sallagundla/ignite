# Topic 1 — Linux Fundamentals: Filesystem, SSH, VMs

> Personal study notebook — full teaching content, commands, outputs, and explanations.
> Distinct from `progress.md` (tracking) and `session_notes.md` (short personal reflection).
> Organized by topic, filled in day by day as the topic is covered.

---

## Day 1 — 2026-07-06 (heavy scaffolding, guided walkthrough)

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

### 2. Permissions — reading `ls -la` output

Example output style:
```
drwxr-x--- 6 devuser devuser 4096 Jul  6 14:28 .cache
-rw------- 1 devuser devuser   16 Apr 26 04:35 .bash_history
```

**Permission string breakdown** (`drwxr-x---`):
```
d rwx r-x ---
│ │   │   │
│ owner group others
type (d=directory, -=file, l=symlink)
```

**Octal notation** — `chmod 700` etc: each digit sums `read=4, write=2, execute=1`.
`7 = 4+2+1 = rwx`, `0 = ---`. So `700` = owner full access, group/others nothing.

**Why `.bash_history` defaults to `600` (owner-only)**: shell history can accidentally contain
sensitive data (a password typed after `mysql -p`, an API token pasted into a `curl` command). If
world-readable, any other user on a shared machine could read it and lift secrets out.

**Why execute doesn't matter on data files**: execute only matters for things meant to be *run*
— scripts, binaries, or (for directories) permission to `cd` into them. Irrelevant on a plain
data file like `.bash_history`.

**Ownership** — files in `/etc` are owned by `root`, not the regular user, because `/etc` is
system-wide config. If any user could edit it, they could reconfigure the whole machine. Root
ownership + restrictive permissions forces `sudo` for system changes — a deliberate safety gate.

**Special directory entries `.` and `..`**: every directory automatically contains these.
- `.` = "this directory itself" (e.g., in `/etc`, `.` refers to `/etc`)
- `..` = "the parent directory, one level up" (e.g., in `/etc`, `..` refers to `/`)
- Used constantly: `cd ..` (go up one level), `./script.sh` (run a script in the current dir)

**`stat` command** — deeper metadata than `ls -l`:
```
stat ~/.bashrc
```
- `Inode` — the filesystem's real internal ID for a file's data; the filename is just a label
  pointing at it (why renames are instant, and how hard links work).
- Four timestamps:
  - **Access** — last time content was *read*
  - **Modify** — last time content was *changed*
  - **Change** — last time *metadata* changed (permissions, owner) — NOT content
  - **Birth** — creation time, never changes after

**Verified hands-on**: ran `chmod 700 ~/.bash_logout` then `chmod 644` back, checking `stat`
before/after each. Confirmed: `Modify` and `Birth` stayed identical (content untouched), `Change`
updated on each `chmod` (metadata changed), `Access` didn't reliably update on a plain `stat` read
(many Linux setups mount with `relatime`/`noatime` for performance, throttling Access updates).

**WSL ↔ Windows File Explorer**: WSL's Linux filesystem is browsable from Windows at
`Linux → Ubuntu → home → <user>` in File Explorer's left sidebar (a separate top-level section,
not nested under "This PC"). It's not literally "inside C:\" — it's a separate virtual disk that
Windows can browse into via a special protocol.

### 3. Filesystem navigation & manipulation

- **`cd`** — absolute path (`cd /etc`, works from anywhere) vs relative path (`cd ..`, `cd
  projects`, relative to current location).
- **`mkdir`** — `mkdir test1` creates a folder. **`mkdir -p a/b/c`** creates the whole nested
  chain in one shot, including missing parents, and doesn't error if directories already exist.
  Verified hands-on: `mkdir a/b/c` (no `-p`) failed with "No such file or directory" since `a`
  didn't exist yet; `mkdir -p a/b/c` succeeded and created all three nested levels.
- **`cp source dest`** — copy a file (`-r` for a directory tree).
- **`mv source dest`** — move, and also how Linux renames a file (no separate `rename` command).
- **`rm file`** — deletes a file. **`rm folder` alone fails** — it refuses to delete directories
  without `-r`. **`rm -r folder`** deletes a folder and everything inside, recursively,
  permanently.
- **No recycle bin at the shell level** — `rm` immediately unlinks the filename from its inode
  and frees the disk space; no confirmation, no undo. This is true even for files that happen to
  be visible from Windows File Explorer (via WSL) — deleting through WSL's `rm` never routes
  through Windows' NTFS delete APIs, so it never touches the Windows Recycle Bin, regardless of
  visibility from Explorer.
- **`touch filename`** — creates an empty file if it doesn't exist, or updates timestamps if it
  does. **`> filename`** also creates/truncates a file to empty as a side effect.

### 4. SSH — concepts (hands-on install blocked, see troubleshooting log)

**Why SSH exists**: `telnet` and similar older tools sent everything, including passwords, in
plain text over the network. SSH (**S**ecure **SH**ell) encrypts the entire session.

**Two authentication methods**:
1. Password-based — weaker, often disabled in production.
2. Key-based — the standard. A key pair: **private key** (secret, stays only on your machine) and
   **public key** (safe to share, placed on the remote server).

**Mechanism (challenge-response)**:
1. Your public key is placed on the server in `~/.ssh/authorized_keys`.
2. On connection attempt, the server generates a random challenge, encrypts it with your public
   key, sends it to you.
3. Your machine decrypts/signs it using the **private** key, sends the response back.
4. Server verifies the response. Proves you hold the private key — the private key itself is
   **never transmitted**, only proof of possession.

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
**Result**: install itself succeeded for package resolution, but package *downloads* failed —
`Cannot initiate the connection ... Network is unreachable` (IPv6) and `connection timed out`
(IPv4 fallback addresses).

**Diagnosis steps**:
1. `which sshd` → empty, confirmed `sshd` wasn't installed yet.
2. `curl -v --max-time 10 https://google.com` and the `http://` variant → **DNS resolved fine**
   (got both IPv4 and IPv6 addresses back), but the actual **TCP connection timed out** on the
   IPv4 address, and IPv6 failed instantly with "Network is unreachable" (WSL has no IPv6 route
   out at all — separate, minor issue).
3. Confirmed Windows browsers (Edge/Chrome) work fine on the same network — ruling out "no
   internet at all," pointing instead at a WSL-specific gap.
4. Checked Windows proxy config: `netsh winhttp show proxy` → "Direct access (no proxy server)"
   at the system level.
5. Checked per-user Internet Settings (Settings → Network & Internet → Proxy): "Automatically
   detect settings" (WPAD-style auto-discovery) was ON; no static address to read off directly.
6. Checked `edge://net-internals/#proxy` for the browser's actual effective proxy → no
   "Effective proxy settings" section populated, suggesting the browser may be using a **direct**
   connection too, and the actual traffic control is likely a network-level
   firewall/DPI appliance (not a classic HTTP proxy), filtering non-browser traffic like `apt`
   differently from browser TLS traffic.

**Conclusion**: root cause is network-level (corporate firewall), not something fixable from
within WSL alone — likely needs an IT-provided proxy address or a policy exception. **Deferred**:
hands-on SSH connection will be done later against an AWS sandbox VM instead, where `sshd` is
pre-installed and this local-install problem doesn't apply.

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

_To be filled in as Day 2 progresses._
