# AE Peak-Frequency Prototypes Implementation Plan

**Goal:** Build reproducible Python and Julia prototypes that read the available AE waveform and experiment-summary data, reproduce the existing single-peak frequency workflow, and compare it with a Top-3 peak extension.

**Architecture:** Create a new standalone project beside the original MATLAB files; never modify `Peak_Freq.m`, `.mat`, or the original workbook. Both implementations consume one shared JSON parameter file and produce the same CSV event-table schema. Python is implemented first and becomes the readable reference; Julia is then implemented against the same synthetic fixtures and output contract.

**Tech Stack:** Python 3.11+, NumPy, SciPy, pandas, openpyxl, Matplotlib, pytest; Julia 1.12+, MAT.jl, XLSX.jl, CSV.jl, DataFrames.jl, DSP.jl, FFTW.jl, Plots.jl, Test.

## Global Constraints

- Source data remains read-only at `/Users/vangogh/Desktop/毕设/Haoyu Wang/T01`.
- The original MATLAB reference remains read-only at `/Users/vangogh/Desktop/毕设/Haoyu Wang/Peak_Freq.m`.
- Use sampling rate `1_000_000 Hz`, 200-sample event windows, and `20 kHz` minimum frequency separation, as stated by the MATLAB script.
- Store all generated CSV, PNG, and temporary copies under the new project `outputs/` directory; do not write results into `T01`.
- Treat composite frequency-band labels as display-only legacy labels; do not claim a damage mechanism from frequency alone.
- The baseline and Top-3 modes must use identical detected events and FFT settings.
- A MATLAB comparison is required before claiming functional agreement with the legacy script; until then call the result a Python/Julia reproduction attempt.

---

## Planned File Structure

```text
/Users/vangogh/Desktop/毕设/Haoyu Wang/ae-peak-frequency/
  README.md
  .gitignore
  config/peak_frequency_parameters.json
  docs/data-contract.md
  fixtures/synthetic_signal.mat
  fixtures/synthetic_summary.csv
  python/
    pyproject.toml
    src/ae_peak_frequency/__init__.py
    src/ae_peak_frequency/config.py
    src/ae_peak_frequency/io.py
    src/ae_peak_frequency/events.py
    src/ae_peak_frequency/spectrum.py
    src/ae_peak_frequency/plots.py
    src/ae_peak_frequency/cli.py
    tests/test_io.py
    tests/test_events.py
    tests/test_spectrum.py
    tests/test_cli.py
  julia/
    Project.toml
    src/AEPeakFrequency.jl
    test/runtests.jl
    run.jl
  outputs/.gitkeep
```

### Task 1: Create the standalone project and shared analysis contract

**Files:**
- Create: `/Users/vangogh/Desktop/毕设/Haoyu Wang/ae-peak-frequency/README.md`
- Create: `/Users/vangogh/Desktop/毕设/Haoyu Wang/ae-peak-frequency/.gitignore`
- Create: `/Users/vangogh/Desktop/毕设/Haoyu Wang/ae-peak-frequency/config/peak_frequency_parameters.json`
- Create: `/Users/vangogh/Desktop/毕设/Haoyu Wang/ae-peak-frequency/docs/data-contract.md`
- Create: `/Users/vangogh/Desktop/毕设/Haoyu Wang/ae-peak-frequency/outputs/.gitkeep`

**Consumes:** `Peak_Freq.m` and the `T01` data folder.

**Produces:** A single documented contract used by both language prototypes.

- [ ] **Step 1: Create the project folders without copying source data**

Run:

```bash
mkdir -p 'ae-peak-frequency/config' 'ae-peak-frequency/docs' \
  'ae-peak-frequency/fixtures' 'ae-peak-frequency/outputs' \
  'ae-peak-frequency/python/src/ae_peak_frequency' \
  'ae-peak-frequency/python/tests' 'ae-peak-frequency/julia/src' \
  'ae-peak-frequency/julia/test'
```

Expected: Empty project structure exists; the original `T01` directory is untouched.

- [ ] **Step 2: Add the shared parameter file**

Create `config/peak_frequency_parameters.json` with:

```json
{
  "sampling_rate_hz": 1000000,
  "event_window_samples": 200,
  "window_overlap_samples": 1,
  "rms_event_threshold": 0.1,
  "min_peak_distance_khz": 20.0,
  "top_peak_count": 3,
  "frequency_limit_khz": 500.0,
  "inserted_gap_samples": 1000000
}
```

