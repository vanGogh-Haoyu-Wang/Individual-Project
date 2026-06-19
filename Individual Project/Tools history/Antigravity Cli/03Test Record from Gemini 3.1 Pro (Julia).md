**User:**
Act as a Senior Scientific Computing Engineer and Julia Specialist. I am working on an MSc project migrating an Acoustic Emission (AE) analysis framework from MATLAB to Julia. Your task is to translate the following MATLAB script into idiomatic Julia. Requirements & Constraints:

1. Data Loading: Use `XLSX.jl` and `DataFrames.jl` to load the "Tensile-processed.xlsx" file. Ensure you read the specific sheet 'CT-07'.
2. Array Indexing: Note that Julia, like MATLAB, uses 1-based indexing. Ensure the column slicing matches the original MATLAB logic correctly (e.g., MATLAB's `data(:, 1)` should be handled appropriately in the context of a DataFrame or Matrix).
3. Broadcasting: Use Julia's broadcasting dot syntax (e.g., `sin.(x)`) for element-wise operations to ensure high performance.
4. Visualization: Use the `Plots.jl` library (with the GR backend). Replicate the dual-axis plots (`yyaxis left` and `yyaxis right`) using `twinx()`. Ensure titles, labels, and limits match the original script.
5. Readability: Keep the code modular. Wrap the logic in a main function or descriptive sub-functions. Add brief comments explaining the Julia-specific implementation choices. Here is the original MATLAB code:

```matlab
data = xlsread("Commercial Tensile Tests", 'CT07'); 
% Selection of specific data from the sheet to be used for plotting 
t1 = data(:, 1);
stress = data(:, 4);
strain = data(:, 3); 
time = data(:,5);
rms = data(:, 9);
cumrms = data(:, 10);
energy = data(:, 12);
cumenergy = data(:, 14);

fig1 = figure; % Strain vs Stress plot
plot(strain, stress, 'b')
ylabel('Stress (MPa)');
xlabel('Strain (%)');
ylim([0 520]);
title('T07 Strain vs. Stress');
grid('minor');

fig2 = figure; 
yyaxis left % Stress vs time plot
plot(t1, stress, 'b')
ylabel('Stress (MPa)');
xlabel('Time (s)');
ylim([0 max(stress)]);
xlim([0 250]);

yyaxis right % Normalised RMS scatter plot
plot(time, rms, 'r')
ylim([0 1.05]);
ylabel('Normalised RMS (a.u.)');
title('T09 Commercial Normalised RMS Profile');
grid('minor');

fig3 = figure;
yyaxis left % Stress vs time plot
plot(t1, stress, 'b')
ylabel('Stress (MPa)');
xlabel('Time (s)');
ylim([0 max(stress)]);
xlim([0 300]);

yyaxis right % Normalised cumulative RMS plot
plot(time, cumrms, 'r')
ylim([0 1.05]);
ylabel('Normalised Cumulative RMS (a.u.)');
title('T07 Commercial Normalised Cumulative RMS');
grid('minor');

fig4 = figure;
yyaxis left % Stress vs time plot
plot(t1, stress, 'b')
ylabel('Stress (MPa)');
xlabel('Time (s)');
ylim([0 max(stress)]);
xlim([0 300]);

yyaxis right % Normalised AE energy plot
scatter(time, energy, markersize=5, markerstrokewidth=0, color=:red)
ylabel('Normalised AE Energy (a.u.)');
ylim([0 1.05]);
title('T07 Commercial Normalised AE Energy');
grid('minor');

fig5 = figure;
yyaxis left % Stress vs time plot
plot(t1, stress, 'b')
ylabel('Stress (MPa)');
xlabel('Time (s)');
ylim([0 max(stress)]);
xlim([0 300]);

yyaxis right % Normalised cumulative AE energy plot
plot(time, cumenergy, 'r')
ylabel('Normalised Cumulative AE Energy (a.u.)');
ylim([0 1.05]);
title('T07 Commercial Normalised Cumulative AE Energy');
grid('minor');
```

**Assistant:**
Here is the translated idiomatic Julia code for your Acoustic Emission framework migration. I have encapsulated the script into a modular function, adhered strictly to your library constraints, and added comments detailing the Julia-specific implementation choices.

```julia
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
function process_acoustic_emission_data(filepath::String="Tensile-processed.xlsx", sheetname::String="CT-07")
    
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
```

### Key Julia Concepts Used:
1. **DataFrames & Matrix Loading**: `XLSX.readxlsx(filepath)[sheetname][:]` reads the data indiscriminately as a matrix like MATLAB's `xlsread`. We wrap it with `DataFrame(..., :auto)` to maintain column-based syntax cleanly. 
2. **Broadcasting**: I used `Float64.(...)` to cast your extracted columns into strict floating-point numbers. In Julia, keeping types strict eliminates overhead and enhances computation performance (as well as preventing `Any` type errors inside the `Plots` library).
3. **`twinx()` instead of `yyaxis`**: Unlike MATLAB which tracks the state natively, `Plots.jl` creates a second axis layer tightly coupled to your first plot (passed as `twinx(fig)`). Any new series plotted on the right side uses a bang function (`plot!` or `scatter!`) mutating that specific twin axis to keep everything in one figure.
4. **DRY code (Don't Repeat Yourself)**: Because 4 out of 5 of your plots use the exact same Stress vs. Time left-axis format, I created an internal helper function called `plot_stress_base(x_data, x_limit)`.

---
# Debug

  
---
# Results
Figure 1  
  
Figure 2  
  
Figure 3  
  
Figure 4  
  
Figure 5  

  
---
# Evaluation:

  
---
# Summary