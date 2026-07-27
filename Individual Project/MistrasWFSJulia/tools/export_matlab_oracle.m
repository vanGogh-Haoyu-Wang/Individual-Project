function export_matlab_oracle()
root = fileparts(fileparts(mfilename('fullpath')));
addpath(fullfile(root, 'upstream', 'matlab'));

[data, t, header] = openWFS(fullfile(root, 'test', 'data', 'ExampleWFSdata.wfs'));
reference = fullfile(root, 'test', 'reference');

fid = fopen(fullfile(reference, 'waveforms.f64le'), 'w', 'ieee-le');
cleanup = onCleanup(@() fclose(fid));
fwrite(fid, data, 'double');
clear cleanup;

fid = fopen(fullfile(reference, 'header.tsv'), 'w');
cleanup = onCleanup(@() fclose(fid));
fprintf(fid, 'field\tvalue\n');
fprintf(fid, 'num_channels\t%d\n', header.NumChannels);
fprintf(fid, 'sample_rate_hz\t%s\n', join(string(header.SampleRate_Hz), ','));
fprintf(fid, 'pretrigger_samples\t%s\n', join(string(header.Pretrigger), ','));
fprintf(fid, 'max_voltage_v\t%s\n', join(string(header.MaxVoltage), ','));
fprintf(fid, 'header_length\t%d\n', header.HeaderLength);
fprintf(fid, 'channel_numbers\t%s\n', join(string(header.ChannelNumbers), ','));
fprintf(fid, 'sample_count\t%d\n', size(data, 2));
fprintf(fid, 'time_start_s\t%.17g\n', t(1));
fprintf(fid, 'time_step_s\t%.17g\n', t(2) - t(1));
fprintf(fid, 'time_end_s\t%.17g\n', t(end));
clear cleanup;

fid = fopen(fullfile(reference, 'waveforms.tsv'), 'w');
cleanup = onCleanup(@() fclose(fid));
fprintf(fid, 'row\tchannel\tmin_mv\tmax_mv\n');
for row = 1:size(data, 1)
    fprintf(fid, '%d\t%d\t%.17g\t%.17g\n', row, header.ChannelNumbers(row), ...
        min(data(row, :)), max(data(row, :)));
end
end