- [ ] **Step 3: Write the data contract**

Specify that the event-table CSV columns are exactly:

```text
event_id,file_name,event_time_s,peak_rank,frequency_khz,magnitude
```

Specify that baseline mode writes only `peak_rank=1`, while Top-3 mode writes ranks `1`, `2`, and `3` only when a valid separated peak exists.

- [ ] **Step 4: Add a short README with the scientific boundary**

Include this text:

```text
This project compares one-peak and three-peak FFT reporting for selected AE waveform events.
It does not infer a material damage mechanism from frequency band alone.
```

- [ ] **Step 5: Check the contract is complete**

Run:

```bash
rg -n 'sampling_rate_hz|event_id,file_name|does not infer' \
  'ae-peak-frequency/config' 'ae-peak-frequency/docs' 'ae-peak-frequency/README.md'
```

Expected: One parameter definition, one exact event schema, and the interpretation boundary are found.

### Task 2: Build and test the Python input layer

**Files:**
- Create: `/Users/vangogh/Desktop/毕设/Haoyu Wang/ae-peak-frequency/python/pyproject.toml`
- Create: `/Users/vangogh/Desktop/毕设/Haoyu Wang/ae-peak-frequency/python/src/ae_peak_frequency/config.py`
- Create: `/Users/vangogh/Desktop/毕设/Haoyu Wang/ae-peak-frequency/python/src/ae_peak_frequency/io.py`
- Create: `/Users/vangogh/Desktop/毕设/Haoyu Wang/ae-peak-frequency/python/tests/test_io.py`

**Consumes:** JSON parameters, `.mat` files with a `data` variable, `.xlsx` summaries, and `.csv` summaries.

**Produces:** `load_waveform(path) -> numpy.ndarray` and `load_summary(path, sheet_name=None) -> pandas.DataFrame`.

- [ ] **Step 1: Write the failing waveform-loader tests**

```python
def test_load_waveform_uses_first_data_column(mat_path):
    signal = load_waveform(mat_path)
    assert signal.ndim == 1
    assert signal.dtype == np.float64
    assert signal.tolist() == [0.0, 1.0, -1.0]

def test_load_waveform_rejects_missing_data_variable(tmp_path):
    bad_path = tmp_path / "bad.mat"
    savemat(bad_path, {"other": np.array([1.0])})
    with pytest.raises(ValueError, match="data"):
        load_waveform(bad_path)
```

- [ ] **Step 2: Run the input tests and confirm failure**

Run:

```bash
cd 'ae-peak-frequency/python'
python -m pytest tests/test_io.py -v
```

Expected: FAIL because `load_waveform` and `load_summary` do not yet exist.

- [ ] **Step 3: Implement the smallest input API**

```python
def load_waveform(path: Path) -> np.ndarray:
    raw = loadmat(path)
    if "data" not in raw:
        raise ValueError(f"{path} does not contain a data variable")
    data = np.asarray(raw["data"], dtype=float)
    if data.ndim != 2 or data.shape[1] < 1:
        raise ValueError(f"{path} data must have at least one column")
    return data[:, 0]

def load_summary(path: Path, sheet_name: str | None = None) -> pd.DataFrame:
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    if path.suffix.lower() == ".xlsx":
        return pd.read_excel(path, sheet_name=sheet_name, header=None)
    raise ValueError("summary input must be .csv or .xlsx")
```

Define the configuration type in `config.py` so every later function uses the same names:

```python
@dataclass(frozen=True)
class Config:
    sampling_rate_hz: int
    event_window_samples: int
    window_overlap_samples: int
    rms_event_threshold: float
    min_peak_distance_khz: float
    top_peak_count: int
    frequency_limit_khz: float
    inserted_gap_samples: int
```

- [ ] **Step 4: Add summary-reader tests for both formats**

```python
def test_load_summary_reads_csv_and_xlsx(csv_path, xlsx_path):
    assert load_summary(csv_path).shape == (2, 2)
    assert load_summary(xlsx_path, "CT-01").shape[1] >= 15
```

- [ ] **Step 5: Run all Python input tests**

Run:

```bash
python -m pytest tests/test_io.py -v
```

