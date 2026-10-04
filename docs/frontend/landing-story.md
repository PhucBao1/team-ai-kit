# Landing story

Specification of the main product landing page (screen L1). Built on [MASTER](../../design-system/proactive-care/MASTER.md) and
the Landing deviations in [pages/landing.md](../../design-system/proactive-care/pages/landing.md); motion is specified in
[landing-motion-map.md](landing-motion-map.md). Source: owner brief of 2026-10-03 (ten sections). No code; nothing here changes P-073.

**Status.** Part of design contract v1.0 (MASTER §18). The opening section (L-01) and the three narrative sequences (L-02) stay blocked until amendments A-01 and A-02
to `taste-rules.md` are merged ([design-governance.md](design-governance.md) §9). Until then the page can still be built static.

**Language.** Copy direction is written in Vietnamese, the product language (`lang="vi"`, [content.md](../../design-system/proactive-care/content.md)).
The owner's English lines are kept beside each Vietnamese line as the source meaning, ready for an English version if D-10 decides one.

---

## 1. What a first-time visitor must understand

| # | Understanding (owner brief) | Where | How the page proves it |
|---|---|---|---|
| 1 | What problem exists | S02 | The reactive track: the customer carries every step and the waiting |
| 2 | What reactive care looks like | S02 | Five steps, all started by the customer, with a visible gap labelled "Chờ" |
| 3 | What proactive care means | S01, S03 | The AI's message lands on the time axis days before the customer's question; the start of the track moves earlier |
| 4 | How the system works | S04 | One signal becomes a verified outcome in six stages, each stage's output shown as a real artifact |
| 5 | Why an Agent is needed | S06 | Three real fixture signals pull in three directions; a rule alone picks an unreachable workshop |
| 6 | Why not every event calls an LLM | S04, S07 | Layer tags on every stage; sample events stop at the cheapest tier that can handle them |
| 7 | What the flagship UC1 looks like | S05 | Seven beats of the synthetic scenario, both sides at each beat |
| 8 | What the customer experiences | S05, S08 | The phone stays quiet until help arrives; one confirmation; a verified ending |
| 9 | What the CSKH employee experiences | S05, S08 | The case file and the handoff card at the same moments |
| 10 | How to enter the two experiences | S01, S08, S10 | The same two door labels in all three places |

## 2. Page structure

| ID | Section | Anchor | Job | Layout family | Motion |
|---|---|---|---|---|---|
| S01 | Mở đầu (hero) | `#dau-trang` | Make "proactive" obvious in seconds; offer the doors | Split statement (7 + 5) over a full-width time axis | None |
| S02 | Vấn đề | `#van-de` | Make the reactive friction felt | Sticky time track beside short text (shared with S03) | M1, part 1 |
| S03 | Chuyển dịch | `#chuyen-dich` | Same story, earlier start, burden moved to the system; the appointment is one intervention | (same sticky sequence as S02) | M1, part 2 |
| S04 | Bộ máy | `#bo-may` | One signal through six stages | Stage text column beside a sticky stage rail and artifact panel | M2 |
| S05 | UC1 | `#uc1` | One case end to end, from both sides | Beats column beside two sticky figures (phone, console) | M3 |
| S06 | Vì sao cần Agent | `#vi-sao-agent` | Rules detect, the agent reasons, people decide | Contrast pair over one worked example | None |
| S07 | Dùng AI có chọn lọc | `#chon-loc` | Not every event needs an LLM | Tiered sieve with sample events | None (selection highlight only) |
| S08 | Hai trải nghiệm | `#hai-trai-nghiem` | Two doors with real previews | Two asymmetric doors (5 + 7) | Feedback only |
| S09 | Tin cậy và an toàn | `#tin-cay` | What the AI does and does not do | Gate sequence over a two-column ledger | None |
| S10 | Bắt đầu | `#bat-dau` | One last, clear choice | Closing statement with two buttons | Feedback only |

**Page frame.**
- **Skip link** "Bỏ qua tới nội dung chính" (first focusable).
- **Header**, sticky, at most 72px, one line: product name (D-07); at `lg` and up the current chapter name in text; a link "Hai trải nghiệm" to S08; the theme switch.
- **Footer:** "Mọi kịch bản và dữ liệu trên trang là dữ liệu mẫu, dùng để minh hoạ cho MVP.", team and competition context, theme switch.
- **Section labels:** no section numbers or "01 / 10" labels appear on the page.

## 3. Page-wide rules

