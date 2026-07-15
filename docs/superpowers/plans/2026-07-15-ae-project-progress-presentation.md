# AE Project Progress Presentation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a verified 15-slide English PowerPoint with embedded English speaker notes for a 15–20 minute academic project-progress presentation.

**Architecture:** Build one editable 16:9 deck with `@oai/artifact-tool` in a temporary presentation workspace, using the Codex Grid white-background layouts as composition references. Keep all generated source, previews, layouts, and QA files outside the repository; export only the final `.pptx` to the project presentation directory.

**Tech Stack:** JavaScript ES modules, `@oai/artifact-tool`, bundled Node.js, bundled slide render/QA scripts, existing project PNG/CSV/JSON evidence.

## Global Constraints

- Use English for all visible copy and speaker notes.
- Target 15 slides and approximately 17 minutes of speaking time.
- Use a white 16:9 canvas, black/dark-grey text, restrained dark blue emphasis, and orange only for limitations or unresolved issues.
- Use at least 35 pt for slide titles, 16 pt for body copy, and 9 pt only for evidence-source footers.
- Present adaptive selection as greater sensitivity, not greater physical accuracy.
- Present Top-3 FFT as exploratory.
- Do not claim that CT07 mechanics and raw-waveform time bases are aligned.
- State the unresolved steel/composite scope mismatch.
- Do not add stock photography, decorative illustrations, animation, or new dependencies.
- Embed one English speaker script in each slide's speaker notes.
- Render and inspect every slide; fix every unintended overlap, clipping, wrapping, or source mismatch before delivery.

## File Structure

- Create final deck: `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/Presentation/AE_Project_Progress_Review.pptx`
- Create scratch workspace: `/var/folders/1m/zcbwdr_x7mn3nz0hct3jfw1m0000gn/T/codex-presentations/manual-ae-progress-20260715/ae-project-progress-review`
- Create scratch source: `/var/folders/1m/zcbwdr_x7mn3nz0hct3jfw1m0000gn/T/codex-presentations/manual-ae-progress-20260715/ae-project-progress-review/tmp/build_deck.mjs`
- Create source ledger: `/var/folders/1m/zcbwdr_x7mn3nz0hct3jfw1m0000gn/T/codex-presentations/manual-ae-progress-20260715/ae-project-progress-review/tmp/source-notes.txt`
- Create QA ledger: `/var/folders/1m/zcbwdr_x7mn3nz0hct3jfw1m0000gn/T/codex-presentations/manual-ae-progress-20260715/ae-project-progress-review/tmp/qa/qa-ledger.txt`
- Create rendered slide previews and layout JSON under the scratch `tmp/preview` and `tmp/layout` directories.
- Read but do not modify formal project documents, validation outputs, experiment CSVs, or existing plots.

---

### Task 1: Freeze the Evidence Ledger

**Files:**
- Create: `/var/folders/1m/zcbwdr_x7mn3nz0hct3jfw1m0000gn/T/codex-presentations/manual-ae-progress-20260715/ae-project-progress-review/tmp/source-notes.txt`
- Read: `/Users/vangogh/Desktop/毕设/Aims, Objectives & Gantt Chart.docx`
- Read: `/Users/vangogh/Desktop/毕设/MSc_project_P15_2026_VB.docx`
- Read: `/Users/vangogh/Desktop/毕设/Preparation Assessment Report Haoyu Wang.docx`
- Read: `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/MATLAB Validation Package/Results/legacy_row_comparison_summary.json`
- Read: `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/temp/ae-peak-frequency/outputs/t01-t09-revalidation/summary/t01_t09_comparison_summary.csv`
- Read: `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/Notes/99 AE Peak-Frequency Development Log.md`
- Read: `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/Notes/T01-T09 Legacy vs Adaptive Comparison.md`

**Interfaces:**
- Consumes: formal objectives, verified metrics, limitations, and source paths.
- Produces: a plain-text evidence ledger used verbatim by the deck authoring task.