Expected: PASS.

### Task 3: Implement and test the Python legacy single-peak pipeline

**Files:**
- Create: `/Users/vangogh/Desktop/毕设/Haoyu Wang/ae-peak-frequency/python/src/ae_peak_frequency/events.py`
- Create: `/Users/vangogh/Desktop/毕设/Haoyu Wang/ae-peak-frequency/python/src/ae_peak_frequency/spectrum.py`
- Create: `/Users/vangogh/Desktop/毕设/Haoyu Wang/ae-peak-frequency/python/tests/test_events.py`
- Create: `/Users/vangogh/Desktop/毕设/Haoyu Wang/ae-peak-frequency/python/tests/test_spectrum.py`

**Consumes:** One-dimensional waveform arrays and the shared parameter values.

**Produces:** `detect_events(signal, config) -> list[Event]` and `ranked_peaks(event, config, count) -> list[Peak]`.

Use these exact Python value objects in `events.py` and `spectrum.py`:

```python
@dataclass(frozen=True)
class Event:
    start_sample: int
    samples: np.ndarray

@dataclass(frozen=True)
class Peak:
    frequency_khz: float
    magnitude: float
```

Define this test fixture in both `test_events.py` and `test_spectrum.py` (or place it once in `tests/conftest.py`):

```python
@pytest.fixture
def config_for_test() -> Config:
    return Config(
        sampling_rate_hz=1_000_000,
        event_window_samples=200,
        window_overlap_samples=1,
        rms_event_threshold=0.1,
        min_peak_distance_khz=20.0,
        top_peak_count=3,
        frequency_limit_khz=500.0,
        inserted_gap_samples=1_000_000,
    )
```

- [ ] **Step 1: Write the failing event-detection test**

```python
def test_detect_events_returns_200_sample_segments():
    signal = np.zeros(1000)
    signal[300:305] = 1.0
    events = detect_events(signal, config_for_test())
    assert len(events) == 1
    assert events[0].samples.shape == (200,)
    assert events[0].start_sample == 250
```

- [ ] **Step 2: Implement explicit event selection**

Use a documented 200-sample moving RMS with one-sample overlap. Select windows whose RMS is above `0.1`; extract the corresponding 200 samples. Preserve the legacy DC-offset operation in a named function:

```python
def subtract_legacy_offset(signal: np.ndarray, first_file_mean: float) -> np.ndarray:
    return signal.astype(float, copy=False) - first_file_mean
```

The CLI must expose `--offset-mode legacy-first-file` and `--offset-mode per-file`; the default is `legacy-first-file` for comparison with MATLAB.

- [ ] **Step 3: Write the failing FFT peak test**

```python
def test_ranked_peaks_finds_known_100khz_component():
    fs = 1_000_000
    sample = np.arange(200) / fs
    event = np.sin(2 * np.pi * 100_000 * sample)
    peaks = ranked_peaks(event, config_for_test(), count=1)
    assert len(peaks) == 1
    assert peaks[0].frequency_khz == pytest.approx(100.0, abs=5.0)
```

- [ ] **Step 4: Implement one-peak FFT ranking**

```python
def ranked_peaks(samples: np.ndarray, config: Config, count: int) -> list[Peak]:
    magnitudes = np.abs(np.fft.rfft(samples))
    frequencies_khz = np.fft.rfftfreq(len(samples), d=1 / config.sampling_rate_hz) / 1000
    valid = frequencies_khz <= config.frequency_limit_khz
    indices, _ = find_peaks(
        magnitudes[valid],
        distance=round(config.min_peak_distance_khz / (config.sampling_rate_hz / len(samples) / 1000)),
    )
    ordered = indices[np.argsort(magnitudes[valid][indices])[::-1]]
    return [Peak(float(frequencies_khz[i]), float(magnitudes[i])) for i in ordered[:count]]
```

- [ ] **Step 5: Run the event and FFT tests**

Run:

```bash
python -m pytest tests/test_events.py tests/test_spectrum.py -v
```

Expected: PASS, including the known 100 kHz synthetic event.

### Task 4: Add Python Top-3 output, plots, and an end-to-end command

