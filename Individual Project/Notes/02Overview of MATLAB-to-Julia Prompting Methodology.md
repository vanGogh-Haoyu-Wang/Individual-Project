# Overview of MATLAB-to-Julia Prompting Methodology

## 1. Objectives of Prompt Engineering
The primary goal is to achieve a high-fidelity translation of MATLAB scientific code to Julia, adhering to the principle of **functional equivalence** and leveraging Julia's high-performance capabilities. The strategy focuses on:
- **Index Parity**: Leveraging the fact that both MATLAB and Julia utilize 1-based indexing, while ensuring correct syntax for `DataFrames` or `Arrays`.
- **Performance Optimization**: Encouraging the use of Julia's broadcasting (`.`) and type-stable structures to ensure the translated code is JIT-friendly.
- **Idiomatic Julia**: Implementing "Julian" patterns such as multiple dispatch (where applicable) and efficient data handling via `DataFrames.jl`.

## 2. Structured Prompt Design
To ensure consistency across LLMs (GPT-4, Claude 3.5, etc.), a standardized four-component prompt structure is employed:

### 2.1 Persona Selection (Role Setting)
- **Role**: Senior Scientific Computing Engineer and Julia Specialist.
- **Rationale**: This persona directs the model to prioritize performance, mathematical correctness, and the use of the modern Julia ecosystem (e.g., `Plots.jl`, `DataFrames.jl`).

### 2.2 Task Context
- The prompt identifies the environment as an **MSc research project** focused on **Acoustic Emission (AE) Analysis**. This context ensures the model understands scientific units and signal processing terminology.

### 2.3 Hard Constraints
- **Libraries**: Explicitly requiring `XLSX.jl` for data ingestion and `DataFrames.jl` for structured data management.
- **Indexing**: Instructions to maintain 1-based indexing while respecting Julia's slicing syntax (e.g., `df[:, 1]`).
- **Broadcasting**: Requirement to use the dot syntax (`.`) for element-wise operations to mirror MATLAB's vectorized behavior efficiently.
- **Visualization**: Directing the use of `Plots.jl` to replicate dual-axis (`yyaxis`) plots using the `twinx()` functionality.

### 2.4 Modularization & Documentation
- Requirement for clean, function-wrapped code blocks and comments explaining choice of backend (e.g., GR for `Plots.jl`).

## 3. Test Case Selection: `CT07.m`
The script `CT07.m` serves as the benchmark due to:
- **Excel Ingestion**: Tests `XLSX.jl` handling of named sheets and range selection.
- **Matrix vs. DataFrame**: Tests the model's ability to choose between `Matrix{Float64}` and `DataFrame` for scientific plotting.
- **Complex Plotting**: Requires managing multiple subplots and dual-axis synchronization in `Plots.jl`.

---

# Prompt: MATLAB to Julia Migration

```text
Act as a Senior Scientific Computing Engineer and Julia Specialist. I am working on an MSc project migrating an Acoustic Emission (AE) analysis framework from MATLAB to Julia.

Your task is to translate the following MATLAB script into idiomatic Julia.

Requirements & Constraints:

1. Data Loading: Use `XLSX.jl` and `DataFrames.jl` to load the "Tensile-processed.xlsx" file. Ensure you read the specific sheet 'CT-07'.
2. Array Indexing: Note that Julia, like MATLAB, uses 1-based indexing. Ensure the column slicing matches the original MATLAB logic correctly (e.g., MATLAB's `data(:, 1)` should be handled appropriately in the context of a DataFrame or Matrix).
3. Broadcasting: Use Julia's broadcasting dot syntax (e.g., `sin.(x)`) for element-wise operations to ensure high performance.
4. Visualization: Use the `Plots.jl` library (with the GR backend). Replicate the dual-axis plots (`yyaxis left` and `yyaxis right`) using `twinx()`. Ensure titles, labels, and limits match the original script.
5. Readability: Keep the code modular. Wrap the logic in a main function or descriptive sub-functions. Add brief comments explaining the Julia-specific implementation choices.

Here is the original MATLAB code:

data = xlsread("Tensile-processed.xlsx", 'CT-07'); 
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

---

# 评判标准（Julia 版阅卷指南）

按照以下标准去寻找 Julia 代码中的“破绽”，并在对比文档中记录：

1.  **看索引是否维持 1-based**：虽然 MATLAB 和 Julia 都是 1-based，但由于很多模型被 Python 训练得“先入为主”，可能会错误地将 `data(:, 1)` 转换为 `data[:, 0]`。如果出现 0 索引，**扣分！** 同时检查它是否正确处理了 `DataFrame` 的列名或列序号。

2.  **看 XLSX 库的使用**：是否正确使用了 `XLSX.readtable` 或 `XLSX.gettable`？简单的 `XLSX.readxlsx` 只能得到一个文件句柄，需要进一步转换为 `DataFrame` 或 `Matrix` 才能方便切片。

3.  **看广播操作 (`.`)**：Julia 在处理向量化运算或绘图数据时，推荐使用 `.`。例如 `plot(x, y)` 没问题，但如果是中间有数学运算（如归一化），是否使用了 `energy ./ maximum(energy)` 这种 Julian 风格的代码。

4.  **看双 Y 轴实现**：在 `Plots.jl` 中，实现双轴的标准做法是：
    ```julia
    p = plot(t1, stress, ylabel="Stress", color=:blue)
    plot!(twinx(), time, rms, ylabel="RMS", color=:red)
    ```
    检查模型是否混淆了 Python 的 `twinx()` 对象方法和 Julia 的绘图流程。如果它生成了无法运行的伪代码，说明对 Julia 绘图生态掌握不足。

5.  **看类型声明（进阶项）**：优秀的 Julia 代码通常会考虑性能，观察它是否将代码封装在 `function main()` 中，以避免使用全局变量，这对于 Julia 的 JIT 优化至关重要。
