module AEPeakFrequency

using CSV
using DataFrames
using FFTW
using JSON3
using MAT
using Plots
using Statistics
using XLSX

export AnalysisConfig, Event, Peak, load_waveform, load_summary, legacy_extrema_filter,
       adaptive_threshold, detect_events, ranked_peaks, run_analysis,
       matlab_buffer_frames, run_matlab_legacy

struct AnalysisConfig
    sampling_rate_hz::Int
    event_window_samples::Int
    window_overlap_samples::Int
    legacy_rms_threshold::Float64
    adaptive_sigma_multiplier::Float64
end

struct Event
    start_sample::Int
    samples::Vector{Float64}
end

struct Peak
    frequency_khz::Float64
    magnitude::Float64
end

function load_waveform(path::AbstractString)::Vector{Float64}
    raw = matread(path)
    haskey(raw, "data") || throw(ArgumentError("$path does not contain a data variable"))
    data = raw["data"]
    ndims(data) == 2 && size(data, 2) >= 1 || throw(ArgumentError("$path data must have at least one column"))
    return Float64.(data[:, 1])
end

function load_summary(path::AbstractString; sheet_name::Union{Nothing,String}=nothing)::DataFrame
    lowercase(splitext(path)[2]) == ".csv" && return CSV.read(path, DataFrame; header=false)
    lowercase(splitext(path)[2]) == ".xlsx" || throw(ArgumentError("summary input must be .csv or .xlsx"))
    workbook = XLSX.readxlsx(path)
    sheet = isnothing(sheet_name) ? workbook[1] : workbook[sheet_name]
    return DataFrame(XLSX.getdata(sheet), :auto)
end

function legacy_extrema_filter(signal::Vector{Float64})
    minimum_value, maximum_value = minimum(signal), maximum(signal)
    return [value > minimum_value && value < maximum_value ? 0.0 : value for value in signal]
end

function adaptive_threshold(rms::Vector{Float64}, sigma_multiplier::Float64)
    centre = median(rms)
    return centre + sigma_multiplier * 1.4826 * median(abs.(rms .- centre))
end

function _window_starts(signal_length::Int, config::AnalysisConfig)
    hop = config.event_window_samples - config.window_overlap_samples
    return collect(0:hop:(signal_length - config.event_window_samples))
end

function _window_rms(signal::Vector{Float64}, starts::Vector{Int}, window_length::Int)
    return [sqrt(mean(abs2, signal[start + 1:start + window_length])) for start in starts]
end

function detect_events(signal::Vector{Float64}, config::AnalysisConfig, mode::Symbol)
    centred = signal .- mean(signal)
    working = mode == :legacy ? legacy_extrema_filter(centred) : centred
    starts = _window_starts(length(working), config)
    rms = _window_rms(working, starts, config.event_window_samples)
    threshold = mode == :legacy ? config.legacy_rms_threshold :
        mode == :adaptive ? adaptive_threshold(rms, config.adaptive_sigma_multiplier) :
        throw(ArgumentError("mode must be :legacy or :adaptive"))
    events = [Event(start, working[start + 1:start + config.event_window_samples]) for (start, value) in zip(starts, rms) if value > threshold]
    return events, threshold
end

function ranked_peaks(samples::Vector{Float64}, sampling_rate_hz::Int, min_peak_distance_khz::Float64, count::Int)
    magnitudes = abs.(rfft(samples))
    frequencies = collect(0:length(magnitudes)-1) .* (sampling_rate_hz / length(samples) / 1000.0)
    candidates = [i for i in 2:length(magnitudes)-1 if magnitudes[i] > magnitudes[i-1] && magnitudes[i] >= magnitudes[i+1]]
    sort!(candidates; by=i -> magnitudes[i], rev=true)
    selected = Int[]
    for index in candidates
        all(abs(frequencies[index] - frequencies[chosen]) >= min_peak_distance_khz for chosen in selected) || continue
        push!(selected, index)
        length(selected) == count && break
    end
    return [Peak(frequencies[index], magnitudes[index]) for index in selected]
end

function matlab_buffer_frames(signal::Vector{Float64}, window_samples::Int, overlap_samples::Int)
    hop = window_samples - overlap_samples
    padded = vcat(zeros(overlap_samples), signal)
    starts = 1:hop:(length(padded) - window_samples + 1)
    return hcat([padded[start:start + window_samples - 1] for start in starts]...)
end