| Topic | Rule |
|---|---|
| Doors | One label per intent everywhere (taste-skill §4.5): "Khám phá trải nghiệm khách hàng" and "Khám phá trải nghiệm CSKH". The Demo stage link "Xem cả hai phía cùng lúc" appears only in S08 and S10, quietly (D-09) |
| Honesty | Every figure carries "Dữ liệu mẫu"; S05 carries "Kịch bản mô phỏng, minh hoạ cho MVP"; no number that a fixture, the spec or a live demo run did not produce; token or millisecond figures only from the live demo trace |
| Figures | Real components rendered inert (L-07); counterfactuals labelled and dashed (L-08); explanatory diagrams colored by holder (L-09); no screenshots, stock images, illustrations or decorative SVG |
| Headings | One `h1` (S01); one `h2` per section; `h3` inside S04 stages and S07 tiers; headings are sentences, never labels like "Giải pháp" |
| Copy | Plain editorial, one register (content.md §6); headings at most 2 lines at desktop; body at most 3 lines per block; step labels at most 6 words; no em or en dash, no exclamation mark, no filler words |
| Theme | Light, dark and system, locked per page; no inverted sections (taste-skill §4.11) |
| Performance | The LCP element is the S01 headline text; no images; below-the-fold figures render when near the viewport; spec §21 budget, first load under 2 seconds on 4G |
| Responsive tiers | **Full**: at least 1024px wide and 700px tall: sticky figures and scroll sequences. **Compact**: 768 to 1023px wide, or shorter than 700px: no sticky, discrete states. **Phone**: below 768px: one column, static figures. Zooming to 200% drops to the matching tier |

## 4. Sections

### S01. Mở đầu (hero)

**Purpose.** Make the proactive idea obvious within seconds: the help arrives before the question. Offer the two doors.

**Copy direction.**

| Element | Vietnamese | English source | Limit |
|---|---|---|---|
| Category line | Chăm sóc khách hàng chủ động bằng AI | Proactive AI Customer Care | One line, sentence case, `--muted` |
| Headline (`h1`) | Đừng đợi khách hàng phải hỏi. | Don't wait for the customer to ask. | At most 2 lines at desktop |
| Sub-statement | Hệ thống nhận ra trục trặc dịch vụ ngay khi vừa hình thành, tự kiểm tra, can thiệp và xác minh kết quả, trước khi khách phải liên hệ. | Proactive AI Customer Care for emerging service friction | At most 3 lines |
| Primary door | Khám phá trải nghiệm khách hàng | Explore Customer Experience | One line |
| Secondary door | Khám phá trải nghiệm CSKH | Explore CSKH Experience | One line |
| Axis labels | "08:15 Xe báo cảnh báo lần 3", "08:16 Trợ lý AI nhắn trước", "Vài ngày sau · Không cần gửi" | | At most 6 words each |
| Counterfactual bubble | "Xe tôi báo lỗi làm mát pin mấy lần rồi, phải làm sao?" | | One question, quoted |

**Visual structure.**
- **Desktop, 12 columns.** The left 7 hold the text stack: category line, headline (`--text-display-lg`), sub-statement (`--text-xl`), then the primary door (filled, `--accent`) beside the secondary door (outlined).
- **Right 5 columns.** A ComponentFigure: the real CareCard, summary variant (the four-question head: what was detected, why the customer
  receives it, what the AI is doing, what they need to do), for Nguyễn Văn Minh's VF 8, in WAITING FOR CUSTOMER, with "Dữ liệu mẫu".
- **Bottom band, full width, still inside the first viewport:**
  - A horizontal CareTrace axis with two teal circle nodes at 08:15 and 08:16. A hairline leader runs from 08:16 to the CareCard.
  - A long dashed stretch of axis, then the counterfactual marker (L-08): a dashed-outline bubble holding the question the customer no longer needed to send.
- **The argument.** The distance between the 08:16 node and that bubble *is* the argument.

**Interaction.** The two doors (links). The figure is inert.

**Motion.** None. Nothing animates on load (L-01, motion.md §1). Door hover and press feedback only.

**Responsive.**
- **Phone, inside the first viewport:** category line, headline (may wrap to 3 lines), sub-statement, then the doors full width, stacked, primary first.
- **Phone, below the first viewport:** the CareCard figure at full width, then the axis turned vertical (08:15, 08:16, a dashed stretch, the bubble).
- **Compact:** text full width, then the figure and the axis side by side.

