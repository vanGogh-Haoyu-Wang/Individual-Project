# Overview of Initial Prompting Methodology

## 1. Objectives of Prompt Engineering
The primary goal of the prompting strategy is to ensure a high-fidelity translation of MATLAB scientific code to Python, adhering to the principle of **functional equivalence**. The strategy focuses on:
- Minimising human intervention during the initial translation phase.
- Ensuring correct handling of 1-based to 0-based indexing.
- Implementing idiomatic Python (e.g., NumPy vectorisation) rather than literal line-by-line translation.

## 2. Structured Prompt Design
To ensure consistency across different LLM platforms (ChatGPT, Claude, DeepSeek, Llama), a standardized prompt structure is employed. This structure consists of four key components:

### 2.1 Persona Selection (Role Setting)
- **Role**: Senior Scientific Computing Engineer.
- **Rationale**: Setting this persona encourages the model to prioritise performance (NumPy), type safety, and adherence to scientific coding standards (PEP-8).

### 2.2 Task Context
- The prompt explicitly mentions the context of an **MSc project** and the domain (**Acoustic Emission Analysis**). This helps the model disambiguate domain-specific terms (e.g., "RMS", "Energy").

### 2.3 Hard Constraints
- **Indexing**: Explicit instruction to handle the MATLAB 1-based indexing shift.
- **Libraries**: Directing the use of `pandas` for data loading and `matplotlib` for visualization.
- **Plotting**: Requirement to use object-oriented plotting (`twinx()`) for dual-axis graphs.

### 2.4 Modularisation & Documentation
- Requirements for clean, modular code and brief explanatory comments for implementation choices.

## 3. Test Case Selection: `CT07.m`
The script `CT07.m` was selected as the initial benchmark because it contains several critical transition points:
- **Excel Data Extraction**: Tests the transition from `xlsread` to `pandas`.
- **Column Slicing**: Tests the model's awareness of 0-based indexing.
- **Dual Y-Axis Figures**: Tests the complexity of recreating MATLAB's `yyaxis` in Matplotlib.
- **Multiple Plot Types**: Includes standard line plots and scatter plots.

---
**Status**: This methodology will be applied to all subsequent translation experiments to maintain the validity of the comparison.
![[CT07.m]]![[Commercial Tensile Tests.xlsx]]

---
 Prompt：
