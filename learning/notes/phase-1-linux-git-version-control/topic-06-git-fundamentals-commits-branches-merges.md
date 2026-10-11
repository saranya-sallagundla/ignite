# Topic 6 — Git Fundamentals — Commits, Branches, Merges

> Personal study notebook — full teaching content, commands, outputs, and explanations.
> Distinct from `progress.md` (tracking) and `session_notes.md` (short personal reflection).
> Two-day topic per the roadmap, compressed into one session (Day 1 and Day 2 both covered
> 2026-07-16), ending in the quiz.

---

## Day 1 — 2026-07-16 (heavy scaffolding: commits, branches, fast-forward merge)

Practiced from Windows PowerShell directly (`C:\CloudOps\git-practice`), not WSL — Git's core
behavior is the same either way (line-ending defaults differ, see the CRLF note below); this
environment was chosen since VS Code (native Windows install, not WSL) is the tool used for
GitHub work going forward.

### Today's agenda
1. The save-file analogy.
2. The three-stage model.
3. Setup and identity check.
4. `git init` — starting a repository.
5. `git status`, `git add`, `git commit`.
6. `git log` and `HEAD`.
7. Branches.
8. Merging — fast-forward.

### 1. The save-file analogy

- **Commit** = a save point — a snapshot of the whole project at one moment, with a message
  describing what changed
- **Repository (repo)** = the whole save-file folder, containing every save point ever made
- **Branch** = a separate save-file slot — try something risky in one slot while the main slot
  stays untouched, decide later whether to bring it back in
- **Merge** = combining two branches' progress into one

Unlike a simple "undo," Git tracks *who* changed *what*, *when*, and *why*.

### 2. The three-stage model

1. **Working directory** — actual files on disk right now
2. **Staging area** ("the index") — a holding area where you pick exactly which changes go into
   the *next* commit
3. **Repository (committed history)** — permanent snapshots, once committed

Analogy: packing a box to mail (stage) before actually sealing and shipping it (commit) — you
choose what goes in the box, and can add/remove things before sealing it, but once shipped, that
snapshot is permanent.

**Why a separate staging area matters, worked through with a concrete example**: if two unrelated
files are both changed in the working directory, but only one should go into the next commit as
its own clean, logically separate change — `git add` just that one file, leaving the other
genuinely untouched and uncommitted. Staging is what makes clean, single-purpose commits possible
instead of one commit mixing unrelated changes.

### 3. Setup and identity check

**Syntax**: `git config --global user.name` / `user.email` — show configured commit identity
(every commit is permanently stamped with this).

**Verified hands-on** — already configured, no setup needed:
```
PS> git --version
git version 2.54.0.windows.1
PS> git config --global user.name
Saranya Sallagundla
PS> git config --global user.email
user@example.com
```

### 4. `git init` — starting a repository

**Syntax**: `git init` — turns the current folder into a Git repository (creates a hidden `.git`
folder storing all history).

**Verified hands-on**:
```
PS C:\CloudOps\git-practice> git init
Initialized empty Git repository in C:/CloudOps/git-practice/.git/
PS> ls -force

    Directory: C:\CloudOps\git-practice

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d--h-           7/16/2026  2:21 PM                .git
```

**Git vs. GitHub — a real distinction, asked and answered directly**: Git itself is the offline
version-control tool — everything above (`git init`, commits, history) works completely on its
own, with no internet connection and no GitHub involved at all. GitHub is just one hosting
service for Git repositories, letting you back up and share a repo online (GitLab and Bitbucket
are others that do the same job). Git works fully without ever touching GitHub; GitHub only
becomes relevant once you want to push a repo somewhere else or collaborate with others.

### 5. `git status`, `git add`, `git commit` — the basic workflow

**Syntax**: `git status` — shows current state of working directory/staging area
**Syntax**: `git add FILE` — stage a file
**Syntax**: `git commit -m "MESSAGE"` — create a permanent snapshot of everything staged

**Verified hands-on — full first commit cycle**:
```
PS> "hello.git" > readme.txt
PS> git status
On branch master

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        readme.txt

nothing added to commit but untracked files present (use "git add" to track)

PS> git add readme.txt
warning: in the working copy of 'readme.txt', CRLF will be replaced by LF the next time Git touches it
PS> git status
On branch master

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   readme.txt

PS> git commit -m "Add readme file"
[master (root-commit) 9925f29] Add readme file
 1 file changed, 1 insertion(+)
 create mode 100644 readme.txt
```
- **"Untracked"** → Git sees the file exists but isn't tracking it at all yet.
- **CRLF warning** — a real, common cross-platform Git quirk: Windows text files traditionally
  end lines with `CRLF` (carriage-return + line-feed); Linux/Mac use just `LF`. Git normalizes to
  `LF` internally to keep the repository consistent regardless of which OS commits to it.
  Informational only, not an error.
