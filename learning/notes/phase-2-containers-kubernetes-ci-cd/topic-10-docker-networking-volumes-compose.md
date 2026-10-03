# Topic 10 — Docker: Networking, Volumes, Docker Compose

> Personal study notebook — full teaching content, commands, outputs, and explanations.
> Distinct from `progress.md` (tracking) and `session_notes.md` (short personal reflection).
> Two-day topic per the roadmap — covered across two sessions, ending in the quiz.

---

## Day 1 — 2026-07-22 / 2026-07-23

### Today's agenda
1. Docker networking — bridges, container-to-container communication, DNS by name.
2. Port publishing, tied to Topic 5's private/public IPs.
3. Docker volumes — bind mounts vs. named volumes.

### 1. The Docker bridge network

**Analogy used**: two separate neighborhoods with no road connecting them — no car can get from
one to the other. A **bridge** connects the two road systems, and cars can now cross. Docker's
`bridge` network driver builds that connecting bridge virtually: every container that joins the
same bridge network is a "neighborhood" now wired into one shared road system.

**Syntax**: `docker network ls`
**Example — verified hands-on**:
```
NETWORK ID     NAME      DRIVER    SCOPE
cc7df9749acd   bridge    bridge    local
e0579f75cd5f   host      host      local
99dd026aa10d   none      null      local
```
- `bridge` — the default network every container joins unless told otherwise.
- `host` — no isolation at all; the container shares the host's real network stack directly. A
  process bound to port 5000 in a `host`-mode container is literally on the host's port 5000, no
  `-p` needed or even possible.
- `none` — no network interface at all except loopback (`127.0.0.1` talking to itself).

**Syntax**: `docker network inspect NETWORK_NAME`
**Example — verified hands-on** (`docker network inspect bridge`):
```json
"Subnet": "172.17.0.0/16",
"Gateway": "172.17.0.1",
"Containers": {},
"Status": { "IPAM": { "Subnets": { "172.17.0.0/16": { "IPsInUse": 3, "DynamicIPsAvailable": 65533 } } } }
```

**Real discovery**: 3 IPs already "in use" on a completely empty network, with zero containers
attached. Reasoned through it plainly (not guessed at, since it was genuinely new ground): every
network reserves a few addresses for its own plumbing before any device joins —
1. The **network address** itself (`172.17.0.0`) — a label for the whole road system, not a device.
2. The **gateway address** (`172.17.0.1`) — the bridge's own entry/exit point, not a container.
3. The **broadcast address** (`172.17.255.255`, the last address in the range) — reserved for
   "send to everyone" messages.

Verified against Topic 5's CIDR math: `/16` → 16 host bits free → `2^16 = 65536` total addresses.
`65536 - 3 = 65533`, matching `DynamicIPsAvailable: 65533` exactly.

### 2. Container-to-container communication

Ran two real containers from the project's own `mission-control-app:v2` image (not a throwaway
image, per the parallel-project rule), on the default bridge:

**Syntax**: `docker run -d --name CONTAINER_NAME IMAGE`
```bash
docker run -d --name app-a mission-control-app:v2
docker run -d --name app-b mission-control-app:v2
```

**Real discovery**: `app-a` reaching `app-b` **by name** over the default bridge genuinely failed:
```
docker exec app-a python -c "import urllib.request; print(urllib.request.urlopen('http://app-b:5000/health', timeout=3).read())"
socket.gaierror: [Errno -2] Name or service not known
```

