from pathlib import Path


def test_matlab_legacy_exporter_contract_is_present():
    matlab_dir = Path(__file__).resolve().parents[2] / "matlab"
    exporter = matlab_dir / "run_legacy_peak_freq_export.m"

    assert exporter.is_file()
    source = exporter.read_text(encoding="utf-8")
    assert "dsp.MovingRMS(Len, +1)" in source
    assert "exist('buffer', 'file') ~= 0" in source
    assert "exist('findpeaks', 'file') ~= 0" in source
    assert "legacy_top1_events.csv" in source
    assert "legacy_run_metadata.json" in source
    assert "events_without_valid_peak" in source
    assert "Peak_Freq.m" in source
