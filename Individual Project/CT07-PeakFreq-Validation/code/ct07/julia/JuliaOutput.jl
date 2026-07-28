module CT07Output

using CSV
using DataFrames
using JSON3
using Plots

export write_outputs

function dual_plot(mechanical, ae, values, ylabel, title, xmax; scatter=false)
    left = plot(
        mechanical.t1_s,
        mechanical.stress_mpa;
        color=:blue,
        xlabel="Time (s)",
        ylabel="Stress (MPa)",
        xlims=(0, xmax),
        ylims=(0, maximum(mechanical.stress_mpa)),
        title=title,
        minorgrid=true,
        legend=false,
    )
    right = twinx(left)
    plotter = scatter ? scatter! : plot!
    plotter(
        right,
        ae.time_s,
        values;
        color=:red,
        ylabel=ylabel,
        xlims=(0, xmax),
        ylims=(0, 1.05),
        markersize=3,
        legend=false,
    )
    return left
end

function write_outputs(mechanical, ae, output_dir, candidate_id, repairs)
    mkpath(output_dir)
    CSV.write(joinpath(output_dir, "mechanical.csv"), mechanical)
    CSV.write(joinpath(output_dir, "ae.csv"), ae)
    figures = [
        plot(
            mechanical.strain_pct,
            mechanical.stress_mpa;
            color=:blue,
            xlabel="Strain (%)",
            ylabel="Stress (MPa)",
            ylims=(0, 520),
            title="T07 Strain vs. Stress",
            minorgrid=true,
            legend=false,
        ),
        dual_plot(mechanical, ae, ae.rms_norm, "Normalised RMS (a.u.)", "T09 Commercial Normalised RMS Profile", 250),
        dual_plot(mechanical, ae, ae.cumrms_norm, "Normalised Cumulative RMS (a.u.)", "T07 Commercial Normalised Cumulative RMS", 300),
        dual_plot(mechanical, ae, ae.energy_norm, "Normalised AE Energy (a.u.)", "T07 Commercial Normalised AE Energy", 300; scatter=true),
        dual_plot(mechanical, ae, ae.cumenergy_norm, "Normalised Cumulative AE Energy (a.u.)", "T07 Commercial Normalised Cumulative AE Energy", 300),
    ]
    names = [
        "01_strain_stress.png",
        "02_rms.png",
        "03_cumulative_rms.png",
        "04_energy.png",
        "05_cumulative_energy.png",
    ]
    foreach(pair -> savefig(pair[1], joinpath(output_dir, pair[2])), zip(figures, names))
    metadata = Dict(
        "candidate_id" => candidate_id,
        "mechanical_rows" => nrow(mechanical),
        "ae_rows" => nrow(ae),
        "png_count" => length(names),
        "repairs" => repairs,
        "source_inherited_issue" => "Figure 2 title says T09",
    )
    open(joinpath(output_dir, "run_metadata.json"), "w") do io
        JSON3.pretty(io, metadata)
    end
end

end

