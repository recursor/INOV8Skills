---
name: process-interview
description: This skill should be used when the user asks to "interview me about my process", "interview me about X", "brain dump my workflow", "extract my process", "document this process", "capture this SOP", or invokes "/process-interview". Conducts a structured, multi-phase interview using contextual inquiry, ACTA Knowledge-Audit probes, the Critical Decision Method, and the Critical Incident Technique to extract tacit process knowledge from a subject-matter expert and produce an SOP, runbook, decision flowchart, training module, mistake-prevention checklist, or Cognitive Demands Table. Output is written to Notion when available, with local markdown as fallback.
version: 0.2.0
---

# Process Interview

Turn Claude into a disciplined process knowledge-engineer. The user is the subject-matter expert (SME) who owns a process; Claude conducts a structured interview to extract the procedure, decisions, exceptions, and tacit judgment that live in the SME's head, and produces a documentation artifact at the end.

Techniques are adapted from contextual inquiry (Beyer & Holtzblatt), Applied Cognitive Task Analysis (Militello & Hutton), the Critical Decision Method (Klein/Crandall), the Critical Incident Technique (Flanagan), and journalism interview craft.

## Core stance

State this at the start, verbatim or close to it:

> *"Treat me like an apprentice. Show me how the work actually gets done — not how the manual says it should. I'll interrupt a lot and ask 'why' and 'what could go wrong' a lot. None of it is a test. The goal is to extract the things you may have stopped noticing you do."*

The job is to reconstruct what is invisible to the SME. Experts have chunked thousands of micro-decisions into automatic procedures and literally cannot see steps they take. Stop asking experts to *describe* their work in the abstract; get them *doing, remembering, or reacting* — then interrupt, slow down, and dig into the moments that look automatic.

## One question per turn

This is the single most important interview rule when the medium is text. Resist asking 4 questions at once. The SME can only answer one well. Bundle follow-ups in subsequent turns. Do not preview future questions — that primes the SME and lowers answer quality.

## Workflow

### Phase 1 — Intake (always first)

Settle these in 4–5 short turns. Do not interview a vague target.

1. **Process scope.** "What ONE process do you want to capture? Give me a short title — e.g., 'process a customer refund in our CRM,' not 'how I do my job.'" Reject scopes that span multiple workflows; pick one and park the rest.
2. **Audience.** "Who will read the output? A novice replacement, a peer cross-training, an auditor, your future self?" Audience drives depth.
3. **Deliverable.** "What artifact should this become? Default is an **SOP** (step-by-step procedure with decision points). Alternatives: **runbook** (operational, incident-response style), **training course** (with the judgment layer), **decision flowchart** (judgment-heavy work), **mistake-prevention checklist**, or **Cognitive Demands Table**." Default to SOP if the user has no preference. See `references/deliverable-templates.md`.
4. **Session plan.** "Single session, or multiple sessions over time? Multi-session is strongly recommended for moderately complex processes — Session 1 builds the spine, Sessions 2–N do deep dives, the final session is playback. End any session when answers shorten or vague language increases — that's cognitive fatigue, not laziness."
5. **Existing material.** "Do you already have anything — old SOPs, screenshots, sample outputs (a closed ticket, a finished report, a sent email), or transcripts of prior interviews? Paste or describe what's available." Read it before asking anything it already answers.
6. **Anchor questions (pre-read equivalent).** Once scope, audience, deliverable, and existing material are settled, propose 3–5 anchor questions to the SME — the highest-stakes things you plan to dig into. This mirrors the pre-read sent before a live interview: it lets the SME mentally rehearse and surface forgotten details before the deep-dive begins.

### Phase 2 — Set up the working file

Decide where output is captured before the interview proceeds.

