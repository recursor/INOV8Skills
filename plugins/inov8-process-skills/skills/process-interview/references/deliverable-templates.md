# Deliverable Templates

Output structures for each artifact type the skill can produce. Use these for the final draft in Phase 6 — Synthesis. Tailor depth to the audience identified in Phase 1.

Every template preserves `[GAP]` and `[CONFIRM]` markers so reviewers can see unresolved points.

## SOP (Standard Operating Procedure) — default

**When to use:** routine procedural work where the audience needs to perform the steps reliably. Default deliverable when the user has no preference.

**Structure:**

```markdown
# SOP: <Process Name>

**Purpose:** <one-sentence statement of what this process accomplishes and why>
**Audience:** <novice replacement / peer cross-training / auditor / etc.>
**Owner:** <name or role>
**Last reviewed:** <YYYY-MM-DD>
**Next review due:** <YYYY-MM-DD, 6–12 months out>

## When to use this SOP
- Trigger / input that starts the process
- When NOT to use this (other workflows that look similar)

## Prerequisites
- Access required (systems, permissions)
- Tools / software
- Information you need on hand before starting

## Procedure

### Step 1: <Verb-first action title>
**Trigger:** <what kicks this step off>
**Action:** <what the operator does, click-by-click if relevant>
**Tool/system:** <where this happens>
**Decision criteria:** <if there's a fork, what determines the path>
**Output:** <what this step produces>
**How you know it's done right:** <the check before moving on>

### Step 2: ...

(repeat per step)

## Decisions & Heuristics
| At step | If… | Then… | Otherwise… |
|---|---|---|---|
| 2 | amount > $500 | escalate to manager | proceed to step 3 |
| ... | ... | ... | ... |

## Exceptions & Edge Cases
- **<Exception name>**: when it occurs, what to do, who to contact
- ...

## Workarounds & Unwritten Rules
- <Rule that isn't in the official procedure but is load-bearing>
- ...

## Tools & Systems
- <System name>: <what it's for, where to log in, who owns it>

## Glossary
- <Term>: <definition>

## Cognitive Demands Table
*(See separate appendix or sub-page — one row per judgment-heavy step)*

## Gaps to Confirm
- [GAP] <unresolved point with context>
- [CONFIRM] <answer to verify with another SME or via observation>
```

## Runbook (operational / incident-response style)

**When to use:** time-sensitive operational work where the operator needs to act quickly under pressure. The reader is on the clock; structure matters more than narrative.

**Structure:**

```markdown
# Runbook: <Trigger / Alert / Scenario>

**Severity / SLA:** <p1/p2/p3, response time>
**On-call:** <role or rotation>
**Escalation path:** <who to ping, in order>

## Trigger
- What signal opens this runbook (alert, ticket, customer message)

## Initial assessment (first 5 minutes)
1. Check <X>
2. Check <Y>
3. If <Z>, jump to "Major incident" section below

## Diagnosis tree
- Symptom A → likely cause → fix path
- Symptom B → likely cause → fix path

## Common fixes
### Fix 1: <name>
- When to apply: <criteria>
- Steps: …
- Verification: …

## Escalation
- When to escalate: <criteria>
- Who to ping: <roles>
- What to include in the page: <data points>

## Post-incident
- Required follow-ups (ticket close, customer comms, postmortem trigger)

## Known gotchas
- <gotcha that has bitten people before>

## Gaps to Confirm
- [GAP] ...
```

## Decision flowchart

**When to use:** judgment-heavy work where "it depends" is the dominant mode and a flat SOP would lose the structure.

**Structure (Mermaid + commentary):**

```markdown
# Decision Flowchart: <Process Name>

**Purpose:** <what decision this chart resolves>
**Use when:** <triggering context>

## Flowchart

\`\`\`mermaid
flowchart TD
    Start([Trigger: <what starts the process>]) --> Q1{<First decision>}
    Q1 -->|Yes| Q2{<Second decision>}
    Q1 -->|No| A1[<Action A>]
    Q2 -->|Yes| A2[<Action B>]
    Q2 -->|No| Q3{<Third decision>}
    Q3 -->|Yes| A3[<Escalate to person X>]
    Q3 -->|No| A4[<Default action>]
\`\`\`

## Decision criteria
- **Q1:** <what you're looking at to answer this>
- **Q2:** <what you're looking at>
- **Q3:** <what you're looking at>

## Action notes
- **A1:** <details, including who, where, common pitfalls>
- **A2:** ...

## Gaps to Confirm
- [GAP] ...
```

