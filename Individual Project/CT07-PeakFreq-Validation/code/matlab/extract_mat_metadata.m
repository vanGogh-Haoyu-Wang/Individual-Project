function extract_mat_metadata(waveform_root, output_csv)
% Export MAT metadata without loading the 5,000,000-sample waveform arrays.

arguments
    waveform_root (1, :) char
    output_csv (1, :) char
end

groups = compose("T%02d", 1:9);
rows = cell(0, 8);
for group_index = 1:numel(groups)
    group = groups(group_index);
    files = dir(fullfile(waveform_root, group, "*.mat"));
    [~, order] = sort({files.name});
    files = files(order);
    for file_index = 1:numel(files)
        path = fullfile(files(file_index).folder, files(file_index).name);
        info = whos("-file", path);
        data_info = info(strcmp({info.name}, "data"));
        assert(numel(data_info) == 1, "%s has no unique data variable", path);
        loaded = load(path, "FS", "RecordStartTime");
        assert(isfield(loaded, "FS"), "%s has no FS variable", path);
        record_start = "";
        if isfield(loaded, "RecordStartTime")
            try
                record_start = string(loaded.RecordStartTime, ...
                    "yyyy-MM-dd'T'HH:mm:ss.SSSSSS");
            catch
                record_start = string(loaded.RecordStartTime);
            end
        end
        filename_time = datetime(erase(files(file_index).name, ".mat"), ...
            "InputFormat", "yyyyMMdd_HHmmss");
        rows(end + 1, :) = {group, string(files(file_index).name), ...
            string(filename_time, "yyyy-MM-dd'T'HH:mm:ss"), ...
            record_start, double(loaded.FS), data_info.size(1), ...
            data_info.size(2), files(file_index).bytes}; %#ok<AGROW>
    end
end

result = cell2table(rows, VariableNames=[ ...
    "group", "file_name", "filename_start_time", "record_start_time", ...
    "sampling_rate_hz", "data_rows", "data_columns", "file_size_bytes"]);
output_dir = fileparts(output_csv);
if ~isempty(output_dir) && ~isfolder(output_dir)
    mkdir(output_dir);
end
writetable(result, output_csv);
end