**Accessibility.**
- The category line is a paragraph before the `h1`.
- The doors are links, because they navigate, styled as buttons; their accessible names equal the visible labels.
- The figure and axis are `aria-hidden` inside a `figure`. The `figcaption` reads: "Minh hoạ, dữ liệu mẫu: xe báo cảnh báo lần 3 lúc 08:15, trợ lý AI nhắn cho chủ xe lúc 08:16, vài ngày trước khi chủ xe định hỏi."

**Anti-patterns.**
- A centered hero.
- A phone mockup that floats, tilts or glows.
- An animated or typed headline.
- Badges such as "AI-powered" or "Mới", or a version label.
- A metrics strip, logos, a scroll cue, an uppercase eyebrow.
- A gradient or particle background.
- A third call to action.

### S02. Vấn đề

**Purpose.** Make the reactive model's friction felt without explaining it: the customer starts everything, carries every step, and waits.

**Copy direction.**

| Element | Vietnamese | English source |
|---|---|---|
| Heading | Hôm nay, khách phải tự lên tiếng trước. | Today, the customer has to speak up first. |
| Steps | Khách tự nhận ra; Gọi tổng đài; Chờ; Nhân viên tìm hiểu lại; Mới bắt đầu xử lý | Customer notices problem, contacts support, waits, staff investigates, action |
| Friction notes (at most 3) | "kể lại từ đầu", "chờ gọi lại", "đến xưởng thì thiếu linh kiện" | |
| Closing line | Mọi việc chỉ bắt đầu khi khách đã gặp chuyện. | Care starts only after the customer is already in trouble. |

**Visual structure.**
- **Left (5 columns):** the heading, then the five steps as a short ordered list.
- **Right (7 columns, sticky):** the ShiftTimeline in its reactive state on one time axis.
  - Customer steps are amber diamonds; staff steps are ink squares (L-09).
  - "Chờ" is a long dashed span; "kể lại từ đầu" is a small loop drawn back over the track.
  - The whole track is counterfactual (L-08) and labelled "Nếu chờ khách hỏi".
  - The friction notes sit under the track in `--muted`.

**Interaction.** None.

**Motion.** M1 part 1: the reactive track builds as the steps are read, and the "Chờ" span stretches.

**Responsive.**
- **Phone:** the list is the track, drawn vertically and static, with the shapes beside each step; friction notes inline.
- **Compact:** the track appears above the list, static.

**Accessibility.** The ordered list carries everything; the track is `aria-hidden` with a caption. Diamonds and squares always carry words.

**Anti-patterns.**
- Stock photos of an annoyed customer; emoji.
- Red alarm styling: this is friction, not failure.
- Invented statistics ("70% khách…"), blaming staff, paragraphs.

### S03. Chuyển dịch

**Purpose.** The same story with an earlier start and the burden moved to the system. Make it explicit that the appointment is not where care starts.

**Copy direction.**

| Element | Vietnamese | English source |
|---|---|---|
| Heading | Đảo lại: hệ thống bắt đầu trước. | Flip it: the system starts first. |
| Steps | Phát hiện; Kiểm tra; Can thiệp; Xác minh | Detects, investigates, intervenes, verifies |
| Key line (display statement, L-03) | Lịch hẹn không phải điểm bắt đầu. Nó chỉ là một trong các cách can thiệp. | The appointment is not the starting point. |
| Intervention types | Hướng dẫn tự xử lý; Cập nhật phần mềm từ xa; Dịch vụ lưu động; Đặt lịch xưởng (proposal §07 ①) | |
| Start label | Bắt đầu từ tín hiệu của xe | |

**Visual structure.**
- **Same sticky axis as S02.** The start marker now sits earlier, at "Tín hiệu từ xe".
- **The reactive track stays above as a dashed ghost.**
- **The proactive track below it:**
  - Teal circles for Phát hiện and Kiểm tra.
  - A teal circle for Can thiệp, with an inset list of the four intervention types; "Đặt lịch xưởng" is just one item.
  - One small amber diamond, "Khách xác nhận": the only step left to the customer.
  - A circle for Xác minh that ends in the green verified node.
  - There is no "Chờ" span on this track.
- **Legend.** One line of legend for the four shapes sits under the axis (L-09 bound).

**Interaction.** None.

**Motion.** M1 part 2: the start marker slides earlier, the reactive track turns to ghost, the proactive track draws, and the intervention list opens.

**Responsive.**
- **Phone:** the proactive track alone, vertical and static (S02 was just above), with the key line after it.
- **Compact:** both tracks stacked, static.

