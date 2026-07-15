function report = run_legacy_peak_freq_fixed_input(input_file, output_dir)
% Headless audit wrapper for Peak_Freq.m.  It fixes the GUI input only and
% deliberately stops before the original plotting calls if no event exists.

arguments
    input_file (1, :) char
    output_dir (1, :) char
end

if ~isfolder(output_dir)
    mkdir(output_dir);
end

source = load(input_file, 'data');
d = source.data(:, 1);
avg_D = mean(d);
adj_data = d - avg_D;
adj_data = vertcat(adj_data, zeros(1e6, 1));
upthres = max(adj_data);
lowthres = min(adj_data);
mask = adj_data < upthres & adj_data > lowthres;
adj_data(mask) = 0;

Len = 200;
legacy_threshold = 0.1;
max_possible_moving_rms = max(abs(adj_data));
has_dsp_moving_rms = exist('dsp.MovingRMS', 'class') == 8;

if has_dsp_moving_rms
    movRMS = dsp.MovingRMS(Len, +1);
    P = movRMS(adj_data);
    [peaks, ~] = find(P > legacy_threshold);
    status = "completed";
    moving_rms_max = max(P);
    event_count = length(peaks);
    note = "Literal legacy processing completed with DSP System Toolbox.";
else
    % RMS over any window cannot exceed the maximum absolute sample value.
    % This proves no threshold crossing without approximating dsp.MovingRMS.
    assert(max_possible_moving_rms < legacy_threshold);
    status = "verified_without_dsp_toolbox";
    moving_rms_max = [];
    event_count = 0;
    note = "DSP System Toolbox is unavailable. No legacy event is nevertheless mathematically guaranteed because RMS cannot exceed max(abs(filtered_signal)).";
end

report = struct();
report.input_file = input_file;
report.sample_count_before_padding = length(d);
report.sample_count_after_padding = length(adj_data);
report.first_file_mean = avg_D;
report.upper_extreme = upthres;
report.lower_extreme = lowthres;
report.moving_rms_max = moving_rms_max;
report.max_possible_moving_rms = max_possible_moving_rms;
report.legacy_threshold = legacy_threshold;
report.legacy_event_count = event_count;
report.dsp_moving_rms_available = has_dsp_moving_rms;
report.status = status;
if event_count == 0
    report.note = "No events exceed the literal legacy threshold. The original Peak_Freq.m would later fail when plotting max(times) on empty data.";
else
    report.note = "Events were detected; peak-frequency processing has not been changed by this audit wrapper.";
end

save(fullfile(output_dir, 'legacy_peak_freq_report.mat'), 'report');
fid = fopen(fullfile(output_dir, 'legacy_peak_freq_report.json'), 'w');
fprintf(fid, '%s\n', jsonencode(report, PrettyPrint=true));
fclose(fid);
end
