# Techniques: when to use which

A decision guide for picking the right elicitation technique in the moment.

## Technique selection cheat sheet

| Situation | Use this technique | Why |
|---|---|---|
| The work touches a system or document | **Artifact reaction** — ask the SME to paste a recent real example and explain why each part is the way it is | Concrete artifacts force articulation of implicit quality standards |
| The SME is generalizing ("usually I…", "it depends") | **Critical Incident Technique** — "Tell me about the last specific time" | Memory is far more reliable for episodes than abstractions |
| The step looks judgment-heavy ("I just know…") | **Critical Decision Method** — pick a recent complex case and walk it backward | Recency bias works for you; the actual decision path emerges, not the sanitized version |
| You suspect a step has hidden cognition | **ACTA Knowledge-Audit probes** — *Noticing*, *Anomalies*, *Job Smarts*, *Improvising* | Reliably surfaces expert cognition that isn't visible in the work product |
| The SME describes a deterministic procedure but you suspect exceptions | **Edge-case probes** — "what's the weirdest version", "what breaks this" | Experts find it easier to articulate failure than success |
| The official process doesn't match observed behavior | **Workaround probes** — "where does the official process not match" | Surfaces unwritten rules that are load-bearing in real operations |
| You want to test their criteria, not their narrative | **Simulation probes** — present a present-tense scenario and drip-feed complications | Activates procedural memory in a way abstract questions can't |
| The SME has chunked too much into "obvious" | **New-hire framing** — "what would a new hire get wrong here" | Experts can articulate what others get wrong more easily than what they get right |
| You want to drill to the *why* of a rule | **Lateral 5-Whys** — branch when needed, avoid accusatory tone | Distinguishes load-bearing rules from cargo-cult ones |

## Show, don't tell — adapted for text

The original technique relies on screen-share and live observation. In text, approximate it by:

1. Asking the SME to **paste a recent real artifact** (ticket, email, report, screenshot description, command transcript).
2. Asking them to **narrate what they would do, in present tense, with that artifact open** — e.g., "you've got this ticket open right now; what's your first move?"
3. Asking them to **describe what they're looking at on the screen** at each step — even details that feel obvious. "What field do your eyes go to first?"

When the SME goes silent or skips ahead, prompt: *"What did you just check between those two steps?"*

## Critical Incident Technique (Flanagan)

Ask for *specific, recent, concrete events* — not generalizations.

**Recipe:**
1. "Tell me about the last time this process went really smoothly."
2. "Now tell me about the last time it went sideways."
3. Probe both — successes reveal the heuristics, failures reveal the constraints and the recovery patterns.

**Pitfall:** the SME starts generalizing again ("usually what happens is…"). Re-anchor immediately: *"Sorry — pull me back to that specific case last Tuesday. What did *you* do next?"*

## Critical Decision Method (Klein/Crandall)

A four-pass technique adapted for a text interview:

1. **Pass 1 — Incident identification.** "Pick a recent case where you had to think hard. What was it?"
2. **Pass 2 — Timeline construction.** "Walk me through what happened, in order, from start to finish."
3. **Pass 3 — Deepening.** Walk it again, slower. At each decision point, ask: "What were you weighing? What other options were on the table? What told you to go this way?"
4. **Pass 4 — What-if probes.** "If you'd missed cue X, what would have happened? If you were less experienced, what would you have done?"

CDM is heavy. Use it on the 1–2 most cognitively demanding steps in the process, not on every step.

## Knowledge Audit (ACTA)

A lighter-weight ACTA technique. Pick 2–3 of the seven probe categories per deep-dive step (see `question-bank.md`):

- *Past & Future, Big Picture, Noticing, Job Smarts, Improvising, Self-Monitoring, Anomalies.*

Don't ask all seven. Pick the categories that match the step. *Noticing* and *Anomalies* are especially valuable for monitoring/detection work. *Improvising* and *Job Smarts* are valuable for execution work where the SME has clearly developed personal optimizations.

## Simulation / scenario probes

Present a realistic situation in present tense, then drip-feed complications.

**Recipe:**
1. "You just got an email from a customer saying X. Walk me through what you do in the next 30 minutes."
2. Once the SME starts answering, complicate: *"Now you discover Y is also true. What changes?"*
3. Complicate again: *"And the relevant person is on PTO. What do you do?"*

This activates procedural memory in a way abstract questions can't, and it surfaces decision branches that the SME wouldn't have brought up unprompted.

## Vague-language flags

Words that indicate hidden behavior — *check, ensure, validate, normally, usually, sometimes, it depends, basically, just, obvious, good, wrong* — each deserve an immediate, specific follow-up. The full table of flags and probes lives in **`active-listening.md` → Vague-language pouncing**; treat that file as canonical and reach for it on every turn.

## Decision-fork dissection

Every fork in the process is a decision. The interview job is to convert *"it depends"* into an explicit rule. At every fork, in order:

1. **Name the fork.** "So at this step you can either A or B. Right?"
2. **Probe criteria.** "What would have to be true for you to do A?"
3. **Probe boundaries.** "Walk me through the borderline case — where it could have gone either way."
4. **Probe exceptions.** "Is there a case where neither A nor B applies, and you do something else?"
5. **Synthesize.** "So the rule is: A if X; B if Y; escalate if Z. Right?" Wait for correction.

If the SME pushes back on writing the rule down ("you can't really make a rule out of it"), that's a signal that the step is a deep-dive target — keep probing with CDM and CIT until enough cases emerge to extract a pattern. If a clean rule still doesn't emerge, capture it in the *Cognitive Demands Table* as a judgment-heavy step rather than forcing a false rule into the SOP.

## Lateral Five Whys

Use to drill from a surface step to the underlying reason. **Branch when needed.** Avoid an accusatory tone — *"What led to that?"* lands better than *"Why did you do that?"*

**Pattern:**
- "Why do you copy that field into the spreadsheet?"
- → "Because finance needs it in that format."
- "Why that format?"
- → "Because their old system can't read CSV."
- (Stop when "why" yields no new information.)

**Branch when needed:** if a step has multiple drivers, the linear five-whys misses the others. Follow the strongest driver first, then return to the others.

**Don't use as interrogation.** Reframe each "why" as a curiosity question. The SME should feel investigated *with*, not *at*.

## Picking sequencing strategy

For Phase 3 (orientation → deep dives), the sequencing strategy shapes the rest of the interview.

| Strategy | Best for | First question |
|---|---|---|
| **Chronological / day-in-the-life** | Daily/weekly operational rhythms | "Walk me through a typical Tuesday — what's the first thing you do?" |
| **By process area** | Roles with multiple distinct workflows | "What are the main types of work you do? Pick one and we'll start there." |
| **By frequency** | Roles where 80% of work is routine + 20% is rare-but-critical | "What's the work you do most days? Let's start with the common path, then handle the rare cases." |
| **By artifact** | Any work that produces a clear output | "Open a recent finished output. We'll walk through *why* each part of it looks the way it does." |

**Default:** propose *by artifact* first. It is the highest-yield because it anchors abstract reasoning to concrete decisions. Only switch to another strategy if the work doesn't produce a clean artifact (e.g., a relationship-management role).

## When to switch techniques mid-step

Watch for these signals and switch:

- SME is generalizing → switch to **CIT**.
- SME is reciting the official version → switch to **artifact reaction** or **CDM**.
- SME is fluent and surface-level → switch to **ACTA Noticing/Anomalies probes** to surface hidden cognition.
- SME hits "you just know" → switch to **new-hire framing** + **CDM**.
- SME's answers shorten or vague language increases → end the session, schedule the next.
