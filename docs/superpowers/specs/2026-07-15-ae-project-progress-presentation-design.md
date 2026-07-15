# AE Project Progress Presentation Design

## Purpose

Create an academically rigorous progress presentation for the project supervisors and research group. The deck must summarize the full project to date, explain the methodology and the strongest evidence, distinguish verified conclusions from hypotheses, and end with concrete decisions and next steps.

## Deliverables

- One editable 16:9 PowerPoint deck in English.
- Approximately 15 slides for a 15–20 minute presentation.
- English speaker notes/script for every slide, targeting approximately 17 minutes in total.
- A visually verified final `.pptx`; no separate handout or decorative asset pack.

## Audience and Tone

- Audience: project supervisor and research group.
- Tone: technical, cautious, evidence-led, and suitable for an academic research meeting.
- Avoid marketing language, unsupported claims, excessive animation, and decorative imagery.
- State explicitly what has been proven, what is suggested by the data, and what remains unresolved.

## Core Narrative

The presentation will use an evidence-led research story:

1. The project investigates whether legacy MATLAB acoustic-emission analysis can be migrated reliably to open-source Python and Julia with LLM assistance.
2. Early CT07 multi-model experiments exposed practical problems in spreadsheet ingestion, code completeness, and AI-generated scientific software.
3. `Peak_Freq.m` was selected as a focused validation case because it enables exact event-level numerical comparison.
4. MATLAB, Python, and Julia were aligned after reconstructing MATLAB buffer and moving-RMS framing, producing exact event indices and numerical agreement within the specified tolerance.
5. Once equivalence was established, the open implementation was extended with per-file MAD-based adaptive event selection and Top-3 spectral peaks.
6. T01–T09 revalidation shows that adaptive selection retains every legacy-selected window and finds substantially more candidate windows, but additional sensitivity has not yet been proven to represent additional physical AE events.
7. The immediate research priority is physical validation and mechanical/AE alignment, not further feature expansion.

## Slide Structure

1. **Title** — project title, presenter, progress-review context.
2. **Background and motivation** — AE analysis, legacy MATLAB dependency, need for open and reproducible scientific computing.
3. **Aim and research questions** — reliable migration, LLM benchmarking, numerical equivalence, and extensibility.
4. **Overall methodology** — deconstruct, translate, verify, extend, evaluate.
5. **Phase 1: CT07 multi-model migration** — models/tools, Python and Julia outputs, purpose of the experiment.
6. **Lessons from CT07** — spreadsheet schema, missing-data alignment, Julia strictness, LLM hallucination and human-in-the-loop requirement.
7. **Why `Peak_Freq.m` became the validation case** — focused inputs/outputs and exact event-level testability.
8. **Reconstructing the legacy algorithm** — 1 MHz sampling, 200-sample windows, fixed RMS threshold, MATLAB framing, Top-1 FFT peak.
9. **Exact cross-language validation** — 42 files and 3,098 rows; identical event indices; zero time/frequency error; maximum magnitude error approximately `5.68e-13`; Python and Julia test evidence.
10. **Adaptive extension** — per-file centering, median/MAD threshold, unchanged FFT baseline, and exploratory Top-3 peak ranking.
11. **T01–T09 experimental design** — nine groups, 377 MAT files, 11,366,550 candidate windows, legacy versus adaptive comparison.
12. **Full quantitative results** — 16,240 legacy-selected windows, 522,216 adaptive rows, 32.16× ratio, all legacy windows retained, no missing windows, one no-peak case in T09.
13. **Interpretation and evidence boundary** — greater sensitivity is proven; greater physical accuracy is not; frequency centres remain broadly stable; selection logic drives the difference.
14. **Strengths, limitations, and risks** — reproducibility and exact validation versus steel/composite scope mismatch, missing mechanical alignment, incomplete Top-3 validation, and incomplete controlled performance benchmarking.
15. **Conclusions and next steps** — freeze scope, validate adaptive-only samples, align mechanical and AE records, confirm material scope with supervisor, complete controlled benchmarks, and begin dissertation integration.

## Evidence and Claim Rules

- Use the formal aims, project brief, preparation report, development log, validation JSON, test outputs, and T01–T09 summary as the evidence base.
- Present the T01 exact migration as the strongest verified result.
- Describe the adaptive method as detecting more candidate windows, not as improving accuracy by 32.16 times.
- Describe Top-3 as an exploratory extension until physical or classification value is demonstrated.
- Keep CT07 analysis and raw-waveform `Peak_Freq.m` analysis as complementary layers; do not imply that their time bases or specimens are already aligned.
- State the unresolved mismatch between the formal steel-structures scope and the currently validated composite tensile data.
- Include concise source footers on evidence-heavy slides.

## Visual Design

- 16:9 layout with a white background.
- Black or very dark grey text; one dark blue accent and one restrained orange highlight for warnings or unresolved issues.
- Minimum 35 pt slide titles and 16 pt body text; prefer 20–24 pt body text where content permits.
- Use flat academic layouts rather than cards, dashboards, gradients, stock photography, or decorative illustrations.
- Use existing result plots where they add evidence. Otherwise use large numbers, one simple methodology flow, and compact tables.
- No animations are required.
- Maintain consistent margins, slide numbering, source footers, and terminology.

## Speaker Script and Timing

- Total target: approximately 17 minutes, leaving time within a 15–20 minute slot.
- Title and transitions: 15–30 seconds each.
- Background and methodology slides: approximately 45–60 seconds each.
- Exact validation and T01–T09 result slides: approximately 75–90 seconds each.
- Limitations and next steps: approximately 60–75 seconds each.
- Speaker notes must explain the argument and evidence rather than read the slide verbatim.

## Quality Checks

- Verify all displayed totals directly from source CSV/JSON files.
- Re-run Python and Julia tests before final delivery.
- Render and inspect every slide at full size.
- Correct clipping, wrapping, unintended overlap, inconsistent alignment, and unreadable source text.
- Confirm that no visible slide contains internal planning language or unqualified scientific claims.
- Confirm that the deck can be delivered coherently in 15–20 minutes using the final speaker script.

## Scope Boundary

This deliverable is a progress-review presentation, not the final dissertation defence. It will not introduce new algorithms, rerun large scientific experiments, or attempt to resolve the material-scope and physical-validation questions inside the slide-production task. Existing verified results will be presented accurately, and unresolved items will be converted into explicit next-step decisions.
