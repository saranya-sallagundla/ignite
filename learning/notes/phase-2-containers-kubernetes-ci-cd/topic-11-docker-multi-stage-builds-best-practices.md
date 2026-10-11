# Topic 11 — Docker — Multi-Stage Builds and Best Practices

> Personal study notebook — full teaching content, commands, outputs, and explanations.
> Distinct from `progress.md` (tracking) and `session_notes.md` (short personal reflection).
> Single-day topic per the roadmap — covered in one session, ending in the quiz.

---

## Day 1 — 2026-07-24 (multi-stage builds, non-root user, gunicorn, a real layer-duplication bug found and fixed)

### Today's agenda
1. Why multi-stage builds exist — the problem a single-stage Dockerfile has.
2. Foundational terms needed to understand that problem: compiler, interpreter, binary, native code.
3. Multi-stage mechanics: stages, `FROM ... AS`, `COPY --from=`.
4. A second problem, unrelated to multi-stage builds but due for a fix today: root vs. non-root,
   Flask's dev server vs. a real production server.
5. Rewrite `orbit/app/Dockerfile` for real, covering every item Topic 10's audit deferred here.
6. Combined scenario: a real stuck container, and a real bug found and proven fixed.
7. Quiz.

### 1. The problem multi-stage builds solve

Every Dockerfile so far (Topics 9-10) has been **single-stage** — one `FROM` line, everything
after it piling into that same image. Whatever gets installed during a build stays in the final
image forever, even tools only needed temporarily — making the image bigger and increasing its
**attack surface** (the total set of things in a system an attacker could potentially exploit —
more installed tools/packages means more surface).

### 2. Foundational terms (built from scratch, since none of this was assumed)

- **Source code**: the text you write — e.g. `app.py`. Human-readable.
- **Machine code**: the only thing a CPU can actually run — raw numeric instructions.
- **Compiler**: translates source code into machine code, all at once, ahead of time. Analogy
  used: translating a whole book into another language before anyone reads it.
- **Binary** (executable): the finished, ready-to-run file a compiler produces.
- **Build toolchain**: "toolchain" = a chain (sequence) of tools used one after another. A build
  toolchain is the compiler plus whatever else (e.g. a linker, stitching multiple compiled pieces
  together) is needed to go from source code to a finished binary.
- **Interpreter**: translates *live*, line by line, as the program runs — no separate finished
  file produced ahead of time. Analogy used: a live interpreter at an event, translating sentence
  by sentence as the speaker talks, instead of a pre-translated book. This is exactly what runs
  `python app.py` — no compile step, ever.
- **Native code**: some Python packages have parts written in a compiled language (usually C) for
  speed. `pip install` sometimes has to compile that C part on the spot, which is the one moment a
  C compiler (`gcc`) could briefly get pulled in — even though our own dependency (`flask`) is pure
  Python and doesn't need this.

### 3. Multi-stage build mechanics

A **stage** is everything that follows one `FROM` line. A Dockerfile can have more than one. A
**multi-stage build** uses an early "builder" stage to do the heavy setup work, then a final stage
copies over only the finished result, leaving the builder stage (and anything not explicitly
copied) behind.

**Analogy used**: building a chair. The workshop (saws, glue, sawdust) is the builder stage — it
never ships. Only the finished chair (the final stage) gets delivered.

**Syntax**:
```dockerfile
FROM <base-image> AS <stage-name>
... build steps ...

FROM <base-image>
COPY --from=<stage-name> <path-in-that-stage> <path-in-this-stage>
... final steps ...
```
- `AS <stage-name>` gives a stage a nickname so a later stage can refer back to it.
- `COPY --from=<stage-name>` copies a file/folder from an *earlier stage's filesystem*, not from
  the host machine. Everything else in that earlier stage is discarded.

**Proof the builder stage really does get discarded, and that it's cached, not deleted**:
built just the builder stage on its own, using a new flag, `--target`.

**Syntax**: `docker build --target <stage-name> -t <tag> <path>`
**Example — verified hands-on**, from `orbit/app`:
```
docker build --target builder -t builder-stage-check .
...
=> => naming to docker.io/library/builder-stage-check:latest
```
Confirmed the builder stage sticks around, cached, as its own image — it doesn't vanish, it's just
never included in the final image unless explicitly copied over.

