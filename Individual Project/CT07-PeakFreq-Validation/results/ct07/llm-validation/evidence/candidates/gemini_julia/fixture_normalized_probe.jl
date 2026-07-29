# Import the required packages
using XLSX
using DataFrames
using Plots

# Set the plotting backend to GR for high performance
gr()

"""
    process_acoustic_emission_data(filepath::String, sheetname::String)

Loads Acoustic Emission data from an Excel file, extracts relevant columns
into a DataFrame, and generates dual-axis plots for analysis.
"""
function process_acoustic_emission_data(filepath::String="Commercial Tensile Tests.xlsx", sheetname::String="CT07")
    
    # ==========================================
    # 1. Data Loading
    # ==========================================
    # Read the raw data from the specified Excel sheet.
    # `xf[sheetname][:]` loads the sheet block into a standard Julia Matrix.
    xf = XLSX.readxlsx(filepath)
    raw_data = xf[sheetname][:]
    
    # Convert the matrix into a DataFrame. 
    # `:auto` provides generic column names (x1, x2, etc.) mimicking MATLAB's generic matrix loading.
    df = DataFrame(raw_data, :auto)

    # ==========================================
    # 2 & 3. Array Indexing and Broadcasting
    # ==========================================
    # Extract columns by their 1-based index, identical to MATLAB `data(:, col)`.
    # We use Julia's broadcasting dot syntax `Float64.(...)` to cast the data element-wise 
    # into strict floating-point arrays, ensuring high performance in downstream plotting.
    t1        = Float64.(df[:, 1])
    strain    = Float64.(df[:, 3])
    stress    = Float64.(df[:, 4])
    time      = Float64.(df[:, 5])
    rms       = Float64.(df[:, 9])
    cumrms    = Float64.(df[:, 10])
    energy    = Float64.(df[:, 12])
    cumenergy = Float64.(df[:, 14])

    max_stress = maximum(stress)

    # Helper function to plot the common left-axis (Stress vs Time) to keep the code modular and DRY
    function plot_stress_base(x_data, x_limit)
        return plot(x_data, stress, 
            color=:blue, 
            ylabel="Stress (MPa)", 
            xlabel="Time (s)",
            ylim=(0, max_stress),
            xlim=x_limit,
            grid=true,
            minorgrid=true, # Equivalent to MATLAB's grid('minor')
            legend=false
        )
    end

    # ==========================================
    # 4. Visualization
    # ==========================================

    # --- Figure 1: Strain vs Stress ---
    fig1 = plot(strain, stress, 
        color=:blue, 
        ylabel="Stress (MPa)", 
        xlabel="Strain (%)",
        ylim=(0, 520),
        title="T07 Strain vs. Stress",
        grid=true,
        minorgrid=true,
        legend=false
    )
    display(fig1)

    # --- Figure 2: Stress vs time / Normalised RMS ---
    fig2 = plot_stress_base(t1, (0, 250))
    # twinx() creates a linked secondary Y-axis overlay (equivalent to `yyaxis right`)
    ax2_fig2 = twinx(fig2) 
    plot!(ax2_fig2, time, rms, 
        color=:red, 
        ylim=(0, 1.05),
        ylabel="Normalised RMS (a.u.)",
        title="T09 Commercial Normalised RMS Profile",
        legend=false
    )
    display(fig2)

    # --- Figure 3: Stress vs time / Normalised Cumulative RMS ---
    fig3 = plot_stress_base(t1, (0, 300))
    ax2_fig3 = twinx(fig3)
    plot!(ax2_fig3, time, cumrms, 
        color=:red, 
        ylim=(0, 1.05),
        ylabel="Normalised Cumulative RMS (a.u.)",
        title="T07 Commercial Normalised Cumulative RMS",
        legend=false
    )
    display(fig3)

    # --- Figure 4: Stress vs time / Normalised AE Energy (Scatter) ---
    fig4 = plot_stress_base(t1, (0, 300))
    ax2_fig4 = twinx(fig4)
    # Note the use of scatter!() with bang (!) to mutate the secondary axis
    scatter!(ax2_fig4, time, energy, 
        markersize=5, 
        markerstrokewidth=0, 
        color=:red,
        ylabel="Normalised AE Energy (a.u.)",
        ylim=(0, 1.05),
        title="T07 Commercial Normalised AE Energy",
        legend=false
    )
    display(fig4)

    # --- Figure 5: Stress vs time / Normalised Cumulative AE Energy ---
    fig5 = plot_stress_base(t1, (0, 300))
    ax2_fig5 = twinx(fig5)
    plot!(ax2_fig5, time, cumenergy, 
        color=:red, 
        ylabel="Normalised Cumulative AE Energy (a.u.)",
        ylim=(0, 1.05),
        title="T07 Commercial Normalised Cumulative AE Energy",
        legend=false
    )
    display(fig5)

    # Return the plot objects in a tuple
    return fig1, fig2, fig3, fig4, fig5
end

# Execute the function
# figs = process_acoustic_emission_data()