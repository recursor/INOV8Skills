---
name: inov8-orthopedics-design
description: This skill should be used when the user wants to design, prototype, or build anything branded for INOV8 Orthopedics or INOV8 Surgical (Houston, TX), such as a web page, slide, mock, email, form, dashboard, or production UI. Triggers on phrases like "INOV8 branding", "make this look like INOV8", "INOV8 design system", "INOV8 colors", "INOV8 Orthopedics page", "use our brand", or any request for INOV8-branded output. Fetches the INOV8 Orthopedics design system from the public recursor/Design repository, reads its brand book and tokens, and enforces the brand's hard rules while designing.
version: 0.1.0
---

# INOV8 Orthopedics design

Design with the INOV8 Orthopedics design system rather than from memory. The system lives in the public repository `recursor/Design` under `systems/inov8-orthopedics/`; this skill fetches it and follows its own `SKILL.md`.

## Step 1 — Get the system

Check for an existing checkout first: a directory named `Design` beside the current project, or any path the user names. Otherwise clone it into a scratch location:

```bash
git clone --depth 1 https://github.com/recursor/Design.git <scratch>/Design
```

If cloning is impossible (no network, no git), fetch the two files that matter most directly:

```bash
curl -sL https://raw.githubusercontent.com/recursor/Design/main/systems/inov8-orthopedics/README.md
curl -sL https://raw.githubusercontent.com/recursor/Design/main/systems/inov8-orthopedics/tokens.css
```

If neither works, say so, then design from the hard rules in Step 3 only and tell the user the token values were not loaded.

## Step 2 — Read the system's own skill

Open `systems/inov8-orthopedics/SKILL.md` in the checkout and follow it. It names the reading order (brand book, `tokens.css`, `tokens.json`, the `api/` cards, the component previews), the working method for mocks versus production code, and the open substitutions to flag. Everything below is a fallback summary, not a replacement.

## Step 3 — Hard rules (fallback summary)

- Write the brand name as **INOV8**: all caps, the digit 8, no space, no hyphen.
- Sentence case for headlines, buttons, navigation, and labels. No exclamation marks, no emoji, no urgency marketing.
- "We" for the practice, "you / your" for the patient. Never "I".
- Specialties in this order: Hip, Knee, Shoulder, Elbow, Sports Medicine, Physical Therapy.
- The brand gradient (teal to navy) is for the wordmark, hero accents, and the 4 px divider rule only. Never as a CTA fill, never behind body text.
- Primary CTA and accent: cyan `#00A9D2` (`--cyan-500`). Dark surfaces: navy `#20265A` (`--navy-900`).
- Display headings in Jost Light (300); never bold or black weights for display. Body in DM Sans.
- Cards and buttons at 10 px radius, chips and the primary CTA pill-shaped. Shadows soft and navy-tinted, never pure black. Never remove focus rings.
- Icons are Lucide, 1.5 px stroke. Photography over illustration. Flat backgrounds.

## Step 4 — Produce the work

Use the token variables and component classes from the checkout, never retyped values. For mocks, produce one self-contained HTML file with `tokens.css` inlined and the logo embedded as a data URI. For production code, copy `tokens.css` and `components/bundle.css` into the project and reference them. When the user gives no brief, ask what they want to build, who will see it, and whether it is a mock or production work.

## Keeping this skill in sync

The hard rules above mirror `systems/inov8-orthopedics/SKILL.md` in `recursor/Design`. When that file or the system's README changes a rule, a token name, or a file path named here, update this skill and bump its version in the three places this repo's `CLAUDE.md` lists.