### 4. A second, unrelated problem, fixed in the same Dockerfile today

- **root**: the Linux super-user account with unrestricted access to everything. Containers run as
  root by default unless told otherwise. **Risk**: if a bug in the app ever let someone run their
  own commands inside the container, and the app is root, those commands run as root too — full,
  immediate access, no extra step needed. A limited user never has that access to begin with —
  there's no command (`sudo` or otherwise) that would grant it, since it was never configured.
  (`sudo` itself isn't actually relevant here — it's a separate command for letting an *approved*
  non-root user act as root temporarily on a normal system; our minimal image doesn't even have it
  installed. What matters is simply which user the container's main process runs as, directly.)
  **Analogy used**: root is a master key that opens every door in a building — running as root is
  handing that key to someone whose job never required it.
- **Flask's dev server** (`app.run(...)` in `app.py`) prints its own warning every time it starts:
  *"This is a development server. Do not use it in a production deployment."* It's built for a
  developer's own convenience, not for reliably serving real traffic.
- **Web framework** (Flask): defines the app's logic — what happens when a request comes in
  (routing, building the response). Doesn't know how to manage real network traffic itself.
- **Server**: separate software whose job is managing real incoming connections and handing each
  request to the framework.
- **WSGI**: the standard interface any Python framework uses to hand off to any Python server, so
  frameworks and servers can be mixed and matched.
- **gunicorn**: a real production WSGI server, replacing Flask's dev server.
  **Analogy used**: Flask is the chef (knows the recipes); gunicorn is the host stand (manages the
  actual flow of customers). Flask's own dev server is the chef also trying to run the host stand
  alone — fine for one friend, not a real dinner rush.

### 5. Rewriting `orbit/app/Dockerfile`

Before, from `orbit/app`:
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]
```

`requirements.txt` updated first — added gunicorn, and bumped Flask to the patched release the
Topic 10 audit flagged:
```
flask==3.1.1
gunicorn==23.0.0
```

New Dockerfile (first version) — a **virtual environment** (a self-contained folder of installed
Python packages, isolated from the rest of the system) is what gets handed from the builder stage
to the final stage. This is the fully annotated version — the notebook is where line-by-line
comments belong; the real `orbit/app/Dockerfile` stays clean (see the note below):
```dockerfile
# ---- Stage 1: builder — installs dependencies, discarded after this stage ----
FROM python:3.12-slim AS builder
WORKDIR /app

# Create a virtual environment at /opt/venv — a self-contained folder of Python
# packages, isolated from the rest of the system. This is what Stage 2 copies
# over whole, instead of copying pip's cache or any leftover build files.
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# --no-cache-dir skips pip's own download cache, keeping the image smaller.

# ---- Stage 2: final — what actually ships and runs ----
FROM python:3.12-slim
WORKDIR /app

# Pull in ONLY the finished virtual environment from Stage 1 — Stage 1 itself,
# and anything in it not explicitly copied here, is discarded.
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Python normally buffers stdout, which can delay logs appearing during a live
# demo. This makes output print immediately instead.
ENV PYTHONUNBUFFERED=1

COPY app.py .

# Create a plain, unprivileged user and hand ownership of /app and the venv
# over to it, then switch to running as that user instead of root — so a bug
# in the app can't hand an attacker full root access inside the container.
RUN useradd --create-home appuser \
    && chown -R appuser /app /opt/venv
USER appuser

# Documents which port the app listens on inside the container. This is
# metadata only — it does NOT publish the port to the host; that's still
# `-p`/`ports:` in docker-compose.yml.
EXPOSE 5000

# Docker periodically runs this command inside the running container to check
# it's actually still healthy, not just "started". Uses Python instead of curl,
# since curl isn't installed in the slim base image (the same gap Topic 10
# found earlier).
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

# gunicorn — a real production WSGI server — replaces Flask's dev server.
# "app:app" means: in the file app.py, use the object named `app`.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

**A note on file cleanliness**: the version above, with a comment on nearly every instruction, is
deliberately how it's kept *here*, in the notebook. The first draft put these same comments
directly into the real `orbit/app/Dockerfile`, which made that file look intimidatingly large,
and also directly broke `CLAUDE.md`'s own "Repo quality standards" (no teaching-style comments in
`orbit/` code — that explanation belongs here instead). The real file was stripped down to just
two short section labels (`# Stage 1: builder`, `# Stage 2: final`) — see `orbit/app/Dockerfile`
for the actual, clean, shipped version.

