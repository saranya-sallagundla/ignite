# Topic 7 — Git Deep Dive — Rebase, Cherry-Pick, Branching Strategies

> Personal study notebook — full teaching content, commands, outputs, and explanations.
> Distinct from `progress.md` (tracking) and `session_notes.md` (short personal reflection).
> Single-day topic per the roadmap — covered in one session, ending in the quiz.

---

## Day 1 — 2026-07-18 (rebase, cherry-pick, branching strategies)

Practiced in the same `C:\CloudOps\git-practice` folder from Topic 6, Windows PowerShell/VS Code.

### Today's agenda
1. Rebase — the core concept.
2. Cherry-pick.
3. Branching strategies (conceptual).
4. Combined scenario.
5. The quiz.

### 1. Rebase — the core concept

Analogy: **merge** is like joining two roads at an intersection (both paths still visible,
converging point marked with a merge commit). **Rebase** picks up one road and re-lays it
starting from further down the other road — as if it were built that way from the start, no
intersection visible at all. Produces clean, linear history instead of a branching one.

**Syntax**: `git rebase BRANCH` (replays the current branch's commits onto the tip of `BRANCH`)

**Setup — creating real divergence to rebase**:
```
PS> git checkout master
Already on 'master'
PS> "rebase demo line" >> readme.txt
PS> git add readme.txt
warning: in the working copy of 'readme.txt', CRLF will be replaced by LF the next time Git touches it
PS> git commit -m "master commit before rebase demo"
[master cdbaba9] master commit before rebase demo
 1 file changed, 1 insertion(+)

PS> git checkout -b rebase-demo
Switched to a new branch 'rebase-demo'
PS> "rebase branch line" >> readme.txt
PS> git add readme.txt
warning: in the working copy of 'readme.txt', CRLF will be replaced by LF the next time Git touches it
PS> git commit -m "rebase branch commit"
[rebase-demo 4907ec6] rebase branch commit
 1 file changed, 1 insertion(+)

PS> git checkout master
Switched to branch 'master'
PS> "another master commit" >> readme.txt
PS> git add readme.txt
warning: in the working copy of 'readme.txt', CRLF will be replaced by LF the next time Git touches it
PS> git commit -m "another master commit after branching"
[master 05bdadd] another master commit after branching
 1 file changed, 1 insertion(+)
```

**Real mistake, hit first**: typed `git log --oneline -all -graph` (single dashes) and got a
real error: `` error: switch `l' expects an integer value with an optional k/m/g suffix `` — with
a single dash, `-all` gets parsed as a cluster of short flags (`-a -l -l`), not the long-form flag
intended, and one of those short flags (`-l`) expects a number, which is exactly what broke. That
error aborts the command before `-graph` is ever reached, so it doesn't actually prove anything
about how `-graph` itself would parse — checked separately: `git log --oneline -graph` on its own
returns `fatal: unrecognized argument: -graph`, not a short-flag decomposition. Single-dash
clustering only applies to `-all`, not to every multi-letter flag typed with one dash.

**Syntax**: `git log --oneline --all --graph` — compact visual of every branch at once (`--all`
= every branch, not just current; `--graph` = ASCII branch/merge shape; note the double-dash for
these long-form flags, not single-dash — confirmed by the error above).

**Real discovery — an unrecognized commit found via the graph**: `d94a95b "commit"` appeared,
not matching anything from Topic 6's documented session. Investigated with `git show d94a95b`
rather than ignoring it — turned out to be the `"one more line"` content from Topic 6's `git
diff` demo, which had only ever been shown as an *unstaged* example at the time, apparently
committed later (likely via VS Code's Source Control panel's default commit button, generating
the generic message `"commit"`) — same category of accidental action as the earlier merge-UI
click mishap. Harmless: confirmed the actual content matched what was already known, nothing
destructive.

**Reading the graph shape itself, explained separately**: the diamond shape (`|\` / `|`) around
`0d41a29` is the actual Topic 6 merge commit — that's where two lines genuinely converge back
into one. Everything before it in a straight single line is the earlier fast-forward merges,
which never branched at all. From `cdbaba9` onward, `rebase-demo` and `master` have visibly
diverged into two separate lines — exactly the divergence this session's setup was built to
create.

**Reinforcing `HEAD` behavior, tested directly across two branches** (extended past what was
asked, to see it firsthand rather than just being told):
```
PS> git checkout rebase-demo
PS> git log --oneline --all --graph
* 05bdadd (master) another master commit after branching
| * 4907ec6 (HEAD -> rebase-demo) rebase branch commit
|/
* cdbaba9 master commit before rebase demo
...

PS> git checkout real-conflict
PS> git log --oneline --all --graph
* 05bdadd (master) another master commit after branching
| * 4907ec6 (rebase-demo) rebase branch commit
|/
* cdbaba9 master commit before rebase demo
* d94a95b commit
* 2a5302c add gitignore
*   0d41a29 Resolve merge conflict on line 1, keep master version
|\
| * 85fd936 (HEAD -> real-conflict) edit 1st line on real-conflict branch
...
```
Confirmed: `HEAD -> BRANCHNAME` moves to sit next to whichever branch's tip commit you're
currently on — proven directly rather than just described.

**Verified hands-on — the rebase, including a real conflict**:
```
PS> git checkout rebase-demo
PS> git rebase master
Auto-merging readme.txt
CONFLICT (content): Merge conflict in readme.txt
error: could not apply 4907ec6... rebase branch commit
hint: Resolve all conflicts manually, mark them as resolved with
hint: "git add/rm <conflicted_files>", then run "git rebase --continue".
hint: You can instead skip this commit: run "git rebase --skip".
hint: To abort and get back to the state before "git rebase", run "git rebase --abort".
```
**Conflict markers seen** (both lines legitimately wanted — resolved via **Accept Both Changes**,
a different choice than Topic 6's "pick one side"; shown here with a leading `|` on each marker
line so this notebook itself doesn't get mistaken for a live unresolved conflict — same real
gotcha as Topic 6's notes):
```
| <<<<<<< HEAD
another master commit
| =======
rebase branch line
| >>>>>>> 4907ec6 (rebase branch commit)
```
**Key nuance vs. a normal merge conflict**: during a rebase, `HEAD` represents the branch being
rebased **onto** (`master`), and the labeled incoming side is your **own** commit being replayed
— the reverse framing from a regular merge, where `HEAD` is normally your own current branch.

```
PS> git add readme.txt
PS> git rebase --continue
[detached HEAD 4b2fbee] rebase branch commit
 1 file changed, 1 insertion(+)
Successfully rebased and updated refs/heads/rebase-demo.
```
`[detached HEAD ...]` — normal, internal mechanic: rebase works in a temporary detached-HEAD
state while replaying each commit, then moves the branch pointer to match once done.

**Confirmed via `git log --oneline --all --graph`**: `rebase-demo`'s new commit (`4b2fbee`) now
sits in a single straight line directly on top of `master`'s tip (`05bdadd`) — no more `|`/`|\`
branching shape for this pair at all, proving the history is now linear.

**Pager tip**: a trailing `~` and `:...skipping...` sometimes showed up at the bottom of
`git log --graph` output — that means the terminal opened a pager (history didn't fit on one
screen). Press `q` to exit it cleanly, rather than letting it keep repeating or scrolling
awkwardly.

**Key confirmed fact (quiz-tested)**: rebase does **not** move the original commit — it
**creates a brand-new commit** replaying the same changes on the new base. Proof: the original
commit hash (`4907ec6`) became a different hash (`4b2fbee`) after rebasing — if it were the exact
same commit just relocated, the hash would be unchanged, since a commit hash is derived from its
content + parent. The original commit still technically exists until garbage-collected; it's
just no longer referenced by any branch.

### 2. Cherry-pick

Copies the changes from **one specific commit** onto the current branch, without touching the
rest of that commit's original branch.

**Syntax**: `git cherry-pick COMMIT_HASH`

**Verified hands-on — including a real conflict, and a real mistake caught and fixed** (commit
`714ab7c` is the "add feature line" commit created on `feature-branch` back in Topic 6):
```
PS> git checkout real-conflict
PS> git cherry-pick 714ab7c
Auto-merging readme.txt
CONFLICT (content): Merge conflict in readme.txt
error: could not apply 714ab7c... add feature line
hint: ... "git cherry-pick --continue" / "--skip" / "--abort" ...

PS> git add readme.txt
PS> git cherry-pick --continue
[real-conflict f2047ec] add feature line
 Date: Thu Jul 16 15:13:59 2026 -0400
 1 file changed, 3 insertions(+)
```

**Real mistake — resolved conflict markers were never actually removed**: `git add` +
`--continue` succeeded, but checking `cat readme.txt` afterward revealed the literal marker
syntax was still sitting in the file (again shown with a leading `|` on each marker line for the
same reason as above):
```
hello.git "EDITED ON REAL-CONFLICT BRANCH"
hello.git, second line
new feature line
| <<<<<<< HEAD
master line
| =======
| >>>>>>> 714ab7c (add feature line)
```
**Key lesson**: `git add` only marks a conflict as staged/"resolved" from Git's bookkeeping
perspective — it does **not** verify the actual content is clean. It trusts the human to have
genuinely fixed it. This is a real, common mistake.

**Syntax**: `git commit --amend --no-edit` — replaces the last commit with a corrected version,
keeping the same message. Fixed via this — took **two attempts** to get fully clean:
- Attempt 1: removed the `<<<<<<<`/`=======`/`>>>>>>>` marker lines themselves, but left a stray
  leftover fragment behind: `714ab7c (add feature line)` (the commit-hash/message label Git
  appends after `>>>>>>> `, partially deleted).
- Attempt 2: removed that stray line fully. Confirmed clean via `cat readme.txt`.

**Verifying "clean" at scale, beyond just `cat`-ing a small file**:

**Syntax**: `git diff --check` — built-in Git command that scans staged/working changes and flags
leftover conflict markers (and certain whitespace errors) automatically, regardless of file
size. Returned nothing on the clean file — no output means no issues found. Some teams wire
this into a pre-commit hook to block commits containing leftover markers automatically.

**Syntax**: `Select-String -Pattern "PATTERN" FILE` — PowerShell's equivalent of Linux's
`grep` (which doesn't exist natively in PowerShell — a real distinction surfaced this session by
actually trying `grep` here first and hitting the real error:
`grep: The term 'grep' is not recognized as a name of a cmdlet, function, script file, or
executable program.` — Linux-tool practice from Topic 2 happens in a separate WSL terminal,
this Windows PowerShell folder uses PowerShell-native commands instead).

**Example**: `Select-String -Pattern "<<<<<<<|=======|>>>>>>>" readme.txt`

### 3. Branching strategies (conceptual, no hands-on)

**Git Flow** — separate long-lived branches: `main` (production), `develop` (integration/staging
area where finished features accumulate and get tested together before a scheduled release),
plus short-lived `feature/*`, `release/*`, `hotfix/*` branches.
```
main    ─────────────────────────●───────────●──── (production releases only)
                                 /           /
release/1.2 ──────●────────────●
                  /
develop ─●───●───●───●───●───●───●───●─────────●──── (integration branch)
          \       \
feature/A  ●──●──●  feature/B  ●──●──●
```
Real-world fit: scheduled-release software (enterprise, banking) needing a clear audit trail of
what's in production vs. still integrating.

**Trunk-based development** — everyone commits directly to one main branch (`trunk`/`main`)
frequently; very short-lived feature branches (hours/a day, not weeks); relies on feature flags
instead of long-lived branches to hide incomplete work; needs strong CI.
```
main ─●──●──●──●──●──●──●──●──●──●──●──●──── (everyone commits here, constantly)
        \  /  \  /  \  /
     short-lived feature branches, merged back almost immediately
```
Real-world fit: teams deploying multiple times a day.

**GitHub Flow** — just `main` + feature branches merged via pull requests (code review gate); no
`develop`/`release` layers; `main` is always assumed deployable. What gets practiced hands-on in
Topic 8.
```
main ─●────────────●────────●──────●──── (always deployable)
        \          /\        \    /
   feature/x ●──●─●  feature/y ●──●
        (PR + review)      (PR + review)
```

**The core `develop`-branch distinction, worked through carefully (needed real back-and-forth to
land)**: `develop` exists specifically to let multiple in-progress features **wait together** for
a shared, scheduled release date (Git Flow's assumption). GitHub Flow has **no shared release
date** — every merge into `main` deploys immediately on its own, so there's nothing to
collectively wait for, and therefore nothing for a staging branch to do. Concrete side-by-side:
Git Flow — Feature A and B both merge into `develop`, sit together for testing, ship together on
one scheduled release day. GitHub Flow — Feature A merges into `main` and deploys same-day; B
merges 3 days later and deploys separately, never waiting for A.

**Hotfix scenario walked through under all three, to make the tradeoff concrete**:
- **Git Flow**: branch `hotfix/*` off `main` directly (not `develop`), fix, merge into **both**
  `main` (deploy) **and** `develop` (so the fix isn't silently lost when `develop` eventually
  merges into `main` for the next scheduled release — an easy step to forget in practice).
- **Trunk-based**: commit the fix directly to trunk (maybe via a very short-lived branch), rely
  on CI, deploy — no second branch to reconcile with since there's only one long-lived branch.
- **GitHub Flow**: branch off `main`, fix, PR + expedited review, merge, deploy — no second merge
  needed since there's no separate `develop` to keep in sync.

**Real-world way to identify a project's strategy** (not hands-on yet — proper GitHub practice is
Topic 8): check the Branches tab for `develop`/`release/*`/`hotfix/*` naming (Git Flow) vs. just
`main` + short-lived branches (trunk-based/GitHub Flow); check the commit graph/network view for
long parallel lines (Git Flow) vs. mostly one line with quick side-branches (trunk-based/GitHub
Flow); check for a `CONTRIBUTING.md` documenting the convention; check release frequency
(frequent small releases → trunk-based/GitHub Flow, infrequent versioned releases → Git Flow).

**Concrete real-world example, given directly**: Git itself traditionally used something close
to Git Flow-style long-lived branches, matching its own history of scheduled, versioned
releases — while many fast-moving SaaS products (GitHub itself being the namesake example)
popularized GitHub Flow instead, matching their continuous-deploy release rhythm.

### 4. Combined scenario

**Scenario**: on a feature branch with 5 commits; team lead asks to (1) clean up history to look
linear against `main` before merging, and (2) grab one urgent bugfix commit sitting on a
teammate's unrelated branch, without waiting for their whole branch.

**Answered correctly**: (1) **rebase** — replays the branch's commits on top of `main`'s current
tip, producing linear history with no merge commit. (2) **cherry-pick** — pulls in just that one
specific commit's changes, without needing the rest of that branch to be ready or merged.

---

## Topic 7 Quiz — Attempt 1: PASS, 82/100

Interview-style, open-ended, 4 questions. Question and full correct answer for each:

1. **Merge vs. rebase — what actually happens to the commits, not just "does it make a merge
   commit."**
   A merge joins two branches at a single point by creating a new **merge commit** with two
   parents — both branches' histories stay intact and visible, like two roads converging at an
   intersection. A rebase does something structurally different: it takes the current branch's
   commits and **replays** them one by one on top of the target branch's current tip, as if they
   had been written there from the start — like picking up a road and re-laying it starting
   further down the other one, with no intersection left at all. Critically, rebase does **not**
   move the original commits — each replayed commit is a **brand-new commit** with a new hash,
   because a commit's hash is derived from its content plus its parent, and the parent has
   changed. This was proven directly in this session: the original commit `4907ec6` ("rebase
   branch commit") became a different commit, `4b2fbee`, after `rebase-demo` was rebased onto
   `master` — same changes, new hash. The original commit still technically exists until Git
   garbage-collects it; it's just no longer referenced by any branch. The practical payoff is
   that rebase produces clean, linear history, while merge preserves a branching shape with a
   visible merge point.

2. **Safe conflict-resolution habit, based on today's real mistake.**
   The real mistake this session was that `git add` followed by `--continue` (during both a
   rebase and a cherry-pick) succeeded even though the literal conflict marker text
   (`<<<<<<<`, `=======`, `>>>>>>>`, plus a stray leftover fragment from the `>>>>>>>` label) was
   still sitting in the file. The key lesson: `git add` only marks a conflict as
   staged/"resolved" from Git's bookkeeping perspective — it does not verify the content is
   actually clean. It trusts the human to have genuinely fixed it, so it's entirely possible to
   "resolve" a conflict without actually removing the markers. The safe habit is to verify before
   trusting the add: open the file and read it (`cat`) for small files, and for anything bigger
   or to make it automatic, run **`git diff --check`** — a built-in Git command that scans
   staged/working changes and flags leftover conflict markers (and certain whitespace errors)
   automatically regardless of file size, returning no output when the file is clean. On
   PowerShell specifically (which has no native `grep`), the equivalent check is
   **`Select-String -Pattern "<<<<<<<|=======|>>>>>>>" FILE`**. Some teams wire `git diff --check`
   into a pre-commit hook so a commit containing leftover markers is blocked automatically rather
   than relying on a human remembering to check.

3. **Cherry-pick vs. merge — the tradeoff, concrete risk.**
   Cherry-pick copies the changes from **one specific commit** onto the current branch without
   touching the rest of that commit's original branch — the gain is a smaller, clean, precisely
   targeted change, useful when you want just one fix (e.g. an urgent bugfix) without pulling in
   an entire branch that isn't ready yet. The concrete risk is that cherry-pick creates a **new
   commit with a different hash** than the original, even though it carries the same change. If
   that original branch is later merged in full anyway, Git has no way of recognizing the
   cherry-picked commit and the original commit as "the same change" — it sees two different
   commits. This leaves a duplicate commit permanently sitting in the history (both the
   cherry-picked copy and the original, recorded as if they were separate changes) and, if the
   surrounding code has shifted since, real merge conflicts between the cherry-picked copy and the
   original when that branch eventually merges.

4. **Why GitHub Flow has no `develop` branch, Git Flow does.**
   `develop` exists specifically to let multiple in-progress features **wait together** for a
   shared, scheduled release date — Git Flow's core assumption is that releases happen on a
   schedule, so finished features accumulate on `develop`, get tested together, and ship as one
   batch on release day. GitHub Flow has no shared release date at all: every merge into `main`
   is assumed deployable and deploys on its own, immediately. Since there's nothing to
   collectively wait for, there's nothing for a staging branch to do. Concretely: under Git Flow,
   Feature A and Feature B both merge into `develop`, sit together while being tested, and ship
   together on one scheduled release day. Under GitHub Flow, Feature A merges into `main` and
   deploys the same day; Feature B merges three days later and deploys separately, never waiting
   on A. This same distinction shows up in the hotfix scenario: Git Flow needs a hotfix merged
   into **both** `main` (to deploy immediately) and `develop` (so the fix isn't silently lost
   when `develop` eventually merges into `main` for the next scheduled release), while GitHub
   Flow only needs one merge, straight into `main`, since there's no second long-lived branch to
   keep in sync.

**How the actual quiz session went** (for context, not the answers themselves): Q1's first answer
conflated merge and rebase loosely before being sharpened via the real hash-change evidence; Q2
passed cleanly first try; Q3 got the gain right immediately but needed a follow-up to state the
concrete risk precisely; Q4's first answer redirected to the wrong angle (PR usage) before fully
correcting once pointed back to the release-timing assumption.

**Score: 82/100**
- **Quiz 28/40** — all 4 ultimately correct, 3 of 4 needed a real follow-up push, including one
  full redirect on Q4.
- **Hands-on 30/30** — genuinely excellent: a real rebase conflict resolved, a real bad
  conflict-resolution mistake caught and fixed via `git commit --amend` (twice, since the first
  fix attempt left a stray fragment), a cherry-pick conflict resolved independently, and testing
  both `git diff --check` and `Select-String` as verification methods.
- **Depth 24/30** — good scenario/strategy reasoning, though the branching-strategies material
  took more back-and-forth than other topics to fully solidify.

**Verdict**: **Topic 7 CLEARED, attempt 1, 82/100.**
