# R260_2 supplementary analysis

This directory contains a read-only, streaming analysis of:

`/Users/vangogh/Documents/毕设/Rail Steel/Copy of current R260_2.xlsx`

The 99 MB source workbook is never modified or loaded as one in-memory table.
The script streams worksheet XML so the large S1–S10 sheets remain
reproducible on the current machine.

Run:

```sh
python tools/analyse_r260.py \
  "/Users/vangogh/Documents/毕设/Rail Steel/Copy of current R260_2.xlsx" \
  --output results

uv run tools/plot_s3.py
```

Primary outputs:

- `results/analysis_report.md`
- `results/specimen_summary.tsv`
- `results/s3_feature_summary.tsv`
- `results/s3_crack_growth.tsv`
- `results/analysis.json`
- two S3 analysis figures

The workbook is treated as a processed rail-steel AE dataset labelled
`R260_2`. Its exact steel grade and specimen provenance remain unconfirmed.