`docker-compose.yml` also updated — added a real, versioned image tag instead of an
auto-generated one:
```yaml
services:
  app:
    build: ./app
    image: orbit-app:2.1
    ports:
      - "5000:5000"
```

> **Note, added 2026-08-31**: at the time this session ran, `docker-compose.yml` set no
> `container_name`, so Compose auto-generated one (`orbit-app-1`, seen throughout the section
> below) — accurate for what was actually run and captured. The 2026-07-29 `project` → `orbit`
> rename later added `name: orbit` and `container_name: orbit-app` to the real file, so today the
> container is simply named `orbit-app`, no numeric suffix. Left the captured commands below as
> originally run rather than rewriting real historical output to match a file that didn't exist
> yet at the time.

### 6. Combined scenario — two real issues, found and resolved live

**Issue 1 — a container stuck in the `Created` state.**

Running `docker compose up --build` from `orbit/`, the terminal output stopped right after
"Container Created," with no startup logs at all — no dev-server warning, no gunicorn output,
nothing.

**New terms — container lifecycle states**:
- **Created**: the container exists (has an ID, filesystem set up) but its process was never
  actually started.
- **Up**: the process is currently running.
- **Exited**: the process ran, then stopped (cleanly or via a crash).

Diagnosed via:
```
docker ps -a
# STATUS column showed: Created   (not Up, not Exited)
docker logs orbit-app-1
# (empty — nothing to log, since the process never started)
```
`Created` with no logs meant Docker never attempted to actually run `gunicorn` — most likely
because the `docker compose up --build` command itself was interrupted right between "container
created" and "container started."

**Fix**:
```
docker start -a orbit-app-1
```
`-a` attaches the terminal to the container's live output. This showed real gunicorn startup logs:
```
[INFO] Starting gunicorn 23.0.0
[INFO] Listening at: http://0.0.0.0:5000 (1)
[INFO] Using worker: sync
[INFO] Booting worker with pid: 7
```
No dev-server warning at all — confirmed gunicorn, not Flask's `app.run()`, is now serving.

**Verified from a separate terminal** (the first one was busy streaming live logs):
```
docker ps
# STATUS: Up 2 minutes (healthy)
# PORTS: 0.0.0.0:5000->5000/tcp
curl http://localhost:5000/health
# {"status":"ok","version":"2.1"}
docker exec orbit-app-1 whoami
# appuser
```
All three best-practice items (gunicorn, healthcheck, non-root user) proven working together, not
just trusted from the Dockerfile alone.

**Issue 2 — the final image was bigger than the builder-only image, which shouldn't happen.**

Comparing sizes after the first Dockerfile draft:

| Image | Size |
|---|---|
| `builder-stage-check` (builder stage only) | 210MB |
| `orbit-app:2.1` (final image) | **231MB** |

The whole point of a multi-stage build is that the final stage should be smaller — carrying only
the finished result, nothing extra. Something was adding weight back in.

**New term — layer**: every Dockerfile instruction creates a **layer**, a stored snapshot of what
changed on the filesystem at that step. An image is a stack of these layers.