- [ ] **Step 1: Create the scratch directory tree**

Run:

```bash
mkdir -p "/var/folders/1m/zcbwdr_x7mn3nz0hct3jfw1m0000gn/T/codex-presentations/manual-ae-progress-20260715/ae-project-progress-review/tmp/preview" \
  "/var/folders/1m/zcbwdr_x7mn3nz0hct3jfw1m0000gn/T/codex-presentations/manual-ae-progress-20260715/ae-project-progress-review/tmp/layout" \
  "/var/folders/1m/zcbwdr_x7mn3nz0hct3jfw1m0000gn/T/codex-presentations/manual-ae-progress-20260715/ae-project-progress-review/tmp/assets" \
  "/var/folders/1m/zcbwdr_x7mn3nz0hct3jfw1m0000gn/T/codex-presentations/manual-ae-progress-20260715/ae-project-progress-review/tmp/qa" \
  "/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/Presentation"
```

Expected: all directories exist and no project evidence file is modified.

- [ ] **Step 2: Recalculate the T01–T09 totals from the CSV**

Run the bundled Python interpreter with `csv.DictReader` and calculate these exact fields:

```text
groups=9
files=377
candidate_windows=11366550
legacy_selected=16240
legacy_rows=16239
no_peak=1
adaptive_rows=522216
adaptive_only=505976
matched=16240
missing=0
ratio=32.16
```

Expected: every recomputed value matches the block above; stop authoring if any value differs.

- [ ] **Step 3: Re-read the exact migration JSON**

Expected evidence:

```text
input_file_count=42
matlab_rows=3098
python_rows=3098
julia_rows=3098
event_indices_identical=true
time_s_error=0.0
peak_frequency_khz_error=0.0
peak_magnitude_error=5.684341886080801e-13
all_numeric_rows_match_within_tolerance=true
```

- [ ] **Step 4: Write the source ledger**

Record the exact values above, the formal aim, the steel/composite mismatch, the unaligned time-base limitation, the Top-3 evidence boundary, and the source path assigned to each slide. Use `.txt`, not Markdown.

- [ ] **Step 5: Run the existing scientific checks**

Run:

```bash
cd "/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/temp/ae-peak-frequency/python"
.venv/bin/python -m pytest -q
```

Expected: `19 passed`.

Run:

```bash
cd "/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/temp/ae-peak-frequency/julia"
/Users/vangogh/.julia/juliaup/julia-1.12.6+0.aarch64.apple.darwin14/Julia-1.12.app/Contents/Resources/julia/bin/julia --project=. test/runtests.jl
```

Expected: five test summaries with 1, 2, 3, 1, and 4 passing assertions respectively.

### Task 2: Author the Deck Source and Speaker Notes

**Files:**
- Create: `/var/folders/1m/zcbwdr_x7mn3nz0hct3jfw1m0000gn/T/codex-presentations/manual-ae-progress-20260715/ae-project-progress-review/tmp/build_deck.mjs`
- Copy for embedding: `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/Tools history/Claude code Desktop Sonnet 4.6/outputs/03Test Outputs/01_ct07_strain_stress.png`
- Copy for embedding: `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/temp/ae-peak-frequency/outputs/t01-t09-revalidation/t01-python-adaptive/baseline_peak_frequency.png`

**Interfaces:**
- Consumes: `source-notes.txt`, two evidence images, and exact metrics from Task 1.
- Produces: a `Presentation` with 15 slides, named visual objects, embedded notes, PNG previews, layout JSON files, a montage, and a PPTX export.

- [ ] **Step 1: Initialise the artifact-tool workspace**

Run:

```bash
/Users/vangogh/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node \
  "/Users/vangogh/.codex/plugins/cache/openai-primary-runtime/presentations/26.709.11516/skills/presentations/container_tools/setup_artifact_tool_workspace.mjs" \
  --workspace "/var/folders/1m/zcbwdr_x7mn3nz0hct3jfw1m0000gn/T/codex-presentations/manual-ae-progress-20260715/ae-project-progress-review/tmp"
```

Expected: the scratch workspace can resolve `@oai/artifact-tool` without adding a project dependency.

- [ ] **Step 2: Implement the deck-level constants and helpers**

The module must define these exact constants and helper interfaces:

```js
const W = 1280;
const H = 720;
const C = { canvas: "#FFFFFF", ink: "#111111", muted: "#5B6470", panel: "#EDEDED", rule: "#B8BCC4", blue: "#2457A6", orange: "#B85C1E" };
const FONT = "Helvetica Neue";

function addText(slide, name, value, position, style = {}) { /* editable textbox */ }
function addTitle(slide, number, title, subtitle = "") { /* 35+ pt title and optional subtitle */ }
function addFooter(slide, number, source = "") { /* source left, slide number right */ }
function addNotes(slide, script) { slide.speakerNotes.textFrame.setText(script); slide.speakerNotes.setVisible(true); }
function addMetric(slide, name, value, label, position, accent = C.blue) { /* large value and concise label */ }
function addClaimPanel(slide, name, heading, body, position, accent = C.blue) { /* flat academic callout */ }
```

Each helper must create named objects so layout inspection can locate them.

- [ ] **Step 3: Implement the 15-slide content map**

Use these takeaway titles exactly unless shortening is required to prevent wrapping:

```text
1  Reliable Migration of Acoustic-Emission Analysis from MATLAB to Open Source
2  The research problem is reliability, not code translation alone
3  Four questions define success for the migration
4  The study separates translation, verification, and extension
5  CT07 exposed the practical limits of one-shot LLM translation
6  Data ingestion—not plotting—was the dominant early failure mode
7  Peak_Freq.m provides an event-level numerical validation case
8  Exact replication required reconstructing MATLAB framing semantics
9  MATLAB, Python, and Julia agree for all 3,098 T01 results
10 Adaptive thresholds test sensitivity without changing the FFT baseline
11 Revalidation covers nine groups and 11.37 million candidate windows
12 Adaptive selection retains every legacy event and finds 32.16× more candidates
13 The evidence proves greater sensitivity—not greater physical accuracy
14 The technical core is strong; physical interpretation remains the main risk
15 The next phase should validate events, align data, and freeze scope
```

Slide compositions must adapt Codex Grid layout families 01, 05, 14, 17, 19, and 20 rather than repeat one silhouette. Use one process diagram on slide 4, one algorithm comparison on slide 10, one grouped bar chart on slide 12, one compact evidence table on slide 9, and the two supplied project plots only on slides 5 and 11.

- [ ] **Step 4: Add the speaker script**

Write 80–170 spoken words per slide, except slide 1 may use 50–80 words. Each script must:

- explain why the slide matters;
- state the evidence boundary when discussing adaptive selection or Top-3;
- transition naturally to the next slide;
- avoid reading bullet points verbatim;
- total approximately 1,900–2,200 English words, corresponding to roughly 15–18 minutes at 125–135 words per minute.

- [ ] **Step 5: Export previews, layouts, montage, and PPTX**

Use the artifact-tool exports:

```js
for (const [index, slide] of presentation.slides.items.entries()) {
  const stem = `slide-${String(index + 1).padStart(2, "0")}`;
  await writeBlob(`${PREVIEW_DIR}/${stem}.png`, await presentation.export({ slide, format: "png", scale: 2 }));
  await fs.writeFile(`${LAYOUT_DIR}/${stem}.layout.json`, await (await slide.export({ format: "layout" })).text());
}
await writeBlob(`${QA_DIR}/deck-montage.webp`, await presentation.export({ format: "webp", montage: true, scale: 1 }));
const pptx = await PresentationFile.exportPptx(presentation);
await pptx.save(FINAL_PPTX);
```