- **`(root-commit)`** — flags this as the very first commit in the repo's history (no parent).
- **`9925f29`** — the commit hash, a unique ID generated from the content itself.

**Branch-naming aside**: notice `On branch master` above — Git itself still defaults a repo's
first branch to `master` unless `init.defaultBranch` is configured otherwise (confirmed on this
same, current Git version). GitHub, however, defaults new repos created through its own UI to
`main` instead. Flagged as
relevant again once Topic 8 (GitHub) is reached, since a locally-initialized repo and a
freshly-created GitHub repo can genuinely start on differently-named default branches.

### 6. `git log` and `HEAD`

**Syntax**: `git log` — shows commit history, most recent first.

**Verified hands-on — second commit, growing history**:
```
PS> "hello.git, second line" >> readme.txt
PS> git add readme.txt
PS> git commit -m "Add 2nd line to readme"
[master b2a0446] Add 2nd line to readme
 1 file changed, 1 insertion(+)

PS> git log
```
> **Note**: raw git commit metadata below reflects the machine's actual local clock (US Eastern,
> UTC-4) — narrative dates in this notebook stay IST, per `CLAUDE.md`'s standing rule.
```
commit b2a04469245e2eb042bd3d8d7bb50b63f6106ffc (HEAD -> master)
Author: Saranya Sallagundla <user@example.com>
Date:   Thu Jul 16 15:06:17 2026 -0400

    Add 2nd line to readme

commit 9925f299c623efb1722e7b77d075dd1542d31b9b
Author: Saranya Sallagundla <user@example.com>
Date:   Thu Jul 16 14:54:34 2026 -0400

    Add readme file
```
**`HEAD`** — a special pointer marking "where you currently are." Right now it points at
`master`, which itself points at the latest commit. As new commits happen, `HEAD` and the branch
both move forward together. Becomes central once branches are involved — `HEAD` is what actually
moves when switching branches, not the commits themselves.

### 7. Branches

**Syntax**: `git branch` — list branches (current one marked with `*`)
**Syntax**: `git branch NAME` — create a branch without switching
**Syntax**: `git checkout NAME` (or `git switch NAME`) — switch to a branch
**Syntax**: `git checkout -b NAME` — create AND switch in one step

**Verified hands-on**:
```
PS> git branch
* master
PS> git checkout -b feature-branch
Switched to a new branch 'feature-branch'
PS> git branch
* feature-branch
  master
```

**Proven hands-on — branches are genuinely isolated**:
```
PS> "new feature line" >> readme.txt
PS> git add readme.txt
PS> git commit -m "add feature line"
[feature-branch 714ab7c] add feature line
 1 file changed, 1 insertion(+)

PS> git checkout master
Switched to branch 'master'
PS> cat readme.txt
hello.git
hello.git, second line
```
The "new feature line" is **absent** on `master` even though it was just committed on
`feature-branch` moments earlier — real proof of isolated, separate history per branch.

### 8. Merging — fast-forward

**Syntax**: `git merge BRANCH_NAME` — while standing on the target branch, pull in another
branch's changes.

**Verified hands-on** — included an extra, unprompted verification step (checking the file's
content on `feature-branch` again right before merging, confirming exactly what would be pulled
in) before actually merging:
```
PS> git switch feature-branch
Switched to branch 'feature-branch'
PS> cat readme.txt
hello.git
hello.git, second line
new feature line

PS> git checkout master
Switched to branch 'master'
PS> git merge feature-branch
Updating b2a0446..714ab7c
Fast-forward
 readme.txt | 1 +
 1 file changed, 1 insertion(+)
PS> cat readme.txt
hello.git
hello.git, second line
new feature line
```
**Confirmed via `git log`** — both `master` and `feature-branch` ended up pointing at the *same*
commit:
```
PS> git log
commit 714ab7c901b6f554e2f4ee786719ccc642371b17 (HEAD -> master, feature-branch)
Author: Saranya Sallagundla <user@example.com>
Date:   Thu Jul 16 15:13:59 2026 -0400

    add feature line

commit b2a04469245e2eb042bd3d8d7bb50b63f6106ffc
Author: Saranya Sallagundla <user@example.com>
Date:   Thu Jul 16 15:06:17 2026 -0400

    Add 2nd line to readme

commit 9925f299c623efb1722e7b77d075dd1542d31b9b
Author: Saranya Sallagundla <user@example.com>
Date:   Thu Jul 16 14:54:34 2026 -0400

    Add readme file
```
`(HEAD -> master, feature-branch)` on one line — the literal definition of a fast-forward:
`master` had zero new commits since the branch point, so Git simply moved its pointer forward to
match, no real "combining" needed.

