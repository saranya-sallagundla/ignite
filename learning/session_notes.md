# Session notes (personal recap)

> Not used for logic — this file is for your own review.
> Dates are IST (UTC+5:30), format YYYY-MM-DD. After each session, 2-4 lines: what happened,
> what was hard, what to remember.

## Session 1 — 2026-07-06
VM vs container took two full passes to actually click — first explanation didn't land, the
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
words-on-a-line instead of whole-lines — both cleared up fast once tested directly rather than
just re-explained. Good habit forming: testing predictions against real output before trusting an
assumption, instead of just accepting the first plausible-sounding answer.

## Session 4 — 2026-07-09
Said out loud "I'm not able to remember everything" partway through a dense command-heavy
session — worth remembering that's a normal reaction to volume, not a sign of falling behind;
the notebook exists precisely so memorization isn't the job right now, repetition across future
topics is. The ping-vs-curl discovery (ICMP allowed, TCP blocked on the same network) was the
best moment of the day — genuinely surprised me and then made complete sense once explained,
which is a better kind of learning than being told a fact upfront. Quiz was noticeably shakier on
exact syntax (grep -r flag placement, find scope) than Topic 1's quiz — watch whether that's
fatigue from the length of the session or a real gap to reinforce next time shell commands come up.

## Session 5 — 2026-07-10
`classify.sh` was a genuine grind — real, distinct syntax mistakes one after another (else/fi
separators, merged blocks, then a nano-vs-printf `\n` mixup that broke everything in a confusing
new way). Kept wanting to just be handed the answer partway through, but pushing through to write
it myself paid off — the final self-debugged syntax error (fixed by reading the line number bash
pointed to) felt like the first "real" debugging moment of this whole plan, not a guided exercise.
Worth remembering next time something feels this frustrating: it's often exactly the sign that
real learning is happening, not that something's wrong.

## Session 6 — 2026-07-11 / 2026-07-12
First real quiz miss of the whole program — function scoping genuinely didn't land on attempt 1,
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

<!-- Copy the block above for each new session -->