**Accessibility.** The steps, the key line and the intervention types are real text and lists; the tracks are `aria-hidden` with a caption that names both starts.

**Anti-patterns.**
- A calendar as the hero image of this section (it re-centers the appointment).
- A drag-only before/after slider.
- "Tiết kiệm X giờ" claims.

### S04. Bộ máy

**Purpose.** Show how it works: one signal becomes a verified outcome, each stage consuming the previous stage's output, with the place of rules, models, validator and people visible.

**Copy direction.**

| Element | Vietnamese | English source |
|---|---|---|
| Heading | Một tín hiệu, sáu bước. | One signal, six steps. |
| Intro (2 lines) | Mỗi bước nhận đầu ra của bước trước. Chỉ một số bước cần đến model. | |
| 1 Tín hiệu | Xe gửi một cảnh báo về hệ thống làm mát pin. | Signal |
| 2 Phát hiện (L0, 0 token) | Luật nhận ra cảnh báo lặp lại và tạo một ứng viên cần xem xét. | Detection |
| 3 Ngữ cảnh (L0) | Hệ thống đọc đúng những dữ liệu cần, mỗi dữ kiện kèm nguồn. | Context |
| 4 Suy luận AI (L2, chỉ khi cần) | Khi phải đối chiếu nhiều nguồn, Agent mới được gọi để chọn cách can thiệp. | AI Reasoning |
| 5 Can thiệp (L1, Validator, người) | Tin được kiểm tra rồi mới gửi; khách xác nhận trước khi hệ thống hành động. | Intervention |
| 6 Xác minh (L0) | Chỉ tính là xong khi dữ liệu xe xác nhận lỗi không quay lại. | Verification |
| Breadth line | Cùng bộ máy này xử lý trục trặc sạc (UC2) và điều phối lịch dịch vụ (UC3). | |

**Visual structure.**
- **Left column (5 columns):** six stage blocks, each an `h3`, its line and its LayerTag.
- **Right column (7 columns, sticky):** the EngineSequence panel:
  - **Stage navigation** above.
  - **The stage rail:** six nodes, the current one in its holder color and past ones neutral, per "color marks the present".
  - **The case packet:** a small chip that travels along the rail and relabels at each stage: "1 cảnh báo", "1 ứng viên", "5 nguồn đã đọc", "2 phương án", "1 tin đã gửi", "Đã xác minh".
  - **The artifact of the current stage**, each a real component with fixture data:

| Stage | Artifact |
|---|---|
| Tín hiệu | Event card: `vehicle.dtc.raised`, `BATT-COOL-01`, WARNING, `VF8-4821`, 08:15 |
| Phát hiện | Rule verdict: three events merging into one candidate; arbitration line "được phép liên hệ" |
| Ngữ cảnh | EvidenceList: bảo dưỡng đủ 5 kỳ; phần mềm 4.2.1; bảo hành đủ điều kiện sơ bộ; linh kiện có ở 3 xưởng; pin 42%, đủ đi tới |
| Suy luận AI | The decision gate with three exits (tất định đủ, phân loại là đủ, cần Agent), the "cần Agent" exit taken; InvestigationSteps: không sửa từ xa được, cần xưởng, xưởng có linh kiện và đi tới được; OptionList with two options and one excluded with its reason |
| Can thiệp | CareCard with "Tin tự động" and "Vì sao anh nhận tin này"; ValidationList "Đạt"; the DecisionBlock, then "Đang đặt lịch…", then the receipt "Đã đặt lịch" |
| Xác minh | VerificationMeter, guard then a 7-day window, ending in RESOLVED |

**Interaction.**
- **Stage navigation:** six links, "Tín hiệu" to "Xác minh", plus "Bước trước" and "Bước sau". Each jumps to its stage block; the panel follows whichever block is active.
- **Scroll is the single source of truth.** There is no hidden state that can disagree with the page position.

**Motion.** M2, the page's main narrative moment.

**Responsive.**
- **Compact and phone:** no sticky panel and no packet. Each stage block shows its artifact inline, in its final state.
- **Navigation:** the stage links become a wrapping row of chips under the heading, never a horizontal scroller.

**Accessibility.**
- **Structure:** stage blocks are an ordered list; the stage navigation is a `nav` labelled "Các bước của bộ máy", with `aria-current="step"` on the active link.
- **Focus:** after a jump, focus moves to the stage heading.
- **Announcements:** a polite live region announces the stage name only after a jump, never during scrolling.
- **Artifacts:** inert figures with captions, so everything they show is also in the stage text.