function run_matlab_legacy(mat_paths::Vector{String}, output_dir::Union{Nothing,String}, config::AnalysisConfig; padding_samples::Int=1_000_000)
    isempty(mat_paths) && throw(ArgumentError("at least one MAT file is required"))
    paths = sort(mat_paths; by=basename)
    first_mean = mean(load_waveform(paths[1]))
    first_working = vcat(load_waveform(paths[1]) .- first_mean, zeros(padding_samples))
    upper_extreme, lower_extreme = maximum(first_working), minimum(first_working)
    rows = NamedTuple[]
    global_frame_offset = 0
    for path in paths
        working = vcat(load_waveform(path) .- first_mean, zeros(padding_samples))
        working[(working .< upper_extreme) .& (working .> lower_extreme)] .= 0.0
        frames = matlab_buffer_frames(working, config.event_window_samples, config.window_overlap_samples)
        rms = [sqrt(mean(abs2, view(frames, :, column))) for column in axes(frames, 2)]
        for frame in findall(value -> value > config.legacy_rms_threshold, rms)
            peaks = ranked_peaks(Vector(view(frames, :, frame)), config.sampling_rate_hz, 20.0, 1)
            isempty(peaks) && continue
            peak = peaks[1]
            event_index = global_frame_offset + frame
            push!(rows, (event_index=event_index, time_s=event_index * config.event_window_samples / config.sampling_rate_hz, peak_frequency_khz=peak.frequency_khz, peak_magnitude=peak.magnitude))
        end
        global_frame_offset += size(frames, 2)
    end
    events = isempty(rows) ? DataFrame(event_index=Int[], time_s=Float64[], peak_frequency_khz=Float64[], peak_magnitude=Float64[]) : DataFrame(rows)
    metadata = Dict(
        "mode" => "matlab_legacy_multifile",
        "input_files" => paths,
        "file_count" => length(paths),
        "first_file_mean" => first_mean,
        "upper_extreme" => upper_extreme,
        "lower_extreme" => lower_extreme,
        "padding_samples" => padding_samples,
        "window_samples" => config.event_window_samples,
        "sample_rate_hz" => config.sampling_rate_hz,
        "event_rms_threshold" => config.legacy_rms_threshold,
        "event_count" => nrow(events),
    )
    if !isnothing(output_dir)
        mkpath(output_dir)
        CSV.write(joinpath(output_dir, "legacy_top1_events.csv"), events)
        open(joinpath(output_dir, "legacy_run_metadata.json"), "w") do io
            JSON3.write(io, metadata)
        end
    end
    return events, metadata
end

const EVENT_COLUMNS = [:event_id, :file_name, :event_time_s, :peak_rank, :frequency_khz, :magnitude]

function _rows(events, path, config, peak_count, first_id)
    rows = NamedTuple[]
    for (offset, event) in enumerate(events)
        for (rank, peak) in enumerate(ranked_peaks(event.samples, config.sampling_rate_hz, 20.0, peak_count))
            push!(rows, (event_id=first_id + offset - 1, file_name=basename(path), event_time_s=event.start_sample / config.sampling_rate_hz, peak_rank=rank, frequency_khz=peak.frequency_khz, magnitude=peak.magnitude))
        end
    end
    return rows
end

function _event_frame(rows)
    isempty(rows) && return DataFrame(event_id=Int[], file_name=String[], event_time_s=Float64[], peak_rank=Int[], frequency_khz=Float64[], magnitude=Float64[])
    return DataFrame(rows)
end

function _plot_events(frame, title, path)
    plot(frame.event_time_s, frame.frequency_khz; seriestype=:scatter, markersize=2, color=:red, legend=false, xlabel="Time (s)", ylabel="Peak Frequency (kHz)", ylims=(0, 500), title=title, grid=true)
    savefig(path)
end

function run_analysis(mat_paths::Vector{String}, output_dir::String, config::AnalysisConfig; summary_path::Union{Nothing,String}=nothing, summary_sheet::Union{Nothing,String}=nothing)
    mkpath(output_dir)
    baseline_rows, top3_rows = NamedTuple[], NamedTuple[]
    thresholds, legacy_counts = Dict{String,Float64}(), Dict{String,Int}()
    next_id = 1
    for path in mat_paths
        signal = load_waveform(path)
        legacy_events, _ = detect_events(signal, config, :legacy)
        events, threshold = detect_events(signal, config, :adaptive)
        legacy_counts[basename(path)] = length(legacy_events)
        thresholds[basename(path)] = threshold
        append!(baseline_rows, _rows(events, path, config, 1, next_id)); append!(top3_rows, _rows(events, path, config, 3, next_id)); next_id += length(events)
    end
    baseline, top3 = _event_frame(baseline_rows), _event_frame(top3_rows)
    CSV.write(joinpath(output_dir, "baseline_events.csv"), baseline); CSV.write(joinpath(output_dir, "top3_events.csv"), top3)
    gr(); _plot_events(baseline, "AE Peak Frequency: Top-1", joinpath(output_dir, "baseline_peak_frequency.png")); _plot_events(top3, "AE Peak Frequency: Top-3", joinpath(output_dir, "top3_peak_frequency.png"))
    summary = isnothing(summary_path) ? nothing : let table=load_summary(summary_path; sheet_name=summary_sheet); Dict("path"=>summary_path, "rows"=>nrow(table), "columns"=>ncol(table), "sheet_name"=>summary_sheet) end
    open(joinpath(output_dir, "run_metadata.json"), "w") do io
        JSON3.write(io, Dict("mode"=>"adaptive", "sampling_rate_hz"=>config.sampling_rate_hz, "event_window_samples"=>config.event_window_samples, "window_overlap_samples"=>config.window_overlap_samples, "adaptive_sigma_multiplier"=>config.adaptive_sigma_multiplier, "thresholds"=>thresholds, "legacy"=>Dict("rms_threshold"=>config.legacy_rms_threshold, "event_counts"=>legacy_counts), "summary"=>summary))
    end
end

end
