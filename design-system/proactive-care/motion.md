# Motion

Part of the Proactive Care Design System v1.0. Start at [MASTER.md](MASTER.md). Values: [tokens.md](tokens.md) §7.
Motion direction follows emil-design-eng (pinned in `skills/emil-design-eng/`) inside taste-rules rule 10.

## 1. Principles

1. **Motion explains change.** Valid purposes: feedback (the interface heard you), state change (something became different), spatial
   continuity (where something came from or went), and on Landing only, explanation of a sequence. "It looks nice" is not a purpose.
2. **Frequency decides.** Things seen hundreds of times a day do not animate; occasional things animate briefly; rare moments may
   carry a little more. Keyboard-initiated actions get no feedback motion (no press scale, chevron rotation or switch slide); an
   overlay opened from the keyboard appears by opacity only. The parameters of a confirmation never animate.
3. **Fast and decisive.** UI motion stays at or below `--dur-slow`. Enter with `--ease-out`; move with `--ease-in-out`; exits are
   faster than enters. No ease-in, no bounce, no elastic.
4. **Only transform and opacity move.** Never animate width, height, top, left, filters or blur. The one exception is a hover or
   selection color change, which may transition over `--dur-fast`. Never `transition: all`; list properties.
5. **Interruptible.** Use CSS transitions for anything that can be triggered again mid-flight; keyframes only for one-shot entrances.
6. **Nothing on load.** The first paint is the final layout. Content does not fly in when a page opens. Motion is for change the
   person witnesses: a change that happened while they were away is shown finished and marked in words ("Mới", "Cập nhật lúc 14:18").
7. **Reduced motion is a full design, not an afterthought.** Under `prefers-reduced-motion: reduce` every movement becomes an instant
   change or a plain opacity change, and every loop stops.
8. **No motion libraries** (taste-rules rules 10 and 15): CSS transitions, CSS keyframes, the Web Animations API, IntersectionObserver
   and CSS scroll-driven animations only. No scroll event listeners, no reading scroll position into state.

## 2. Catalogue

Everything that may move. Anything not listed does not move. Customer moments are mapped to these rows in
[customer-motion-map.md](../../docs/frontend/customer-motion-map.md).

| Motion | Purpose | Spec | Landing | Customer | CSKH |
|---|---|---|---|---|---|
| Press feedback | Feedback | scale to `--press-scale`, `--dur-press`, `--ease-out` | yes | yes | no (K-03) |
| Switch | Feedback | thumb translate, `--dur-fast`, `--ease-out`, pointer only; moves back the same way if the save fails | n/a | yes | instant |
| Update control ("N ca mới", "1 việc mới") | State change | Customer: as element enter. CSKH: fades in over `--dur-fast` | n/a | yes | yes (K-03) |
| Hover | Feedback | color and border change only, instant or `--dur-fast`; only under `(hover: hover) and (pointer: fine)` | yes | yes | instant |
| Element enter (chip, row, message, evidence row) | State change | opacity 0 to 1 with `--rise-sm`, `--dur-base`, `--ease-out` | yes | yes | no |
| Block enter (recommendation, receipt) | State change | opacity with `--rise-md`, `--dur-base`, `--ease-out` | yes | yes | no |
| Group enter | State change | as above with `--stagger` between items, at most 6 items staggered | yes | yes | no |
| Popover, menu | Spatial | from `--enter-scale` and opacity, origin at the trigger, `--dur-fast` | yes | yes | instant |
| Dialog | Spatial | from `--enter-scale` and opacity, `--dur-slow` in, `--dur-fast` out | yes | yes | `--dur-fast` opacity only |
| Sheet | Spatial | translate from below, `--dur-slow`, `--ease-drawer`; exit `--dur-fast` | n/a | yes | n/a |
| In-app notice (toast) | State change | enters from its edge with `--rise-md` and opacity, `--dur-base`, `--ease-out`; leaves the same way, `--dur-fast`; a newer notice replaces the text by crossfade, never stacks | n/a | yes | n/a |
| Sticky action bar | Spatial | enters from below by its own height with opacity, `--dur-base`, `--ease-out`; leaves the same way, `--dur-fast`; never on load | n/a | yes | n/a |
| State chip change | State change | crossfade, `--dur-fast`, opacity only | per figure | yes | `--dur-fast`, server-driven only (K-03) |
| Disclosure | State change | chevron rotation `--dur-fast` when opened by pointer, instant by keyboard; content appears without height animation | yes | yes | as Customer |
| Trace node appears | State change | as element enter | scrubbed (L-02) | yes | no |
| RESOLVED settle | State change, rare | node from `--enter-scale` with opacity, `--dur-base`, once | yes | yes | no |
| ESCALATED change | State change | crossfade, `--dur-fast` | yes | yes | `--dur-fast`, server-driven only (K-03) |
| EXECUTING loader | Progress | loader icon rotation, `--ease-linear`, one turn per second, inside the locked button only | n/a | yes | yes |
| Verification segment | State change | segment opacity, `--dur-base` | n/a | yes | `--dur-fast`, server-driven only (K-03) |
| Row change mark | State change | a one-shot overlay in `--sunken` fading by opacity over `--dur-slow`, plus a static "Vừa đổi" time until the element is opened; only for changes the server made while the element was on screen | n/a | n/a | yes (K-03) |
| Narrative sequence | Explanation | scroll-scrubbed, see §4 | yes (L-02) | no | no |

