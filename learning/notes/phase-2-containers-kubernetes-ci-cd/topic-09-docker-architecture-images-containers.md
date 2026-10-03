# Topic 9 — Docker — Architecture, Images, Containers

> Personal study notebook — full teaching content, commands, outputs, and explanations.
> Distinct from `progress.md` (tracking) and `session_notes.md` (short personal reflection).
> Two-day topic per the roadmap — covered across two sessions, ending in the quiz.

---

## Day 1 — 2026-07-20

### Today's agenda
1. Precheck — Docker verified, `project/app/` boilerplate written, `app.py` walked through.
2. Core Docker terms — daemon, client, registry, image, container.
3. `docker run hello-world` — the architecture proven in action.
4. Images vs. containers, proven hands-on.
5. Writing, building, and running a real Dockerfile for `project/app/`.
6. Container lifecycle commands.
7. Exit codes and signals.

### 1. Precheck, before teaching started
- Docker Desktop confirmed installed and running (`docker version` client 29.1.5, server engine
  active) before the lesson began.
- `project/app/` was found still empty (only a placeholder `README.md`) — per `CLAUDE.md`'s
  trigger rule, the initial boilerplate had to be written before Topic 9 could begin. Wrote a
  minimal Flask app (`app.py`, initially with a `/health` endpoint and a root `/` endpoint) and
  `requirements.txt` (`flask==3.1.0`) first, explicitly noted as Claude-authored per the Phase 5
  exception (not yet defensible in an interview — gets rewritten for real once Python, Topics
  45-46, is reached).

