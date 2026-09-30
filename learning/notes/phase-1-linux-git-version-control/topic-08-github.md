# Topic 8 — GitHub: PRs, Actions Intro, Repo Management

> Personal study notebook — full teaching content, commands, outputs, and explanations.
> Distinct from `progress.md` (tracking) and `session_notes.md` (short personal reflection).
> Single-day topic per the roadmap, and the final topic in Phase 1 — covered in one session,
> ending in the quiz.

---

## Day 1 — 2026-07-19/20 — Remotes, Pull Requests, GitHub Actions, repo management

Practiced using a dedicated, temporary GitHub repo (`your-org/git-practice`) created specifically
for this topic — intended to be deleted once Topic 8 is complete, since the lasting record lives
in this notebook, not the throwaway repo.

**Repo-creation logistics, discussed before starting**: considered reusing the existing handbook
repo instead of creating a new one, but ruled that out — it already had a real `index.html` site
living in it, and deliberately practicing risky Git operations (force pushes, branch deletion,
rebase) against it risked actually breaking something real. A fresh, disposable practice repo
avoids that risk entirely. Also discussed personal-vs-work GitHub account tradeoffs for where
practice repos like this should live. Separately, an "AppID" reference that came up was clarified
as an org-specific concept tied to this particular organization's setup, not a standard GitHub
term or feature everyone would encounter.

### Today's agenda
1. Remotes — connecting local Git to GitHub.
2. Pull Requests, hands-on.
3. GitHub Actions — intro.
4. Repo management — branch protection rules.
5. Combined scenario.
6. The quiz.

### 1. Remotes — connecting local Git to GitHub