**Files:**
- Create: `/Users/vangogh/Desktop/毕设/Haoyu Wang/ae-peak-frequency/python/src/ae_peak_frequency/plots.py`
- Create: `/Users/vangogh/Desktop/毕设/Haoyu Wang/ae-peak-frequency/python/src/ae_peak_frequency/cli.py`
- Create: `/Users/vangogh/Desktop/毕设/Haoyu Wang/ae-peak-frequency/python/tests/test_cli.py`
- Modify: `/Users/vangogh/Desktop/毕设/Haoyu Wang/ae-peak-frequency/python/pyproject.toml`

**Consumes:** Event objects and ranked peaks from Tasks 2–3.

**Produces:** `baseline_events.csv`, `top3_events.csv`, `baseline_peak_frequency.png`, and `top3_peak_frequency.png`.

- [ ] **Step 1: Write a failing command-line test**

```python
def test_cli_writes_both_csv_files_and_pngs(tmp_path, mat_path):
    result = runner.invoke(main, [str(mat_path), "--output-dir", str(tmp_path)])
    assert result.exit_code == 0
    assert set(p.name for p in tmp_path.iterdir()) == {
        "baseline_events.csv", "top3_events.csv",
        "baseline_peak_frequency.png", "top3_peak_frequency.png",
    }
```

- [ ] **Step 2: Build the event rows with the exact shared schema**

```python
row = {
    "event_id": event_id,
    "file_name": source_path.name,
    "event_time_s": event.start_sample / config.sampling_rate_hz,
    "peak_rank": rank,
    "frequency_khz": peak.frequency_khz,
    "magnitude": peak.magnitude,
}
```

- [ ] **Step 3: Implement the two plots**

Use a scatter plot with x-axis `Time (s)`, y-axis `Peak Frequency (kHz)`, y-limit `0–500`, and a clear title distinguishing `Top-1` from `Top-3`. Do not use the legacy material-mechanism legend in the new plots.

- [ ] **Step 4: Run the end-to-end test**

Run:

```bash
python -m pytest tests/test_cli.py -v
```

Expected: PASS; each PNG decodes and each CSV contains the six shared columns.

- [ ] **Step 5: Run the real-data Python command into a fresh output folder**

Run:

```bash
python -m ae_peak_frequency.cli \
  '/Users/vangogh/Desktop/毕设/Haoyu Wang/T01/20221018_140051.mat' \
  --output-dir '../../outputs/python-single-file'
```

Expected: Four freshly generated files, or a recorded actionable error about the source data structure.

### Task 5: Implement the Julia prototype against the same contract

**Files:**
- Create: `/Users/vangogh/Desktop/毕设/Haoyu Wang/ae-peak-frequency/julia/Project.toml`
- Create: `/Users/vangogh/Desktop/毕设/Haoyu Wang/ae-peak-frequency/julia/src/AEPeakFrequency.jl`
- Create: `/Users/vangogh/Desktop/毕设/Haoyu Wang/ae-peak-frequency/julia/run.jl`
- Create: `/Users/vangogh/Desktop/毕设/Haoyu Wang/ae-peak-frequency/julia/test/runtests.jl`

**Consumes:** The same JSON configuration, `.mat` waveform files, `.csv` and `.xlsx` summaries.

**Produces:** The identical six-column event-table schema and matching PNG names under `outputs/julia-single-file`.

- [ ] **Step 1: Write Julia tests before the module**

```julia
@testset "known sine peak" begin
    fs = 1_000_000
    samples = sin.(2π * 100_000 .* (0:199) ./ fs)
    peaks = ranked_peaks(samples, config_for_test(), 1)
    @test length(peaks) == 1
    @test isapprox(peaks[1].frequency_khz, 100.0; atol=5.0)
end

@testset "event table schema" begin
    @test names(event_dataframe) == [
        "event_id", "file_name", "event_time_s", "peak_rank", "frequency_khz", "magnitude"
    ]
end
```

Define the Julia test configuration before these testsets:

```julia
config_for_test() = (
    sampling_rate_hz = 1_000_000,
    event_window_samples = 200,
    window_overlap_samples = 1,
    rms_event_threshold = 0.1,
    min_peak_distance_khz = 20.0,
    top_peak_count = 3,
    frequency_limit_khz = 500.0,
    inserted_gap_samples = 1_000_000,
)

event_dataframe = DataFrame(
    event_id = Int[], file_name = String[], event_time_s = Float64[],
    peak_rank = Int[], frequency_khz = Float64[], magnitude = Float64[],
)
```