### 2. Walking through `app.py`, line by line
The initial boilerplate (before Day 2's later changes) had two endpoints:
```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify(status="ok"), 200

@app.route("/")
def index():
    return jsonify(service="ignite-capstone", message="hello from the capstone app"), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```
Taught as a full walkthrough, not just handed over silently:
- **Flask** — a Python library for building web applications; `Flask(__name__)` creates the
  actual application object everything else attaches to.
- **`@app.route("/path")` + a function directly under it** — a pairing: the route declares which
  URL path this covers, the function immediately below it is what actually runs when that path is
  requested. The two always go together.
- **HTTP status codes** — `200` means success; `404` means "not found" — these are the same
  numbers visible in a browser's dev tools when a page loads (or fails to).
- **The root route (`/`)** — the URL with nothing after the domain/port at all; here it just
  returns a simple identifying message for the service.
- **`app.run(host="0.0.0.0", port=5000)`** — explicitly tied back to Topic 5: `0.0.0.0` as a bind
  address means "accept connections on every interface," not `127.0.0.1`'s loopback-only
  restriction — directly reusing that distinction, plus Topic 5's port concept generally.
- **`if __name__ == "__main__":`** — a standard Python idiom meaning "only run this block if the
  file is executed directly, not if it's imported by something else."

### 3. Why containers exist (tied to Topic 1)
Topic 1 covered VMs virtualizing hardware, each carrying a full guest OS kernel. A container is
narrower: it isolates a *process* using Linux kernel features (namespaces for isolation, cgroups
for resource limits) while sharing the host's kernel — no kernel boot involved, so containers
start in milliseconds where VMs take tens of seconds. Docker is the tooling that makes building,
shipping, and running containers practical.

### 4. Core terms — plain definitions first
Explicitly taught in isolation, one at a time, before any context connecting them together — a
direct user request mid-lesson ("don't directly go to the terminology, 1st lemme understand what basics
are then go to the context"), saved to memory as a standing habit going forward:
- **Daemon** — a program that runs quietly in the background, always on, waiting to do work when
  something asks it to.
- **Client** — the CLI you actually type into (`docker`). Doesn't do the work itself — it just
  sends the request somewhere else and shows you the result.
- **Registry** — an online storage location where ready-made images are kept, so people can
  download one instead of building it themselves from scratch. Docker Hub is one example.
- **Image** — a saved, complete snapshot of an application and everything it needs to run, stored
  as a file. Doesn't do anything by itself — just sits there, like a template.
- **Container** — a live, running copy made *from* an image. The thing actually executing.

**Recipe-card analogy** (the one that made image vs. container actually click): an **image** is like a
recipe card — it lists what's needed and the steps, but by itself it's just paper, it doesn't do
anything. A **container** is what happens when someone actually *cooks* from that recipe — a real,
active thing. You could follow the same recipe card 5 times and get 5 separate cooked dishes — one
recipe (image), many dishes (containers).

**Restaurant-phone-call analogy** (for who talks to who): you call a restaurant — you don't cook
anything yourself, you place the order and wait. You are the **client**. The **daemon** is the
kitchen, working in the background, doing everything — fetching recipes, cooking, plating. The
**registry** is a central recipe library (*Docker Hub*) the kitchen can call if it doesn't already
have a recipe card on hand. *Flow: you ask → kitchen checks if it has the recipe already → if not,
grabs one from the recipe library → cooks (creates a container) → hands you the finished dish.*

### 5. Checking the installation — `docker --version` vs `docker version`
What these are for: confirming Docker is actually installed and working, and — for the full
form — seeing the client/server split explained below.

General syntax vs. shorthand:
```
docker --version    # shorthand — client version only, one line
docker version      # full — shows Client: and Server: as two separate sections
```

What actually got run first, before the shorthand/full distinction had been made:
```
PS C:\Users\devuser> docker --version
Docker version 29.1.5, build 0e6fee6
```
Correction made on the spot: `docker --version` (double dash) only prints the client's one-line
version. `docker version` (no dashes) prints the full split instead — run next, real output:
```
Client:
 Version:           29.1.5
 API version:       1.52
 Go version:        go1.25.6
 Git commit:        0e6fee6
 Built:             Fri Jan 16 12:51:08 2026
 OS/Arch:           windows/amd64
 Context:           desktop-linux

Server: Docker Desktop 4.58.0 (216728)
 Engine:
  Version:          29.1.5
  API version:      1.52 (minimum version 1.44)
  Go version:       go1.25.6
  Git commit:       3b01d64
  Built:            Fri Jan 16 12:48:42 2026
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          v2.2.1
  GitCommit:        dea7da592f5d1d2b7755e3a161be07f43fad8f75
 runc:
  Version:          1.3.4
  GitCommit:        v1.3.4-0-gd6d73eb8
 docker-init:
  Version:          0.19.0
  GitCommit:        de40ad0
```
The `Server` section reports `OS/Arch: linux/amd64` even though the host is Windows (`Client`
section shows `windows/amd64`) — the client/server split made visible.

### 6. Where images/containers are actually stored on the PC
Directly asked and answered: containers need a Linux kernel underneath (namespaces/cgroups are
Linux kernel features). Windows doesn't have this natively, so Docker Desktop quietly runs a small
Linux VM in the background — the exact VM concept from Topic 1. The daemon actually lives inside
that Linux VM (confirmed by `Context: desktop-linux` and `OS/Arch: linux/amd64` on the Server
line above), not directly on Windows. So images and containers aren't ordinary files findable in
Windows File Explorer under `C:\Users\...` — they live inside that Linux VM's own virtual disk, a
single opaque blob Docker Desktop manages. `docker system df` was mentioned as the way to see how
much space they're using without needing to find the raw file (explained, not actually run this
session).

### 7. `docker run hello-world` — the architecture in action
What this command is for: `docker run IMAGE_NAME` creates and starts a **container** from an
**image**, pulling the image from the **registry** first if it isn't already cached locally.
`hello-world` is a tiny official test image whose only job is to print a confirmation message —
used here purely to see the whole client → daemon → registry → image → container chain happen for
real, not to build anything useful itself.

Real output:
```
PS C:\Users\devuser> docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
4f55086f7dd0: Pull complete
d5e71e642bf5: Download complete
Digest: sha256:c3cbe1cc1aa588a64951ac6286e0df7b27fe2e6324b1001c619bb358770c0178
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```
Mapped line by line, using the restaurant analogy:
- `docker run hello-world` → you (the client) placing the order: "make me hello-world."
- `Unable to find image 'hello-world:latest' locally` → the kitchen (daemon) checks its own shelf
  first — no recipe card for "hello-world" there yet.
- `latest: Pulling from library/hello-world` / `Pull complete` / `Download complete` → the kitchen
  calls the recipe library (the registry, Docker Hub) and the recipe card gets delivered piece by
  piece.
- `Status: Downloaded newer image for hello-world:latest` → the recipe card (the image) is now on
  the kitchen's shelf, ready to use.
- `Hello from Docker!` onward → the kitchen actually cooked from that recipe (created a container)
  and handed over the finished dish — this text is that dish.

### 8. Images vs. containers — proven hands-on
Two commands, each explained for what it's *for* before running anything:
- **`docker images`** — lists every image currently stored locally (the recipe cards sitting on
  the shelf).
- **`docker ps`** — lists containers. Reused directly from Topic 2's Linux `ps` ("process status"),
  since a running container is fundamentally a wrapped process underneath.
- **`-a`** ("all") — added to `docker ps` so it also shows stopped/exited containers, not just
  currently-running ones. Without it, a finished container like `hello-world` (which runs and
  exits immediately) wouldn't show up at all.

**First check**, later the same session, after the single earlier `hello-world` run:

`docker images`:
```
IMAGE                ID             DISK USAGE   CONTENT SIZE   EXTRA
hello-world:latest   c3cbe1cc1aa5       25.9kB         9.49kB    U
```

`docker ps -a`:
```
CONTAINER ID   IMAGE         COMMAND    CREATED       STATUS                   PORTS     NAMES
6dae8ab55c08   hello-world   "/hello"   3 hours ago   Exited (0) 3 hours ago             interesting_poitras
```

One image, one container — as expected so far.

**Second check** — ran `docker run hello-world` again. No `Unable to find`/`Pulling` lines at all
this time (image already cached locally, no registry call needed); the identical "Hello from
Docker!" message printed again.

`docker ps -a` afterward:
```
CONTAINER ID   IMAGE         COMMAND    CREATED          STATUS                      PORTS     NAMES
fcc0c59945a3   hello-world   "/hello"   13 seconds ago   Exited (0) 12 seconds ago             unruffled_bassi
6dae8ab55c08   hello-world   "/hello"   5 hours ago      Exited (0) 5 hours ago                interesting_poitras
```

Two separate `CONTAINER ID`s and two different auto-generated `NAMES`, from the exact same
`IMAGE` — confirming "one image, many containers" with real output, not just the analogy. This was
predicted correctly ("it would reuse the image, and show two containers") *before* running the
command, based purely on reasoning from the recipe-card analogy.

### 9. Location note — does the current folder matter?
Directly asked: can `docker run`/`docker ps -a` be run from any location, specifically from VS
Code's integrated terminal at `C:\CloudOps\ignite>`? Answer: yes, from anywhere — the client
doesn't do any work itself, it just sends the request over to the daemon inside the Linux VM, and
that connection doesn't care what folder the terminal is sitting in. One exception flagged ahead of
time: `docker build` *does* care about the current folder, since it needs to read local files (the
Dockerfile and app code) to build the image — it needs to be run from, or pointed at, the folder
containing them (the "build context").

### 10. The Dockerfile — plain definitions first, written line by line
A Dockerfile is a plain text file — a list of instructions Docker reads top to bottom to build an
image. Five instruction types needed for this simple app, defined one at a time before writing
anything:
- **`FROM`** — picks a starting point to build on top of, instead of starting from nothing.
- **`WORKDIR`** — sets the "current folder" *inside the image* for every instruction after it —
  like doing `cd` before the rest of the recipe.
- **`COPY`** — copies a file from the real computer into the image being built.
- **`RUN`** — executes a command *while the image is being built*.
- **`CMD`** — the command that runs automatically the moment a container starts from this image.

Created via VS Code (right-click `project/app/` → New File → `Dockerfile`, no extension). Written
and confirmed one line at a time, in this exact order:
1. `FROM python:3.12-slim` — official pre-built image from Docker Hub with Python 3.12 already
   installed on a minimal Linux base; "slim" means it skips extra stuff not needed, keeping the
   image smaller.
2. `WORKDIR /app` — everything below happens inside a folder called `/app` *inside the image*
   (a fresh folder Docker creates inside the Linux image — not the Windows
   `C:\CloudOps\ignite\project\app\` folder).
3. `COPY . .` — first `.` means "everything in the current folder on your computer" (`project/app/`,
   where the Dockerfile lives); second `.` means "into the current folder inside the image" (`/app`,
   from `WORKDIR`). Copies `app.py` and `requirements.txt` in.
4. `RUN pip install -r requirements.txt` — grounded fresh since new: `pip` is Python's tool for
   installing packages (pre-written code libraries other people published); `requirements.txt` is
   just a shopping list of which packages the app needs (currently just `flask`). This line
   installs everything on that list while the image is being built.
5. `CMD ["python", "app.py"]` — the command that runs automatically when a container starts:
   starts the Flask app and its `/health` endpoint.

Final file, confirmed correct:
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

### 11. Building the image
General syntax:
```
docker build -t IMAGE_NAME PATH
```
- `-t` — "tag," gives the image a memorable name instead of a random ID.
- `PATH` — the build context (folder with the Dockerfile and the files it needs).

Concrete example, run after `cd project/app` (moving from `C:\CloudOps\ignite>` into
`C:\CloudOps\ignite\project\app>` first, since this is the one command that cares about the
current folder):
```
docker build -t mission-control-app .
```
Real (trimmed) build log:
```
[+] Building 62.4s (9/9) FINISHED
 => [internal] load build definition from Dockerfile
 => [internal] load metadata for docker.io/library/python:3.12-slim
 => [internal] load .dockerignore
 => [1/4] FROM docker.io/library/python:3.12-slim@sha256:57cd7c3a7a273101a6485ba99423ee568157882804b1124b4dd04266317710de   39.3s
 => [internal] load build context
 => [2/4] WORKDIR /app                                    0.5s
 => [3/4] COPY . .                                        0.1s
 => [4/4] RUN pip install -r requirements.txt             9.8s
 => exporting to image
 => => naming to docker.io/library/mission-control-app:latest
```
The 4 numbered steps, `[1/4]` through `[4/4]`, map exactly to `FROM`/`WORKDIR`/`COPY`/`RUN` from
the Dockerfile — `CMD` did not run during build (`CMD` only fires when a *container* starts, not
while the image is being built). `pip install` alone took ~9.8s, installing Flask.

`docker images` afterward confirmed:
```
IMAGE                        ID             DISK USAGE   CONTENT SIZE   EXTRA
hello-world:latest           c3cbe1cc1aa5       25.9kB         9.49kB    U
mission-control-app:latest   3ed884b5a5aa        199MB           49MB
```

### 12. Running the container
New flags, plain definitions first:
- **`-d`** ("detached") — runs the container in the background, hands the terminal back
  immediately instead of tying it up.
- **`-p HOST_PORT:CONTAINER_PORT`** — maps a port on the real PC to a port inside the container, so
  the browser (outside) can reach the Flask app (inside, listening on port 5000).

```
docker run -d -p 5000:5000 mission-control-app
```
Output: `f44fd9197b7d734a500f981dc9bf0472bbc54288c85554f91a71bdf8d6384036` (the new container's ID).

Verified with:
```
docker ps
```
```
CONTAINER ID   IMAGE                 COMMAND           CREATED              STATUS              PORTS                                         NAMES
f44fd9197b7d   mission-control-app   "python app.py"   About a minute ago   Up About a minute   0.0.0.0:5000->5000/tcp, [::]:5000->5000/tcp   unruffled_greider
```
And by opening `http://localhost:5000/health` in the browser — real response:
```
{"status":"ok"}
```
First real, working containerized app end to end — an actual Flask app, running inside a
container Docker built from a Dockerfile written line by line, serving real traffic.

### 13. Container lifecycle commands
```
docker logs CONTAINER    # everything the container has printed since it started
docker stop CONTAINER    # tells a running container to shut down
docker rm CONTAINER      # deletes a stopped container (not run this session — kept for reference)
docker rmi IMAGE         # deletes an image (not run — mission-control-app kept for Day 2 reuse)
```
Used the container's auto-generated name (`unruffled_greider`) instead of its ID this time — either
works.

Real `docker logs unruffled_greider` output:
```
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.17.0.2:5000
Press CTRL+C to quit
172.17.0.1 - - [21/Jul/2026 05:02:54] "GET /health HTTP/1.1" 200 -
172.17.0.1 - - [21/Jul/2026 05:02:54] "GET /favicon.ico HTTP/1.1" 404 -
172.17.0.1 - - [21/Jul/2026 05:03:03] "GET /health HTTP/1.1" 200 -
```
Two small real details explained:
- The `"GET /health HTTP/1.1" 200 -` lines are the actual browser requests from earlier, captured
  live with a success (200) status.
- The `"GET /favicon.ico HTTP/1.1" 404 -` right after is just the browser automatically trying to
  fetch a site icon that was never defined — harmless, not something built or broken.

**Why the WARNING appears** (directly asked): Flask ships with two ways to run — the simple one
(`app.run()`, what the `CMD` uses) is meant purely for development/testing, quick to start but not
built to handle real, simultaneous visitors safely or efficiently. A "production WSGI server" (a
separate piece of software, e.g. Gunicorn) is what actually fronts real users. The warning is Flask
telling you "you're using the quick/testing version, don't expose this directly to real users."
Completely expected right now since we're only testing locally — something to actually fix later
once deployment topics (CI/CD, Kubernetes) are reached, not today.

### 14. Exit codes — a real discovered detail, tied to Topic 2's signals
Ran:
```
docker stop unruffled_greider
docker ps -a
```
Real output:
```
CONTAINER ID   IMAGE                 COMMAND           CREATED          STATUS                        PORTS     NAMES
f44fd9197b7d   mission-control-app   "python app.py"   11 minutes ago   Exited (137) 19 seconds ago             unruffled_greider
6dae8ab55c08   hello-world           "/hello"          6 hours ago      Exited (0) 6 hours ago                  interesting_poitras
```
Noticed and asked about directly: **`Exited (137)`** for `mission-control-app`, different from
`hello-world`'s **`Exited (0)`**.

Explanation, tied straight back to Topic 2's signals content: `docker stop` doesn't kill a
container instantly — it first sends a polite request to shut down (`SIGTERM`, signal 15, "please
exit") and waits ~10 seconds. If the process hasn't exited by then, Docker escalates to a forceful
kill (`SIGKILL`, signal 9 — the same `kill -9` from Topic 2, "exit now, no cleanup allowed"). Exit
code 137 is Docker's way of recording that a container had to be force-killed.

Follow-up Q&A on the number itself:
- **Q: "why does this warning note came?"** — see the WARNING explanation above (asked in the
  middle of the logs discussion, not really about exit codes, but captured here for completeness
  since it came up in the same stretch).
- **Q: "what's 128?"** — 128 isn't calculated, it's a fixed Linux/Unix convention. Normally an exit
  code is just a number the program itself chooses when it finishes (0 usually means success).
  But when a process is terminated **by a signal** instead of exiting on its own, the OS needs a
  way to say "this wasn't a normal exit, a signal killed it" — the convention is **128 + the signal
  number**. So `128 + 9` (`SIGKILL`) = `137`. A process killed by `SIGTERM` (signal 15) instead
  would show `143` (`128 + 15`). `128` is the fixed marker; the number added to it is the actual
  signal.
- Correctly self-confirmed the whole formula unprompted — 128 marking a signal-based exit, plus
  signal 9, giving 137 — reasoned through `137 = 128 + 9` independently using only Topic 2's
  signals knowledge, without being handed the formula first.

Contrast kept explicit: `hello-world`'s `Exited (0)` — that one finished its own work and exited
normally by itself, no signal involved at all. `mission-control-app`'s `Exited (137)` — Flask's dev
server apparently didn't respond to the polite `SIGTERM` fast enough, so Docker had to escalate.

### 15. Day 1 wrap-up — agenda recap
1. Finish connecting the 5 terms using the real `hello-world` output.
2. Images vs. containers, hands-on (run `hello-world` twice, compare).
3. The Dockerfile — what it is, the 5 instructions needed.
4. Write a real Dockerfile for `project/app/`.
5. Build and run it, prove it's serving real traffic via `/health`.
6. Basic container lifecycle commands — inspect and clean up.
7. Exit codes and signals — the real `137` vs. `0` contrast.

All seven were completed today. Declined the offer to continue into Day 2 material early (would have
meant covering layer/rebuild edge cases, image tagging/versions, a harder independent task, and the
quiz today) — chose to stop after Day 1's full agenda instead.

---

## Day 2 — 2026-07-21 (final day)

### Today's agenda
1. Layer/rebuild edge cases — what actually gets reused vs. rebuilt on a code change, and why
   Dockerfile instruction order matters for build speed.
2. Image tags/versions — moving off the default `:latest`.
3. A harder, more independent task.
4. Tying it deeper into the project.
5. The quiz — both days together.

### 1. Layer/cache-invalidation edge case
Prediction asked before testing: if `app.py` changes and the image is rebuilt, which Dockerfile
steps actually rerun? Initial guess: "all of them, since app.py changed" — refined together: `FROM`
and `WORKDIR` don't touch any files at all, so they're reused from cache regardless; only `COPY`
and everything after it reruns.

Proved hands-on with the *original* (single-`COPY`) Dockerfile — changed `app.py`'s `/health`
response to include `version="1.0"`, then rebuilt:
```
docker build -t mission-control-app .
```
Real log: `WORKDIR` showed `CACHED`; `COPY . .` and `RUN pip install -r requirements.txt` both
re-ran (no `CACHED` label on either), confirming `RUN` reran even though `requirements.txt` never
changed. Directly asked why: **Docker's cache check is deliberately simple — it only asks "did the
immediately previous layer's output change?", never "does this command's argument only reference
one specific file?"** It never reads `pip install -r requirements.txt` and reasons about what it
actually depends on. Since `COPY . .` bundles `app.py` and `requirements.txt` into one layer,
changing `app.py` breaks that layer's cache, and `RUN` — coming right after — inherits that break
regardless of relevance. Confirmed this precisely when asked directly: *"something much simpler is
happening, docker doesn't understand if actually the pip install -r req.txt only needs req.txt
alone or something else."*

**The fix** — rewritten independently:
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]
```
First attempt omitted the final `COPY app.py .` entirely — self-caught only after being asked to
trace through where `app.py` would actually exist inside the image at the point `CMD` runs
("it's not copied anywhere"). Corrected immediately.

**Proved the fix** with two real builds:
- First build (fresh baseline with the new structure): `13.3s`, all 5 steps ran (nothing to cache
  yet against this new instruction order).
- Changed `app.py`'s version to `"1.1"`, rebuilt again: `2.3s` — `WORKDIR`, `COPY requirements.txt
  .`, and `RUN pip install` **all** showed `CACHED`; only the final `COPY app.py .` re-ran. Exactly
  the intended fix, proven with real timing and real `CACHED` labels, not just theory.

### 2. Image tagging and versions
Directly asked: does relying on the default `:latest` tag cause a rollback problem? Correctly
reasoned before testing: *"it got overwritten each time, same tag, so i can't rollback."*

New command, plain definition first:
- **`docker tag SOURCE_IMAGE TARGET_IMAGE`** — creates an additional name pointing at an image
  that already exists, without rebuilding anything.

Two-step proof:
```
docker tag mission-control-app:latest mission-control-app:v1
```
(labeling the current `version="1.1"` image as `v1`, so it's not only reachable via the disposable
`latest` tag), then bumped the app to `version="2.0"` and built with an explicit tag instead of the
bare name:
```
docker build -t mission-control-app:v2 .
```
`docker images` afterward:
```
IMAGE                        ID             ...
mission-control-app:latest   3791121b6785   ...
mission-control-app:v1       3791121b6785   ...
mission-control-app:v2       ca0bb287d44e   ...
```
Real, notable detail: `latest` and `v1` share the *exact same* `ID` — `docker tag` just added a
second name onto the already-existing image. But `latest` was **never updated** to point at `v2` —
it's still pointing at the old content. This directly disproves the intuitive assumption that
`:latest` means "the newest build"; it's just a label that only moves when explicitly rebuilt or
retagged under that exact name — right now it's stale.

**Rollback proven for real** — ran both tagged versions simultaneously on different host ports:
```
docker run -d -p 5001:5000 mission-control-app:v1
docker run -d -p 5002:5000 mission-control-app:v2
```
Browser confirmed: `http://localhost:5001/health` → `{"status":"ok","version":"1.1"}`;
`http://localhost:5002/health` → `{"status":"ok","version":"2.0"}` — two real, distinct versions
coexisting and independently reachable, proving tagging genuinely preserves rollback capability.

Clarified a related misconception: retagging an image does **not** affect already-running
containers at all — a container is a fixed snapshot from whatever the image contained the moment
`docker run` executed; renaming/retagging/even deleting the image afterward never touches
containers that already exist. Tag changes only affect *future* `docker run`/`docker build`
commands.

### 3. Harder independent task — `/ready` endpoint
Context (previewed ahead of Kubernetes, taught fresh): **liveness** ("is the process still alive?")
vs. **readiness** ("is it actually ready to serve traffic?") are different questions apps expose
separately. Task: add a `/ready` endpoint to `project/app/app.py`, build/tag/run it independently.

**Why this distinction concretely matters for Kubernetes** (previewed, not yet formally taught):
if `/health` fails, Kubernetes **restarts** the container — it assumes the process itself is
broken. If `/ready` fails instead, Kubernetes **stops routing traffic to it without restarting**
— it assumes the process is fine but temporarily can't serve requests (e.g. still starting up, or
a dependency isn't reachable yet). Two different failures need two different responses, which is
exactly why the two checks exist separately rather than one combined endpoint. Tied explicitly to
the actual capstone project: Mission Control's own monitoring will poll endpoints like these to
know what's actually happening inside the app it's watching.

First attempt duplicated `/health`'s exact payload (`status`/`version`, no distinct signal) —
corrected after being asked to reconsider what a readiness check should actually convey. Second
attempt: `jsonify(ready="true", version="2.1")` — a real Python bug, `"true"` in quotes is a string,
not a boolean. Grounded fresh since Python isn't formally taught yet (Phase 5): quotes make
anything text to Python, even the word "true"; a real boolean is written `True`/`False`, capitalized,
no quotes. Corrected to `ready=True, version="2.1"`.

Realized mid-task that an image had already been built *before* the fix was saved — confirmed
this matters: images are frozen snapshots of the files at build time, editing `app.py` afterward
doesn't retroactively change an already-built image (same lesson as Day 1).

**Safe cleanup of the buggy image** — identified the exact tag via `docker images`
(`mission-control-app:health-ready`, marked `U` for in-use), found the specific dependent container
via `docker ps -a` (`869907bb06ca`, `inspiring_dewdney`, still `Up`), then:
```
docker stop inspiring_dewdney
docker rm inspiring_dewdney
docker rmi mission-control-app:health-ready
```
— stopping and removing the container first, since Docker refuses to delete an image still tied to
an existing container.

**Final build/run/verify**, done independently: rebuilt `mission-control-app:health-ready` clean
(deliberately reused the same tag name this time, since the old buggy content was already deleted —
a legitimate descriptive-tag naming choice, not a mistake, distinct from the earlier `:latest`
problem where old content was still wanted), ran it on port 5000, verified in browser:
`/health` → `{"status":"ok","version":"2.1"}`, `/ready` → `{"ready":true,"version":"2.1"}` — a
genuine JSON boolean this time.

---

## Topic 9 Quiz — both days combined — Attempt 1: PASS, 86/100
5 open-ended questions, no multiple choice. Question and full correct answer for each:

1. **Walk through `docker run some-image` end to end, naming every component.**
   The **client** (the `docker` CLI) sends the request to the **daemon** first. The daemon checks
   whether the **image** already exists locally; if not, it pulls it from the **registry** (e.g.
   Docker Hub). Once the image is available locally, the daemon creates a new **container** from
   it and runs it, then streams the output back through the client to the terminal.

2. **The actual difference between an image and a container, and why running the same image
   3 times matters in practice.**
   An image is a saved, read-only template — a complete snapshot of an app and everything it needs
   to run, stored as a file; it doesn't execute anything by itself. A container is a live, running
   instance created *from* an image. Running `docker run` on the same image 3 times produces 3
   separate, independent containers from that one image — which matters in practice because it's
   exactly how you scale an app to handle more traffic (spin up more instances of the same image)
   or run isolated copies for other purposes, without needing multiple images.

3. **Why did `RUN pip install` rerun even though `requirements.txt` never changed, and how did
   reordering the Dockerfile fix it?**
   Docker's build cache check is deliberately simple: for each layer, it only asks "did the layer
   immediately before me change?" — it never inspects a command's arguments to figure out what it
   actually depends on. The original Dockerfile's `COPY . .` bundled `app.py` and
   `requirements.txt` into one layer, so changing `app.py` broke that layer's cache, and `RUN pip
   install` — coming right after — inherited that break regardless of its own real dependency. The
   fix: split the copy so only `requirements.txt` is copied (and installed) before `app.py` ever
   enters the picture — `COPY requirements.txt .` → `RUN pip install -r requirements.txt` → `COPY
   app.py .`. Now an `app.py`-only change only invalidates the final `COPY`, not the install step.

4. **What actually went wrong relying on the default `:latest` tag, and what a tag fundamentally
   is.**
   A tag is just a movable label pointing at a specific image — it isn't glued to one image
   forever. Every `docker build` without an explicit tag re-points the `latest` label at the newest
   image built, silently orphaning whatever image `latest` used to point to (that old image still
   exists, but there's no longer a name to ask for it by). The fix is giving builds explicit
   version tags (e.g. `v1`, `v2`) so old versions stay reachable and rollback is possible.

5. **The actual difference between `mission-control-app`'s exit code 137 and `hello-world`'s exit
   code 0.**
   `docker stop` doesn't kill a container instantly — it first sends a polite `SIGTERM` (signal
   15, "please exit") and waits (~10s). If the process hasn't exited by then, Docker escalates to
   a forceful `SIGKILL` (signal 9, "exit now, no cleanup"). Exit code 137 = `128 + 9` — `128` is
   the fixed Linux/Unix convention marking "this exit code reports a signal, not a self-chosen
   code," and `9` is the signal that did it. `mission-control-app` exited this way because
   `docker stop` was run against it and its Flask dev server didn't respond to `SIGTERM` fast
   enough. `hello-world`, by contrast, was never sent any stop signal at all — it finished its own
   tiny task and exited normally by itself, which is why its code is a plain `0`.

**How the actual quiz session went** (for context, not the answers themselves): Q1 needed one
follow-up to add the missing client-initiates step; Q2 left the "why it matters" half unaddressed
until asked; Q3's answer was correct but tangled, clarified with one follow-up; Q4 was answered
completely and correctly first try; Q5 needed two rounds to stop conflating `hello-world` with
`docker stop`, which was never run against it.

**Score: 86/100**
- **Quiz 32/40** — 2 needed a quick follow-up to surface an already-understood detail, 1 left
  "why it matters" unaddressed until asked, 1 had a genuine two-round factual mix-up, tagging
  answered flawlessly.
- **Hands-on 29/30** — excellent independent Day 2 execution (Dockerfile reorder proved with real
  before/after build logs, `v1`/`v2` tagging with a live rollback proof, safe `stop`→`rm`→`rmi`
  cleanup), with two genuine execution gaps (a missing `COPY app.py .`, `/ready` initially
  duplicating `/health`'s payload). Note: a separate Python string-vs-boolean detail
  (`ready="true"` vs. `ready=True`) is excluded from this score entirely, since Python isn't
  formally taught until Phase 5.
- **Depth 25/30** — tracks the same two quiz gaps, balanced against correctly predicting the
  "2 containers" outcome before testing and defending a deliberate custom tag-naming choice with
  sound reasoning.

**Verdict**: **Topic 9 CLEARED, attempt 1, 86/100.**