---

## Day 2 — 2026-07-16 (harder: real merge conflicts, `.gitignore`, `git diff`, combined scenario)

### Today's agenda
1. Why the first "conflict" attempt wasn't actually a conflict.
2. Setting up and resolving a real conflict.
3. `.gitignore`.
4. `git diff`.
5. Combined scenario — shared-file merge outcomes.
6. The quiz.

### 1. Why the first "conflict" attempt wasn't actually a conflict

**First attempt** (didn't produce a conflict, and this was a useful real lesson):

```
PS> git checkout master
Switched to branch 'master'
PS> "master line" >> readme.txt
PS> git add readme.txt
PS> git commit -m "Add master-only line"
[master 300c00a] Add master-only line
 1 file changed, 1 insertion(+)

PS> git checkout -b conflict-branch
Switched to a new branch 'conflict-branch'
... edited line 1 via VS Code ...
PS> git add readme.txt
PS> git commit -m "edit 1st line on conflict-branch"
[conflict-branch e9e86c7] edit 1st line on conflict-branch

PS> git checkout master
Switched to branch 'master'
PS> git merge conflict-branch
Updating 300c00a..e9e86c7
Fast-forward
 readme.txt | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
```
Created `conflict-branch` from a commit, edited line 1 there, merged back into `master` with **no
new commits made on `master` in between** → another fast-forward, not a conflict. **Root
lesson**: a genuine conflict requires **both** branches to change **after diverging**,
specifically editing the **same line** differently — simply branching and editing on one side is
not enough.

### 2. Setting up and resolving a real conflict

**Correct setup**: branched off `real-conflict` from `master`'s current tip and committed an edit
there *first*, then switched **back** to `master` and made a **new, separate commit** there
*after* branching off — that second commit on `master` is what created genuine divergence (both
branches now have a commit the other doesn't), with both edits landing on the identical line.

**Verified hands-on — the conflict occurring**:
```
PS> git checkout -b real-conflict
Switched to a new branch 'real-conflict'
PS> code readme.txt
... edited line 1 to hello.git "EDITED ON REAL-CONFLICT BRANCH" ...
PS> git add readme.txt
PS> git commit -m "edit 1st line on real-conflict branch"
[real-conflict 85fd936] edit 1st line on real-conflict branch
 1 file changed, 1 insertion(+), 1 deletion(-)

PS> git checkout master
Switched to branch 'master'
PS> code readme.txt
... edited line 1 to hello.git "edited on Master" ...
PS> git add readme.txt
PS> git commit -m "edit line 1 on master"
[master 1f6d20d] edit line 1 on master
 1 file changed, 1 insertion(+), 1 deletion(-)

PS> git merge real-conflict
Auto-merging readme.txt
CONFLICT (content): Merge conflict in readme.txt
Automatic merge failed; fix conflicts and then commit the result.
```

**The actual conflict markers, exactly as VS Code's editor displayed them** (shown here with a
leading `|` on each marker line so this notebook itself doesn't get mistaken for an unresolved
conflict by an editor's merge-conflict detector — a real gotcha hit once already while writing
these notes):
```
| <<<<<<< HEAD (Current Change)
hello.git "edited on Master"
| =======
hello.git "EDITED ON REAL-CONFLICT BRANCH"
| >>>>>>> real-conflict (Incoming Change)
hello.git, second line
new feature line
master line
```
- **`<<<<<<< HEAD`** (start-of-conflict marker) — opens with the **current branch's** version
  (`master`, since `HEAD` points there). VS Code highlights this down to `=======` in one color
  and appends the `(Current Change)` label itself — that label is editor annotation, not real
  Git output.
- **`=======`** (divider marker) — separates the two conflicting versions.
- **`>>>>>>> real-conflict`** (end-of-conflict marker) — closes with the **incoming** branch's
  version. VS Code highlights this section in a second color and appends `(Incoming Change)` the
  same way.
- A clickable text row floats directly above the conflict block, each option doing exactly what
  it says (not manual marker-deleting):
  - **Accept Current Change** — keep `HEAD`'s version, discard incoming
  - **Accept Incoming Change** — keep the incoming version, discard current
  - **Accept Both Changes** — keep both, one after another
  - **Compare Changes** — side-by-side diff view
- A separate **"Resolve in Merge Editor"** button sits off to the side, opening a dedicated
  side-by-side comparison view instead of resolving inline.

Chose **Accept Current Change** (kept master's version) — a real, common resolution choice: one
side is simply judged correct and the other dropped.

**Verified hands-on — after resolving**:
```
PS> git add readme.txt
PS> git commit -m "Resolve merge conflict on line 1, keep master version"
[master 0d41a29] Resolve merge conflict on line 1, keep master version

PS> cat readme.txt
hello.git "edited on Master"
hello.git, second line
new feature line
master line
```
Confirmed clean — no marker lines remain, only the chosen version of line 1.

### 3. `.gitignore`

Some files should never be tracked — temp files, secrets, build artifacts. `.gitignore` is a
plain-text file listing patterns Git should ignore.

**Verified hands-on**:
```
PS> "*.log" > .gitignore
PS> "secret.txt" >> .gitignore
PS> git add .gitignore
warning: in the working copy of '.gitignore', CRLF will be replaced by LF the next time Git touches it
PS> git commit -m "add gitignore"
[master 2a5302c] add gitignore
 1 file changed, 2 insertions(+)
 create mode 100644 .gitignore
```

### 4. `git diff`

**Syntax**: `git diff` — shows exact line-by-line changes in the working directory that aren't
staged yet.

**Verified hands-on**:
```
PS> "one more line" >> readme.txt
PS> git diff
warning: in the working copy of 'readme.txt', CRLF will be replaced by LF the next time Git touches it
diff --git a/readme.txt b/readme.txt
index 3345eaa..afbf2f9 100644
--- a/readme.txt
+++ b/readme.txt
@@ -2,3 +2,4 @@ hello.git "edited on Master"
 hello.git, second line
 new feature line
 master line
+one more line
```
**Decoding the output**:
- `-` lines = removed, `+` lines = added (`+one more line` here — pure addition, nothing removed)
- **Hunk header** `@@ -OLD_START,OLD_COUNT +NEW_START,NEW_COUNT @@` — here `@@ -2,3 +2,4 @@`
  means: old version starts at line 2, shows 3 lines; new version starts at line 2, shows 4
  lines. Same starting point, one more line in the new version — matches the single addition made.

### 5. Combined scenario — shared-file merge outcomes

**Scenario**: working on a feature branch for two days while a teammate merges changes into
`master` touching the same file. What happens on merging back, and what are the two possible
outcomes?

**Answered correctly**: if the **same lines** were changed on both sides → real conflict,
requiring manual resolution (exactly what was just practiced). If **different lines/files**
changed → Git auto-merges cleanly (matches both fast-forward merges done earlier, and the
resolved conflict which only collided on one specific line).

(The related "why use branches over direct commits to a shared `master`" question came up
separately, as Quiz Question 5 below — not part of this pre-quiz scenario discussion.)

---

## Topic 6 Quiz — both days combined — Attempt 1: PASS, 84/100

Interview-style, open-ended, 5 questions covering both days. Question and full correct answer for
each:

1. **Three-stage model, and why a separate staging area matters.**
   The three-stage model describes how Git tracks changes across three areas: the **working
   directory** (the actual files on disk right now, as edited), the **staging area** ("the
   index" — a holding area where specific changes are chosen to go into the *next* commit), and
   the **repository** (the permanent, committed history, once a commit is made). The analogy:
   packing a box to mail — you choose what goes in the box (staging) before actually sealing and
   shipping it (committing); items can be added or removed before sealing, but once shipped, that
   snapshot is permanent.

   A separate staging area matters because it's what makes clean, single-purpose commits
   possible instead of one commit mixing unrelated changes. Concretely: if two unrelated files
   are both modified in the working directory, but only one of them should go into the next
   commit as its own clean, logically separate change, `git add` just that one file — leaving the
   other file genuinely untouched (modified, but unstaged and uncommitted). Without staging,
   every changed file would have to be committed together, forcing messy, mixed commits.

2. **What `HEAD` is, and what happens to it on `git checkout`.**
   `HEAD` is a special pointer marking "where you currently are" in the repository's history.
   Normally it points at whichever branch is currently checked out (e.g. `master`), and that
   branch itself points at its latest commit; as new commits happen, `HEAD` and the branch move
   forward together automatically.

   On `git checkout NAME` (or `git switch NAME`), `HEAD` is what actually moves — it re-points
   from the old branch to the target branch, which in turn points at that branch's own latest
   commit. The commits themselves never move; only `HEAD` (and which branch it's attached to)
   changes. This is exactly why switching branches instantly changes the file contents seen in
   the working directory — checking out `master` vs. `feature-branch` showed genuinely different
   `readme.txt` contents, because each branch has its own separate commit history and `HEAD` was
   pointing at a different one each time.

3. **Why a merge showed "Fast-forward" instead of a real merge.**
   A "Fast-forward" merge happens specifically when the branch being merged *into* (the one
   currently checked out, e.g. `master`) has had **zero new commits since the point where the
   other branch diverged from it**. In that case, `master`'s history is just a strict subset of
   the other branch's history, so Git doesn't need to combine two divergent histories at all — it
   simply moves `master`'s pointer forward to match the other branch's latest commit. This was
   confirmed via `git log` showing both branch names next to the exact same commit hash (e.g.
   `(HEAD -> master, feature-branch)` on one line) — no new merge commit is created, because
   nothing needed reconciling. This condition breaks down, producing a real merge or a conflict,
   only once `master` has gained its own separate commits after the branch point — meaning the
   two histories have genuinely diverged.

4. **Conflict marker lines — order and meaning.**
   When both branches change the exact same line differently after diverging, Git can't
   auto-resolve it and instead writes conflict markers directly into the file for manual
   resolution. In order:
   - `<<<<<<< HEAD` opens the conflict block and marks the start of the **current** branch's
     version — the branch `HEAD` is presently on (`master` in the practiced example). VS Code
     labels this "Current Change."
   - The current branch's conflicting content follows directly.
   - `=======` is the divider marking the boundary between the two versions.
   - The **incoming** branch's conflicting content follows the divider.
   - `>>>>>>> branch-name` closes the block, naming the incoming branch and marking the end of
     its version. VS Code labels this "Incoming Change."

   Resolving means editing the file down to the single intended content and deleting all three
   marker lines (`<<<<<<<`, `=======`, `>>>>>>>`) entirely, then `git add` and `git commit` to
   record the resolution. VS Code also offers clickable shortcuts directly above the block —
   Accept Current Change, Accept Incoming Change, Accept Both Changes, Compare Changes — which do
   this automatically instead of manually deleting markers.

5. **Direct commits to a shared `master` vs. branches — the real problem and the fix.**
   Committing directly to a shared `master` with multiple people risks a **silent overwrite**:
   without an isolated branch, two people's changes to the same file can clash without any clear
   signal at the time, since there's no separate space where a conflict would have to surface
   before it lands on the shared branch everyone relies on.

   Branches fix this by giving each person, or each unit of work, an isolated slot to make
   changes in — separate from `master` and from each other — so work-in-progress can be committed
   freely without touching shared history. A conflict only actually needs to be surfaced and
   resolved at the moment that branch is merged back into `master`, not on every individual
   commit — meaning problems are caught deliberately at one visible integration point, instead of
   silently landing in shared history as they happen.

**How the actual quiz session went** (for context, not the answers themselves): Q1 passed on the
core purpose immediately, needed one follow-up for a concrete example; Q2 passed cleanly, first
try; Q3 passed cleanly, first try; Q4's first answer had the marker order/labels wrong, corrected
cleanly once asked to check against the actual real output from earlier in the session; Q5 named
the silent-overwrite risk unprompted, needed one nudge to complete the second half.

**Score: 84/100**
- **Quiz 30/40** — correct throughout, 2 of 5 needed a real follow-up correction, not just a
  light nudge.
- **Hands-on 28/30** — genuinely excellent, full real workflow including **two** fast-forward
  merges — one where the "conflict" setup didn't actually conflict, correctly understood and
  re-set-up properly — plus an actual resolved merge conflict via VS Code's UI, `.gitignore`, and
  `git diff`.
- **Depth 26/30** — strong scenario reasoning, and the trial-and-error in properly setting up a
  genuine conflict showed real engagement with *why* fast-forward happens, not just memorized
  steps.

**Verdict**: **Topic 6 CLEARED, attempt 1, 84/100.**
