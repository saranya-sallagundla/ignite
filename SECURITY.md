# Security policy

## What this repository is

Educational reference material. `orbit/` is a learning project built incrementally alongside a
curriculum — it is **not production-hardened infrastructure**, and it is not deployed anywhere that
serves real traffic. Please do not deploy it as-is.

That shapes what a meaningful security report looks like here.

## The realistic risk, stated plainly

The likeliest security problem in this repo is not a vulnerability in a running service. It is
**an example that teaches an insecure pattern, which someone then copies into something real.**

A Dockerfile with a subtly wrong permission model, a Terraform snippet that leaves a bucket open, a
Kubernetes manifest missing a `securityContext` — reproduced in a notebook, read by someone learning
from it, and carried into production somewhere else. That is the failure mode worth reporting, and it
is treated as a real defect rather than a documentation nit.

## How to report

**Insecure examples or teaching patterns** → open a normal public issue. There is nothing to
coordinate; the sooner it is visible, the fewer people copy it. Please point at the file and line and
say what the safe version is.

**A genuine vulnerability** — a leaked credential, an exposed secret in history, a supply-chain issue,
or anything that would be harmful if published before it is fixed → please use GitHub's
**private vulnerability reporting** on this repository (Security tab → Report a vulnerability) rather
than opening a public issue or emailing.

Private reporting is used deliberately in place of a contact address, so that reporting a problem does
not require publishing an email address anywhere in this repo.

## Scope

| In scope | Out of scope |
|---|---|
| `orbit/` — application code, Dockerfile, Compose, manifests, infrastructure config | Prose or explanations in `learning/` notebooks that are merely *incomplete* rather than wrong |
| `.github/` workflows and their permissions, once added | The scores in `learning/handbook_status.md` — self-assessed and AI-graded by design, and labelled as such |
| Dependency and base-image supply chain | Third-party command output reproduced as factual record |
| Anything committed to git history, including in deleted files | Findings that require access to the author's machine |

## Response

This is a single-person project run alongside full-time work, so there is no formal SLA. Realistically:
an acknowledgement within a few days, and secret- or credential-class reports prioritised over
everything else, including the curriculum.

## What has already been checked

A full public-readiness audit was run before this repository was promoted publicly — covering every
tracked file and the complete commit history for credentials, tokens, keys, personal data, and
infrastructure disclosure, plus container and dependency posture. Findings and remediation are recorded
in [`audits.md`](audits.md). Git history was rewritten to remove identity metadata that a
working-tree-only check would have missed.

If you find something that audit missed, that is exactly the report worth making.