- [ ] **Step 2: Run the Julia tests and confirm failure**

Run:

```bash
julia --project=julia -e 'using Pkg; Pkg.test()'
```

Expected: FAIL because module functions are not yet defined.

- [ ] **Step 3: Implement the Julia module API**

Export these functions only:

```julia
load_waveform(path::AbstractString)::Vector{Float64}
load_summary(path::AbstractString; sheet_name::Union{Nothing,String}=nothing)::DataFrame
detect_events(signal::Vector{Float64}, config)::Vector{Event}
ranked_peaks(samples::Vector{Float64}, config, count::Int)::Vector{Peak}
write_outputs(events, source_path, output_dir, config)::Nothing
```

Use `MAT.matread(path)["data"][:, 1]` for waveform loading, `CSV.read` for CSV summaries, and `XLSX.readtable` only for summary inspection. Keep the waveform algorithm independent of the workbook table shape.

- [ ] **Step 4: Implement Top-1 and Top-3 ranking with FFTW and DSP**

Use `rfft`, a non-negative frequency vector, and `findpeaks` or an explicitly tested local-maximum routine. Sort peaks by magnitude descending, enforce the shared 20 kHz separation, and return at most `count` peaks.

- [ ] **Step 5: Run Julia unit tests**

Run:

```bash
julia --project=julia -e 'using Pkg; Pkg.test()'
```

Expected: PASS.

- [ ] **Step 6: Run the real-data Julia command**

Run:

```bash
julia --project=julia julia/run.jl \
  '/Users/vangogh/Desktop/毕设/Haoyu Wang/T01/20221018_140051.mat' \
  '../../outputs/julia-single-file'
```

Expected: The same four file names as Python, with a documented reason if a Julia package cannot read the MATLAB v5 file.

### Task 6: Compare Python and Julia, then check against MATLAB when available

**Files:**
- Create: `/Users/vangogh/Desktop/毕设/Haoyu Wang/ae-peak-frequency/docs/validation-record.md`
- Create: `/Users/vangogh/Desktop/毕设/Haoyu Wang/ae-peak-frequency/python/tests/test_cross_language_contract.py`
- Modify: `/Users/vangogh/Desktop/毕设/Haoyu Wang/ae-peak-frequency/README.md`

**Consumes:** The four generated CSV files and PNG files from Tasks 4–5.

**Produces:** A concise evidence record that separates: Python/Julia agreement, MATLAB comparison, and physical interpretation.

- [ ] **Step 1: Write a cross-language schema test**

```python
def test_python_and_julia_use_identical_event_columns(python_csv, julia_csv):
    python = pd.read_csv(python_csv)
    julia = pd.read_csv(julia_csv)
    assert python.columns.tolist() == julia.columns.tolist()
    assert python.columns.tolist() == [
        "event_id", "file_name", "event_time_s", "peak_rank", "frequency_khz", "magnitude"
    ]
```

- [ ] **Step 2: Add numerical comparison on the synthetic fixture**

```python
assert np.allclose(
    python_events[["event_time_s", "frequency_khz", "magnitude"]],
    julia_events[["event_time_s", "frequency_khz", "magnitude"]],
    rtol=1e-6,
    atol=1e-9,
)
```

- [ ] **Step 3: Run the cross-language test**

Run:

```bash
cd python
python -m pytest tests/test_cross_language_contract.py -v
```

Expected: PASS on the synthetic fixture before comparing real data.

- [ ] **Step 4: Record the real-data comparison honestly**

In `docs/validation-record.md`, record: selected `.mat` files, configuration hash, event counts, CSV row counts, peak-frequency ranges, output paths, package versions, and whether MATLAB comparison was performed.

- [ ] **Step 5: Obtain MATLAB reference evidence before making an equivalence claim**

Run `Peak_Freq.m` in MATLAB with the same selected files and preserve its output figure or exported event data. Add a table with these rows:

```text
Input files | MATLAB event count | Python event count | Julia event count | Result | Explanation
```

Use `Not yet checked` rather than `Equivalent` if MATLAB is unavailable.

- [ ] **Step 6: Update README with the final result boundary**

Include:

```text
Top-3 peak reporting adds frequency observations; it does not by itself validate a material damage classification.
```