**New term — copy-up**: modifying a file that came from an earlier layer — even just changing who
owns it, not its content — forces the storage system to copy that entire file into the new layer
first (layers can't be edited in place once written).

**Root cause**: the Dockerfile did `COPY --from=builder /opt/venv /opt/venv`, then in a separate,
later step: `RUN useradd --create-home appuser && chown -R appuser /app /opt/venv`. That
`chown -R` recursively changed ownership of every file in `/opt/venv` — forcing copy-up on the
entire ~50MB virtual environment into a brand-new layer, on top of the copy that already existed
from the `COPY --from=builder` step. The venv's content effectively existed twice.

**Fix**: set ownership *during* the copy itself, with `COPY --chown=`, instead of a separate
`chown -R` afterward:
```dockerfile
FROM python:3.12-slim
WORKDIR /app
RUN useradd --create-home appuser
COPY --from=builder --chown=appuser /opt/venv /opt/venv
COPY --chown=appuser app.py .
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
USER appuser
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

**Proof the fix actually worked** — rebuilt and compared sizes again:

| Image | Before fix | After fix |
|---|---|---|
| `builder-stage-check` | 210MB | 210MB (unchanged) |
| `orbit-app:2.1` | 231MB (bigger than the builder!) | **204MB** (smaller, as it should be) |

Restarted the corrected container and re-verified everything still worked:
```
docker compose up -d
docker ps
# STATUS: Up About a minute (healthy)
```
Cleaned up the temporary comparison image afterward: `docker rmi builder-stage-check`.

---

## Topic 11 Quiz — Attempt 1: PASS, 90/100

Five interview-style, open-ended questions:

1. **Why does a multi-stage build actually end up producing a smaller final image, and what
   happens to the builder stage's contents?**
   Answer: the builder stage (compilers, dependencies, build tools) never becomes part of the
   final image — it sits cached, separately. `COPY --from=builder` pulls only the actual finished
   output into a fresh, minimal final stage; only that final stage's layers ship. — Correct,
   confirmed on follow-up that the builder stage is cached (not deleted), citing
   `builder-stage-check` as direct evidence from earlier in the session.
2. **What's the difference between a compiler and an interpreter, and why did that matter today
   even though our app doesn't need a compiler?**
   Answer: a compiler converts the whole source code to machine code upfront and produces a
   binary; an interpreter runs live, without producing a separate finished file. It mattered
   because some Python packages have compiled (native) parts, so the general Docker technique
   still applies even though `flask` itself doesn't need a compiler. — Correct concept; one word
   slip flagged and corrected ("compile everything line to line" → the right word is *interpret*,
   not compile).
3. **Why do we run the container as `appuser` instead of root — what's the actual risk root poses
   that a limited user doesn't?**
   Answer described root giving full access and a limited user preventing that if compromised —
   correct core idea, but framed around `sudo` specifically ("can't run commands with sudo").
   Corrected: `sudo` isn't actually the relevant mechanism (the image doesn't even have it
   installed) — what matters is that root's own process already has full access with nothing to
   unlock, while `appuser` never has that access to begin with, with or without `sudo`.
4. **What's the actual difference between Flask and gunicorn — what job does each do, and why
   can't gunicorn replace Flask entirely?**
   Answer: Flask handles routes/logic; gunicorn handles real traffic; WSGI is the standard way any
   server talks to any framework. — Correct and concise; gunicorn can't replace Flask since it has
   no knowledge of the app's actual routes/logic.
5. **Walk through the bug we found and fixed today — why was the final image bigger than the
   builder-only image at first, and what specifically fixed it?**
   Answer: correctly described layers, copy-up, that `COPY --from=builder` followed by a separate
   `chown -R` forced every file to be copy-up'd into a new layer unnecessarily, and that setting
   ownership during the copy itself (`COPY --chown=`) resolved it. — Technically accurate
   throughout, despite rough phrasing.

**How the actual quiz session went** (for context, not the answers themselves): asked for a full
revision recap of the entire session before attempting the quiz, given how much foundational
material (compiler/interpreter/WSGI) was genuinely new — a good instinct, and the recap was
followed by five answers with real reasoning rather than memorized lines. Q1, Q4, and Q5 were
answered cleanly. Q2 and Q3 each needed one real-time correction — a word-choice slip and a
root/`sudo` conflation — both cleared up precisely once flagged, not left fuzzy.

**Score: 90/100**
- **Quiz 36/40** — all 5 core mechanisms genuinely understood; 2 of 5 needed a specific correction
  (interpret vs. compile, root vs. sudo), neither reflecting a real gap once corrected.
- **Hands-on 29/30** — the full Dockerfile rewrite executed correctly, plus two real issues
  independently worked through: a stuck `Created` container diagnosed via `docker ps -a`/
  `docker logs` and resolved with `docker start -a`, and a genuine image-size bug found via a
  `--target` build comparison, root-caused to `chown -R`/copy-up, and fixed with a measured
  before/after proof (231MB → 204MB) rather than just trusting the fix.
- **Depth 25/30** — needed substantial ground-up teaching first (compiler, interpreter, binary,
  WSGI, framework vs. server, layers, copy-up — none of it assumed), more than most topics so far,
  but the requested full-session revision recap before the quiz paid off in clearly demonstrated
  understanding across all five questions.

**Verdict**: **Topic 11 CLEARED, attempt 1, 90/100.**