**Anti-patterns.**
- An 11-box arrow diagram (documentation look).
- Raw JSON or code blocks.
- Autoplaying the sequence.
- Neon data streams, a brain icon on the reasoning stage.
- Implying a model is used where none is.
- Counters that tick.

### S05. UC1

**Purpose.** Tell one case end to end from both sides: the customer experiences almost nothing until help arrives, while CSKH can see every step.

**Copy direction.**
- Heading: "Anh Minh chưa đặt lịch. Hệ thống đã bắt đầu." (Minh has not booked anything. The system already started.)
- Scenario label, at the top of the section and on both figures: "Kịch bản mô phỏng, minh hoạ cho MVP" (Synthetic / illustrative MVP scenario).

| Beat | Time | Line (at most 20 words) | Customer figure | CSKH figure |
|---|---|---|---|---|
| 1 | Trước 29/09 | Xe đã báo cảnh báo làm mát pin hai lần. Anh Minh chưa đặt lịch, chưa gọi ai. | "Chưa có tin mới" | Nothing |
| 2 | Thứ Ba 29/09, 08:15 | Cảnh báo lần thứ ba trong 14 ngày. | Unchanged | New case, DETECTED |
| 3 | 08:15 | Luật tạo một ứng viên: cảnh báo lặp lại, chưa có lịch hay ticket, được phép liên hệ. | Unchanged | Rule and arbitration in the trace |
| 4 | 08:15 | Hệ thống kiểm tra: bảo dưỡng đủ, bảo hành đủ điều kiện sơ bộ, có linh kiện, pin đủ đi tới. | Unchanged | Evidence with sources |
| 5 | 08:16 | Agent kết luận nên can thiệp: lỗi lặp lại, không sửa từ xa được, cần xưởng. Nếu chưa đủ căn cứ, hệ thống chỉ theo dõi. | Unchanged | Recommendation; the "chỉ theo dõi" branch shown muted |
| 6 | 08:16 | Anh Minh nhận tin trước khi phải hỏi, chọn Long Biên 14:00 thứ Sáu 02/10 và xác nhận. | CareCard arrives; confirmation; receipt | "Chờ khách xác nhận", then confirmed |
| 7 | Sau khi sửa | Hệ thống theo dõi 7 ngày. Cảnh báo không quay lại, việc được tính là xong. | VerificationMeter, then RESOLVED | "Đã xác minh" |

Optional aside under beat 7, in `--muted`: "Nếu linh kiện bị điều đi trước ngày hẹn, xem nhánh lập lại phương án trong demo." (LQ-4.)

**Visual structure.**
- **Beats column (4 columns)** beside two sticky figures:
  - The phone (3 columns): customer density, C1 then C2.
  - The CSKH console (5 columns): compact density, a queue row, the CaseFile header and its trace.
- **Shared clock label** above both figures: "Thứ Ba 29/09, 08:15".
- **The phone stays visibly quiet** through beats 1 to 5; that stillness is the point.

**Interaction.** None beyond scrolling.

**Motion.** M3. Each figure moves like its own surface: the phone uses the customer catalogue, the console changes instantly (K-03).

**Responsive.**
- **Compact and phone:** no sticky figures. Each beat is followed by compact snapshots of its final state.
- **Beats 1 to 5 on small screens:** the phone snapshot is replaced by one line, "Điện thoại của anh Minh: chưa có tin.", instead of repeating an empty phone.

**Accessibility.**
- **Structure:** the beats form an ordered list, with each time in a `time` element.
- **Scenario label:** read before the beats.
- **Figures and clock:** the figures are inert, with captions per beat; the clock label is not announced.

**Anti-patterns.**
- Framing the scenario as a real customer, a testimonial or a case study.
- Hiding or shrinking the scenario label.
- Typing dots in the phone.
- Animating the CSKH figure.
- Outcome statistics.

### S06. Vì sao cần Agent

**Purpose.** Explain the division of labor without overselling: rules detect, the agent reasons only when signals conflict, people decide.

**Copy direction.**

