# Session notes (personal recap)

> Not used for logic — this file is for your own review.
> Dates are IST (UTC+5:30), format YYYY-MM-DD. After each session, a short recap: what happened,
> what was hard, what to remember.

## Session 1 — 2026-07-06
VM vs container took two full passes to actually click — first explanation didn't land; the
apartment/foundation analogy is what finally made it stick. Also caught myself asking for
double-checks before running `chmod`/`rm` on my own files even though the risk was near zero —
good instinct to keep, don't let it fade once things feel routine. The network/proxy dead-end was
frustrating but worth sitting with rather than skipping past. Was already tired from a long
stretch since last night — watch for this pattern once night shifts start this month; may need to
split sessions shorter rather than push through fatigue like this one.

## Session 2 — 2026-07-07
Hard links vs symlinks didn't click from explanation alone — needed to actually break things
(force-overwrite a real link and watch data disappear) before it stuck for real. Good sign: kept
pushing back on my own answers ("privacy" wasn't good enough, kept digging until I could name
"kernel" specifically) instead of accepting a vague-but-safe answer — that's the interview muscle
actually building. First quiz passed on attempt 1, but ran way over the 20-min cap — worth
watching whether that becomes a pattern as topics get harder, or if it's just first-quiz jitters.

## Session 3 — 2026-07-08
Genuinely enjoyed chaining commands into one pipeline at the end — that felt like the first time
something clicked as "this is what the job actually looks like" rather than isolated flashcard
facts. Tripped on `-v` with a case-sensitivity mismatch and initially misread `uniq` as comparing
words-on-a-line instead of whole lines — both cleared up fast once tested directly rather than
just re-explained. Good habit forming: testing predictions against real output before trusting an
assumption, instead of just accepting the first plausible-sounding answer.

## Session 4 — 2026-07-09
Said out loud "I'm not able to remember everything" partway through a dense command-heavy
session — worth remembering that's a normal reaction to volume, not a sign of falling behind;
the notebook exists precisely so memorization isn't the job right now, repetition across future
topics is. The ping-vs-curl discovery (ICMP allowed, TCP blocked on the same network) was the
best moment of the day — genuinely surprised me and then made complete sense once explained,
which is a better kind of learning than being told a fact upfront. Quiz was noticeably shakier on
exact syntax (`grep -r` flag placement, `find` scope) than Topic 1's quiz — watch whether that's
fatigue from the length of the session or a real gap to reinforce next time shell commands come up.

## Session 5 — 2026-07-10
`classify.sh` was a genuine grind — real, distinct syntax mistakes one after another (else/fi
separators, merged blocks, then a nano-vs-printf `\n` mixup that broke everything in a confusing
new way). Kept wanting to just be handed the answer partway through, but pushing through to write
it myself paid off — the final self-debugged syntax error (fixed by reading the line number bash
pointed to) felt like the first "real" debugging moment of this whole mission, not a guided
exercise.
Worth remembering next time something feels this frustrating: it's often exactly the sign that
real learning is happening, not that something's wrong.

## Session 6 — 2026-07-11 / 2026-07-12
First real quiz miss of the whole mission — function scoping genuinely didn't land on attempt 1,
even after several analogies. Said "it's not going inside my brain" out loud instead of pretending
it clicked — the right instinct, and directly led to trying something different: a real script
that prints `$1` at three points, watching actual values instead of reasoning abstractly. That
worked almost immediately. Asked to retake the *entire* quiz fresh rather than just retest the
weak spot — good call, and it passed cleanly across the board, including the exact concept that
failed an hour earlier. Big lesson to hold onto: when an explanation isn't landing, switch to
"run it and watch" much sooner instead of trying a fourth variation of the same kind of
explanation. Also: took a real fatigue-driven pause mid-session and came back rested rather than
pushing through, then had the energy to push through a full retest same night — both were the
right calls at the time they were made.

## Session 7 — 2026-07-12
Genuinely satisfying session — no major stuck points like Topic 3's functions, just steady
building on real curiosity (kept asking to filter by more STAT modifiers than asked, which paid
off). The `/proc`/`fd` exploration finally explained `2>&1` from Topic 3, which felt like a real
payoff for sticking with the material instead of just memorizing it at the time. Forgot the sudo
password mid-session and fixed it without panic, once reassured it wouldn't touch any files —
good to remember that account/credential stuff feels riskier than it usually is. Best moment: the
NTP timeout logs turning out to be the same corporate proxy issue from Topic 1, and then proving
myself right by re-searching with a different keyword instead of accepting an empty result.

## Session 8 — 2026-07-13 / 2026-07-14
Real production carryover felt great — connecting the "df timing out" alert my own team actually
gets to the liveness-vs-corruption distinction we just learned made the material click
immediately, more than any invented scenario would have. Got genuinely confused re-reading back a
sequence of commands mid-session (worried something had broken when nothing had) — asking for a
plain step-by-step retrace cleared it up fast, worth doing that sooner next time instead of
sitting with the confusion. Reasoned through the inode-vs-block exhaustion scenario correctly with
just a small hint rather than a direct answer — good sign the "why" behind concepts is sticking,
not just command syntax. Topic 4 cleared on quiz attempt 1, tying the best hands-on score so far (28/30).

