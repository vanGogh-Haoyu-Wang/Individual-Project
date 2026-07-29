# CT07 candidate evidence and validation record

MATLAB R2026a produced the only numerical oracle: 1,807 mechanical records and
5,850 AE records. The two domains were filtered independently, retaining their
original MATLAB matrix row numbers.

## Evidence layers

Each of the eight LLM candidates is represented by three distinct layers:

1. `original_generation`: the directly saved generation artifact or, where that
   file was later edited, code reconstructed from the recorded response;
2. `fixture_normalized_probe`: the original code with only
   `Tensile-processed.xlsx → Commercial Tensile Tests.xlsx` and
   `CT-07 → CT07` applied when required;
3. `candidate_derived_validation_runner`: the audited runnable implementation
   under `code/ct07/` that produced the retained numerical result.

The machine-readable source of truth is
[`evidence/candidate_manifest.json`](evidence/candidate_manifest.json), with a
one-row-per-candidate view in
[`evidence/candidate_manifest.csv`](evidence/candidate_manifest.csv). Prompt,
response, historical record, original source, normalized probe, final runner
and result hashes are recorded separately.

The following original-generation sources were reconstructed from their
Markdown records because the standalone working files had already been edited:

- Sonnet 4.6 Python;
- Sonnet 4.6 Julia;
- GPT-5.5 Python.

They are explicitly marked `reconstructed_from_record`; they are not described
as byte-exact surviving raw files. Generation dates or session identifiers that
cannot be established from the retained record are `not_available`.

## Historical execution evidence

Existing execution records remain the evidence for the first observed and
first code-level failures. Recovery-time syntax parsing is recorded separately
and does not replace those historical outcomes. Environment failures are
distinguished from code-level failures, and `silent_data_loss` is
`not_evaluable` when execution stopped before a comparable result existed.

Sonnet Julia previously mixed three different states. They are now separated:

- the reconstructed original failed on the prompt-specified input name;
- the normalization-only probe inferred nine worksheet columns and failed at
  column 10;
- a later debug artifact loaded from row 4, produced 5,848 AE rows and five
  images, but silently lost the first two AE records and changed Figure 2 from
  the source-inherited `T09` title to `T07`;
- the candidate-derived validation runner restored all 5,850 AE rows and
  retained the source-inherited `T09` title.

For GPT-5.5 Python, the historical filename containing `max` is only a filename
alias. The recorded model setting is `GPT-5.5 XHigh`. The unmodified original
does not have a surviving strict-run log, so its first code-level execution
status is `not_available`; the two-constant normalized probe is reported
separately.

## Candidate-derived numerical validation

The eight runnable implementations are located only under `code/ct07/python/`
and `code/ct07/julia/`. They preserve candidate-specific loading and masking
logic while using small language-specific helpers for the standard CSV,
metadata and image contract.

The final result is recorded in
[`comparison_summary.json`](comparison_summary.json). Acceptance requires zero
missing and extra records, zero matrix-row and field mismatches at
`rtol=1e-12, atol=1e-12`, and exactly five non-empty, decodable PNG files for
each candidate. All eight candidate-derived validation runners pass.

This result does not mean that the eight original generations executed
successfully, received equivalent intervention, or were repaired minimally.
Current runner diffs are not used to rank repair effort or general model
quality. SMOP remains a separate deterministic-transpiler baseline and is not
included in the eight LLM candidates.

The superseded provenance summary and raw-score table are retained under
`evidence/historical_superseded/` solely as historical snapshots.
