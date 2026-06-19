using Test

const OUTPUT_DIR = @__DIR__
const EXPECTED_FILES = [
    "figure_1_strain_stress.png",
    "figure_2_rms.png",
    "figure_3_cumulative_rms.png",
    "figure_4_ae_energy.png",
    "figure_5_cumulative_ae_energy.png",
]

function read_be32(bytes::Vector{UInt8})
    return (UInt32(bytes[1]) << 24) |
           (UInt32(bytes[2]) << 16) |
           (UInt32(bytes[3]) << 8) |
           UInt32(bytes[4])
end

function png_dimensions(path::String)
    bytes = read(path)
    @test length(bytes) > 10_000
    @test bytes[1:8] == UInt8[0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]
    @test String(bytes[13:16]) == "IHDR"
    return Int(read_be32(bytes[17:20])), Int(read_be32(bytes[21:24]))
end

@testset "Exactly five valid plot PNGs" begin
    existing_pngs = filter(name -> endswith(lowercase(name), ".png"), readdir(OUTPUT_DIR))
    @test sort(existing_pngs) == sort(EXPECTED_FILES)

    for filename in EXPECTED_FILES
        path = joinpath(OUTPUT_DIR, filename)
        @test isfile(path)
        if isfile(path)
            width, height = png_dimensions(path)
            @test width == 1200
            @test height == 800
        end
    end
end