## 3. Motion and the AI states

From MASTER §12, summarized for implementers:

| State | Motion |
|---|---|
| DETECTED | Enters once. No loop |
| INVESTIGATING | Each finished check enters as it completes. No spinner, no pulse, no typing dots. Elapsed time as text after 2 seconds without news |
| RECOMMENDING | Block enters; Customer options stagger |
| WAITING FOR CUSTOMER, WAITING FOR HUMAN | None. Waiting is never animated |
| EXECUTING | The loader in the locked button. The only loop on Customer and CSKH |
| VERIFYING | None while waiting; segment change only |
| RESOLVED | Customer: one settle. CSKH: no settle; the chip changes like any server-driven change (K-03). No confetti |
| ESCALATED | Crossfade. No alarm, no shake |

Safety banners appear instantly. Urgency is carried by placement, words and color, never by motion. CSKH applies K-03 to every row of
this table: entries are instant with the change mark, chips and segments change over `--dur-fast`, and nothing settles.

## 4. Landing narrative motion (deviation L-02, pending amendment A-02)

MOTION_INTENSITY 8 on Landing is achieved through **choreography tied to the reader's scroll**, not through longer, slower or looping animation.

- **Three sequences only**: the ShiftTimeline (S02 into S03), the EngineSequence (S04) and the StoryChapter (S05). Every movement is
  listed in [landing-motion-map.md](../../docs/frontend/landing-motion-map.md); anything not listed there does not move.
- **Scroll-scrubbed only.** Sequences are bound to scroll position with CSS scroll-driven animations; where unsupported, an
  IntersectionObserver switches discrete states with ordinary `--dur-base` transitions. The reader controls the pace and can scroll back.
- **Full tier only.** Sequences run at 1024px wide and 700px tall or more; smaller or zoomed viewports get the static final states.
- **Each figure moves like its own surface.** Customer figures use the customer catalogue; CSKH figures change instantly, because a
  scrubbed change is caused by the reader and K-03 never animates a person's own action;
  loops inside figures are off on Landing.
- **Jumps are instant.** In-page navigation never smooth-scrolls, so scrubbed sequences never play in fast-forward.
- **One moving focal element at a time.** When the trace draws, nothing else moves.
- **No scroll hijacking.** Scroll speed, snapping and direction are never changed. Sticky figures are allowed; pinned sections that
  swallow scroll are not.
- **No parallax**, no background motion, no autoplaying video, no loops.
- **Time-based transitions stay at or below `--dur-slow`.**
- **Static first.** Without support, or under reduced motion, every chapter shows its final state: the complete trace, the final
  figure, the full diagram. The page must be fully understandable with zero motion.
- **Performance.** Compositor-only properties; no layout reads during scroll; no animation on more than one subtree at once.

## 5. Reduced motion

| Normal | Reduced |
|---|---|
| Enter with rise | Opacity only, `--dur-fast`, or instant |
| Stagger | All at once |
| Popover, dialog scale | Opacity only |
| Sheet slide | Opacity only |
| In-app notice | Opacity only |
| Sticky action bar, switch thumb, state chip change | Instant |
| CSKH change mark | The static "Vừa đổi" time only |
| EXECUTING loader rotation | Static loader icon; the label carries the meaning |
| RESOLVED settle | Instant |
| Landing scroll sequences | Final states, no scrubbing |

## 6. Review checklist (from emil-design-eng, adapted)

- [ ] Every animation has a purpose from §1 and appears in the §2 catalogue for this surface.
- [ ] No `transition: all`; only transform and opacity animate (plus hover or selection color over `--dur-fast`).
- [ ] Nothing starts from scale 0; popovers start at `--enter-scale` from their trigger.
- [ ] No ease-in; enters use `--ease-out`; exits are faster than enters.
- [ ] No animation on keyboard-initiated actions or CSKH list navigation.
- [ ] Hover motion is gated by `(hover: hover) and (pointer: fine)`.
- [ ] Nothing animates on page load.
- [ ] Reduced motion tested: every loop stopped, every sequence shows its final state.
- [ ] No scroll listeners; Landing sequences use scroll-driven animations or IntersectionObserver.