```text
Act as a Senior Scientific Computing Engineer. I am working on an MSc project migrating an Acoustic Emission (AE) analysis framework from MATLAB to an open-source Python environment. 

Your task is to translate the following MATLAB script into Python. 

Requirements & Constraints:

1. Data Loading: Replace MATLAB's `xlsread` with an appropriate Python library (e.g., `pandas`).
2. Array Indexing: Pay strict attention to the 1-based to 0-based indexing conversion between MATLAB and Python. Ensure data slicing is correct.
3. Visualization: Use `matplotlib` (and/or `seaborn`) to replicate the exact plots. Handle MATLAB's `yyaxis left` and `yyaxis right` elegantly using Python's object-oriented plotting approach (e.g., `twinx()`).
4. Readability: Keep the code clean, modular, and PEP-8 compliant. Add brief comments explaining the Python-specific implementation choices.

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
scatter(time, energy, 5, 'filled', 'r')
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
**评判标准（阅卷指南）**

  按照以下标准去寻找它们的“破绽”，并在对比文档中记录：
  
   1. **看索引变没变**：如果 Python 代码里依然是 data[:, 1] 或者 data.iloc[:, 1] 取 t1，**扣分！** 正确的应该是 data.iloc[:, 0] 或者转换为 numpy array 后 data_arr[:, 0]。

   2. **看 pandas 用法**：有没有正确加上 header=None 或者跳过表头？（因为单纯切片 [:, 0] 如果包含了 Excel 表头字符会报错）。

   3. **看绘图对象管理**：好的代码会写出类似这样的结构：

   1    fig2, ax1 = plt.subplots()

   2    ax1.plot(t1, stress, 'b')

   3    ax2 = ax1.twinx()

   4    ax2.plot(time, rms, 'r')

   如果代码乱写一气或者忘记绑定副 Y 轴，说明该模型在绘图 API 掌握上较弱。

---
这个脚本 CT07.m 是一个 MATLAB 数据可视化脚本，主要用于分析材料拉伸试验（Tensile Test）与声发射（Acoustic Emission,
  AE）信号之间的关系。

  简单来说，它的工作就是：读取指定的 Excel 数据，提取力学参数和声发射参数，然后画出 5 张对比图。

  以下是详细的分析：

  1. 它是不是把 Excel 喂给它然后画图？
  是的。 
  脚本的第一行明确指定了输入文件：

   1 data = xlsread("Tensile-processed.xlsx", 'CT-07');
  它会读取当前目录下名为 Tensile-processed.xlsx 的 Excel 文件中名为 CT-07 的工作表。

  2. 工作流程是什么？
  该脚本的工作流程分为三个阶段：

   * 数据导入与提取：
      从 Excel 的特定列中提取数据：
       * 第 3、4 列：应变（Strain）和应力（Stress）。
       * 第 1、5 列：对应的时间轴。
       * 第 9、10 列：声发射的 RMS（均方根值）及其累积值。
       * 第 12、14 列：声发射的能量（Energy）及其累积值。

   * 数据处理：
      脚本中使用了 yyaxis left 和 yyaxis
  right，这意味着它在同一张图上使用了双纵坐标轴。左轴通常显示应力（反映材料受力状态），右轴显示声发射特征（反映内部损伤
  或微裂纹活动）。

   * 图形生成（生成 5 个图窗）：
       1. Fig 1: 标准的应力-应变曲线（Stress vs. Strain）。
       2. Fig 2: 应力与 RMS 随时间的变化（注：此处标题写的是 T09，可能是作者从其他脚本复制过来的笔误）。
       3. Fig 3: 应力与 累积 RMS 随时间的变化。
       4. Fig 4: 应力与 声发射能量 的散点对比图。
       5. Fig 5: 应力与 累积声发射能量 随时间的变化。

  3. 核心用途
  这个脚本的主要目的是研究材料在拉伸过程中何时产生声发射信号。
   * 通过观察 Fig 3 或 Fig 5
     的斜率变化，研究人员可以判断材料何时进入塑性变形阶段，或者何时发生了显著的内部断裂，因为这些通常伴随着累积能量的陡
     增。

  注意事项：
   * 文件依赖：运行此脚本必须确保 Tensile-processed.xlsx 文件位于 MATLAB 的当前工作路径下。
   * 硬编码限制：脚本中有很多硬编码的坐标轴范围（如 ylim([0 520]) 和 xlim([0
     300])），如果你的新数据范围超出了这些值，图片可能会显示不全。
### 1. 运行结果的评价标准 (Evaluation Criteria) 根据方法论笔记，我们制定以下具体评分维度：
1. **索引转换准确性 (Indexing Accuracy)**: 
* **核心指标**: MATLAB 是 1-based，Python 是 0-based。 
* **正确示例**: `data(:, 1)` (第1列) 应转换为 `data.iloc[:, 0]` 或 `data_arr[:, 0]`。 
* **错误示例**: 仍使用 `data.iloc[:, 1]` (这将错误地获取第2列)。 
2. **Pandas 数据加载规范性 (Data Loading)**: 
* **核心指标**: 是否处理了 Excel 表头？ 
* **正确做法**: 使用 `header=None` 或明确跳过表头，防止将列名（字符串）当作数据读取导致 `pd.to_numeric` 报错或数据错位。 
* **错误做法**: 直接读取且未处理表头，导致第一行数据偏移或类型错误。 
3. **绘图 API 掌握程度 (Plotting API Proficiency)**: 
* **核心指标**: 是否使用面向对象 (OO) 接口？双 Y 轴 (`yyaxis`) 是否正确使用 `twinx()` 绑定到同一个 X 轴？ 
* **正确示例**: ```python fig, ax1 = plt.subplots() ax2 = ax1.twinx() ax1.plot(...) ax2.plot(...) ``` 
* **错误做法**: 使用 `plt.plot` 全局状态机混用，或者 `twinx()` 后未正确关联 X 轴范围，导致双轴图错位。 
4. **代码模块化与可读性 (Modularity & Readability)**: 
* **核心指标**: 是否将重复的双轴绘图逻辑封装为函数？是否遵循 PEP-8？