**Syntax** (checking a container's IP directly): `docker inspect -f 'GO_TEMPLATE' CONTAINER_NAME`
— `-f` (format) prints only one specific field instead of the full JSON dump; `{{ }}` is Docker's
template syntax pointing at exactly where that field lives.
```bash
docker inspect -f '{{.NetworkSettings.Networks.bridge.IPAddress}}' app-b
# → 172.17.0.3
```
Reaching `app-b` by that IP succeeded, returning `{"status":"ok","version":"2.0"}` — proving the
network path itself was fine; only name resolution was missing.

**Fix — create a custom, user-defined network, and connect both containers to it:**

**Syntax**: `docker network create NETWORK_NAME`, then `docker network connect NETWORK_NAME CONTAINER_NAME`
```bash
docker network create my-net
docker network connect my-net app-a
docker network connect my-net app-b
```
A container can belong to more than one network at once — `app-a`/`app-b` stayed on `bridge` and
gained `my-net` too. Re-ran the exact same by-name request — this time it succeeded.
**Conclusion**: the default bridge network does not provide automatic name-based lookup between
containers; a user-defined network does. This is exactly why Docker Compose (Day 2) can let
services call each other by name automatically.

### 3. Port publishing, tied to Topic 5

Container private IPs (like `app-b`'s `172.17.0.3`) are only reachable *inside* the Docker
network — same concept as Topic 5's **private IP**, unreachable from outside directly. The `-p`
flag (already used in Topic 9) does the same job as Topic 5's **NAT** concept: bridging a
container's private address to the host's own reachable address, just at the container's edge
instead of a home router's edge.

### 4. Volumes — the problem, and the bind mount fix

**Proved the problem first.** Wrote a file inside a container, deleted the container, created a
fresh one from the same image, and confirmed the file was gone:
```bash
docker exec app-a sh -c "echo hello > /tmp/test.txt && cat /tmp/test.txt"   # → hello
docker rm -f app-a
docker run -d --name app-a mission-control-app:v2
docker exec app-a cat /tmp/test.txt
# → cat: /tmp/test.txt: No such file or directory
```
Container storage is temporary by default — deleting a container wipes everything written inside it.

**Fix — bind mount.** A bind mount connects a real folder on the host machine directly to a
folder inside the container.

**Syntax**: `docker run -d --name NAME -v HOST_PATH:CONTAINER_PATH IMAGE`
**Example — verified hands-on**:
```bash
mkdir data
docker run -d --name app-c -v C:\CloudOps\ignite\project\data:/app/data mission-control-app:v2
docker exec app-c sh -c "echo saved-data > /app/data/proof.txt"
```
Confirmed the file appeared on the **host side**, completely outside Docker — using **`type`**,
Windows' own equivalent of Linux's `cat` (just prints a file's contents):
```powershell
type data\proof.txt
# → saved-data
```
Then deleted the container (`docker rm -f app-c` — **`-f`**/"force" skips the safety check that
normally refuses to remove a still-running container, stopping it and removing it in one step)
and created a brand-new one with the same mount — the file was still there. **Proved**: a
container's mounts are locked in at creation and can never be changed on a running container; the
only way to change them is delete-and-recreate.

---

## Day 2 — 2026-07-23 / 2026-07-24 (final day)

### Today's agenda
1. Named volumes.
2. Safely adding a mount to a running container.
3. Docker Compose, from scratch.
4. Quiz — both days together.

**Side fact confirmed**: container names must be unique on a machine. Trying to run a second
container with a name already in use by an existing one (even a different, unrelated container)
fails outright with a "name already in use" error — the existing container has to be removed or
renamed first before the name is free again.

### 5. Named volumes

Same guarantee as a bind mount (data survives container deletion), except Docker manages the
storage location instead of you picking a real folder.

**Syntax**: `docker volume create NAME`
```bash
docker volume ls
# DRIVER    VOLUME NAME
# local     Volume-A
```
Found an existing empty volume (`Volume-A`) rather than creating a new one — checked it was
genuinely empty first, using a throwaway container:

**Syntax**: `docker run --rm -v VOLUME_NAME:/check IMAGE ls /check` — `--rm` means "delete this
container automatically the moment it finishes," useful for one-off checks that shouldn't leave
clutter behind.
```bash
docker run --rm -v Volume-A:/check mission-control-app:v2 ls /check
# (empty — confirmed clean)
```

**Example — verified hands-on**: used `Volume-A` with `-v Volume-A:/app/data` on a container
named `app-d`, wrote `proof.txt` and `proof2.txt` into it, deleted `app-d`, then created a
brand-new container attached to `Volume-A` and confirmed both files were still there — proving
persistence the same way as the bind mount, via a completely different mechanism (Docker-managed
storage, not a chosen host path).

**`docker volume rm NAME`** deletes a volume, but refuses if any container still references it.
**No `docker volume rename` exists** — unlike containers, volumes can't be renamed directly; the
real workaround is create-new, copy data across via a temporary container, then delete the old one.

### 6. Real troubleshooting tangent — VPN and `docker network create`

A prior (unlogged) session had hit `docker network create` hanging when connected to a corporate
VPN that couldn't be disconnected, reportedly needing a full machine restart to recover. Went in
cautiously this time rather than blindly repeating the same command — with VPN active again,
`docker network create my-net` was retried directly, and it completed normally with no hang.
**Lesson**: not every environment/VPN combination reproduces this kind of conflict — worth trying
the real command first (with a plan to disconnect/interrupt quickly if it hangs) rather than
assuming the worst case every time, but staying aware it's a known failure mode on this network.

### 7. PowerShell vs. Linux commands

Wanted to create `docker-compose.yml` from the terminal for real Linux command practice — since
the actual terminal in use is PowerShell (`PS C:\CloudOps\ignite\project>`), not WSL/bash, several
real differences surfaced:

- **`touch docker-compose.yml`** — fails outright in PowerShell (`touch: The term 'touch' is not
  recognized...`). PowerShell's equivalent: **`New-Item docker-compose.yml -ItemType File`**.
- **`cat`** — actually *does* work in PowerShell, but not because PowerShell understands Linux —
  it's a built-in alias for PowerShell's own `Get-Content` cmdlet (same idea as `ls` →
  `Get-ChildItem`, `pwd` → `Get-Location`). It can display a file's contents fine, but Linux-style
  heredoc redirection (`cat > file << EOF ... EOF`) does **not** work, since `Get-Content`
  underneath has no concept of that bash-specific syntax.
- **Here-string** (PowerShell's equivalent of a heredoc, for writing literal multi-line text as
  one block) — **Syntax**: `@' ... '@ | Out-File -FilePath NAME -Encoding utf8`. Everything
  between `@'` and `'@` is one literal block of text, line breaks included.
- **`code FILENAME`** — VS Code's own CLI tool, opens the given file in a VS Code editor tab
  directly from the terminal. Used this as the practical way to "go inside and write" content
  after creating the empty file with `New-Item`, since PowerShell has no built-in terminal text
  editor like Linux's `nano`.

**Real conclusion**: real Linux command practice specifically requires an actual Linux/WSL
terminal — PowerShell only has partial, alias-based overlap with Linux commands, not the real
thing, even when a command name looks identical.

### 8. Safely adding a mount to an existing container

**Reinforced rule**: a running container's mounts (or any creation-time setting) can never be
changed in place — confirmed again when trying to add `Volume-A` to the already-running `app-a`
(which already had the bind mount).

**Real catch**: two different storage sources can't point at the same container path at once —
like two cars trying to park in one labeled parking spot. `Volume-A` had to go at a different
path, `/app/volume-data`, since `/app/data` was already taken by the bind mount. Agreed a
going-forward convention: `/app/volume-data` for anything volume-based, `/app/data` stays
reserved for the bind mount.

**Safe technique used** — verify before cutting over, instead of delete-then-hope:

1. Checked `app-a`'s exact current settings first, so nothing would be lost rebuilding it:
   ```bash
   docker inspect app-a --format 'Image: {{.Config.Image}}{{println}}Binds: {{.HostConfig.Binds}}{{println}}Networks: {{range $k, $v := .NetworkSettings.Networks}}{{$k}} {{end}}'
   # Image: mission-control-app:v2
   # Bind Mounts: [C:\CloudOps\ignite\project\data:/app/data]
   # Networks: bridge my-net
   ```
2. Created `app-a-duplicate` with **both** mounts, plus the same network:
   ```bash
   docker run -d --name app-a-duplicate -v C:\CloudOps\ignite\project\data:/app/data -v Volume-A:/app/volume-data mission-control-app:v2
   docker network connect my-net app-a-duplicate
   ```
3. Verified both paths showed the expected files (`docker exec app-a-duplicate ls /app/data`,
   `ls /app/volume-data`) **before** touching the real `app-a`.
4. Only then, the actual swap:
   ```bash
   docker rm -f app-a
   docker rename app-a-duplicate app-a
   docker network connect my-net app-a
   ```
   **`docker rename OLD NEW`** only changes a container's name — it can't add/change mounts or
   networks, which is exactly why the duplicate had to be a genuinely new container in the first
   place, not a renamed version of the old one.

**Important contrast worth remembering**: mounts/volumes are locked in at creation time, full
stop — but **networks are not**. `docker network connect`/`docker network disconnect` can be run
against an already-running container at any time, in any order, which is why the network
connection was safely re-added *after* the rename above rather than needing to be baked in from
the very first `docker run`. Same container, two very different rules depending on which setting.

Repeated the same technique for `app-b` (moving its single volume from `/app/data` to
`/app/volume-data` for path-naming consistency — not a technical conflict this time, since `app-b`
never had a bind mount to collide with).

**Closed the day with a full consistency audit** — checked everything against what was actually
intended, not just assumed correct:

| Check | Result |
|---|---|
| `app-a` bind mount | `/app/data` ✅ has `proof.txt`, `proof2.txt` |
| `app-a` volume | `/app/volume-data` ✅ has `proof.txt`, `proof2.txt` |
| `app-a` networks | `bridge` + `my-net` ✅ |
| `app-b` volume | `/app/volume-data` ✅ has `proof.txt`, `proof2.txt` (no stray bind mount) |
| `app-b` networks | `bridge` + `my-net` ✅ |
| `Volume-A` itself | exactly 2 files, matching what both containers see |
| Host folder (`C:\CloudOps\ignite\project\data`) | exactly 2 files, matching `app-a`'s bind mount |
| Volumes on the system | only `Volume-A` — no stray leftover from an abandoned idea earlier |
| Leftover containers | none — no orphaned `app-c`, `app-d`, or `*-duplicate` containers |

Everything matched exactly, confirming the duplicate-and-swap technique left nothing
inconsistent or orphaned behind.

**Also learned**: volume/container contents can be checked visually instead of via terminal —
Docker Desktop's **Volumes** tab (click a volume to browse its files) and a container's
**Files** tab (browse its whole filesystem) give the same information as `docker exec ... ls`,
just graphically.

### 9. Docker Compose

**Concept**: one file describing every container's build, ports, volumes, and networks, replacing
manual `docker run`/`docker network create` commands typed by hand. Written in **YAML** — plain
text where **indentation shows what belongs to what**.

**First file — `project/docker-compose.yml`**:
```yaml
services:
  app:
    build: ./app
    ports:
      - "5000:5000"
```
- `services:` — the top-level section listing every container to run.
- `app:` — a name chosen for this service.
- `build: ./app` — build a fresh image from the Dockerfile in `./app`, instead of using an
  already-built tag.
- `ports:` / `- "5000:5000"` — same job as `-p`: host port : container port.

**Syntax**: `docker compose up -d` — reads the file, builds/creates/starts everything it describes.
Ran it — built the image, created a network (`project_default`) **automatically**, and created a
container (`project-app-1`), all from one command. Verified live:
`curl http://localhost:5000/health` → `{"status":"ok","version":"2.1"}`.

**Auto-naming convention noticed in the real output** — nothing here needed a manual `--name`:
- Image: `project-app` (folder name + service name)
- Network: `project_default` (folder name + `_default`)
- Container: `project-app-1` (folder name + service name + instance number)

Same pattern held later for the volume (`project_app-data`) and the second service's container
(`project-app2-1`) — Compose consistently derives every name from the project folder and the
service names written in the YAML, instead of anything being typed by hand.

**Extended with a volume and a second service:**
```yaml
services:                             # top-level section: list of containers to run
  app:                                # indented under "services": name of this container (1st container)
    build: ./app                      # indented under "app": belongs to the "app" service
    ports:
      - "5000:5000"                   # belongs to "app": host_port:container_port
    volumes:
      - app-data:/app/volume-data     # belongs to "app": which volume this container uses

  app2:                               # 2nd container
    build: ./app                      # indented under "app2": belongs to the "app2" service
    volumes:
      - app-data:/app/volume-data     # same volume as "app" above

volumes:                              # separate section: declares volumes to create
  app-data:                           # name of the volume
```
The bottom-level `volumes:` (unindented, a sibling of `services:`) is a completely different thing
from the `volumes:` indented under each service — the first declares every named volume that
exists in the project so Compose creates/manages it; the second says which of those volumes a
*specific* service should mount.

Re-ran `docker compose up -d`. **Real discovery, directly tying back to Day 1's mount rule**:
```
✔ Image project-app2       Built
✔ Volume project_app-data  Created
✔ Container project-app2-1 Created
✔ Container project-app-1  Recreated
```
`app` (whose config changed — it gained a volume it didn't have before) showed **"Recreated"**,
while `app2` (brand new) showed **"Created"** — the exact same "mounts are locked at creation"
rule from Day 1, applied automatically by Compose instead of done by hand.

**Verified both new pieces hands-on**:
- Name resolution, automatic, no manual network setup:
  ```bash
  docker exec project-app-1 python -c "import urllib.request; print(urllib.request.urlopen('http://app2:5000/health', timeout=3).read())"
  # → {"status":"ok","version":"2.1"}
  ```
  Compose creates its own custom network per project and every service gets DNS resolution by
  **service name** (`app`, `app2` — not the longer container name `project-app2-1`).
- Shared volume:
  ```bash
  docker exec project-app-1 sh -c "echo hello-from-app > /app/volume-data/shared.txt"
  docker exec project-app2-1 cat /app/volume-data/shared.txt
  # → hello-from-app
  ```
  Confirmed both services share the exact same named volume declared in the file.

**For future reference — not run today, but the natural counterpart to `up`**: **`docker compose
down`** stops and removes every container/network Compose created from the file in one command
(add `-v` to also remove the volumes declared in it) — the reverse operation to `docker compose
up -d`, useful for a full clean teardown instead of manually removing each piece by hand.

## Topic 10 Quiz — both days combined — Attempt 1: PASS, 92/100

Five interview-style, open-ended questions covering both days:

1. **Why does name resolution fail on the default bridge but work on a custom network?**
   Answer: both containers share a virtual network so IP-based communication works directly, but
   the default bridge has no built-in DNS to translate a name into an IP; a custom network comes
   with automatic DNS between containers. — Correct, complete.
2. **What's the real difference between a bind mount and a named volume, and how do you choose?**
   Answer: a bind mount points at a specific host path you choose, Docker doesn't manage it; a
   named volume's storage is picked and owned by Docker, referenced only by name — more portable.
   Use a bind mount when a specific host file/folder is needed, a named volume for data that just
   needs to persist and be managed by Docker. — Correct, complete.
3. **If you delete a container with a named volume attached, what happens to the volume?**
   Answer: it stays, because its lifecycle is independent of any container using it. — Correct.
   (Minor mix-up on a related follow-up: attributed the "can't mount two sources at one path"
   reasoning to `app-b`'s move to `/app/volume-data`, which was actually just a consistency choice,
   not a real conflict like `app-a` had — corrected in the moment.)
4. **Why did `app` get "Recreated" while `app2` was just "Created"?**
   Answer: `app`'s settings changed (it gained a volume it didn't have before), and since mounts
   can only be set at creation, Compose had to recreate it; `app2` was brand new, nothing to
   recreate. — Correct, strong synthesis connecting back to Day 1's mount rule.
5. **How do `app` and `app2` find each other by name with no manual network commands run today?**
   Answer: Compose automatically created a custom network (`project_default`, seen directly in the
   real output) and attached both services to it; custom networks come with built-in name
   resolution. — Correct, grounded in real observed output.

**How the actual quiz session went** (for context, not the answers themselves): Q1 and Q2 were
answered completely and correctly on the first attempt, solid enough that the offered follow-up
questions were explicitly declined as unnecessary rather than skipped out of uncertainty — a real,
confident judgment call about when a follow-up adds value versus when it doesn't. Q3 was correct
on the core question but needed a small real-time correction on a related follow-up detail. Q4
and Q5 were both answered completely and correctly first try, with genuine synthesis tying back to
concepts from earlier in the topic rather than restating them.

**Score: 92/100**
- **Quiz 36/40** — all 5 core answers correct and well-reasoned; one minor mix-up on a bonus
  follow-up, corrected immediately once flagged.
- **Hands-on 30/30** — exceptional breadth: real bridge/DNS proof (both failure and success cases),
  bind mount and named volume persistence both proven independently, the safe
  duplicate-and-swap technique for updating a live container without data loss, a full
  before/after consistency audit, and a real multi-service Compose file with a shared volume and
  automatic networking, all verified live rather than assumed.
- **Depth 26/30** — genuine understanding reached and clearly demonstrated in Q4/Q5's synthesis,
  though this topic needed more scaffolding, restarts, and simplification passes than most to get
  there.

**Verdict**: **Topic 10 CLEARED, attempt 1, 92/100.**
