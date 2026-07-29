import pandas as pd
import matplotlib.pyplot as plt

def main():
    # ---------------------------------------------------------
    # 1. Data Loading
    # ---------------------------------------------------------
    # In Python, pandas is the standard for loading and manipulating tabular data.
    # Note: Ensure you have pandas and openpyxl installed to read .xlsx files 
    # (e.g., pip install pandas openpyxl matplotlib)
    file_path = "Commercial Tensile Tests.xlsx"
    sheet_name = "CT07"
    
    try:
        # MATLAB's xlsread often skips headers and returns a purely numeric matrix.
        # We use header=None so that the first row isn't incorrectly parsed as column names.
        # If your Excel file does have headers, remove `header=None` and adjust the column indexing.
        data = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
    except FileNotFoundError:
        print(f"Error: Could not find '{file_path}'. Please ensure the file is in the same directory.")
        return

    # ---------------------------------------------------------
    # 2. Array Indexing
    # ---------------------------------------------------------
    # Python uses 0-based indexing, whereas MATLAB uses 1-based indexing.
    # Therefore, we subtract 1 from all the MATLAB column indices.
    # We use `.iloc[:, column_index]` for integer-location based selection.
    t1 = data.iloc[:, 0]         # MATLAB: data(:, 1)
    strain = data.iloc[:, 2]     # MATLAB: data(:, 3)
    stress = data.iloc[:, 3]     # MATLAB: data(:, 4)
    time = data.iloc[:, 4]       # MATLAB: data(:, 5)
    rms = data.iloc[:, 8]        # MATLAB: data(:, 9)
    cumrms = data.iloc[:, 9]     # MATLAB: data(:, 10)
    energy = data.iloc[:, 11]    # MATLAB: data(:, 12)
    cumenergy = data.iloc[:, 13] # MATLAB: data(:, 14)

    # ---------------------------------------------------------
    # 3. Visualization
    # ---------------------------------------------------------
    
    # Figure 1: Strain vs Stress plot
    fig1, ax1 = plt.subplots()
    ax1.plot(strain, stress, 'b')
    ax1.set_ylabel('Stress (MPa)')
    ax1.set_xlabel('Strain (%)')
    ax1.set_ylim([0, 520])
    ax1.set_title('T07 Strain vs. Stress')
    # Replicating MATLAB's grid('minor')
    ax1.minorticks_on()
    ax1.grid(True, which='minor', linestyle=':', alpha=0.6)
    ax1.grid(True, which='major', linestyle='-', alpha=0.8)

    # Figure 2: Stress vs time / Normalised RMS
    # Using ax.twinx() to replicate MATLAB's yyaxis left and right behavior
    fig2, ax2_left = plt.subplots()
    
    # Left Axis (yyaxis left)
    ax2_left.plot(t1, stress, 'b')
    ax2_left.set_ylabel('Stress (MPa)', color='b')
    ax2_left.tick_params(axis='y', labelcolor='b') # Color the ticks to match
    ax2_left.set_xlabel('Time (s)')
    ax2_left.set_ylim([0, stress.max()])
    ax2_left.set_xlim([0, 250])
    
    # Right Axis (yyaxis right)
    ax2_right = ax2_left.twinx()
    ax2_right.plot(time, rms, 'r')
    ax2_right.set_ylabel('Normalised RMS (a.u.)', color='r')
    ax2_right.tick_params(axis='y', labelcolor='r')
    ax2_right.set_ylim([0, 1.05])
    
    ax2_left.set_title('T09 Commercial Normalised RMS Profile')
    ax2_left.minorticks_on()
    ax2_left.grid(True, which='minor', linestyle=':', alpha=0.6)
    ax2_left.grid(True, which='major', linestyle='-', alpha=0.8)

    # Figure 3: Stress vs time / Normalised Cumulative RMS
    fig3, ax3_left = plt.subplots()
    
    ax3_left.plot(t1, stress, 'b')
    ax3_left.set_ylabel('Stress (MPa)', color='b')
    ax3_left.tick_params(axis='y', labelcolor='b')
    ax3_left.set_xlabel('Time (s)')
    ax3_left.set_ylim([0, stress.max()])
    ax3_left.set_xlim([0, 300])
    
    ax3_right = ax3_left.twinx()
    ax3_right.plot(time, cumrms, 'r')
    ax3_right.set_ylabel('Normalised Cumulative RMS (a.u.)', color='r')
    ax3_right.tick_params(axis='y', labelcolor='r')
    ax3_right.set_ylim([0, 1.05])
    
    ax3_left.set_title('T07 Commercial Normalised Cumulative RMS')
    ax3_left.minorticks_on()
    ax3_left.grid(True, which='minor', linestyle=':', alpha=0.6)
    ax3_left.grid(True, which='major', linestyle='-', alpha=0.8)

    # Figure 4: Stress vs time / Normalised AE Energy (Scatter plot)
    fig4, ax4_left = plt.subplots()
    
    ax4_left.plot(t1, stress, 'b')
    ax4_left.set_ylabel('Stress (MPa)', color='b')
    ax4_left.tick_params(axis='y', labelcolor='b')
    ax4_left.set_xlabel('Time (s)')
    ax4_left.set_ylim([0, stress.max()])
    ax4_left.set_xlim([0, 300])
    
    ax4_right = ax4_left.twinx()
    # s=5 parameter controls the area of the scatter points, replicating MATLAB's size parameter
    ax4_right.scatter(time, energy, s=5, c='r') 
    ax4_right.set_ylabel('Normalised AE Energy (a.u.)', color='r')
    ax4_right.tick_params(axis='y', labelcolor='r')
    ax4_right.set_ylim([0, 1.05])
    
    ax4_left.set_title('T07 Commercial Normalised AE Energy')
    ax4_left.minorticks_on()
    ax4_left.grid(True, which='minor', linestyle=':', alpha=0.6)
    ax4_left.grid(True, which='major', linestyle='-', alpha=0.8)

    # Figure 5: Stress vs time / Normalised Cumulative AE Energy
    fig5, ax5_left = plt.subplots()
    
    ax5_left.plot(t1, stress, 'b')
    ax5_left.set_ylabel('Stress (MPa)', color='b')
    ax5_left.tick_params(axis='y', labelcolor='b')
    ax5_left.set_xlabel('Time (s)')
    ax5_left.set_ylim([0, stress.max()])
    ax5_left.set_xlim([0, 300])
    
    ax5_right = ax5_left.twinx()
    ax5_right.plot(time, cumenergy, 'r')
    ax5_right.set_ylabel('Normalised Cumulative AE Energy (a.u.)', color='r')
    ax5_right.tick_params(axis='y', labelcolor='r')
    ax5_right.set_ylim([0, 1.05])
    
    ax5_left.set_title('T07 Commercial Normalised Cumulative AE Energy')
    ax5_left.minorticks_on()
    ax5_left.grid(True, which='minor', linestyle=':', alpha=0.6)
    ax5_left.grid(True, which='major', linestyle='-', alpha=0.8)

    # Automatically adjust subplot parameters to give specified padding
    fig1.tight_layout()
    fig2.tight_layout()
    fig3.tight_layout()
    fig4.tight_layout()
    fig5.tight_layout()

    # Show all plots simultaneously
    plt.show()

if __name__ == '__main__':
    main()