A **remote** is a reference to a copy of the repository hosted elsewhere (GitHub being the most
common host) — the piece connecting Git (the tool, fully local/offline-capable) to GitHub (one
company's hosting service for Git repos).

**Syntax**: `git remote add NAME URL` — register a remote (conventionally `origin`)
**Syntax**: `git push REMOTE BRANCH` — upload local commits to the remote
**Syntax**: `git pull REMOTE BRANCH` — download and merge remote changes into the local branch
**Syntax**: `git clone URL` — copy an entire remote repo down for the first time

**Verified hands-on — connecting and first push**:
```
PS> git remote add origin https://github.com/your-org/git-practice.git
PS> git remote -v
origin  https://github.com/your-org/git-practice.git (fetch)
origin  https://github.com/your-org/git-practice.git (push)

PS> git push -u origin master
Enumerating objects: 34, done.
...
Writing objects: 100% (34/34), 3.10 KiB | 41.00 KiB/s, done.
...
To https://github.com/your-org/git-practice.git
 * [new branch]      master -> master
branch 'master' set up to track 'origin/master'.
```
`-u` sets the upstream tracking relationship — future `push`/`pull` on this branch won't need the
remote/branch specified again. `[new branch]` confirms GitHub now has a matching branch.

### 2. Pull Requests — hands-on, including a real mistake caught and fixed

**Real mistake — a PR accidentally branched off the wrong base**: created `add-notes` right after
starting the session, but the local repo was still sitting on whatever branch was last checked
out at the *end* of Topic 7 (`real-conflict`), not `master` — nothing explicitly switched back to
`master` first. `git checkout -b add-notes` branched off wherever the repo actually was.

**Diagnosed properly, not guessed**:
```
PS> git log --oneline --graph --all
* f4023ce (HEAD -> add-notes, origin/add-notes) add notes file for PR request
* dc448e5 (real-conflict) add feature line
| * 4b2fbee (rebase-demo) rebase branch commit
| * 05bdadd (origin/master, master) another master commit after branching
...
* | 85fd936 edit 1st line on real-conflict branch
| * 1f6d20d edit line 1 on master
...

PS> git merge-base add-notes master
85fd936e6e2c7e4c501466cf6a5d6942f5089448
```
Confirmed: `add-notes` branched from `dc448e5` (on `real-conflict`), and its true common ancestor
with `master` was `85fd936` — way back before `master`'s later commits. This connects directly to
Topic 7's quiz reasoning about cherry-picked commits creating duplicate-content risk later — now
hit for real, on GitHub's side: the PR showed **"This branch has conflicts that must be
resolved"** and included an unexpected extra commit that had nothing to do with the intended
change.

**Real lesson**: always verify which branch you're actually on (`git branch`) before creating a
new one — "current branch" can silently carry over from a previous session's last checkout.

**Fixed by deleting and recreating properly**:
```
PS> git checkout master
PS> git branch -D add-notes
Deleted branch add-notes (was f4023ce).
PS> git push origin --delete add-notes
 - [deleted]         add-notes
```
(Deleting the remote branch auto-closed the associated GitHub PR — expected behavior.)
```
PS> git checkout -b add-notes
PS> "topic 8 practice notes" > notes.txt
PS> git add notes.txt
PS> git commit -m "add notes file for PR request"
PS> git push -u origin add-notes
Enumerating objects: 4, done.
...
Writing objects: 100% (3/3), 363 bytes | 90.00 KiB/s, done.
...
remote: Create a pull request for 'add-notes' on GitHub by visiting:
remote:      https://github.com/your-org/git-practice/pull/new/add-notes
```
Only 3 objects transferred this time (vs. 34 before) — confirming a clean, minimal branch off
`master`'s actual current tip. The new PR showed exactly 1 commit, 1 file changed, **no
conflicts** — confirmed the fix worked.

**Merge strategy choice, reasoned through**: GitHub offers three options — **Create a merge
commit** (standard, keeps full history + a merge commit, has two parent commits), **Squash and
merge** (combines all PR commits into one clean commit — valuable when a PR has many messy
intermediate commits, not relevant here since this PR had only one), **Rebase and merge** (replays
PR commits directly onto the target, linear history, no merge commit). Chose **Create a merge
commit**, correctly reasoning squashing wouldn't change anything for a single-commit PR.

**Syncing back down and cleanup**:
```
PS> git checkout master
PS> git pull origin master
...
Updating 05bdadd..d3ef013
Fast-forward
 notes.txt | 1 +
PS> git branch -d add-notes
Deleted branch add-notes (was a9a5fea).
```
**Real observation**: even though "Create a merge commit" was chosen on GitHub, the local `pull`
still showed **`Fast-forward`** — because local `master` had zero new commits since the last
push, so pulling in GitHub's new merge commit was just moving the local pointer forward. Same
fast-forward concept from Topic 6, triggered via `pull` this time instead of a direct `merge`.

`git branch -d` (lowercase, used here) vs `-D` (uppercase, used earlier to force-delete the
mis-based branch): lowercase refuses to delete a branch with unmerged work — a safety check —
while `-D` deletes regardless.

### 3. GitHub Actions — intro

GitHub's built-in CI/CD system — automatically runs code (tests, builds, deployments) in response
to repo events, via a workflow file GitHub watches for automatically.

**Location**: `.github/workflows/*.yml`

**General shape**:
```yaml
name: WORKFLOW_NAME
on: TRIGGER
jobs:
  JOB_ID:
    runs-on: RUNNER
    steps:
      - name: STEP_NAME
        run: SHELL_COMMAND
```

**Workflow written and explained line by line**:
```yaml
name: Hello World Workflow

on: push

jobs:
  say-hello:
    runs-on: ubuntu-latest
    steps:
      - name: Print a greeting
        run: echo "Hello from GitHub Actions, Topic 8 practice!"
```
- `name:` — the workflow's display name, shown in GitHub's "Actions" tab.
- `on: push` — the **trigger**; runs on every push (other common triggers: `pull_request`,
  `schedule` for cron-based runs, `workflow_dispatch` for a manual trigger button).
- `jobs:` / `say-hello:` — jobs are units of work, run in parallel by default; the name is an
  arbitrary label.
- `runs-on: ubuntu-latest` — the **runner** spec: which kind of temporary VM GitHub provisions
  to execute this job. Other options: `windows-latest`, `macos-latest`.
- `steps:` — run sequentially within a job; `name` is a human-readable log label, `run` is the
  actual shell command executed.

**What a "runner" actually is, explained from scratch (grounded only in Topic 1's VM concept, not
assumed CI/CD familiarity)**: a runner is the actual virtual machine — a full virtual computer
with its own CPU, memory, disk, and OS, same concept as Topic 1's VMs — that GitHub temporarily
creates just to execute a workflow's steps. The full sequence:
1. Code gets pushed to GitHub.
2. GitHub reads the workflow file and checks if the trigger (`on:`) matches what just happened.
3. GitHub creates a **brand-new, temporary VM** matching `runs-on:` — this VM is the "runner." It
   didn't exist a moment before; GitHub provisions it fresh, on its own infrastructure, for this
   one job only.
4. That VM executes each `step` in the workflow, in order.
5. Once the job finishes, GitHub **destroys that VM completely** — nothing persists; the next run
   gets a brand-new runner, not a reused one.

Visually: `Workflow file (instructions) → triggers → GitHub creates a VM matching "runs-on" →
this VM, while working, is called the runner → executes each step → VM/runner destroyed.`

**Verified hands-on — pushing the workflow and watching it actually run**:
```
PS> git add .github/workflows/hello.yml
PS> git commit -m "Add hello world GitHub Actions workflow"
PS> git push origin master
```
Checked the real run under GitHub's **"Actions"** tab — completed successfully in 9 seconds.
Inspected the actual logs:
- **"Set up job"** section showed: `Operating System: Ubuntu / 24.04.4 / LTS` (confirms
  `ubuntu-latest` resolved to a real, specific version) and `Azure Region: eastus` — a concrete
  real detail: GitHub Actions runners are actually hosted on **Microsoft Azure's cloud
  infrastructure** (Microsoft owns GitHub) — a genuine, physically-provisioned VM, not an
  abstraction. Also showed a full `GITHUB_TOKEN Permissions` list — scoped write/read access
  automatically granted to this specific job.
- **"Print a greeting"** step showed the exact command executed and its real output:
  ```
  Run echo "Hello from GitHub Actions, Topic 8 practice!"
  Hello from GitHub Actions, Topic 8 practice!
  ```
- **"Complete job"** showed `Cleaning up orphan processes` — the teardown beginning, right
  before the VM gets destroyed.

**Why `ubuntu-latest` was chosen over `windows-latest`, worked through in detail**:
- **No dependency on the contributor's own OS** — `runs-on` specifies a temporary cloud VM;
  someone on Windows, Mac, or Linux can all use `ubuntu-latest` and it behaves identically for
  everyone, since execution happens on GitHub's VM, never the contributor's own machine.
- **Cost** — Linux runners are the cheapest; Windows runners cost roughly 2x the minutes, macOS
  roughly 10x.
- **The real reason for the cost gap**: **licensing** (Linux is free/open-source; Windows Server
  licensing costs pass through; macOS is tied to Apple's ecosystem) and, more significantly,
  **hardware constraints** — Apple's license terms only permit macOS to run on genuine Apple
  hardware, so GitHub must provision actual physical Mac machines for macOS runners rather than
  cheap virtualized commodity servers, unlike Linux/Windows which virtualize freely at scale.
- **Speed** — Linux VMs are lightweight and provision faster than Windows/macOS ones.
- **Industry alignment** — most production servers/containers/cloud infrastructure (AWS,
  Kubernetes — everything later in this roadmap) run Linux; testing in the same OS family as
  production catches more real issues.
- **When `windows-latest`/`macos-latest` actually make sense**: only when the job genuinely needs
  that OS — e.g., building a Windows `.exe`, testing PowerShell-specific/.NET Framework (not
  Core) behavior, or building an iOS app (requires macOS specifically).

**Important callout — GitHub Actions security considerations**:

The `GITHUB_TOKEN` seen in the "Set up job" logs is a **real, automatically-generated
credential**, scoped and time-limited by design:
- **Scope**: limited only to the specific repo the workflow runs in — not the whole account
- **Lifespan**: generated fresh for each run, expires immediately once the job completes — not a
  long-lived credential sitting around to be stolen

Despite that safe-by-default design, three real risks exist in practice, all tying back to
Topic 1's privilege-escalation lesson (a writable file executed by a more-privileged process):

1. **Untrusted third-party Actions** — workflows often use pre-built Actions written by other
   people/organizations. If one is malicious or gets compromised, it runs with the same
   token/permissions as your own job — a real, documented supply-chain attack vector. The actual
   danger: a compromised Action can act on the repo with the job's real permissions/access,
   without the user's knowledge (e.g., stealing secrets, pushing malicious code).
2. **Secrets accidentally shown in the run's log output** — if a command in the workflow outputs
   a stored password/API key (a "secret") directly, that value becomes visible to anyone who can
   view the workflow's logs — a very common real mistake.
3. **Pull requests from outside contributors** — on "public" repos (ones anyone on the internet
   can view and copy, as opposed to "private" ones only specific people can access), GitHub
   restricts outside contributors' proposed changes from running workflows with full
   write-permission tokens by default, specifically to stop an external attacker from hijacking
   CI to steal secrets or push malicious code.

**Real mitigations teams actually use**: pin third-party Actions to a specific trusted commit
hash (not just `@latest`), grant the token only the minimum permissions actually needed (not the
full default list), never print secrets to logs, and require manual approval before running
workflows triggered by external/fork PRs.

### 4. Repo management — branch protection rules

Branch protection rules enforce rules on important branches (e.g., requiring PR review before
merging, blocking direct pushes, requiring status checks to pass). Location: **Settings →
Branches**, which offered two paths — the newer **"Add branch ruleset"** system, or **"Add
classic branch protection rule."** Chose **classic** specifically, since it maps more directly
to what's being learned conceptually here.

**Options explored, tied to prior topics**:
- **"Require a pull request before merging"** — enforces the PR workflow already practiced;
  blocks direct pushes to the protected branch. Checking this auto-checked its sub-option
  **"Require approvals"** to `1` required approval. Other sub-options ("dismiss stale approvals,"
  "require review from Code Owners") were left alone — noted as team-only refinements not needed
  on a solo practice repo.
- **"Require status checks to pass before merging"** — can require a GitHub Actions workflow
  (here, the `say-hello` job) to succeed before a PR is allowed to merge. The screen initially
  showed "No required checks" — had to manually search for and select `say-hello` from a search
  box before it took effect.
- **"Require linear history"** — ties directly to Topic 7's rebase concept — forbids regular
  merge commits entirely (which have two parents, breaking a single line), forcing every merge to
  go through squash or rebase instead.
- **"Allow force pushes"** / **"Allow deletions"** — **a real mistake, caught and fixed**: these
  were actually checked (enabled) by mistake alongside "Require linear history," not deliberately
  left unchecked. Caught directly: checking them would *permit* the exact risky actions
  (overwriting shared history, deleting a protected branch) that Topics 6/7 flagged as
  dangerous — the opposite of what a protection rule should do. Unchecked both once the mistake
  was pointed out.

**Real discovery #1 — branch protection doesn't apply to repo admins by default**:
```
PS> git push origin master
...
remote: Bypassed rule violations for refs/heads/master:
remote: - Changes must be made through a pull request.
remote: - Required status check "say-hello" is expected.
To https://github.com/your-org/git-practice.git
   9b35f5c..a971ec4  master -> master
```
The push **succeeded** despite active rules, because GitHub's classic branch protection
**doesn't apply to repo owners/admins by default** — a genuine, common real-world gotcha. Fixed
by enabling **"Do not allow bypassing the above settings"** on the rule, then retesting:
```
PS> git push origin master
...
remote: error: GH006: Protected branch update failed for refs/heads/master.
remote: - Changes must be made through a pull request.
remote: - Required status check "say-hello" is expected.
 ! [remote rejected] master -> master (protected branch hook declined)
error: failed to push some refs to 'https://github.com/your-org/git-practice.git'
```
Genuinely blocked this time — `GH006` is GitHub's specific error code for this rejection, and the
push was cleanly rejected client-side too (`protected branch hook declined`). Cleaned up the
local-only test commit with `git reset --hard HEAD~1`, safe since it was never pushed.

**Real discovery #2 — the self-approval block**: with "Require approvals" (1 required) enabled,
opened a PR (`test-pr-approval`) and tried to merge immediately without approving — the merge
button was greyed out, showing "Review required." Confirmed the `say-hello` status check had
already passed (green) **independently** of the approval gate — proving these are two separate,
independent requirements, not one combined check. GitHub generally doesn't allow approving one's
own PR, so as the sole account on this practice repo, this genuinely blocked the merge until
"Require approvals" was unchecked.

**Real discovery #3 — linear history restricting merge options directly, not just in theory**:
once unblocked and merging the approval-test PR, the merge button's dropdown showed **only
"Squash and merge" and "Rebase and merge"** — "Create a merge commit" was absent entirely,
confirming "Require linear history" genuinely enforces what was only discussed conceptually in
Topic 7.

**Real mix-up, resolved — squash-merge sequencing**: after clicking "Squash and merge" for
`test-pr-approval`, ran local cleanup commands (`git pull` and related) *before* actually
confirming the squash had gone through — `git pull` reported "Already up to date," which looked
suspicious. Verified with `git log --oneline origin/master -5` and confirmed the squash commit
genuinely hadn't landed yet; the sequence had gotten ahead of itself. Correct order: let the
merge on GitHub actually complete first, *then* pull locally — not the other way around.

### 5. Combined scenario

**Scenario**: a teammate says a direct push to `master` got rejected yesterday, but the same
action went through fine today. What's the most likely explanation?

**Answered correctly** (after a timeline mix-up was clarified — initially read the scenario's
before/after order backwards): most likely, **"Do not allow bypassing the above settings" was
unchecked** (or the pushing account has admin/bypass permission that wasn't restricted) — the
protection rule still exists, but silently stopped applying to that person, exactly the real
gotcha discovered firsthand earlier in the session.

---

## Topic 8 Quiz — Attempt 1: PASS, 94/100

Interview-style, open-ended, 4 questions. Question and full correct answer for each:

1. **What's the core distinction between Git and GitHub?**
   Git is the actual version control tool — it runs locally, works entirely offline, and is what
   tracks commits, branches, and history on a machine's own files. GitHub is one company's hosting
   service built on top of Git: a remote place to store, share, and collaborate on Git
   repositories online (via remotes, pull requests, Actions, branch protection, etc.). Git doesn't
   need GitHub to function; GitHub is a layer added on top for hosting and collaboration.

2. **What was the actual root cause of the `add-notes` PR showing an unexpected conflict and an
   extra commit?**
   The branch was created with `git checkout -b add-notes` without first switching back to
   `master`. At the start of the session, the local repo was still sitting on whatever branch had
   been last checked out at the *end* of the previous topic (`real-conflict`) — nothing had
   explicitly run `git checkout master` first. Because "current branch" silently carries over
   between sessions, `add-notes` ended up branching off `real-conflict`'s tip (`dc448e5`) instead
   of `master`'s actual current tip. Diagnosing it with `git log --oneline --graph --all` and
   `git merge-base add-notes master` confirmed the branch's true common ancestor with `master` was
   `85fd936` — far behind `master`'s later commits — which is why the PR showed an unrelated extra
   commit and a conflict. The fix was deleting the branch (`git branch -D add-notes` plus deleting
   the remote branch, which auto-closed the PR) and recreating it correctly from `master` after
   checking out `master` first. The lesson: always confirm which branch you're actually on
   (`git branch`) before creating a new one.

3. **What are the three GitHub merge strategies, and why does enabling "Require linear history"
   eliminate one of them?**
   GitHub offers three merge options on a PR: **Create a merge commit** — the standard option,
   keeps the full commit history plus adds a new merge commit that has two parent commits;
   **Squash and merge** — combines every commit in the PR into a single clean commit on the target
   branch, useful when a PR has many messy intermediate commits; and **Rebase and merge** —
   replays the PR's commits directly onto the tip of the target branch, producing linear history
   with no merge commit at all. "Require linear history" forbids regular merge commits entirely,
   because a merge commit has two parent commits, which breaks a single straight line of history.
   With that rule enabled, "Create a merge commit" disappears from the merge button's dropdown
   entirely, leaving only "Squash and merge" and "Rebase and merge" as options.

4. **What's the security risk with `GITHUB_TOKEN` when a workflow uses untrusted third-party
   Actions, and what mitigates it?**
   `GITHUB_TOKEN` is a real, automatically-generated credential that GitHub Actions creates fresh
   for every workflow run — scoped only to the specific repo the workflow runs in, and expiring as
   soon as the job finishes. The risk: workflows commonly use pre-built Actions written by other
   people or organizations, and if one of those Actions is malicious or gets compromised, it runs
   with that same job's token and permissions — meaning it can act on the repo (e.g. stealing
   secrets, pushing malicious code) with the job's real access, without the user's knowledge. This
   is a genuine, documented supply-chain attack vector. The real mitigations: pin third-party
   Actions to a specific trusted commit hash rather than a floating tag like `@latest`; grant the
   token only the minimum permissions actually needed rather than the full default set; never
   print secrets to workflow logs (anyone who can view the logs can see them); and require manual
   approval before running workflows triggered by pull requests from outside/fork contributors.

**How the actual quiz session went** (for context, not the answers themselves): Q1 passed
cleanly, first try. Q2 initially restated the symptom (branched from `real-conflict` instead of
`master`) rather than the cause, and needed real redirection to reach it — the one genuine gap in
this quiz. Q3 was answered fully and correctly, then extended with one follow-up adding the
precise reason a merge commit breaks linearity. Q4 immediately and correctly listed all four
mitigations, then extended with one follow-up adding the precise danger mechanism itself.

**Score: 94/100**
- **Quiz 36/40** — genuinely 1 real gap out of 4 (Q2), not 3; Q3 and Q4 were both comprehensive
  and correct on the first pass, only extended with one more precise sentence each, which is
  meaningfully different from needing an actual correction.
- **Hands-on 30/30** — genuinely the richest session yet: remotes setup, a real self-diagnosed PR
  mistake fixed via `git log`/`merge-base` rather than guessed, a working GitHub Actions run
  inspected in full log detail, and thorough branch-protection testing uncovering three separate
  real discoveries (bypass-by-default, self-approval block, linear history restricting merge
  options).
- **Depth 28/30** — strong real-world reasoning throughout, correct diagnoses backed by direct
  evidence rather than assumptions.

**Verdict**: **Topic 8 CLEARED, attempt 1, 94/100** — Phase 1 (Linux, Git & Version Control) complete.
