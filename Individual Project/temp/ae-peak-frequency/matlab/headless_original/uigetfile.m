function [file_list, path_n] = uigetfile(varargin)
% Test harness only: supplies Peak_Freq.m with the deterministic T01 inputs.
% The original Peak_Freq.m remains unmodified.

input_dir = '/Users/vangogh/Desktop/毕设/Haoyu Wang/T01';
files = dir(fullfile(input_dir, '*.mat'));
[~, order] = sort({files.name});
files = files(order);
file_list = cell(length(files), 1);
for index = 1:length(files)
    file_list{index} = fullfile(files(index).folder, files(index).name);
end
path_n = input_dir;
end