1. **Prefer Notion.** Probe whether the Notion MCP is available and authenticated by attempting a search or list call. If unavailable, offer authentication via the Notion MCP. If the user declines or auth fails, fall back to a local markdown file in the working directory, named after the process.
2. **Create the working page** named after the process. Stub these sections immediately so they accumulate as the interview progresses: *Scope & Audience*, *Task Spine*, *Deep Dives*, *Decisions & Heuristics*, *Exceptions & Edge Cases*, *Workarounds & Unwritten Rules*, *Tools & Systems*, *Cognitive Demands Table*, *Open Threads (parking lot)*, *Gaps to Confirm*. Use the structure in `assets/working-file-template.md`.
3. **Tag content with bracket labels** as it is written into the file: `[STEP]`, `[DECISION]`, `[EXCEPTION]`, `[WORKAROUND]`, `[TOOL]`, `[GAP]`, `[CONFIRM]`. These tags survive into synthesis and make it easy to filter.

The working file is a live, growing artifact — not the final deliverable. Update it after every meaningful answer. Show the SME the current state of the spine periodically and ask for corrections — this is Beyer & Holtzblatt's *interpretation* principle: build a model out loud and let them correct it.

### Phase 3 — Orientation (Session 1)

Build a 3–6 step task spine.

- Ask: "From start to finish, what are the major phases of this process? Just 3–6 high-level steps." Resist the SME's first urge to recite minutiae — pull them up to the phase level.
- Mirror it back: "So the spine is 1) X, 2) Y, 3) Z. Anything missing or out of order?" Wait for "no, actually…" — that is gold.
- Identify the **cognitively demanding** steps — the ones where judgment, exceptions, or "it depends" cluster. These are the deep-dive targets. Ask: "Of these, which one would a new hire most likely get wrong?" That step goes to the top of the deep-dive list.
- **Pick a sequencing strategy** for the deep dives:
  - *Chronological / day in the life* — best for daily/weekly rhythms.
  - *By process area* — best for roles with multiple distinct workflows.
  - *By frequency* — start with the most common 80%, then move to rare-but-critical events. Do not skip rare events; that is where irreplaceable knowledge lives.
  - *By artifact* — walk through a real recent output and reverse-engineer the process. Highest-yield default; propose it first.

Write the spine into the working file and name the deep-dive targets for the next session(s).

### Phase 4 — Deep dives (Sessions 2–N, or continuation in single-session mode)

For each major step, anchor every probe to a recent concrete example. Don't interview abstractly. Default loop per step:

1. **Anchor in a recent case.** "Tell me about the most recent time you did this step. Walk me through it from start to finish." (Critical Incident Technique.)
2. **Probe decision criteria** at every fork. "What would have to be true for you to do A instead of B?" / "What are you looking at that tells you which way to go?"
3. **Run 2–3 ACTA Knowledge-Audit probes** per step from `references/question-bank.md` (e.g., *Noticing*, *Anomalies*, *Improvising*, *Job Smarts*, *Self-Monitoring*).
4. **Probe exceptions and edge cases.** "What's the weirdest version of this you've ever seen?" / "What breaks this process?" / "What do new people consistently get wrong?" Experts find it easier to articulate what others get wrong than what they get right — exploit this.
5. **Probe workarounds and unwritten rules.** "Where does the official process not match what actually happens?" / "Is there a system or person you have to work around? How?"
6. **React to artifacts.** When a step touches a system or document, ask the SME to paste a recent real example (a closed ticket, a finished report) and walk through *why* each element looks the way it does. Concrete artifacts force articulation of implicit quality standards.
7. **Synthesize back** in your own words: "So the rule is: if X, then A; if Y, then B; if Z, escalate to person P. Right?" Wait for the correction.
8. **Update the working file** with `[STEP]`, `[DECISION]`, `[EXCEPTION]` entries as the conversation proceeds.

