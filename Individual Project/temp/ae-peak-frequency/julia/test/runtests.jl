using Test
using CSV
using DataFrames
using MAT
using Statistics

include("../src/AEPeakFrequency.jl")
using .AEPeakFrequency

const CONFIG = AnalysisConfig(1_000_000, 200, 1, 0.1, 8.0)

@testset "MAT waveform input" begin
    mktempdir() do directory
        path = joinpath(directory, "signal.mat")
        matwrite(path, Dict("data" => [0.0 10.0; 1.0 11.0; -1.0 12.0]))
        @test load_waveform(path) == [0.0, 1.0, -1.0]
    end
end

@testset "CSV summary input" begin
    mktempdir() do directory
        path = joinpath(directory, "summary.csv")
        CSV.write(path, DataFrame(:Column1 => Any["time", 0.0], :Column2 => Any["stress", 10.0]); writeheader=false)
        summary = load_summary(path)
        @test size(summary) == (2, 2)
        @test summary[1, 1] == "time"
    end
end

@testset "adaptive event selection" begin
    signal = zeros(600)
    signal[251:300] .= 0.1 .* sin.(2pi .* (0:49) ./ 20)
    events, threshold = detect_events(signal, CONFIG, :adaptive)
    @test 0.0 < threshold < 0.01
    @test length(events) == 1
    @test events[1].start_sample == 199
end

@testset "Top-3 FFT ranking" begin
    sample = (0:199) ./ 1_000_000
    waveform = 0.8 .* sin.(2pi .* 100_000 .* sample) .+
               0.5 .* sin.(2pi .* 200_000 .* sample) .+
               0.2 .* sin.(2pi .* 300_000 .* sample)
    peaks = ranked_peaks(waveform, 1_000_000, 20.0, 3)
    @test [peak.frequency_khz for peak in peaks] ≈ [100.0, 200.0, 300.0]
end

@testset "MATLAB legacy buffer framing" begin
    frames = matlab_buffer_frames(collect(1.0:400.0), 200, 1)
    @test size(frames) == (200, 2)
    @test sqrt(mean(abs2, frames[:, 1])) ≈ 115.0369505854532
    @test frames[1:3, 1] == [0.0, 1.0, 2.0]
    @test frames[1:3, 2] == [199.0, 200.0, 201.0]
end