| Element | Vietnamese | English source |
|---|---|---|
| Heading (display statement, L-03) | Luật phát hiện. Agent suy luận. | Rules detect. Agent reasons. |
| Rules column | Ngưỡng, cửa sổ thời gian, bỏ trùng, điều kiện loại trừ. Nhanh, rẻ, kiểm tra được. Ví dụ: 3 lần trong 14 ngày, chưa có lịch, thì tạo ứng viên. | |
| Agent column | Đối chiếu nhiều nguồn, cân nhắc các cách can thiệp, giải thích lý do. Chỉ được gọi khi luật không đủ. | |
| Example title | Ba tín hiệu, ba hướng | |
| Example (VF 6 `VF6-2290`, fixture) | Camera ADAS báo lỗi, sửa được từ xa; pin còn 3%, không xưởng nào đi tới được; đã lỡ hai kỳ bảo dưỡng | |
| Rule-only outcome (counterfactual, L-08) | Chỉ có luật: đề xuất xưởng gần nhất, dù xe không đi tới được. | |
| Agent outcome | Cập nhật phần mềm từ xa trước, xe không phải di chuyển; gợi ý điểm sạc gần nhất hoặc dịch vụ lưu động; nói rõ bảo hành cần xưởng xác nhận. | |
| Boundary line | Agent đề xuất. Luật kiểm tra. Khách hoặc nhân viên quyết định. | The agent proposes; people decide |

**Visual structure.**
- **Contrast pair:** two columns ("Luật" at 5, "Agent" at 7) divided by a hairline, with no cards.
- **The worked example below:**
  - Three evidence rows with sources.
  - Thin connectors from each row to the outcome block it shapes.
  - The rule-only outcome, dashed and muted (L-08), beside the agent outcome.
- **The boundary line** closes the section.

**Interaction.** Hovering or focusing an evidence row emphasizes its connector and the clause it drives, instantly. The same correlation is written in text, so the highlight adds nothing essential.

**Motion.** None.

**Responsive.** Columns stack. Connectors are replaced by inline text after each row ("→ cập nhật từ xa").

**Accessibility.** The correlation is in the text; the highlight is decorative. The boundary line is a paragraph, not an image.

**Anti-patterns.**
- Brain, sparkles or robot imagery.
- "Agent hiểu bạn", "thông minh vượt trội".
- Accuracy percentages.
- Any suggestion that the agent diagnoses or decides warranty.

### S07. Dùng AI có chọn lọc

**Purpose.** Show that each event stops at the cheapest tier that can handle it: deterministic detection, selective reasoning, people when needed.

**Copy direction.**

| Element | Vietnamese | English source |
|---|---|---|
| Heading | Không phải sự kiện nào cũng cần LLM. | Not every event needs an LLM. |
| Principle | Mỗi sự kiện dừng ở tầng thấp nhất xử lý được nó. | |
| Tier L0 | Luật, 0 token: phát hiện, gộp, loại trừ, luồng an toàn | Deterministic detection |
| Tier L1 | Model nhỏ: khi chỉ cần phân loại | Selective reasoning |
| Tier L2 | Agent: khi nhiều nguồn, nhiều bước, còn mơ hồ | Selective reasoning |
| Tier Người | Nhân viên: an toàn, khiếu nại, mức 3, khách muốn gặp người | Human handoff |

Sample events (from fixtures and spec §09), each with its stop and reason:

| Event | Stops at | Reason shown |
|---|---|---|
| `TPMS-02` INFO | L0 | Gộp, không tạo ứng viên |
| `BATT-COOL-01`, lần 1 | L0 | Ghi nhận, chưa đủ để can thiệp |
| `BATT-COOL-01`, lần 3 trong 14 ngày | L2 | Nhiều nguồn cần đối chiếu |
| Linh kiện bị điều đi, lịch còn dưới 72 giờ | L2 | Lập lại phương án |
| `HV-ISO-99` CRITICAL | Người, không qua LLM | Luồng an toàn, mẫu tin duyệt sẵn |
| Khách nhắn "cho tôi gặp người" | L1, rồi Người | Phân loại ý định, chuyển ngay |

**Visual structure.**
- **The LayerSieve:** four tiers stacked top to bottom, each narrower by indentation, not by funnel geometry.
- **The entry rail** runs along the top.
- **Each event chip** sits in the tier where it stops, with a thin path line from the rail and its reason beside it.
- **No percentages.** Any token or timing figure comes from the live demo trace and carries "Dữ liệu mẫu".

**Interaction.** The event chips are toggle buttons. Selecting one emphasizes its path and reason and dims the others; Escape clears the selection. With nothing selected, everything is visible.

**Motion.** None; the emphasis change is instant, or `--dur-fast` opacity.

**Responsive.** Tiers become a list with their events and reasons under each; selection is not needed and is turned off.

