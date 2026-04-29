# Active Listening Discipline

The interview habits that separate a good elicitation from a meandering one. Apply every turn.

## The single-question rule

In a text interview, ask **one question per turn**. The SME can only answer one well. Bundling 4 questions produces shallow answers to all 4 — usually only the easiest one is answered fully. Save follow-ups for subsequent turns.

If multiple questions are urgent, list them as a parking lot in the working file ("I want to come back to X and Y"), then ask the highest-value one now.

## Silence — the text equivalent

Journalists call this the three-second rule: after the SME finishes a thought, wait. They almost always add the most valuable detail in the second pass.

Text equivalent: when the SME's answer feels complete but a bit thin, **don't immediately pile on a new question**. Acknowledge briefly and ask a single focused follow-up that invites them to keep going:

- "Got it. What else was happening at that moment?"
- "That makes sense. Anything you almost said and held back?"
- "That tracks. What were you watching for next?"

These are *invitations*, not new topics. They give the SME room to add the second-pass detail.

## Paraphrase to confirm — the *interpretation* principle (Beyer & Holtzblatt)

Build a model out loud and let them correct it.

**Pattern:**
- "So what I'm hearing is — you check the dashboard first, and only if X is above threshold do you escalate. Is that right?"
- "Let me make sure I have it: the rule is A if condition X, B if condition Y. Anything missing?"

**The corrections are gold.** *"No, that's not quite right…"* surfaces precision the SME wouldn't have volunteered. Wait for the correction; don't smooth it over.

**Pitfall:** don't paraphrase in a way that smooths over inconsistencies. If the SME said two contradictory things, surface the contradiction: *"Earlier you said A always happens before B. Just now it sounded like sometimes B comes first. Which is it?"*

## Vague-language pouncing

Words that flag hidden behavior. Pounce immediately — don't let them pass.

| Vague language | Probe |
|---|---|
| **check / verify / validate / make sure** | "What *exactly* do you check for? What does pass-vs-fail look like?" |
| **review** | "Walk me through one specific review you did recently — what were you looking for?" |
| **ensure** | "How do you know it's actually ensured? What's the test?" |
| **normally / usually** | "Usually meaning how often? And what's the exception?" |
| **sometimes** | "Sometimes meaning how often? Give me a recent example." |
| **it depends** | "What does it depend on? Give me three examples that went different ways." |
| **basically / kind of / more or less** | "Drop the qualifier — what's the precise version?" |
| **just** | "When you say 'just' — slow that down. What are the actual steps?" |
| **obvious / you just know** | "Pretend I'm replacing you in three months. What do I need to see to 'just know' it?" |
| **good / right / clean** | "What makes it good? Give me a specific quality I could measure or check." |
| **wrong / off / weird** | "What specifically tells you it's off? What are you comparing it to?" |

## Convert abstractions to examples

Every generalization gets met with: *"Can you give me a recent specific example?"*

Without exception. The pattern is:

1. SME says: "Usually I check the system before I respond."
2. Claude: "Walk me through one recent specific time you did that. What did you check for?"

Generalizations are how SMEs paraphrase their own work. Examples are how they *do* their work. Always pull them back to the example.

## Don't lead

Avoid questions that imply an answer. The SME will accommodate.

| Leading | Open |
|---|---|
| "So you just hit approve, right?" | "What do you do next?" |
| "And you'd escalate if X happens?" | "When does this go to someone else?" |
| "You wouldn't normally need to check Y, right?" | "What do you check before you commit?" |
| "That's the only exception, isn't it?" | "What other exceptions have come up?" |

The cost of leading is invisible: the SME confirms the prior assumption, and the rest goes unsaid.

## Refuse "it's obvious"

This is the single most important moment in the interview. When the SME says *"it's obvious"* or *"you just know"*, do not let it pass.

**Stock response:**
> *"Pretend I'm the person replacing you in three months. What do I need to see, hear, or check to 'just know' it?"*

Alternate forms:

- "What's the cue you're using that you've stopped noticing you're using?"
- "If a new hire watched you for a week, what would they have to internalize before they could do this without you?"
- "Walk me through three cases where 'just knowing' kicked in. What was the pattern?"

## Watch for jumps

Glossed-over steps hide micro-procedures. *"Then I run the report"* — between *what* and *run*, there are usually 6 sub-steps.

**Pattern:** any time the SME compresses a step, slow them down:

- "Before you run it, what happens between *finished entering data* and *clicking run*?"
- "You said 'pull the data and submit.' Walk me through the *pull* part — what tool, what query, what do you check before submitting?"
- "There's a gap between step 3 and step 4 — what fills that gap?"

If the answer is short, the gap is large.

## Track open threads — the parking lot

Maintain a visible parking lot in the working file. Every deferred question gets written down immediately, then signaled to the SME:

> *"I'm parking that one for later — it's on the list. We'll come back to it before we wrap."*

This does three things:
1. The SME knows nothing is being lost.
2. The thread isn't forgotten.
3. The current line of inquiry can be followed without anxiety about losing the parked thread.

At the end of each session, **walk the parking lot**. Anything still unresolved becomes `[GAP]` or `[CONFIRM]` in the working file.

## Dig-cues — when to push

Dig harder when one of these signals appears:

- **The answer is shorter than expected.** Short answer = compressed cognition. Slow them down.
- **The SME laughs or sighs** ("oh, that's a whole thing…"). Translation: *there's a story here I haven't told.* Pull on it.
- **Body language shifts.** In text, the equivalent is tonal — defensiveness, hedging, excessive qualification. Note it and probe.
- **The answer contradicts something they said earlier.** Surface the contradiction directly, gently.
- **The SME volunteers a story unprompted.** Stories carry expert cognition. Let them finish, then probe for the decision logic.
- **The SME uses "the" instead of "a"** for something not yet established. *"Then I open the dashboard"* — *which* dashboard? When did *the* dashboard become a defined thing?

## When to stop a session

Cognitive fatigue degrades elicitation quality fast. End the session when:

- The SME's answers shorten without depth.
- Vague language increases ("usually", "kind of", "sometimes" appearing more than at the start).
- The SME starts volunteering "I think" instead of "I do".
- The SME asks how much longer.
- The probing itself starts getting weaker — shorter follow-ups, accepting "yeah basically" without dissecting it.

End cleanly: thank the SME, summarize what's parked for next time, confirm the next session, save the working file.

## Anti-pattern detection

Audit interviewer behavior for these warning signs:

- **Talking more than the SME.** The SME should be doing 70%+ of the talking.
- **Paraphrasing without confirming.** Always close paraphrases with *"is that right?"*
- **Accepting "it depends" without follow-up.** Every *"it depends"* is a missed decision rule.
- **Asking questions whose answers are already known.** Wastes time and signals to the SME that the interview is performative.
- **Skipping discomfort.** When the SME hesitates, sighs, or qualifies, that's the moment to dig — not the moment to move on.
