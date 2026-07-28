function run_ct07_reference(script_path, workbook_path, output_dir)
% Run the user-normalised CT07.m unchanged and export its numeric workspace.

arguments
    script_path (1, :) char
    workbook_path (1, :) char
    output_dir (1, :) char
end

assert(isfile(script_path), "CT07.m was not found: %s", script_path);
assert(isfile(workbook_path), "Workbook was not found: %s", workbook_path);
source = fileread(script_path);
assert(contains(source, "Commercial Tensile Tests.xlsx"), ...
    "CT07.m still uses the old workbook name; apply the agreed manual edit first.");
assert(contains(source, "'CT07'") || contains(source, '"CT07"'), ...
    "CT07.m still uses the old worksheet name; apply the agreed manual edit first.");

if ~isfolder(output_dir)
    mkdir(output_dir);
end

old_dir = pwd;
old_visibility = get(groot, "defaultFigureVisible");
cleanup = onCleanup(@() restore_environment(old_dir, old_visibility)); %#ok<NASGU>
cd(fileparts(workbook_path));
set(groot, "defaultFigureVisible", "off");
evalin("base", source);
required = ["data", "t1", "strain", "stress", "time", "rms", ...
    "cumrms", "energy", "cumenergy"];
available = string(evalin("base", "who"));
assert(all(ismember(required, available)), ...
    "CT07.m did not create every required numeric workspace variable.");
data = evalin("base", "data");
t1_values = evalin("base", "t1");
strain_values = evalin("base", "strain");
stress_values = evalin("base", "stress");
time_values = evalin("base", "time");
rms_values = evalin("base", "rms");
cumrms_values = evalin("base", "cumrms");
energy_values = evalin("base", "energy");
cumenergy_values = evalin("base", "cumenergy");
assert(size(data, 2) >= 14, "CT07.m data has %d columns; at least 14 are required.", size(data, 2));

mechanical_mask = isfinite(t1_values) & isfinite(strain_values) & isfinite(stress_values);
mechanical_rows = find(mechanical_mask);
mechanical = table( ...
    (1:length(mechanical_rows))', mechanical_rows, ...
    t1_values(mechanical_mask), strain_values(mechanical_mask), stress_values(mechanical_mask), ...
    VariableNames=["record_index", "matrix_row", "t1_s", "strain_pct", "stress_mpa"]);

ae_mask = isfinite(time_values) & isfinite(rms_values) & isfinite(cumrms_values) & ...
    isfinite(energy_values) & isfinite(cumenergy_values);
ae_rows = find(ae_mask);
ae = table( ...
    (1:length(ae_rows))', ae_rows, time_values(ae_mask), rms_values(ae_mask), ...
    cumrms_values(ae_mask), energy_values(ae_mask), cumenergy_values(ae_mask), ...
    VariableNames=["record_index", "matrix_row", "time_s", "rms_norm", ...
    "cumrms_norm", "energy_norm", "cumenergy_norm"]);

writetable(mechanical, fullfile(output_dir, "ct07_mechanical_reference.csv"));
writetable(ae, fullfile(output_dir, "ct07_ae_reference.csv"));
save(fullfile(output_dir, "ct07_reference.mat"), ...
    "data", "t1_values", "strain_values", "stress_values", "time_values", ...
    "rms_values", "cumrms_values", "energy_values", "cumenergy_values", ...
    "mechanical", "ae");

metadata = struct( ...
    "script_path", script_path, ...
    "script_sha256", "23b0b5948faa13dd8ffa340b5741bcfb0aaa741ffa400912890fd9ce0416b784", ...
    "workbook_path", workbook_path, ...
    "workbook_sha256", "89033ea6af74f0b99cfe44a1dcda4e59e4fea709d1f4e4c4acba3745edc33b2d", ...
    "sheet_name", "CT07", ...
    "data_rows", size(data, 1), ...
    "data_columns", size(data, 2), ...
    "mechanical_rows", height(mechanical), ...
    "ae_rows", height(ae), ...
    "matlab_version", version);
fid = fopen(fullfile(output_dir, "ct07_reference_metadata.json"), "w");
assert(fid >= 0, "Could not create CT07 metadata file.");
fprintf(fid, "%s\n", jsonencode(metadata, PrettyPrint=true));
fclose(fid);
close all force;
evalin("base", "clear data t1 strain stress time rms cumrms energy cumenergy");
end

function restore_environment(old_dir, old_visibility)
close all force;
set(groot, "defaultFigureVisible", old_visibility);
cd(old_dir);
end