**Accessibility.** Chips are buttons with `aria-pressed`; every reason is always in text; tiers have `h3` headings; no meaning is carried only by the path lines.

**Anti-patterns.**
- Cost charts; "tiết kiệm 90%" claims.
- Funnels with percentages.
- Falling particles or animated data.
- A pricing comparison.

### S08. Hai trải nghiệm

**Purpose.** Give the two doors with enough preview that the visitor knows what each experience will show. The CSKH door is where the staff side becomes concrete.

**Copy direction.**

| Element | Vietnamese | English source |
|---|---|---|
| Heading | Một ca, hai phía. | One case, two sides. |
| Customer door | Khám phá trải nghiệm khách hàng. "Nhận tin trước khi phải hỏi, xem bằng chứng, xác nhận một lần, theo dõi đến khi xong." | Explore Customer Experience |
| CSKH door | Khám phá trải nghiệm CSKH. "Thấy trục trặc trước khi khách gọi: vì sao có ca, bằng chứng nào, AI đề xuất gì, người cần quyết định gì." | Explore CSKH Experience |
| Demo link | Xem cả hai phía cùng lúc | |

**Visual structure.**
- **Two asymmetric doors:** customer at 5 columns, CSKH at 7. Each door is one large link holding its label, one line and a ComponentFigure.
  - **Customer door figure:** the phone with the CareCard summary of UC1 ("Hệ thống làm mát pin báo lỗi lặp lại", in WAITING FOR CUSTOMER).
  - **CSKH door figure:** the UC1 case header and its first three sections (why the case exists: `BATT-COOL-01` three times in 14 days;
    what was detected; the evidence), so the staff side also starts from the signal.
  - **Why not an appointment:** neither door shows a booking or a job at "Chờ hẹn"; an appointment is one intervention, never the
    opening image of either side (design review, check 4).
- **The Demo stage link** sits under the doors in `--muted` text.

**Interaction.** Each door is a single link; the figure inside is inert.

**Motion.** Feedback only: on hover the border turns to `--fg` over `--dur-fast`; press uses `--press-scale`. The figures do not move.

**Responsive.** Doors stack, customer first; figures scale to the column; the demo link follows.

**Accessibility.** One link per door whose accessible name is the door label; the description is linked with `aria-describedby`; no nested interactive elements.

**Anti-patterns.**
- Two identical equal-width cards.
- "Dùng thử miễn phí" style labels.
- Screenshots.
- Badges.

### S09. Tin cậy và an toàn

**Purpose.** Answer, concretely, "what stops the AI from doing something wrong?"

**Copy direction.**
- Heading: "Trợ lý AI làm gì, và không làm gì." (What the AI does, and does not do.)
- Gate labels: Đề xuất, Kiểm tra trước khi gửi, Khách hoặc nhân viên xác nhận, Thực hiện có kiểm soát, Xác minh bằng dữ liệu thật.

| Guarantee (brief) | Line (at most 2 lines) |
|---|---|
| Validation | Mọi con số, ngày giờ, mã trong tin đều phải có nguồn; không khớp thì chặn lại. |
| Controlled execution | Việc ảnh hưởng khách cần khách xác nhận; tiền, an toàn, định danh cần nhân viên duyệt. Không báo "đã xong" trước khi hệ thống xác nhận. |
| Verification | "Xong" nghĩa là dữ liệu xe xác nhận lỗi không quay lại. |
| Human handoff | Khách muốn, AI không chắc, có yếu tố an toàn hay khiếu nại: chuyển người ngay, kèm đủ thông tin để khách không phải kể lại. |
| No unsupported diagnosis | Trợ lý AI không kết luận xe hỏng gì; xưởng kiểm tra và kết luận. |
| No final warranty decision | Trợ lý AI chỉ nói "đủ điều kiện sơ bộ"; xưởng xác nhận. |

**Visual structure.**
- **The TrustGate**, in the node grammar (L-09). An AI circle ("Đề xuất") leads to a system circle tagged Validator ("Kiểm tra"), then a diamond ("Khách hoặc nhân viên xác nhận"), then a circle ("Thực hiện"), then the green verified node.
- **Branch.** A square branch to "Nhân viên" hangs off the line; one line of legend for the shapes sits under it.
- **Ledger below**, in two columns: "Luôn có" (validation, controlled execution, verification, handoff, "Gặp nhân viên", the label "Trợ lý AI") and "Không bao giờ" (chẩn đoán xe khi chưa có xác nhận, kết luận bảo hành, tự hứa bù đắp, hành động mức 2 hoặc 3 khi chưa có xác nhận).