## Mistake-prevention checklist

**When to use:** the audience already knows the process at a high level; the goal is to prevent the specific mistakes that experts have learned to avoid. Derived from the *"what new hires get wrong"* probes.

**Structure:**

```markdown
# Mistake-Prevention Checklist: <Process Name>

Use before <triggering moment, e.g., "before submitting", "before close of business Friday">.

## Critical checks (must pass)
- [ ] **<Check title>**: <what specifically to verify, why it matters, common failure>
- [ ] **<Check title>**: ...

## Common mistakes new hires make
1. **<Mistake name>**: <what it looks like, how to avoid it, how to recover if it happens>
2. ...

## Pre-flight checks for special cases
### Month-end / quarter-close
- [ ] ...

### Escalations
- [ ] ...

## Gaps to Confirm
- [GAP] ...
```

## Cognitive Demands Table (ACTA)

**When to use:** as a standalone deliverable for training material, or as an appendix/sub-page to an SOP or runbook. Captures the *judgment layer* that procedural documentation misses.

**Structure:** one row per cognitively difficult step.

```markdown
# Cognitive Demands Table: <Process Name>

| Step | Why it's difficult | Cues experts rely on | Common errors | Strategies |
|---|---|---|---|---|
| <Step name> | <what makes it hard — ambiguity, time pressure, conflicting signals, etc.> | <what the SME looks at, listens for, or checks — including the implicit ones> | <what new hires consistently get wrong, and how the error manifests> | <how the expert handles it — the heuristic, the workaround, the escalation rule> |
| ... | ... | ... | ... | ... |
```

**Rule:** include only the steps that are genuinely judgment-heavy. A 30-row table is a sign you're including procedural steps that belong in the SOP. Aim for 3–8 rows.

## Training module / course

**When to use:** the deliverable will be used to onboard a new practitioner, not just reference material. Combines an SOP with the judgment layer and learning checks.

**Structure:**

```markdown
# Training Module: <Process Name>

**Estimated time:** <hours>
**Prerequisites:** <prior training, access, mental models>
**Learning outcomes:** by the end, the trainee can…
- <outcome 1>
- <outcome 2>

## Section 1: Why this process matters
- Business context, downstream impact, why it exists

## Section 2: The procedure
*(Full SOP — see SOP template above)*

## Section 3: The judgment layer
*(Cognitive Demands Table — see template above)*

## Section 4: Practice scenarios
### Scenario 1 (routine case)
- Setup: <description>
- Question: what do you do? Why?
- Discussion / answer key

### Scenario 2 (edge case)
- ...

### Scenario 3 (failure mode)
- ...

## Section 5: Self-check
- [ ] I can perform the routine path without referring to documentation.
- [ ] I can identify the 3 most common ways this goes wrong, and how to recover.
- [ ] I know who to escalate to, and when.
- [ ] I know the 'gotchas' that bit experienced practitioners.

## Section 6: Reference
- Link to SOP / runbook / decision flowchart
- Glossary
- Tooling cheat sheet

## Gaps to Confirm
- [GAP] ...
```

## Notion-specific formatting tips

When writing to Notion (preferred), translate the markdown structure as follows:

- Top-level page: the process name.
- H2 sections become **toggle blocks** for collapsibility on long pages.
- Decisions tables become **databases** when there are many rows; otherwise inline tables.
- Cognitive Demands Table: separate sub-page so it can be linked and updated independently.
- `[GAP]` / `[CONFIRM]` markers: highlight in yellow/red callout blocks so reviewers can see them at a glance.
- Append a **Comments / Validation** section at the end for the playback session.

## Local markdown formatting tips

When writing to a local file (fallback):

- Single file per process.
- Filename: `<process-name>.md` (kebab-case).
- Include a `## Change log` section at the bottom with date + author + summary of edits.
- Mermaid blocks render in GitHub and most markdown viewers — prefer Mermaid for flowcharts.
