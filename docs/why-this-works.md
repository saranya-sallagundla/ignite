# Why this works

The Ignition Engine's rules look strict — same-session quizzes, a hard attempt limit, a ban on
repeating explanations, timestamps that can never be edited. None of them are arbitrary. Each
maps to something reasonably well-established about how people actually retain and transfer
skills. This page states the reasoning in plain language, rule by rule, and then — because this
repo does not do hype — states its limits.

## Testing is the teaching, not the measurement

**The rule:** every topic ends in a quiz the same session, and the quiz is open-ended — "walk me
through it" — never multiple choice.

**The reasoning:** retrieving something from memory strengthens it far more than re-reading it.
This is the *testing effect*, one of the most replicated findings in learning research (Roediger
and Karpicke's 2006 studies are the usual reference: students who practised recall outperformed
students who spent the same time re-studying, and the gap widened over time). Multiple choice
tests recognition; open-ended questioning tests *reconstruction*, which is what an interview, an
incident, or a 2 a.m. page actually demands. Practising in the format you will be tested in is
the whole reason the quizzes are conducted like interviews from day one — the six months of daily
quizzing double as six months of interview practice, instead of interview prep getting crammed at
the end against the clock.

**The honest trade-off:** research also shows *delayed* tests beat immediate ones for long-term
retention. Same-session testing is chosen anyway, deliberately: it guarantees the feedback loop
happens at all (a "quiz tomorrow" is the first thing a tired schedule drops), and it catches
misunderstandings before a night's sleep consolidates them. The spacing that immediate testing
gives up is bought back elsewhere — deferred-mastery revisits, later topics that force earlier
ones to be retrieved again, and the audits.

## Failed attempts must be taught differently

**The rule:** repeating an explanation across attempts is banned. Attempt 2 requires a different
explanation and analogy; attempt 3 requires decomposing the topic into its smallest parts and
confirming each alone.

**The reasoning:** if an explanation did not produce understanding, its repetition produces
familiarity instead — the feeling of knowing without the substance, which is the most expensive
failure mode in self-study because it goes undetected until an interview. A genuinely different
angle creates a second retrieval path to the same idea; the decomposition step on attempt 3 is
mastery learning's core move — find the exact sub-component that is broken instead of re-teaching
the whole, and rebuild from there. Mission #1 has a live example: Topic 3 failed on function
invocation, was re-taught through concrete line-by-line tracing instead of another analogy, and
passed a full fresh retest the same session.

## Deferral over denial

**The rule:** three failed attempts do not stall the mission and do not get waved through. The
topic is logged as *deferred mastery* with a hard revisit deadline — within three sessions, and
before anything that builds on it.

**The reasoning:** two failure modes kill six-month plans. Grinding on a stuck topic until morale
breaks is one; quietly moving on and letting the gap compound is the other. Deferral with a
deadline refuses both. The forced gap is also not dead time — returning to a topic after days
away is *spaced practice*, which reliably beats massed repetition, so the revisit tends to land
on more receptive ground than attempt 3 did. The deadline is what keeps this honest: without one,
"deferred" decays into "dropped."

## The failure stays visible

**The rule:** failed attempts are logged where they happened, scores are never revised, and the
lowest score in the repo stays on display.

**The reasoning:** partly record integrity — a log with no failures in it is indistinguishable
from a log that hides them, so visible failures are what make the successes worth believing. And
partly memory: errors that are confidently made and then clearly corrected are remembered
unusually well (the *hypercorrection effect*). The wrong answer, kept next to its correction, is
a better study artifact than the correction alone.

## One real system instead of disposable tutorials

**The rule:** if the mission defines a parallel project, hands-on work lands in it from Day 0 —
wherever a topic can advance the real system, it does.

**The reasoning:** skills transfer poorly out of the context they were learned in. A practice
folder that gets deleted teaches commands; a growing system teaches *consequences* — the Docker
build you optimise in week 4 is the same one your Kubernetes deployment pulls in week 8, so old
material keeps getting retrieved under new pressure. That accumulation is spaced practice again,
disguised as engineering. It also produces the artifact self-study usually lacks: something
demonstrable at the end that was genuinely built, not assembled for show in the final week.

## Escalating depth across multi-day topics

**The rule:** multi-day topics run from heavy scaffolding to independent work to a realistic
worst-case scenario — never the same difficulty twice.

**The reasoning:** support that fades as competence grows sits close to the edge of what the
learner can do — hard enough to force real processing, not so hard it just produces flailing.
Learning research calls difficulty of that kind *desirable* (Bjork's term): conditions that make
practice feel harder, like having support withdrawn, tend to improve retention even though they
feel worse than smooth practice in the moment. The final-day scenario also moves the material one
step closer to the format it will be needed in — production is a scenario, not a definition.

## A record that cannot be quietly edited

**The rule:** one commit per session, check-in/check-out timestamps never touched, the status
line overwritten but the log only appended, pacing recalculated against a baseline that never
changes.

**The reasoning:** this one is less about memory than about the psychology of long solo projects.
Every rule here removes a place where drift could hide: an editable timestamp invites rounding,
a flexible baseline makes "am I on track?" unanswerable, a batched commit blurs which session did
what. The engine assumes motivation will fluctuate over six months and makes the *record* bear
the discipline instead of the mood. Light days are legal and logged without interrogation — but
their pacing cost is stated out loud every time, so rest stays a choice rather than a leak.

## The limits, stated plainly

- **This is an n of 1.** The engine generalises one person's working protocol; mission #1 is its
  only completed-in-progress test. The research cited is real, but the specific combination here
  has not been studied.
- **The scores are self-assessed and AI-graded.** They are computed against a fixed rubric and
  are internally consistent, but nothing external validates them. They tell you which topics are
  shaky relative to the others; they are not a certification.
- **An AI examiner can be lenient.** Pushback on vague answers is in the protocol precisely
  because the failure mode of an agreeable examiner is passing you when it shouldn't. The rule
  helps; it does not make the risk zero.
- **The lab findings are about memory more than skill.** The testing effect and spacing
  literature mostly measures recall of studied material. Engineering skill involves recall plus
  judgment plus tooling fluency — the evidence supports the retention half of that; the rest
  rides on the project and the scenarios.
- **None of this replaces production experience.** It compresses the path to competence. The
  final artifact is a person who can reason out loud and a system they can defend — the engine
  makes no larger claim than that.