**Interaction.** None.

**Motion.** None.

**Responsive.** The gate turns vertical; the ledger columns stack.

**Accessibility.** The gate is an ordered list; the ledger is two lists under `h3` headings.

**Anti-patterns.**
- Walls of shield and lock icons.
- "An toàn tuyệt đối".
- Compliance badges, fine print.

### S10. Bắt đầu

**Purpose.** Close the story with one clear choice.

**Copy direction.** Heading "Chọn một phía để bắt đầu." (Choose a side to start.), the two door labels unchanged, and the demo link.

**Visual structure.** The statement on the left; the two buttons; generous space; no figures, because S08 already previewed both sides.

**Interaction.** Links.

**Motion.** Feedback only.

**Responsive.** Buttons full width, stacked, primary first.

**Accessibility.** An `h2` and links with the same names as in S01 and S08.

**Anti-patterns.**
- A contact or newsletter form.
- "Liên hệ bán hàng".
- Countdowns, repeated figures, a third intent.

## 5. Page-wide anti-patterns

| The page is not | So it never has |
|---|---|
| A dashboard | KPI tiles, charts, live counters, tables of metrics, status walls |
| A documentation page | Long paragraphs, code blocks, the full eleven-stage pipeline as boxes and arrows, API names in body copy, FAQ accordions |
| A generic AI SaaS landing page | Purple or blue gradients, glass, glow, orbs, particles, sparkles, "AI-powered" badges, logo walls, testimonials, pricing, three equal feature cards, bento grids, typing effects, scroll cues |

## 6. Summary

**Proposed page structure.**

| Section | Content |
|---|---|
| S01 | The answer arrives before the question |
| S02 | The customer carries everything |
| S03 | The start moves earlier |
| S04 | One signal, six steps |
| S05 | Minh's case, both sides |
| S06 | Rules detect, the agent reasons |
| S07 | Each event stops at the cheapest tier |
| S08 | Two doors |
| S09 | What the AI does and does not do |
| S10 | Choose a side |

Motion lives in three places only (S02 into S03, S04, S05).

**Strongest hero concept: the answer arrives before the question.**
- **Copy:** the headline "Đừng đợi khách hàng phải hỏi."
- **Figure:** the real CareCard pinned to 08:16 on a time axis.
- **Counterfactual:** a dashed bubble, "Vài ngày sau · Không cần gửi", holds the question the customer would have asked.
- **Why it works:** proactivity becomes a visible distance in time. It is drawn with the product's own node grammar, needs no motion, and makes no claim beyond the sample data.

**Strongest interactive storytelling moment: S04, "Một tín hiệu, sáu bước".**
- **What happens:** one real artifact changes form as the reader scrolls or steps through:
  - a raw warning;
  - three warnings merging into one candidate at 0 token;
  - an evidence list with sources;
  - the decision gate taking the "cần Agent" exit, with options and one excluded with its reason;
  - a validated proactive message, then a confirmation and a server receipt;
  - a verification window that ends in a green check.
- **What the reader sees:** the case packet moves along the rail, and the layer tags show exactly where a model is used. The output of each step visibly becomes the input of the next: causality, not decoration.

**Open design questions.**

| ID | Question | Related |
|---|---|---|
| LQ-1 | Vietnamese only, or also an English version? The owner's core lines are English; this spec makes Vietnamese primary | D-10 |
| LQ-2 | Product name and mark for the header, the AI's introduction and the footer | D-07 |
| LQ-3 | Door wording: keep "Khám phá trải nghiệm…" (closest to the brief) or switch to the shorter, more concrete "Vào vai khách hàng" / "Vào vai nhân viên CSKH" | |
| LQ-4 | Should S05 include the UC3 twist (parts reallocated, customer asks for a person, staff finalizes)? It shows CSKH work in the story itself but lengthens it; the default keeps it in the Demo stage | J2 |
| LQ-5 | Is the Demo stage public and linked from S08 and S10? | D-09 |
| LQ-6 | May S07 show token and millisecond figures from a live demo run (labelled "Dữ liệu mẫu"), or stay qualitative? | |
| LQ-7 | Is the S01 counterfactual bubble the right tone for an enterprise audience, or should S01 show only the CareCard on the axis? | L-08 |
| LQ-8 | Amendments A-01 and A-02 must be approved before S01 and the three sequences can ship as specified | D-02 |