Expected: 15 PNG files, 15 layout JSON files, one montage, and one editable PPTX.

### Task 3: Validate Content and Layout

**Files:**
- Inspect: all files in the scratch `tmp/preview` and `tmp/layout` directories.
- Create: `/var/folders/1m/zcbwdr_x7mn3nz0hct3jfw1m0000gn/T/codex-presentations/manual-ae-progress-20260715/ae-project-progress-review/tmp/qa/qa-ledger.txt`
- Verify: `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/Presentation/AE_Project_Progress_Review.pptx`

**Interfaces:**
- Consumes: exported deck, previews, layouts, notes, and source ledger.
- Produces: a corrected final deck and a complete QA record.

- [ ] **Step 1: Run structural slide tests**

Run:

```bash
/Users/vangogh/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  "/Users/vangogh/.codex/plugins/cache/openai-primary-runtime/presentations/26.709.11516/skills/presentations/container_tools/slides_test.py" \
  "/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/Presentation/AE_Project_Progress_Review.pptx"
```

Expected: no slide-canvas overflow errors.

- [ ] **Step 2: Inspect the full-deck montage**

Verify narrative flow, title hierarchy, varied silhouettes, consistent margins, restrained colour use, and evidence emphasis. The montage is not sufficient for final approval.

- [ ] **Step 3: Inspect every slide at full resolution**

Check all 15 PNG files individually for title wrapping, clipped text, unreadable footers, distorted evidence images, chart-label collisions, table crowding, and unintended overlap.

- [ ] **Step 4: Inspect layout JSON for collision evidence**

Search every layout JSON for objects outside the 1280×720 frame and compare suspicious intersecting bounds against the rendered slide. Correct every unintended overlap in `build_deck.mjs`, rebuild, and repeat Tasks 3.1–3.4.

- [ ] **Step 5: Verify speaker notes and timing**

Import or inspect the PPTX with artifact-tool using `kind: "slide,notes"`. Confirm all 15 slides contain visible English notes. Count total script words and require 1,900–2,200 words; revise scripts outside that range.

- [ ] **Step 6: Verify evidence and claim wording**

Confirm these exact conditions:

```text
3,098 rows refers only to the T01 exact cross-language comparison.
16,240 refers to selected legacy windows; 16,239 refers to valid legacy peak rows.
522,216 refers to adaptive Top-1 rows across T01–T09.
32.16× is labelled a candidate-window or sensitivity ratio, not an accuracy gain.
Top-3 is labelled exploratory.
The steel/composite scope mismatch is visible.
Mechanical and raw-waveform time alignment is labelled unresolved.
```

- [ ] **Step 7: Record QA completion**

Write each slide number, inspected status, corrections made, final test output, test timestamp, and notes word count to `qa-ledger.txt`.

### Task 4: Final Delivery Verification

**Files:**
- Verify: `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/Presentation/AE_Project_Progress_Review.pptx`

**Interfaces:**
- Consumes: the QA-approved deck.
- Produces: the final user-facing PowerPoint link and a concise delivery summary.

- [ ] **Step 1: Confirm the output exists and is non-empty**

Run:

```bash
test -s "/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/Presentation/AE_Project_Progress_Review.pptx"
```

Expected: exit code 0.

- [ ] **Step 2: Perform a final clean render**

Render the final PPTX with `render_slides.py` into a fresh QA directory and confirm exactly 15 slide images are produced.

- [ ] **Step 3: Re-run `slides_test.py` on the final file**

Expected: exit code 0 and no overflow errors.

- [ ] **Step 4: Deliver only final artifacts**

Return the clickable absolute path to the PPTX, state that the English speaker script is embedded in the speaker notes, and identify the project documents, validation JSON, experiment summary, and existing result plots as the evidence base. Do not attach scratch source, previews, layout JSON, or QA files unless requested.
