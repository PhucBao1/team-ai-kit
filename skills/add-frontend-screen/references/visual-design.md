<!-- Modified by P-073 team, 2026-10-01: bỏ frontmatter; thay đoạn persona bằng brief CSKH hậu mãi xe điện; bỏ "confirm with the client" và "take aesthetic risk"; đổi đoạn hero và chọn phông cho app (không phải landing page); thêm ràng buộc token. Giữ nguyên "Restraint and self-critique" và "More on writing in design". Nguồn: anthropics/skills skills/frontend-design/SKILL.md (Apache-2.0), xem NOTICE.md. -->

> **Luật nhóm P-073 thắng nội dung dưới đây.** Khi mâu thuẫn, làm theo `../SKILL.md` và `taste-rules.md`
> (phông, cỡ chữ, 1 màu nhấn, không animation trang trí, OfferCard trung tính). File này chỉ để định hướng thị giác và câu chữ.

# Frontend Design

**Brief (P-073):** an after-sales customer-care app for electric-vehicle owners (simulated data, Vietnamese UI). Users: car owners —
many of them older, reading on a phone — who need to trust what they see before they confirm a booking; customer-care staff working
a handoff console all day; and managers reading a dashboard. Priorities, in order: **trust and legibility first**, then calm clarity,
then personality. Be visually bold only on the manager dashboard (data density, chart treatment); keep the customer screens quiet,
large and plain. Make deliberate, specific choices for this brief rather than templated defaults.

## Ground your designs in the subject matter

The subject, audience and primary job are fixed by the brief above and by the task card; do not invent a different product. The
subject's industry, subject matter, materials, and vernacular are where distinctive visual choices come from — an EV service app
speaks the language of service bookings, battery health, charging, workshop progress and promises kept, not of a startup landing
page. Build with the brief's real content and subject matter throughout (from the API or labelled mock data).

## Design principles

For app screens, the first thing viewers see is the person's current task: the latest message and next action in chat, the
progress of a job in "Việc của tôi", the oldest open handoff in the console. Open with that, plainly. A big number with a small
label, supporting stats, and a gradient accent is the default treatment, so only use it on the dashboard and only if that's truly
the best option.

Typography carries the personality of the page. The team typeface is fixed (Be Vietnam Pro, or Inter with the Vietnamese subset,
self-hosted — see `taste-rules.md`); express hierarchy through a clear type scale following the default guidance of The Elements
of Typographic Style with intentional weights and spacing, not through extra families.

Default to line lengths of less than 80 characters. Serif typefaces can have slightly longer line lengths; give serif body text slightly more line-height than a sans-serif.

Avoid these default typographic treatments; they are the commonest tells of a generated page:
- Accenting just a single word or phrase in a headline, like putting one word in italic/bold or a different color.
- Using all caps for labels.
- Adding unnecessary typographic labels above content.

Visual structure is information. Structural devices like outlines, borders, numbering, eyebrows, dividers, labels, etc., encode useful information about the content rather than decorate it. Many generic designs use numbered markers (01 / 02 / 03), but that's only appropriate if the content actually is a sequence — like a stepped process or a timeline. Before adding numbered markers, check the content really is a sequence.

Use non-user-triggered motion sparingly and deliberately, only to draw attention. A single orchestrated moment — one page-load sequence or one reveal — lands better than scattered effects; fade-and-slide-up entrances on each section and hover transitions on every card are the generic default and read as AI-generated. Motion that answers a person's action (opening, expanding, confirming) is welcome when it shows what changed.

Consider written content carefully. Often a design brief may not contain real content, and it's up to you to come up with copy and placeholder content. Copy can make a design feel as templated as the design itself. See the below section on writing for more guidance.

## Process: plan, review against the brief, build, critique

