# CT07 validation record

MATLAB R2026a produced the only numerical oracle: 1,807 mechanical records and
5,850 AE records. The two domains were filtered independently, retaining their
original MATLAB matrix row numbers.

The eight raw candidates and their first-run outcomes are frozen in
`raw_candidate_scores.csv`. Existing execution logs are reused rather than
overwriting or rerunning interactive raw scripts. Workbook-name and worksheet
normalization are excluded from model-error scoring.

Eight independent fixed runners are in `fixed/`. Candidate-specific loading,
physical column selection and complete-case masks remain separate. The small
`python_output.py` and `JuliaOutput.jl` helpers only standardize CSV, metadata
and five headless PNG outputs; they are not shared data loaders.

The final result is recorded in `comparison_summary.json`. Acceptance requires
zero missing and extra records, zero matrix-row and field mismatches at
`rtol=1e-12, atol=1e-12`, and exactly five non-empty, decodable PNG files for
each candidate. Figure 2's `T09` title is retained and classified as inherited
from the MATLAB source.