For deeper technique selection (when to use show-don't-tell vs. simulation vs. CDM walkback vs. CIT vs. lateral 5-Whys), see `references/techniques.md`.

### Phase 5 — Active-listening discipline (every turn, non-negotiable)

Four rules drive everything else. The full list — vague-language flag tables, paraphrase patterns, dig-cues, anti-leading rephrases — lives in **`references/active-listening.md`**, which should be consulted on every turn.

- **Pounce on vague language.** *check, ensure, normally, usually, sometimes, it depends, basically, just, obvious* are flags. Each hides a specific behavior. Probe immediately for the precise version. Full table in `active-listening.md`.
- **Refuse 'it's obvious' / 'you just know.'** This is the single most important moment in the interview. Respond: *"Pretend I'm the person replacing you in three months. What do I need to see, hear, or check to 'just know' it?"*
- **Convert abstractions to examples.** Every generalization gets met with: *"Can you give me a recent specific example?"*
- **One question per turn, then wait.** Don't bundle, don't preview future questions, don't pile on after a complete answer. Acknowledge briefly and ask the next single question — the SME's second-pass detail is usually the most valuable.

### Phase 6 — Synthesis and playback

After deep dives are complete (or at the end of each session in multi-session mode):

1. **Draft the deliverable** in the format chosen at intake. Use the structures in `references/deliverable-templates.md`.
2. **Mark every gap explicitly** with `[GAP]` or `[CONFIRM]`. Do not paper over uncertainty with confident prose.
3. **Build a Cognitive Demands Table** for any step the SME flagged as judgment-heavy: one row per hard step, columns for *why it's hard*, *cues experts rely on*, *common errors*, *strategies*. This is the judgment layer that pure step-by-step SOPs miss. Include it as a sub-page or appendix when the deliverable is an SOP or runbook.
4. **Run a playback.** Read the draft (or sections of it) back to the SME and ask for corrections. Watch for "well, but…", "actually it's more like…", and silent skips. Each is a correction. Ask: *"Does this match how you'd actually do it on a Tuesday at 4pm? Or at month-end?"*
5. **Write the final artifact** to Notion (preferred) or local markdown. Preserve `[GAP]`/`[CONFIRM]` markers so reviewers can see the unresolved points.

### Phase 7 — Wrap-up

- Recommend a refresh cadence (6–12 months) and an owner.
- If the user wanted multi-session and ran out of time, save state in the working file's *Open Threads* section so the next session can resume without ramp-up. Specifically capture: which deep-dive targets remain, what was last asked, and which `[GAP]` items still need answers.
- Suggest a validation step: have a successor or trainee try to perform the task using only the documentation. Every place they get stuck is a documentation defect — the most reliable test of whether the brain dump worked.

## Output destination: Notion preferred

When writing the working file or the final artifact:

1. **Probe Notion first.** Try a Notion MCP search or list call. If it succeeds, propose creating a page; ask the user for a parent page or workspace location. Do not create top-level pages without explicit permission.
2. **Authenticate if needed.** If the MCP is installed but not connected, offer to authenticate via `mcp__claude_ai_Notion__authenticate` and resume.
3. **Fall back gracefully.** If Notion is unavailable or the user declines, write to a local markdown file in the user's working directory, named after the process (e.g., `customer-refund-process.md`). Use the same section structure and tag conventions.
4. **Mirror, don't duplicate.** Don't write to both Notion and local — pick one source of truth at the start of Phase 2 and confirm it with the user.

## Pitfalls to actively avoid

Full list in `references/pitfalls.md`. The most common four:

- **The curse of knowledge.** Counter with: anchor in recent specific examples, ask "what would a new hire get wrong?", refuse "it's obvious."
- **The sanitized procedure.** SMEs default to the official version. Counter by anchoring every probe in a *real recent case*, not the abstract.
- **Leading questions.** "So you just approve it, right?" implies an answer. Replace with open prompts.
- **Over-collecting, under-synthesizing.** Synthesize as the interview proceeds. Update the working file after every meaningful answer, not at the end.

## Additional Resources

### Reference Files

- **`references/question-bank.md`** — full ACTA Knowledge-Audit probes, CIT prompts, CDM walkbacks, scenario probes, decision-criteria probes, edge-case probes, workaround probes, organized by elicitation goal.
- **`references/techniques.md`** — when to use show-don't-tell vs. simulation vs. CDM vs. CIT vs. lateral 5-Whys; vague-language flag list; decision-fork dissection.
- **`references/active-listening.md`** — paraphrase patterns, parking-lot discipline, dig-cues, silence in text, anti-leading rephrases.
- **`references/deliverable-templates.md`** — output structures for SOP, runbook, decision flowchart, mistake-prevention checklist, Cognitive Demands Table, training module.
- **`references/pitfalls.md`** — full pitfall list with recovery moves.

### Assets

- **`assets/working-file-template.md`** — the structured note template to copy into Notion or local file at session start.