For calibration, AI-generated design right now clusters around some traits:
1. a warm cream background (near #F4F1EA) with a high-contrast serif display and a terracotta or warm-clay accent (often near #D97757 — Anthropic's own Claude-interaction accent, so on a user's brief it reads as a tell);
2. a near-black background with a single bright acid-green or vermilion accent;
3. a broadsheet-style layout with hairline rules, zero border-radius, and dense newspaper-like columns;
4. the SaaS-card kit: content chopped into identical rounded cards, one border-radius on everything regardless of hierarchy, the same soft grey shadow (rgba(0,0,0,.1)) under each, and gradient washes as decoration;
5. template chrome that appears whatever the subject: a tracked-out ALL-CAPS eyebrow label above every heading; meta strings joined with middle dots ('A · B · C'); labels built as 'WORD — fragment' with a spaced em dash; tinted near-black (#0B0B0B, #111) standing in for black; a monospace face for small data labels; a '→' appended to link and button text.

All traits are legitimate for some briefs, but they are defaults rather than choices, and they appear regardless of subject. Where the brief pins down a visual direction, follow it exactly — the brief's own words always win, including when it asks for one of these looks. Where it leaves an axis free, don't spend that freedom on one of these defaults.

Work in two passes. First, brainstorm a short design plan based on the brief: express it with the team's existing CSS-variable tokens (add a token only when none fits, and in both themes).
- Color: describe the core base palette as 4–6 named tokens with their light and dark hex values.
- Type: the type scale and weights (the family is fixed).
- Layout: a layout concept, using one-sentence prose descriptions and ASCII wireframes to ideate and compare, from 320px up. Include alignment guidance; should the content be left aligned, center aligned, justified?
- Principles: the high-level guidance for what makes this screen clear for this brief.

Then review that plan against the brief before building: if any part of it reads like the generic default you would produce for any similar page (work through a similar prompt to see if you arrive somewhere similar) rather than a choice made for this specific brief — revise that part, say what you changed and why. Only after you've confirmed the relative uniqueness of your design plan should you start to write the code, following the revised plan.

When writing the code, be careful of structuring your CSS selector specificities. It's easy to generate CSS classes that cancel each other out (especially with a type-based selector like .section and an element-based selector like .cta). This can happen often with padding/margin between sections.

## Restraint and self-critique

Spend your boldness in one place. Let one element be the memorable thing, keep everything around it quiet and disciplined, and cut any decoration that does not serve the brief. Build to a quality floor without announcing it: responsive down to mobile, visible keyboard focus, reduced motion respected, visually accessible, harmonious color palettes. Critique your own work as you build, taking screenshots to review if your environment supports it — a picture is worth 1000 tokens. Consider Chanel's advice: before leaving the house, take a look in the mirror and remove one accessory. Human creatives have memory and always try to do something new, so if you have a space to quickly jot down notes about what you've tried, it can help you in future passes.

## More on writing in design

Words appear in a design for one reason: to make it easier to understand and use. They are design content, not decoration. Bring the same intentionality and minimalism to copywriting that you would bring to spacing and color. Before writing anything, ask what the design needs to say, and how it can best be said to help the person navigate the experience.

Write from the end user's perspective. Name things by what users will understand in simple language, not by how the system is built. A user manages notifications, not webhook config. Describe what something is or does in plain terms rather than selling it. Being specific and legible to new users is always better than being clever.

Use active voice as default. A CTA says exactly what happens when it is used: "Save changes," not "Submit." An action keeps the same name through the whole flow, so the button that says "Publish" produces a toast that says "Published." The vocabulary of an interface is the signposting for someone navigating the product. Cohesion and consistency are how people learn their way around.

Treat failure and emptiness as moments for direction, not mood. Explain what went wrong and how to fix it, in the interface's voice rather than a person's. Errors don't apologize, and they are never vague about what happened. An empty screen is an invitation to act.

Keep the tone conversational: plain verbs, sentence case, no filler, with tone matched to the brand and the audience. Let each written element do exactly one job.
