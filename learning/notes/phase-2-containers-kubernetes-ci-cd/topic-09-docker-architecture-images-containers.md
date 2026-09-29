# Topic 9 — Docker: Architecture, Images, Containers

## Day 1 — 2026-07-20 / 2026-07-21

### Why containers exist (tied to Topic 1)
Topic 1 covered VMs virtualizing hardware, each carrying a full guest OS kernel. A container is
narrower: it isolates a *process* using Linux kernel features (namespaces for isolation, cgroups
for resource limits) while sharing the host's kernel — no kernel boot involved, so containers
start in milliseconds where VMs take tens of seconds.

### Core terms — plain definitions first
Taught in isolation, before any context connecting them (explicit user request):
- **Daemon** — a program that runs quietly in the background, always on, waiting to do work.
- **Client** — the CLI you type into (`docker`). Doesn't do the work itself — sends the request
  to the daemon and shows the result.
- **Registry** — an online storage location for ready-made images (Docker Hub is the default).
- **Image** — a saved, complete snapshot of an app and everything it needs to run. Doesn't do
  anything by itself — just a template.
- **Container** — a live, running copy made *from* an image.

Recipe-card analogy used to make image vs. container concrete: an image is a recipe card (just
paper, does nothing by itself); a container is what happens when someone actually cooks from it
(a real, active thing). One recipe (image), many possible cooked dishes (containers).

### Architecture — client/server split, proven live
General syntax vs. shorthand:
```
docker --version        # shorthand — client version only, one line
docker version           # full — shows Client: and Server: as two separate sections
```
Real output:
```
Client:
 Version:           29.1.5
 ...
Server: Docker Desktop 4.58.0 (216728)
 Engine:
  Version:          29.1.5
  OS/Arch:           linux/amd64
  ...
```
The `Server` section reports `OS/Arch: linux/amd64` even though the host is Windows — Docker
Desktop runs a Linux VM in the background (tied to Topic 1's VM concept) because containers need
a Linux kernel underneath. The daemon actually lives inside that VM, not directly on Windows.
Images/containers are therefore stored inside that VM's own virtual disk, not as ordinary files
browsable in Windows File Explorer. `docker system df` shows real disk usage without needing to
find the raw file.

### The architecture in action — `docker run hello-world`, line by line
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
...
```
Mapped line by line:
- `docker run hello-world` → client sends the request.
- `Unable to find image ... locally` → daemon checks its own shelf, no image cached yet.
- `Pulling from library/hello-world` / `Pull complete` / `Download complete` → daemon fetches the
  image from the registry (Docker Hub).
- `Status: Downloaded newer image ...` → image now cached locally.
- `Hello from Docker!` onward → daemon created a container from that image and streamed its
  output back through the client.

### Images vs. containers — proven hands-on
```
docker images
docker ps -a
```
First run showed one image (`hello-world:latest`) and one container (`Exited (0)`). Running
`docker run hello-world` a **second** time produced no `Pulling`/`Unable to find` lines at all
(image already cached — no registry call needed), but `docker ps -a` then showed **two** separate
container entries (`fcc0c59945a3`, `6dae8ab55c08`), same image, different container IDs and
auto-generated names — confirming "one image, many containers" with real output, not just the
analogy.

### `docker ps` / `-a` — grounded in Topic 2
- `ps` — reused directly from Topic 2's Linux `ps` (process status) — a running container is
  fundamentally a wrapped process.
- `-a` — "all." Without it, `docker ps` only shows currently-running containers; stopped/exited
  ones (like `hello-world`, which finished immediately) don't show up at all.

### Location note
`docker run`/`docker ps -a`/etc. can be run from any folder (e.g. VS Code's terminal at
`C:\CloudOps\ignite>`) — the client just sends the request over to the daemon; current folder is
irrelevant. Exception: `docker build`, which reads local files and does care about the folder
it's run from (the "build context").

### The Dockerfile — plain definitions first
- **`FROM`** — starting point image to build on top of, instead of starting from nothing.
- **`WORKDIR`** — sets the "current folder" *inside the image* for every instruction after it.
- **`COPY`** — copies a file from the real computer into the image being built.
- **`RUN`** — executes a command *while the image is being built*.
- **`CMD`** — the command that runs automatically the moment a container starts from the image.

Written for `project/app/`, line by line:
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```
`pip` grounded fresh (new concept): Python's tool for installing packages; `requirements.txt` is
just the shopping list of which packages the app needs (currently just `flask`).

### Building the image
General syntax:
```
docker build -t IMAGE_NAME PATH
```
- `-t` — tag, gives the image a memorable name instead of a random ID.
- `PATH` — the build context (folder with the Dockerfile + files it needs).

Concrete example, run from `project/app/`:
```
docker build -t mission-control-app .
```
Build log showed 4 steps, `[1/4]` through `[4/4]`, mapping exactly to `FROM`/`WORKDIR`/`COPY`/
`RUN` — `CMD` doesn't run during build, only when a container actually starts. `docker images`
confirmed `mission-control-app:latest` (199MB) now listed alongside `hello-world`.

### Running the container
New flags, plain definitions first:
- **`-d`** ("detached") — runs in the background, hands the terminal back immediately.
- **`-p HOST_PORT:CONTAINER_PORT`** — maps a port on the real PC to a port inside the container.

```
docker run -d -p 5000:5000 mission-control-app
```
Verified with `docker ps` (`STATUS: Up`, `PORTS: 0.0.0.0:5000->5000/tcp`) and by opening
`http://localhost:5000/health` in the browser — real response: `{"status":"ok"}`. First real,
working containerized app end to end.

### Container lifecycle commands
```
docker logs CONTAINER    # everything the container has printed since it started
docker stop CONTAINER    # tells a running container to shut down
docker rm CONTAINER      # deletes a stopped container (not run this session — kept for reference)
docker rmi IMAGE         # deletes an image (not run — reused tomorrow for Day 2)
```
`docker logs unruffled_greider` showed Flask's real dev-server startup output, including a
`WARNING: This is a development server. Do not use it in a production deployment.` — grounded
fresh: Flask's built-in server (`app.run()`, what our `CMD` uses) is for development/testing only;
a real deployment would front it with a production WSGI server (e.g. Gunicorn) instead — not
something to fix today, relevant again once deployment topics (CI/CD, Kubernetes) are reached.

### Exit codes — a real discovered detail, tied to Topic 2's signals
After `docker stop unruffled_greider`, `docker ps -a` showed:
```
f44fd9197b7d   mission-control-app   ...   Exited (137) 19 seconds ago   ...   unruffled_greider
6dae8ab55c08   hello-world           ...   Exited (0) 6 hours ago        ...   interesting_poitras
```
`docker stop` sends a polite `SIGTERM` (signal 15, "please exit") first, waits ~10 seconds, then
escalates to a forceful `SIGKILL` (signal 9 — the same `kill -9` from Topic 2) if the process
hasn't exited by itself. Exit code `137 = 128 + 9`: `128` is a fixed Linux/Unix convention marking
"this exit code reports a signal, not a self-chosen exit code" (`128 + signal number`); `9` is the
signal that actually did it. Flask's dev server apparently didn't respond to `SIGTERM` fast
enough, so Docker escalated. Contrast: `hello-world`'s `Exited (0)` — that one finished its own
work and exited normally by itself, no signal involved at all.

### Status
Day 1 of 2 complete. No quiz today (non-final day of a multi-day topic, per `CLAUDE.md`). Day 2
still ahead: layer/rebuild edge cases, image tagging/versions, a harder/more independent task,
tying deeper into the project build, then the quiz covering both days together.
