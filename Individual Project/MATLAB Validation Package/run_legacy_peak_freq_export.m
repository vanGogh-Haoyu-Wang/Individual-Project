function run_legacy_peak_freq_export(input_dir, output_dir, original_script_path)
% Exportable, deterministic companion to Peak_Freq.m for a licensed machine.
% It retains the legacy calculations and adds only fixed input selection and
% CSV/MAT/JSON output. Run Peak_Freq.m unchanged first as the visual check.

arguments
    input_dir (1, :) char
    output_dir (1, :) char
    original_script_path (1, :) char
end

assert(isfile(original_script_path), "Peak_Freq.m was not found.");
assert(exist('dsp.MovingRMS', 'class') == 8, ...
    "dsp.MovingRMS requires a licensed DSP System Toolbox installation.");
assert(exist('buffer', 'file') ~= 0, ...
    "buffer is unavailable. This legacy script requires its supporting toolbox.");
assert(exist('findpeaks', 'file') ~= 0, ...
    "findpeaks is unavailable. This legacy script requires its supporting toolbox.");

files = dir(fullfile(input_dir, '*.mat'));
assert(~isempty(files), "No MAT files found in input_dir.");
[~, order] = sort({files.name});
files = files(order);

if ~isfolder(output_dir)
    mkdir(output_dir);
end

% This mirrors Peak_Freq.m lines 11-42, with deterministic selected files.
D = [];
file_list = strings(length(files), 1);
for i = 1:length(files)
    filename = fullfile(files(i).folder, files(i).name);
    file_list(i) = string(filename);
    v = load(filename, 'data');
    D = [D; v]; %#ok<AGROW>
end

blank = zeros(1e6, 1);
P = [];
R = [];
for k = 1:length(file_list)
    d = D(k).data(:, 1);
    if k == 1
        avg_D = mean(d);
    end
    adj_data = d - avg_D;
    adj_data = vertcat(adj_data, blank);
    if k == 1
        upthres = max(adj_data);
        lowthres = min(adj_data);
    end
    mask = adj_data < upthres & adj_data > lowthres;
    adj_data(mask) = 0;
    Len = 200;
    movRMS = dsp.MovingRMS(Len, +1);
    y = movRMS(adj_data);
    P = [P; y]; %#ok<AGROW>
    adj = num2cell(buffer(adj_data, 200, 1), 1);
    R = [R, adj(1:end-1)]; %#ok<AGROW>
end

% This mirrors Peak_Freq.m lines 46-74 and adds stable exported columns.
[event_index, ~] = find(P > 0.1);
val = R(event_index);
times = event_index(:) * (200 / 1e6);
E = [];
for ii = 1:length(val)
    event = cell2mat(val(ii));
    e = abs(fft(event));
    E = [E, e(1:100, :)]; %#ok<AGROW>
end

f = 1e6 / 200 * (0:200-1);
f = f(1:100) / 1000;
F1 = [];
I1 = [];
for iii = 1:size(E, 2)
    [lx, fx] = findpeaks(E(:, iii), f, NPeaks=1, ...
        SortStr="descend", MinPeakDistance=20);
    F1 = [F1; fx]; %#ok<AGROW>
    I1 = [I1; lx]; %#ok<AGROW>
end

events = table(event_index(:), times(:), F1(:), I1(:), ...
    VariableNames=["event_index", "time_s", "peak_frequency_khz", "peak_magnitude"]);
writetable(events, fullfile(output_dir, 'legacy_top1_events.csv'));

metadata = struct();
metadata.original_script_path = original_script_path;
metadata.input_dir = input_dir;
metadata.input_files = cellstr(file_list);
metadata.file_count = length(file_list);
metadata.first_file_mean = avg_D;
metadata.upper_extreme = upthres;
metadata.lower_extreme = lowthres;
metadata.window_samples = Len;
metadata.sample_rate_hz = 1e6;
metadata.event_rms_threshold = 0.1;
metadata.event_count = length(event_index);
metadata.top1_row_count = height(events);
metadata.notes = "Computational lines mirror Peak_Freq.m; this companion fixes input selection and exports data only.";
save(fullfile(output_dir, 'legacy_peak_freq_export.mat'), ...
    'events', 'metadata', 'P', 'F1', 'I1', 'times', 'event_index');

fid = fopen(fullfile(output_dir, 'legacy_run_metadata.json'), 'w');
fprintf(fid, '%s\n', jsonencode(metadata, PrettyPrint=true));
fclose(fid);
end
