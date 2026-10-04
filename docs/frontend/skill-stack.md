# Frontend Skill Stack

Design-governance record for the P-073 frontend. team-ai-kit is the source of truth for design skills, rules and (later) the design
system; P-073 only receives the shipped product. Set up 2026-10-03. No UI has been built from this stack yet.

Frontend surfaces in scope:

| # | Surface | Product spec today |
|---|---|---|
| 1 | Main Product / Story Landing Page | **Not in spec yet** — `docs/spec/20-ui.md` defines four demo screens only (see Security / Reproducibility Notes → open items) |
| 2 | Customer Experience (Chat khách, "Việc của tôi") | `docs/spec/20-ui.md`, `21-fe.md`, `rules/frontend/AGENTS.md` |
| 3 | CSKH / Customer-Service Employee Console | same |

## Installed Skills

All four are vendored into `team-ai-kit/skills/`, using the same convention as the kit's other external skills (`THIRD_PARTY.md`):
pinned commit, upstream text byte-identical under `references/`, `LICENSE` + `NOTICE.md`, and a thin team-rules wrapper as `SKILL.md`.

| Skill | Upstream source | Installed path (kit) | Exposed in P-073 as | Intended role |
|---|---|---|---|---|
| `taste-skill` | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) → `skills/taste-skill/` (install name `design-taste-frontend`, v2) | `skills/taste-skill/` | `.claude/skills/taste-skill/` | Visual art direction |
| `ui-ux-pro-max` | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) → `.claude/skills/ui-ux-pro-max/` | `skills/ui-ux-pro-max/` | `.claude/skills/ui-ux-pro-max/` | UX architecture, design-system generation |
| `emil-design-eng` | [emilkowalski/skill](https://github.com/emilkowalski/skill) → `skills/emil-design-eng/` | `skills/emil-design-eng/` | `.claude/skills/emil-design-eng/` | Motion |
| `web-design-guidelines` | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) → `skills/web-design-guidelines/` + rules from [vercel-labs/web-interface-guidelines](https://github.com/vercel-labs/web-interface-guidelines) `command.md` | `skills/web-design-guidelines/` | `.claude/skills/web-design-guidelines/` | Final UI audit |

Exposure to P-073 needs no new mechanism: the existing `install.sh` symlinks `team-ai-kit/skills/` →
`P-073/.claude/skills`, `.agents/skills`, `.github/skills`, hidden through `.git/info/exclude`, and `no_kit_files.py` blocks committing them.
After `git pull` of the kit, restart Claude Code to load the new skills (with `--copy` on Windows, re-run `install.sh` first).

Layout of each folder:

```
skills/<name>/
├─ SKILL.md                     team wrapper: Vietnamese description ("Dùng khi …"), precedence, overrides, must-not-control
├─ NOTICE.md                    source, commit, sha256, what changed, update procedure
├─ LICENSE                      upstream license, unchanged
└─ references/upstream-SKILL.md upstream SKILL.md, byte-identical (frontmatter kept, but not auto-loaded: not at folder root)
   (ui-ux-pro-max also: data/, scripts/*.py, references/{quick-reference,pro-rules}.md — unchanged)
   (web-design-guidelines also: references/command.md — the pinned rule set)
```

Existing frontend skills that stay in force, and sit **above** this stack as part of the internal design system:

- `add-frontend-screen`: build workflow and `references/taste-rules.md`, the team's 15 visual rules.
- `web-accessibility`: WCAG 2.2 audit.
- `playwright-cli`: visual self-check.

## Responsibilities

| Skill | Owns | Surfaces |
|---|---|---|
| `taste-skill` | Visual personality, typography direction, composition, visual density, design variance (the three dials `DESIGN_VARIANCE` / `MOTION_INTENSITY` / `VISUAL_DENSITY`), one-line "Design Read" | Landing: primary. Customer: limited, inside `taste-rules.md`. CSKH Console: **not used** (upstream itself excludes dashboards, data tables and multi-step product UI) |
| `ui-ux-pro-max` | Information architecture, product UX patterns, flows, responsive structure, design-system generation (`MASTER.md` + page overrides), component / system organisation | All three |
| `emil-design-eng` | Whether to animate, duration, easing, springs, transitions, scroll storytelling, motion review | All three, with intensity per surface: Landing per taste dial; Customer restrained (≤ ~250 ms); Console minimal |
| `web-design-guidelines` | Final audit: accessibility, semantic HTML, interaction quality, responsive issues, focus / keyboard, UI-level performance. Reports only | All three; pair with `web-accessibility` for full WCAG 2.2 + axe |

## Precedence Rules

```
1. Product requirements        spec 20-ui.md / 21-fe.md, task card, contracts/api.yaml, rules/frontend/AGENTS.md
2. Internal design system      add-frontend-screen/references/taste-rules.md, design-system/proactive-care/ (MASTER, tokens, pages/)
3. taste-skill                 visual direction
4. ui-ux-pro-max               product UX
5. emil-design-eng             motion
6. web-design-guidelines       final audit
```

- A higher level always wins. A lower skill may *propose* a change to a higher level, but only through a card or PR that a human approves, never in place.
- No skill may silently override product requirements. When a skill's advice is dropped, the agent says which advice and which higher rule won.
- Upstream content inside a skill folder ranks below that folder's wrapper `SKILL.md`, which records the team overrides.
- When `web-design-guidelines` flags something that a higher level decided on purpose, it reports `theo thiết kế (<source>)` ("by design (<source>)") rather than an error.
- Every wrapper repeats the chain, and so does `rules/frontend/AGENTS.md` (one line), so the rule is visible wherever an agent starts.

## Installation / Version Information

| Skill | Repo commit (date) | Upstream version | Pinned file(s) | sha256 |
|---|---|---|---|---|
| taste-skill | `ce26fc25c0e5e8cab638f883de62d9a86ee5e45b` (2026-09-26) | v2 "experimental" (`design-taste-frontend`) | `references/upstream-SKILL.md` (1206 lines) | `aa194351b246b8b4799099d4ed7b033d29eab6e6e3d58d8d2172978be7b3ec89` |
| ui-ux-pro-max | `09170eec67eefd46a7ae85de61b40c194020f997` (2026-09-27) | 2.13.0 (`skill.json`) | `references/upstream-SKILL.md` | `ea087c341bfb5b23195c7302027268ede86da802554c18a5c4896a6017b439f9` |
| | | | tree: `data/` + `scripts/*.py` + `references/` (excl. upstream-SKILL.md) | `7974f52d0eadae317289829d6783229bcda31f26688ee204e534e9599d237bb5` |
| emil-design-eng | `e8a175de22ae1e49370fc144c1f3bb9aeedf988d` (2026-10-02) | — (no version field) | `references/upstream-SKILL.md` (674 lines) | `ffbe68e6007fb42cb8149f089b400a1ca007d59ba23e8948e2be4476f3175939` |
| web-design-guidelines | agent-skills `063bee94c3f4df8453406c830b0a7df0f2860278` (2026-08-28) | metadata `1.0.0` | `references/upstream-SKILL.md` | `f4647ca866a3accf763777f83e7682954f0187cd6bea7eea0399796652414e8f` |
| | web-interface-guidelines `e3d624baaf29dc1fc645aff3e38f03e564d2d6b1` (2026-08-17) | — | `references/command.md` (190 lines) | `5a775e6411f790f518dbc9c1fa7c50a89e6873502d9a3530a6eb223a590bcfe8` |

Official upstream install mechanisms, and why the kit vendors instead:

| Skill | Upstream says | Why not used as-is |
|---|---|---|
| taste-skill | `npx skills add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend"` | Tracks the default branch (unpinned), writes into the product repo, needs Node, and gives no place for team overrides |
| ui-ux-pro-max | `/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill` + `/plugin install ui-ux-pro-max@ui-ux-pro-max-skill`, or `npm i -g ui-ux-pro-max-cli && uipro init --ai claude` | Global npm install; the plugin route is per-user and unpinned; `uipro init` writes into P-073's `.claude/` |
| emil-design-eng | `npx skills@latest add emilkowalski/skills` | Same as taste-skill, and `@latest` is unpinned |
| web-design-guidelines | `npx skills add vercel-labs/agent-skills` | Installs every Vercel skill, and the skill itself fetches its rules at runtime (see below) |

Size: 3.5 MB total (ui-ux-pro-max 3.3 MB, mostly CSV data; the others ≤100 KB). The kit does **not** copy full repos: it leaves out upstream
tests, CLI, gallery, images, sibling skills and research folders.

Verify the pins (from `team-ai-kit/`):

```bash
sha256sum skills/{taste-skill,emil-design-eng,ui-ux-pro-max,web-design-guidelines}/references/upstream-SKILL.md \
          skills/web-design-guidelines/references/command.md
(cd skills/ui-ux-pro-max && find data scripts/*.py references -type f ! -name upstream-SKILL.md | LC_ALL=C sort | xargs sha256sum | sha256sum)
PYTHONUTF8=1 python3 guardrails/validate_kit.py
```

Updating a skill means clone at a new commit → `diff` against the pinned files → read every change (network fetches, install commands,
odd instructions) → copy over → update the commit + sha256 in `NOTICE.md` **and** this table → PR with review. There is no auto-update.

## Security / Reproducibility Notes

**web-design-guidelines fetches its rules from the network at runtime (verified at agent-skills `063bee94c3`).** The upstream `SKILL.md`
tells the agent to WebFetch `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` before **every**
review, then to apply "all the rules and output format instructions" in the fetched text. That causes two problems:

- **Not reproducible:** `main` can change between two audits of the same code.
- **Remote instruction channel:** whoever can change that file, or intercept the fetch, steers the agent inside our repo. This is why
  `THIRD_PARTY.md` previously rejected the skill.

**Decision: pin.** `command.md` at `e3d624baaf` was reviewed in full: it is a static rule list plus an output format, with no further fetches or
install commands. It is stored as `references/command.md`. The wrapper `SKILL.md` forbids fetching and reads only the local file. The
upstream `SKILL.md` is kept under `references/` for diffing only and is not loaded as a skill.

Other skills, reviewed at the pinned commits:

| Skill | Runtime network? | Other findings and how they are handled |
|---|---|---|
| taste-skill | No fetch step. Its *output advice* uses remote assets (`picsum.photos`, `cdn.simpleicons.org`) and suggests `npm install` of design systems | Wrapper bans runtime external assets (team rule: self-host) and bans new dependencies without card approval. Its stack advice (Next.js / RSC) is replaced by React + Vite. Its "avoid Inter" advice is overridden by the team font rule |
| ui-ux-pro-max | No. Scripts use only the Python stdlib (checked imports: no `urllib.request`, `requests`, `socket`, `subprocess`) and read local CSVs | `--persist` writes files, so the wrapper restricts it to `--output-dir ../team-ai-kit` (never P-073) and forbids `--force` without review. Upstream script paths use `${CLAUDE_PLUGIN_ROOT}`, which the wrapper replaces with `.claude/skills/ui-ux-pro-max/scripts/` |
| emil-design-eng | No. Two reference links (easing.dev, easings.co) are for humans | The upstream "Initial Response" rule (reply with a canned sentence, then wait) is disabled in the wrapper |

- No pattern scan hits (prompt-override phrases, `curl | sh`, credential paths, telemetry) in any vendored file.
- Name collisions: do **not** also install the plugin or `npx` versions at user scope (`~/.claude/skills`). Same-named skills from two
  scopes make it unclear which copy (pinned + wrapped, or unpinned) is loaded.

Open items (not resolved by this setup):

1. **The Landing / Story page has no product requirement yet.** Precedence level 1 is empty for surface 1, so taste-skill would effectively
   lead. A spec section or card should exist before any landing work starts.
2. ~~`team-ai-kit/design-system/` does not exist yet.~~ Resolved 2026-10-03: `design-system/proactive-care/` (v0.1 draft) is hand-governed;
   ui-ux-pro-max output is a proposal only and is never persisted into it (see [design-governance.md](design-governance.md)).
3. **taste-skill v2 is labelled "experimental" upstream.** v1 (`skills/taste-skill-v1/`) exists but was not vendored; switch only if v2 proves unstable.
4. **vercel-labs/agent-skills has no LICENSE file at the pinned commit.** Its README states MIT; the LICENSE shipped is the one from
   web-interface-guidelines (MIT, Vercel Labs), which covers `command.md`, the substantive content.
5. Skills load only in Claude Code sessions opened in **P-073** (through the `install.sh` symlink). Sessions opened in team-ai-kit do not
   auto-load them. Read the wrapper `SKILL.md` directly there, or open the session in P-073.

## How Claude Should Invoke Each Skill

Claude Code auto-selects skills from their `description`; each wrapper's description is scoped narrowly to its role, so they should not
compete with `add-frontend-screen`. Name a skill explicitly when the task spans several roles. Recommended order per piece of UI work:

1. **Requirements first:** card + `docs/spec/20-ui.md` / `21-fe.md` + `add-frontend-screen/references/taste-rules.md`.
2. **`taste-skill`** (Landing; Customer only lightly) → output a one-line Design Read, three dial values, and a list of upstream advice dropped
   because of team rules. Dial values come from `design-system/proactive-care/MASTER.md` §2.1; changes go through a design PR.
3. **`ui-ux-pro-max`** → IA, flows, responsive structure. From the P-073 root:
   `python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<query>" --design-system -p "<surface>"`
   (no `--persist`: the design system is hand-governed; accepted proposals enter it by PR).
4. **`add-frontend-screen`** → build (outside the scope of this document).
5. **`emil-design-eng`** → add or review motion, at the intensity allowed for the surface.
6. **`web-design-guidelines`** on the changed files → findings as `file:line`. Then `web-accessibility` for WCAG/axe, and `playwright-cli`
   for light / dark / 390×844 screenshots.

Example prompts (run inside P-073):

- "Dùng skill taste-skill: đề xuất Design Read + 3 dial cho Landing page, theo taste-rules.md." ("Use taste-skill: propose a Design Read + 3 dials for the Landing page, following taste-rules.md.")
- "Dùng skill ui-ux-pro-max: kiến trúc thông tin cho Console CSKH (hàng đợi handoff, chi tiết job)." ("Use ui-ux-pro-max: information architecture for the CSKH Console — handoff queue, job detail.")
- "Dùng skill emil-design-eng: review motion của frontend/src/features/chat/." ("Use emil-design-eng: review the motion in frontend/src/features/chat/.")
- "Dùng skill web-design-guidelines: audit frontend/src/features/console/**/*.tsx." ("Use web-design-guidelines: audit frontend/src/features/console/**/*.tsx.")

## What Each Skill Must NOT Control

| Skill | Must not control |
|---|---|
| All four | Product requirements, scope, copy meaning · API, backend, `contracts/` · tech stack and dependencies (no installs without card approval) · anything in `taste-rules.md` · committing files to P-073 · fetching remote instructions |
| `taste-skill` | Information architecture, flows, responsive structure · motion timing / easing · audit verdicts · the CSKH Console at all · fonts (fixed: Be Vietnam Pro / Inter `vietnamese`, self-hosted) · colours outside the token system |
| `ui-ux-pro-max` | Visual personality and typography direction (taste-skill / internal DS) · motion (incl. its GSAP presets) · final audit · writing `design-system/` into P-073 · overriding team thresholds (44 px targets, 16/18 px body, AA in both themes) with its CSV data |
| `emil-design-eng` | Whether a feature or screen exists · layout, colour, type · IA · a11y thresholds · adding motion libraries · motion on Confirm parameters or OfferCard urgency effects |
| `web-design-guidelines` | Design decisions of any higher level · editing code (it reports only) · rules it lists that conflict with team rules: Title Case, `autocomplete="off"`, CDN `preconnect`, 24 px targets, SSR hydration checks on the Vite SPA |
