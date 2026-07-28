function run_adaptive_peak_freq_export(input_dir, output_dir)
% Deterministic MATLAB reference for per-file adaptive RMS and Top-1/Top-3 FFT peaks.

arguments
    input_dir (1, :) char
    output_dir (1, :) char
end

assert(exist("findpeaks", "file") ~= 0, "findpeaks is required.");
files = dir(fullfile(input_dir, "*.mat"));
assert(~isempty(files), "No MAT files found in %s.", input_dir);
[~, order] = sort({files.name});
files = files(order);
if ~isfolder(output_dir)
    mkdir(output_dir);
end

sample_rate = 1e6;
window_samples = 200;
hop_samples = 199;
sigma_multiplier = 8.0;
frequencies_khz = (0:100)' * (sample_rate / window_samples / 1000);

selected_parts = cell(length(files), 1);
top1_parts = cell(length(files), 1);
top3_parts = cell(length(files), 1);
threshold_parts = cell(length(files), 1);
next_event_id = 1;

for file_index = 1:length(files)
    path = fullfile(files(file_index).folder, files(file_index).name);
    loaded = load(path, "data");
    assert(isfield(loaded, "data") && size(loaded.data, 2) >= 1, ...
        "%s does not contain data(:,1).", path);
    signal = double(loaded.data(:, 1));
    centred = signal - mean(signal);
    starts0 = (0:hop_samples:(length(centred) - window_samples))';
    indices = (1:window_samples)' + starts0';
    frames = centred(indices);
    rms_values = sqrt(mean(frames .^ 2, 1))';
    centre = median(rms_values);
    threshold = centre + sigma_multiplier * 1.4826 * median(abs(rms_values - centre));
    selected_columns = find(rms_values > threshold);
    selected_count = length(selected_columns);

    event_id = (next_event_id:next_event_id + selected_count - 1)';
    start_sample = starts0(selected_columns);
    event_time_s = start_sample / sample_rate;
    selected_rms = rms_values(selected_columns);
    valid_peak_count = zeros(selected_count, 1);
    top1_rows = cell(selected_count, 1);
    top3_rows = cell(selected_count, 1);

    for event_offset = 1:selected_count
        frame = frames(:, selected_columns(event_offset));
        magnitude = abs(fft(frame));
        magnitude = magnitude(1:101);
        [peak_magnitude, peak_frequency] = findpeaks( ...
            magnitude, frequencies_khz, ...
            NPeaks=3, SortStr="descend", MinPeakDistance=20);
        valid_peak_count(event_offset) = length(peak_magnitude);
        if isempty(peak_magnitude)
            continue
        end
        peak_rank = (1:length(peak_magnitude))';
        repeated_event_id = repmat(event_id(event_offset), length(peak_rank), 1);
        repeated_file = repmat(string(files(file_index).name), length(peak_rank), 1);
        repeated_start = repmat(start_sample(event_offset), length(peak_rank), 1);
        repeated_time = repmat(event_time_s(event_offset), length(peak_rank), 1);
        top3_rows{event_offset} = table( ...
            repeated_event_id, repeated_file, repeated_start, repeated_time, ...
            peak_rank, peak_frequency(:), peak_magnitude(:), ...
            VariableNames=["event_id", "file_name", "start_sample", ...
            "event_time_s", "peak_rank", "frequency_khz", "magnitude"]);
        top1_rows{event_offset} = top3_rows{event_offset}(1, :);
    end

    file_names = repmat(string(files(file_index).name), selected_count, 1);
    thresholds = repmat(threshold, selected_count, 1);
    selected_parts{file_index} = table( ...
        event_id, file_names, start_sample, event_time_s, selected_rms, ...
        thresholds, valid_peak_count, ...
        VariableNames=["event_id", "file_name", "start_sample", ...
        "event_time_s", "rms", "threshold", "valid_peak_count"]);
    top1_parts{file_index} = vertcat_nonempty(top1_rows, peak_table());
    top3_parts{file_index} = vertcat_nonempty(top3_rows, peak_table());
    threshold_parts{file_index} = table( ...
        string(files(file_index).name), length(starts0), selected_count, threshold, ...
        VariableNames=["file_name", "candidate_window_count", ...
        "selected_event_count", "threshold"]);
    next_event_id = next_event_id + selected_count;
end

selected_events = vertcat(selected_parts{:});
baseline_events = vertcat(top1_parts{:});
top3_events = vertcat(top3_parts{:});
thresholds = vertcat(threshold_parts{:});
writetable(selected_events, fullfile(output_dir, "selected_events.csv"));
writetable(baseline_events, fullfile(output_dir, "baseline_events.csv"));
writetable(top3_events, fullfile(output_dir, "top3_events.csv"));
writetable(thresholds, fullfile(output_dir, "thresholds.csv"));

metadata = struct( ...
    "mode", "adaptive_matlab_reference", ...
    "input_dir", input_dir, ...
    "input_files", string(fullfile({files.folder}, {files.name})), ...
    "file_count", length(files), ...
    "sampling_rate_hz", sample_rate, ...
    "window_samples", window_samples, ...
    "overlap_samples", 1, ...
    "hop_samples", hop_samples, ...
    "adaptive_sigma_multiplier", sigma_multiplier, ...
    "min_peak_distance_khz", 20, ...
    "selected_event_count", height(selected_events), ...
    "top1_row_count", height(baseline_events), ...
    "top3_row_count", height(top3_events), ...
    "matlab_version", version);
save(fullfile(output_dir, "adaptive_reference.mat"), ...
    "selected_events", "baseline_events", "top3_events", "thresholds", "metadata");
fid = fopen(fullfile(output_dir, "run_metadata.json"), "w");
assert(fid >= 0, "Could not create metadata JSON.");
fprintf(fid, "%s\n", jsonencode(metadata, PrettyPrint=true));
fclose(fid);
end

function result = vertcat_nonempty(parts, empty_table)
keep = ~cellfun(@isempty, parts);
if any(keep)
    result = vertcat(parts{keep});
else
    result = empty_table;
end
end

function result = peak_table()
result = table( ...
    zeros(0, 1), strings(0, 1), zeros(0, 1), zeros(0, 1), ...
    zeros(0, 1), zeros(0, 1), zeros(0, 1), ...
    VariableNames=["event_id", "file_name", "start_sample", "event_time_s", ...
    "peak_rank", "frequency_khz", "magnitude"]);
end