## Session 9 — 2026-07-14 / 2026-07-16
Honest moment worth remembering: asked to move fast through Topic 5 to fit both days in one
sitting, passed the quiz (74/100), but admitted afterward "the 1st time doesn't work that great
with me" instead of just moving on — and that was the right call. The revision pass (simpler
analogy table, real `curl -v` tests to actually *see* refused vs. no-route vs. timeout side by
side) made things land far better than the original faster-paced pass did, and the retest score
(82/100) proved it wasn't just a feeling. Real lesson to keep: speed and depth are a genuine
trade-off, not free — when something's rushed and it shows, saying so and looping back beats
pretending it's fine. Also good instinct catching "wait, aren't 127.0.0.1 and 0.0.0.0 both
non-private, so shouldn't they be public?" — a sharp question that surfaced a genuinely missing
third category (reserved/special addresses) rather than accepting an incomplete rule.

## Session 10 — 2026-07-16
First topic done outside WSL — deliberately practiced Git from Windows PowerShell/VS Code since
that's the actual real-world setup for GitHub work, and it paid off immediately (VS Code's
built-in merge-conflict UI made resolving a real conflict far more intuitive than manual markers
would have been). Genuinely good moment: the first attempt at engineering a merge conflict didn't
actually conflict, and instead of just being told why, worked through the reasoning myself for
why "branch then immediately merge" can never diverge, then correctly re-set up a real one
requiring edits on both sides after the branch point. That kind of self-correction stuck better
than if I'd just been handed the fix. Quiz went well, hands-on tied the best score so far (28/30).

## Session 11 — 2026-07-18 / 2026-07-19
Real mistake worth remembering long-term: resolved a cherry-pick conflict, ran `git add` and
`--continue`, assumed it was done — but the markers were still literally sitting in the file.
`git add` never actually checks your work — it just trusts you. Caught it by checking `cat`
afterward instead of assuming success, exactly the "verify, don't just trust" habit that's shown
up throughout the whole mission. Took two tries to actually clean it up properly, which was a little
frustrating but a good real lesson in itself. Also asked good clarifying questions on branching
strategies (the `develop`-branch confusion) instead of nodding along at 90% understanding — worth
remembering that pushing past "mostly gets it" is exactly what closes the last 10%. Good
perspective at the end too: didn't fixate on the score number itself, correctly saw it as
feedback on the session, not a verdict on the future — worth holding onto as topics get harder.

## Session 12 — 2026-07-19 / 2026-07-20
Genuinely great session to close out Phase 1 on — pushed back directly and correctly when the
quiz scoring felt unfair (treating a quick, confident follow-up on an already-comprehensive answer
the same as a real correction), and that pushback was right; revised the score up after actually
re-examining it honestly rather than defending the original number out of habit. Also gave clear,
direct feedback mid-session about not assuming outside tech knowledge (the "runner" explanation)
and about redacting the real employer name from the notebooks — both taken seriously and saved to
memory so they carry forward automatically, not just for today. The real GitHub discoveries
(branch protection silently not applying to admins, the self-approval block, linear history
actually restricting merge options) landed well specifically because they were hit firsthand
through genuine mistakes and curiosity, not just described. Phase 1 complete — good foundation
built across 8 topics before Docker/Kubernetes/CI-CD begins in Phase 2.

## Session 13 — 2026-07-20 / 2026-07-21
Docker Day 1 needed a genuinely slower pace than usual — asked twice to hold off on context until
basic terms landed one at a time on their own first (recipe-card analogy for image vs. container
is what made it click), and to get a same-day agenda up front before diving in. Both are now
standing habits going forward, not just for today. Best moment: getting a real `{"status":"ok"}`
from a browser hitting a container built from a Dockerfile written line by line, and then
independently reasoning through exit code 137 (128 + SIGKILL) using only Topic 2's signals
knowledge, without being told the formula first.

## Session 14 — 2026-07-21 / 2026-07-22
Docker Day 2 was the strongest independent hands-on session yet — self-caught a missing `COPY
app.py .` line, a real Python string-vs-boolean bug, and proved the cache-reorder fix with real
before/after build timings rather than taking it on faith. Topic 9 cleared, 86/100.

## Session 15 — 2026-07-22 / 2026-07-23
Docker networking finally made the default-bridge-vs-custom-network distinction click by actually
watching a real name-lookup error (`Name or service not known`) rather than just being told it
happens — that kind of "break it, then fix it" proof stuck harder than any explanation alone
would have. The 3-reserved-IPs puzzle on an empty bridge network (network address, gateway,
broadcast) was a genuinely good "wait, why" moment tied back to Topic 5's CIDR math. Needed the
teaching pace slowed down more than any topic so far — asked directly to be treated as a
total beginner with zero assumed background, and for a same-day agenda plus explicit
"shall I move on?" checkpoints before advancing. Volumes' core lesson (container storage
disappears without one) landed cleanly once proven hands-on with a real deleted container.

## Session 16 — 2026-07-23 / 2026-07-24
Best instinct of the topic: refusing to delete-and-hope when adding a volume to an existing
container, and instead insisting on a verified duplicate-then-swap approach — checked the new
container's mounts were correct before ever touching the original. Docker Compose landed well
once the YAML indentation rules were explained plainly rather than assumed, and seeing Compose
auto-recreate a container whose config changed (echoing the exact "mounts are locked at
creation" rule learned hours earlier) was a genuinely satisfying connection to make independently.
Quiz passed cleanly, all 5 answers correct. Topic 10 cleared, 92/100 — Phase 2 continuing well.

<!-- Copy the block above for each new session -->
