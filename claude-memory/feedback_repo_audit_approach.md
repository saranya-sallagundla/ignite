---
name: feedback-repo-audit-approach
description: "How to run a full-repo professionalism audit — workflow structure, severity triage, fix batching, and what to preserve"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 54fc18ae-44c1-4ab2-8bba-baf5e914af0e
  modified: 2026-07-27T08:22:49.735Z
---

Approach validated on the ignite repo's Topic 10 audit (2026-07-27, ~200 findings across 29
files), confirmed as the right shape by the user's follow-up requests (a dedicated audit folder,
a recurring cadence, memory updates to prevent repeat mistakes). Applies to any future "audit this
whole repo/codebase for quality" request, not just [[project-ignite-learning-mission]].

- **Use the Workflow tool with many parallel agents, one per file-group or cross-cutting
  dimension** (e.g. one agent per 2 notebook files, one for cross-file consistency, one for git
  hygiene), rather than trying to read everything in one context. Why: a 29-file, word-by-word
  audit genuinely doesn't fit one pass, and dedicated agents per dimension catch things a single
  broad pass misses (e.g. a git-hygiene specialist caught missing `.gitignore`/`.gitattributes`
  that a content-focused pass wouldn't have thought to check).

- **Cap large-file auditors at 2 files each, not 4.** Notebook-style files in the 500-800 line
  range caused repeated agent stalls when 4 were assigned per auditor; splitting to 2 files per
  agent (still parallelized, just more agents) resolved it completely. Watch for this specifically
  when auditing dense, long-form documentation rather than short config/code files.

- **Always report findings before fixing anything — never apply fixes silently, even obviously
  correct ones.** Categorize by severity (critical / important / minor / cosmetic) so the user can
  see the shape of the problem and decide priority, rather than getting fixes as a fait accompli.
  Confirmed explicitly: the user reviewed the full report before authorizing any batch.

- **Fix in small, separately-committed batches, not one giant commit.** Each batch should be
  independently reviewable and revertible (e.g. "critical fixes," "repo hygiene," "showcase
  polish," "date/time normalization" as distinct commits) — this also lets the user approve/adjust
  the plan between batches rather than committing to the whole scope up front.

- **Defer genuinely domain-specific best-practice items to when that skill/topic is actually being
  taught or used, instead of fixing them retroactively.** In a learning-repo context specifically:
  Dockerfile hardening (non-root user, multi-stage builds, etc.) was left for Topic 11 rather than
  silently fixed during the audit, since the whole point of the mission is hands-on learning, not
  a clean repo handed to the user pre-solved. Ask whether this applies before batching a fix in
  contexts where the user is meant to learn the underlying skill, not just receive a working repo.

- **Save the full audit record permanently in a dedicated folder in the repo itself** (not just as
  a chat report), with "what was fixed and why it matters" framing per item/batch, not just a raw
  findings list — this is what makes a recurring audit cadence actually useful later (each audit
  can check "did we actually resolve the deferred items from last time," and a future session with
  no memory of this conversation can still see the full reasoning).

- **When redacting something sensitive (e.g. an employer name), double-check the audit record
  itself doesn't quote the original leaked string while describing the fix.** Caught this exact
  mistake in the ignite audit — described a redaction fix by quoting the very string being
  redacted, re-leaking it in the "fix" documentation. Always re-verify the redaction target is
  absent from every new file written during the audit, including meta-documentation about the fix.

- **If the audit should recur on a cadence, make that a durable rule in the repo's own instruction
  file (e.g. `CLAUDE.md`), not just something remembered in [[project-ignite-learning-mission]] or
  my own memory.** A rule embedded in the project's own read-every-session file survives even a
  completely fresh session with no memory continuity; personal memory is a good backup, not the
  primary mechanism, for anything the *repo itself* should durably know about its own process.

- **After producing the raw audit report, always save an unmodified copy of it directly under
  `C:\CloudOps`** (one level above the `ignite` repo itself), in addition to the scratchpad file
  it's originally written to and the permanent `audits/topic-N-audit.md` record. This is now
  written into `ignite/audits/README.md`'s "Rules for every audit" so it isn't dependent on memory
  alone. Confirmed explicitly: the user wants this raw copy saved as-is — do NOT redact or edit
  anything in it (e.g. don't scrub an employer-name instance the way the permanent audit record
  itself should be scrubbed). The scratchpad/raw report and the permanent in-repo record are held
  to different standards: the raw report is a verbatim snapshot, the in-repo record is the
  polished, redaction-clean version shown to others.

- **The audit-record folder lives at the repo's top level (`ignite/audits/`), not nested under
  `learning/`.** Moved there 2026-07-27 after the user pointed out that audits cover `project/`
  too (the interview-facing folder), not just the internal learning-side scaffolding — nesting it
  under `learning/` mischaracterized its scope. Same logic applies to any future repo: put a
  whole-repo audit folder at the root, not inside whichever subfolder happens to be the primary
  content area.

- **A prior audit's findings are not a fixed checklist for the next audit to re-verify — each
  audit should look at the whole repo fresh and surface whatever new issues actually turn up,
  beyond the categories a past audit happened to define.** The user explicitly corrected this:
  "audit means checking everything," and what a first audit found and categorized was that pass's
  findings, not a permanent taxonomy future passes are confined to. Now written into
  `ignite/audits/README.md`'s "Rules for every audit" as the first rule. Applies to any recurring
  audit process: don't let audit N+1 become "check whether audit N's list is still fixed" — it
  should be a genuinely open-ended pass, same as the first one.
