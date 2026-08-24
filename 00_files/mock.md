# MSc Introduction to Materials Modelling: 理论全真模拟考试与开卷课件溯源通关宝典 (Theory Mock Exam & Slide Sourcing Guide)

> **课程名称**：Introduction to Materials Modelling (材料建模导论)  
> **适用场景**：期末/补考 线上开卷机考（理论部分 40~50 分打字快速作答）  
> **使用方法**：
> 1. 本卷严格按照任课教授 Dr. Nils Warnken 出题风格、历年真题及 6 周核心理论模块精心编制。
> 2. **开卷课件精准溯源**：每一道题目均明确标明**来自 Week 几、Lecture 几、对应 PDF 讲义文件名、具体幻灯片页码（Slide XX）及 Vault 对应笔记章节链接**，方便开卷时秒速翻找原文！
> 3. 题目全英文（与真实考卷一致）；答案采用**中英结合**——提供**可直接复制修改的英文满分范文（English Model Answer）**、**极速打字要点（Quick Bullets）**以及**中文考点精析与避坑指南**。
> 4. 开卷/在线打字考试时，**切忌死记硬背课件原句**（会被查重/判定死记硬背），请参考本指南中的 **Paraphrase 句式** 作答。

---

## 目录
1. [考前 3 分钟速查：20 大核心物理量/术语黄金匹配表（含课件出处）](#考前-3-分钟速查20-大核心物理量术语黄金匹配表含课件出处)
2. [【全真模拟试卷】Theory Exam Simulation (40 Marks，带精准课件溯源)](#全真模拟试卷theory-exam-simulation-40-marks带精准课件溯源)
   * [Question 1: Philosophy of Modelling & London Tube Map (5 Marks) 【Week 01 / L01】](#question-1-philosophy-of-modelling--london-tube-map-5-marks-week-01--l01)
   * [Question 2: Spatiotemporal Hierarchy & Scaling Relation (4 Marks) 【Week 02 / L03】](#question-2-spatiotemporal-hierarchy--scaling-relation-4-marks-week-02--l03)
   * [Question 3: Empirical vs Analytical vs Numerical Modelling (5 Marks) 【Week 02 / L04】](#question-3-empirical-vs-analytical-vs-numerical-modelling-5-marks-week-02--l04)
   * [Question 4: CALPHAD Method Capabilities & Misconception Analysis (5 Marks) 【Week 03 / L06b】](#question-4-calphad-method-capabilities--misconception-analysis-5-marks-week-03--l06b)
   * [Question 5: Solidification Models: Equilibrium vs Scheil-Gulliver (6 Marks) 【Week 04 / L07】](#question-5-solidification-models-equilibrium-vs-scheil-gulliver-6-marks-week-04--l07)
   * [Question 6: Microsegregation & Superalloy Heat Treatment Window Design (5 Marks) 【Week 04 / L08】](#question-6-microsegregation--superalloy-heat-treatment-window-design-5-marks-week-04--l08)
   * [Question 7: Thermodynamic Driving Force & Darken's Uphill Diffusion (5 Marks) 【Week 05 / L09】](#question-7-thermodynamic-driving-force--darkens-uphill-diffusion-5-marks-week-05--l09)
   * [Question 8: Chained Modelling Workflow (Equilibrium ➔ Scheil ➔ DICTRA) (5 Marks) 【综合跨模块】](#question-8-chained-modelling-workflow-equilibrium--scheil--dictra-5-marks-综合跨模块)
3. [【重点理论扩展题库】High-Yield Modular Question Bank（带精准课件溯源）](#重点理论扩展题库high-yield-modular-question-bank带精准课件溯源)
   * [Bank 1: Euler ODE Numerical Stability & Timestep Limit Criterion 【Week 01 / L02a】](#bank-1-euler-ode-numerical-stability--timestep-limit-criterion-week-01--l02a)
   * [Bank 2: Discretization Methods (FDM vs CVM/FVM vs FEM) 【Week 02 / L02c】](#bank-2-discretization-methods-fdm-vs-cvmfvm-vs-fem-week-02--l02c)
   * [Bank 3: 8 Microstructure Modelling Methods Comparison 【Week 02 / L04】](#bank-3-8-microstructure-modelling-methods-comparison-week-02--l04)
   * [Bank 4: Gibbs Free Energy Models: Ideal ➔ Regular ➔ R-K ➔ CEF Sublattice 【Week 03 / L06a, L06b】](#bank-4-gibbs-free-energy-models-ideal--regular--r-k--cef-sublattice-week-03--l06a-l06b)
   * [Bank 5: Microstructure Modification: Al-Si-Mg-Fe Alloy with Mn Addition 【Week 04 / L08】](#bank-5-microstructure-modification-al-si-mg-fe-alloy-with-mn-addition-week-04--l08)
   * [Bank 6: Moving Phase Interface (Stefan Condition) & Geometry Selection in DICTRA 【Week 05 / L09】](#bank-6-moving-phase-interface-stefan-condition--geometry-selection-in-dictra-week-05--l09)
4. [打字考试通用防查重 Paraphrase 句型库](#打字考试通用防查重-paraphrase-句型库)

---

# 考前 3 分钟速查：20 大核心物理量/术语黄金匹配表（含课件出处）

> **考试高频第一大题（表格填空/术语匹配）：** 开卷时直接在此表按名称查找对应的符号、单位、尺度与课件精准出处！

| 序号 | 物理量 / 概念 (Terminology) | 常用符号 (Symbol) | 标准单位 (Unit) | 物理意义与关联模型 / 尺度 | 精准课件来源 (Week / Lecture / Slide) | 对应笔记链接 |
| :---: | :--- | :---: | :--- | :--- | :--- | :--- |
| **1** | 独立变量 (Independent Variable) | $t, x$ | $\text{s}, \text{m}$ | 用户自由输入/网格划分变量（时间、空间坐标） | **Week 01** `L02a` Slide 27-28 | [[66_notes/Introduction to Materials Modelling/Note/Note01wk1.md#3-第二部分模型的四大核心组成要素four-core-components-of-a-model\|Note01wk1 §3]] |
| **2** | 因变量 (Dependent Variable) | $N_A, c, G, T$ | $\text{mol}, \text{wt}\%, \text{J/mol}, \text{K}$ | 模型控制方程求解输出的目标变量 | **Week 01** `L02a` Slide 27-28 | [[66_notes/Introduction to Materials Modelling/Note/Note01wk1.md#3-第二部分模型的四大核心组成要素four-core-components-of-a-model\|Note01wk1 §3]] |
| **3** | 材料参数 (Material Parameter) | $\tau, D, \kappa$ | $\text{s}, \text{m}^2/\text{s}, \text{W/(m}\cdot\text{K)}$ | 材料固有物理属性（特征时间常数、扩散系数、导热率） | **Week 01** `L02a` Slide 28 | [[66_notes/Introduction to Materials Modelling/Note/Note01wk1.md#3-第二部分模型的四大核心组成要素four-core-components-of-a-model\|Note01wk1 §3]] |
| **4** | 数值参数 (Numerical Parameter) | $\Delta t, \Delta x$ | $\text{s}, \text{m}$ | 纯离散算法参数（步长、网格），影响精度与数值稳定性 | **Week 01** `L02a` Slide 31; `L02c` | [[66_notes/Introduction to Materials Modelling/Note/Note01wk1.md#6-第五部分数值稳定性与时间步长深度剖析numerical-stability--timestep-analysis\|Note01wk1 §6]] |
| **5** | 吉布斯自由能 (Gibbs Free Energy) | $G, G_m$ | $\text{J}, \text{J/mol}$ | CALPHAD 体系核心热力学势，$G = H - TS$，平衡态极小化 | **Week 03** `L06a` Slide 4-15; `L06b` | [[66_notes/Introduction to Materials Modelling/Note/Note03wk3.md#3-第二部分相平衡热力学与公切线法则thermodynamics-of-alloys--common-tangent-construction\|Note03wk3 §3]] |
| **6** | 化学势 (Chemical Potential) | $\mu_i$ | $\text{J/mol}$ | 偏摩尔自由能 $\mu_i = (\partial G/\partial N_i)$，扩散第一性驱动力 | **Week 03** `L06b` Slide 22; **Week 05** `L09` | [[66_notes/Introduction to Materials Modelling/Note/Note03wk3.md#5-第四部分热力学偏导数网络与-calphad-方法论体系thermodynamic-derivatives--calphad-databases\|Note03wk3 §5]] |
| **7** | 分配系数 (Partition Coefficient) | $k$ | 无量纲 (Dimensionless) | 固/液相界面局部平衡浓度比 $k = C_s^* / C_l^*$ | **Week 04** `L07` Slide 5 | [[66_notes/Introduction to Materials Modelling/Note/Note04wk4.md#2-第一部分凝固科学基础与微观偏析机理solidification-science--microsegregationcoring\|Note04wk4 §2]] |
| **8** | 扩散通量 (Diffusion Flux) | $J, j$ | $\text{mol}/(\text{m}^2\cdot\text{s})$ 或 $\text{kg}/(\text{m}^2\cdot\text{s})$ | 单位时间流经单位面积的溶质质量/摩尔量 | **Week 05** `L09` Slide 14 | [[66_notes/Introduction to Materials Modelling/Note/Note05wk5.md#2-第一部分宏观现象学扩散理论与-fick-定律phenomenological-diffusion--ficks-laws\|Note05wk5 §2]] |
| **9** | 扩散系数 (Diffusivity) | $D$ | $\text{m}^2/\text{s}$ | 描述原子跃迁扩散迁移快慢，$D = D_0 \exp(-Q/RT)$ | **Week 05** `L09` Slide 15-16 | [[66_notes/Introduction to Materials Modelling/Note/Note05wk5.md#3-第二部分微观原子尺度跳跃机制与-arrhenius-温度依赖性atomistic-diffusion-mechanisms--arrhenius-kinetics\|Note05wk5 §3]] |
| **10** | 扩散激活能 (Activation Energy) | $Q$ | $\text{J/mol}$ 或 $\text{kJ/mol}$ | 原子克服点阵势垒跃迁所需的能量障碍 | **Week 05** `L09` Slide 16-17 | [[66_notes/Introduction to Materials Modelling/Note/Note05wk5.md#3-第二部分微观原子尺度跳跃机制与-arrhenius-温度依赖性atomistic-diffusion-mechanisms--arrhenius-kinetics\|Note05wk5 §3]] |
| **11** | 亚点阵占位分数 (Site Fraction) | $y_i^{(s)}$ | 无量纲 ($0 \le y_i \le 1$) | 化合物能量形式 (CEF) 描述有序相/间隙固溶体占位 | **Week 03** `L06b` Slide 18-20 | [[66_notes/Introduction to Materials Modelling/Note/Note03wk3.md#4-第三部分吉布斯自由能数学模型体系演进thermodynamic-solution-models-ideal-regular-r-k--cef\|Note03wk3 §4.4]] |
| **12** | 自由度 (Degrees of Freedom) | $F$ | 无量纲整数 | 吉布斯相律 $F = C - P + 2$ (恒压下为 $C - P + 1$) | **Week 03** `L05a` Slide 10 | [[66_notes/Introduction to Materials Modelling/Note/Note03wk3.md#2-第一部分相平衡热力学与相平衡基本定律phase-diagrams--phase-stability-basics\|Note03wk3 §2]] |
| **13** | 相互作用参数 (Interaction Parameter) | $\Omega$ 或 $L_{ij}$ | $\text{J/mol}$ | 正规溶液/R-K多项式中描述不同原子对亲疏作用的参数 | **Week 03** `L06a` Slide 16; `L06b` Slide 8-12 | [[66_notes/Introduction to Materials Modelling/Note/Note03wk3.md#4-第三部分吉布斯自由能数学模型体系演进thermodynamic-solution-models-ideal-regular-r-k--cef\|Note03wk3 §4.2]] |
| **14** | 界面迁移速度 (Interface Velocity) | $v, v_{\text{int}}$ | $\text{m/s}$ 或 $\mu\text{m/s}$ | DICTRA 移动界面/Stefan 条件计算得出的相边界推移速度 | **Week 05** `L09` Slide 43-46 | [[66_notes/Introduction to Materials Modelling/Note/Note05wk5.md#6-第五部分移动相界面动力学沉淀相生长与几何坐标系选择moving-interface-kinetics-precipitate-growth--coordinate-geometries\|Note05wk5 §6]] |
| **15** | 固相体积分数 (Solid Fraction) | $f_s, f_S$ | 无量纲 ($0 \sim 1$) | 凝固过程中固相所占的体积分数或质量分数 | **Week 04** `L07` Slide 6-12 | [[66_notes/Introduction to Materials Modelling/Note/Note04wk4.md#3-第二部分scheil-gulliver-非平衡凝固模型数学推导与边界极限对比the-scheil-model-derivation--limiting-cases\|Note04wk4 §3]] |
| **16** | 弛豫时间/时间常数 (Relaxation Time) | $\tau$ | $\text{s}$ (秒) | 物理系统恢复平衡的特征时间，欧拉稳定性上限 $\Delta t < \tau$ | **Week 01** `L02a` Slide 31-33; `Pwk1` | [[66_notes/Introduction to Materials Modelling/Note/Note01wk1.md#6-第五部分数值稳定性与时间步长深度剖析numerical-stability--timestep-analysis\|Note01wk1 §6]] |
| **17** | 密度泛函理论 (DFT) | DFT | 电子尺度 ($10^{-10}\text{ m}$) | 求解薛定谔方程，获得 0 K 下基态电子密度与晶格常数 | **Week 02** `L03` Slide 11, 17 | [[66_notes/Introduction to Materials Modelling/Note/Note02wk2.md#4-第三部分材料多尺度模型层级架构materials-model-hierarchy--multiscale-modelling\|Note02wk2 §4]] |
| **18** | 分子动力学 (MD) | MD | 原子尺度 ($10^{-9}\text{ m}, 10^{-12}\text{ s}$) | 牛顿力学，模拟原子轨迹、空位跃迁与位错形核 | **Week 02** `L03` Slide 11; **Week 05** `L09` | [[66_notes/Introduction to Materials Modelling/Note/Note02wk2.md#4-第三部分材料多尺度模型层级架构materials-model-hierarchy--multiscale-modelling\|Note02wk2 §4]] |
| **19** | 相场法 (Phase Field) | PF | 介观尺度 ($10^{-6}\text{ m}$) | 连续弥散界面场变量（序参量），模拟枝晶生长与相变 | **Week 02** `L04` Slide 30-36 | [[66_notes/Introduction to Materials Modelling/Note/Note02wk2.md#6-第五部分三大建模范式与八大微观组织建模方法精析8-microstructure-modelling-methods\|Note02wk2 §6.2]] |
| **20** | 有限元法 (FEM) | FEM | 宏观构件尺度 ($10^{-3} \sim 1\text{ m}$) | 离散弱形式变分方程，求解构件温度场、应力应变与变形 | **Week 02** `L02c` Slide 18-24; `L03` | [[66_notes/Introduction to Materials Modelling/Note/Note02wk2.md#3-第二部分空间与时间离散化数值方法深度剖析numerical-discretization-fdm-cvm-fem\|Note02wk2 §3.3]] |

---

# 【全真模拟试卷】Theory Exam Simulation (40 Marks，带精准课件溯源)

---

### Question 1: Philosophy of Modelling & London Tube Map (5 Marks) 【Week 01 / L01】

> 📍 **精准课件与考点出处 (Slide & Note Sourcing)**:
> * **所属周次与讲次**：Week 01 — Lecture 01 (What is a Model?)
> * **官方课件 PDF**：`L01_whatIsAModel_MSc_MaterialsModelling.pdf` (Slide 2 至 Slide 11)
> * **复习全景笔记**：[[66_notes/Introduction to Materials Modelling/Note/Note01wk1.md#2-第一部分什么是模型模型的哲学与核心定义what-is-a-model|Note01wk1 §2（模型哲学定义）]]、[[66_notes/Introduction to Materials Modelling/Week01/Lecture 01.md|Week 01 Lecture 01]]
> * **历年真题对应**：[[66_notes/Introduction to Materials Modelling/Week06/MSc(PG) Introduction to Materials Modelling.md|MSc(PG) Exam]] Example 1 [5 Marks]

**Exam Prompt:**
> "‘Every model captures specific aspects of reality’. Explain the strengths and weaknesses of models in general and select one example to illustrate your explanation." [5 Marks]

#### 1. English Model Answer (Ready-to-Type in Exam)
A model is a purposeful, simplified mathematical or conceptual representation of a complex physical reality. 

* **Strengths:**
  1. **Selective Abstraction & Efficiency:** By deliberately filtering out non-essential complexities, models make intractable physical systems computationally and analytically solvable.
  2. **Predictive Capability & Insight:** Models allow us to explore parameter spaces, understand underlying governing mechanisms, and predict behavior under conditions that are hazardous, expensive, or impossible to test experimentally.
* **Weaknesses:**
  3. **Loss of Information:** Simplifications inherently mean that certain real-world phenomena are neglected, which introduces systematic approximation errors.
  4. **Domain Limitation (Extrapolation Risk):** A model is only valid within the range of its underlying assumptions; applying it outside its calibrated domain leads to incorrect predictions.
* **Illustrative Example (The London Underground Map):**
  * The London Tube map simplifies reality by preserving topological connectivity, station order, and line intersections while discarding geographic fidelity (true curves, exact distances, and surface topography).
  * *Strength:* Passengers can quickly navigate routes across London without cognitive overload.
  * *Weakness:* It cannot be used to estimate walking distances between adjacent surface street locations because physical spatial distances are distorted.

#### 2. 中文考点精析与得分关键点
* **得分点 1（定义与本质，1分）**：指出模型是“有目的的简化”（Purposeful simplification），而非现实的完美复刻（课件 `L01` Slide 3）。
* **得分点 2（优点，1分）**：降低计算复杂度（Computationally manageable）、提供物理洞察（Physical insight）、节约实验成本（Predictive power）。
* **得分点 3（缺点/局限，1分）**：丢失细节引入误差（Loss of fidelity）、受制于假设边界（Valid only within assumptions）、外推风险（Extrapolation danger）。
* **得分点 4（经典案例阐述，2分）**：结合 Dr. Nils 课上重点举例的 **伦敦地铁图 London Tube Map**（`L01` Slide 8-10），指出它**保留了拓扑连接关系**，**忽略了真实地理空间距离**及其优缺点。

#### 3. 极速打字要点 (Quick Bullets)
* Definition: A model is a simplified representation of reality designed to capture specific target phenomena.
* Strengths: Simplifies complex systems; fast and cost-effective prediction; provides mechanistic insight.
* Weaknesses: Neglects secondary details; valid only within strict boundary assumptions; risks error upon extrapolation.
* Example: London Tube map retains connectivity/interchanges for easy navigation, but ignores true geographic scale/distances.

---

### Question 2: Spatiotemporal Hierarchy & Scaling Relation (4 Marks) 【Week 02 / L03】

> 📍 **精准课件与考点出处 (Slide & Note Sourcing)**:
> * **所属周次与讲次**：Week 02 — Lecture 03 (Materials Model Hierarchy & Multiscale Modelling)
> * **官方课件 PDF**：`L03_modelHirachy_MSc_MaterialsModelling.pdf` (Slide 5 至 Slide 11, Slide 16-18)
> * **复习全景笔记**：[[66_notes/Introduction to Materials Modelling/Note/Note02wk2.md#4-第三部分材料多尺度模型层级架构materials-model-hierarchy--multiscale-modelling|Note02wk2 §4（多尺度模型层级）]]、[[66_notes/Introduction to Materials Modelling/Week02/Lecture 03.md|Week 02 Lecture 03]]
> * **历年真题对应**：[[66_notes/Introduction to Materials Modelling/Week06/MSc(PG) Introduction to Materials Modelling.md|MSc(PG) Exam]] Example 2 [3-4 Marks]

**Exam Prompt:**
> "How does the characteristic time scale of materials models change when the characteristic length scale increases? Explain the underlying physical reasons and give two examples from different levels of the hierarchy." [4 Marks]

#### 1. English Model Answer (Ready-to-Type in Exam)
As the characteristic length scale ($L$) of a materials model increases, the characteristic time scale ($t$) increases dramatically (often by multiple orders of magnitude).

* **Underlying Physical Reasons:**
  1. **Transport & Propagation Kinetics:** Most fundamental physical processes in materials (such as heat transfer, mass diffusion, and wave propagation) are transport-controlled. For diffusive processes governed by parabolic equations, the characteristic time scales with the square of the length scale ($t \approx L^2 / D$). Larger spatial dimensions physically require substantially longer durations for mass, momentum, or thermal energy to traverse the system.
  2. **Collective Atomistic Interactions:** Microscopic processes (like atomic vibration or vacancy hopping) occur locally on ultra-short timescales, whereas macroscopic phenomena (like grain growth or phase homogenization) require the cumulative, cooperative movement of trillions of atoms across macroscopic distances.
* **Hierarchical Examples:**
  * **Atomistic Scale (Molecular Dynamics / MD):** Length scale $\sim 10^{-9}\text{ m}$ (nm), time scale $\sim 10^{-15} - 10^{-12}\text{ s}$ (femtoseconds to picoseconds), simulating individual atomic vibrations and single jump events (`L03` Slide 11).
  * **Macroscale (Finite Element Method / FEM):** Length scale $\sim 10^{-3} - 1\text{ m}$ (mm to meters), time scale $\sim 10^{0} - 10^{6}\text{ s}$ (seconds to days/years), simulating macroscopic component heat treatment, casting solidification, or creep deformation (`L03` Slide 11).

#### 2. 中文考点精析与得分关键点
* **得分点 1（尺度变化规律，1分）**：时间尺度随空间尺度的增加而急剧增大（`L03` Slide 7 图表）。
* **得分点 2（物理机制解释，1.5分）**：写出扩散/传热本构关系 $t \approx L^2 / D$（传输时间与距离平方成正比）；微观单次跃迁快，宏观组织演化需要万亿原子协同位移。
* **得分点 3（两级层级举例，1.5分）**：MD（纳米/皮秒，单原子跃迁）vs FEM（毫米~米/秒~天，构件热处理与凝固）。

---

### Question 3: Empirical vs Analytical vs Numerical Modelling (5 Marks) 【Week 02 / L04】

> 📍 **精准课件与考点出处 (Slide & Note Sourcing)**:
> * **所属周次与讲次**：Week 02 — Lecture 04 & Lecture 10 (Microstructure Modelling Methods)
> * **官方课件 PDF**：`L04_MicrostructureModellingMethods.pdf` (Slide 11 至 Slide 15)
> * **复习全景笔记**：[[66_notes/Introduction to Materials Modelling/Note/Note02wk2.md#6-第五部分三大建模范式与八大微观组织建模方法精析8-microstructure-modelling-methods|Note02wk2 §6.1（三大范式对比）]]、[[66_notes/Introduction to Materials Modelling/Note/Note06wk6.md#核心考题-5经验统计模型-vs-物理模型深度对比-5-marks|Note06wk6 考题5]]

**Exam Prompt:**
> "Compare Empirical (Statistical), Analytical Physical, and Numerical Physical models in materials science in terms of their physical basis, computational cost, adaptability to complex conditions, and extrapolation reliability." [5 Marks]

#### 1. English Model Answer (Ready-to-Type in Exam)

| Criteria                      | 1. Empirical / Statistical Models (e.g., Artificial Neural Networks)      | 2. Analytical Physical Models (e.g., Classical Diffusion Equations)                       | 3. Numerical Physical Models (e.g., DICTRA, Phase-Field, FEM)                             |
| :---------------------------- | :------------------------------------------------------------------------ | :---------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------- |
| **Physical Basis**            | None ("Black-box" data fitting; maps inputs to outputs via statistics).   | Strong (Derived strictly from physical laws, e.g., Fick's laws, conservation).            | Strong (Discretizes exact physical governing partial differential equations).             |
| **Computational Cost**        | Extremely low / Instantaneous after initial training.                     | Very low (Direct evaluation of closed-form mathematical equations).                       | Moderate to Very High (Requires iterative spatiotemporal stepping).                       |
| **Complex Conditions**        | Poor (Cannot handle complex geometry or shifting multi-phase equilibria). | Very Poor (Requires severe simplifying assumptions like constant $D$, 1D, semi-infinite). | Excellent (Handles complex multicomponent thermodynamics, moving boundaries, 2D/3D).      |
| **Extrapolation Reliability** | Terrible (Unphysical and dangerous outside the calibrated training data). | Good within its simplified physical assumptions.                                          | High (Physically sound and predictive across broad compositional and temperature ranges). |

* **Summary Takeaway:** Empirical models offer fast interpolation without physical insight; Analytical physical models give deep fundamental insight for oversimplified ideal cases; Numerical physical models provide the predictive power needed for realistic, complex industrial materials engineering.

#### 2. 中文考点精析与得分关键点
* **经验模型（1.5分）**：黑盒无物理（No physics）、快速拟合、严禁外推（课件 `L04` Slide 13）。
* **解析物理模型（1.5分）**：物理闭式精确解（Exact solution）、计算快、但过度简化无法处理复杂工业合金（`L04` Slide 14）。
* **数值物理模型（1.5分）**：时空离散求解 PDE（Discretization）、可预测复杂多元多相工业问题、计算耗时大（`L04` Slide 15）。
* **结构规范度（0.5分）**：采用表格横向对比，得分效率最高。

---

### Question 4: CALPHAD Method Capabilities & Misconception Analysis (5 Marks) 【Week 03 / L06b】

> 📍 **精准课件与考点出处 (Slide & Note Sourcing)**:
> * **所属周次与讲次**：Week 03 — Lecture 05 (The CALPHAD Method)
> * **官方课件 PDF**：`L06b_CALPHADmethod_MSc_MaterialsModelling.pdf` (Slide 21 至 Slide 33)
> * **复习全景笔记**：[[66_notes/Introduction to Materials Modelling/Note/Note03wk3.md#5-第四部分热力学偏导数网络与-calphad-方法论体系thermodynamic-derivatives--calphad-databases|Note03wk3 §5（CALPHAD数据库体系）]]、[[66_notes/Introduction to Materials Modelling/Note/Note06wk6.md#经典考题-7参考-example-3-5-marks|Note06wk6 考题7]]
> * **历年真题对应**：[[66_notes/Introduction to Materials Modelling/Week06/MSc(PG) Introduction to Materials Modelling.md|MSc(PG) Exam]] Example 3 [5 Marks]

**Exam Prompt:**
> "Discuss the statement: 'CALPHAD calculations, and in particular Thermo-Calc, can only do calculations for up to three components. This is the main limitation of the CALPHAD method.' Is this statement true or false? Explain the thermodynamic principles of CALPHAD databases and extrapolation." [5 Marks]

#### 1. English Model Answer (Ready-to-Type in Exam)
**The statement is completely FALSE.**

* **1. Rebuttal of the Misconception:**
  * Modern CALPHAD calculations and Thermo-Calc can easily perform thermodynamic equilibrium calculations for complex industrial alloys containing **10 to 30 chemical components** (e.g., commercial nickel-base superalloys with 15+ elements: Ni-Cr-Co-Al-Ti-Mo-W-Ta-Re-Ru-C-B-Zr).
  * The misconception arises because **visual graphical phase diagrams** are limited to 2D (binary) or 3D (ternary projections) due to human visual perception limitations. However, numerical thermodynamic equilibrium calculations operate purely in multi-dimensional hyperspace without graphical constraints.

* **2. Core Thermodynamic Mechanism: Database Hierarchy & Extrapolation:**
  * CALPHAD does not require experimental data for the full multicomponent system simultaneously.
  * Instead, it builds thermodynamic databases by rigorously assessing and optimizing Gibbs free energy functions ($G$) for **unary (pure elements), binary ($i-j$), and ternary ($i-j-k$) systems** using experimental phase equilibrium data and DFT calculations (`L06b` Slide 25-28).
  * For higher-order systems (quaternary and beyond), CALPHAD uses geometric extrapolation models (such as Muggianu, Kohler, or Redlich-Kister polynomials) to combine binary and ternary interaction parameters ($L_{ij}, L_{ijk}$).
  * **Physical Justification:** Multi-body atomic collisions (e.g., four or five distinct solute atoms interacting simultaneously at a single lattice site) are statistically negligible. Therefore, higher-order interactions ($L_{ijkl} \approx 0$) can be safely omitted without sacrificing accuracy.

#### 2. 中文考点精析与得分关键点
* **得分点 1（判断正误，1分）**：明确指出说法完全错误（Completely false）。
* **得分点 2（澄清误解根源，1分）**：说明“只能三元”是 2D/3D 图形可视化受限，而非数值计算能力受限（`L06b` Slide 23）。
* **得分点 3（数据库构建与外推，2分）**：数据库基于单组元、二元和三元的评估优化，通过几何模型外推到 10~30 组元（`L06b` Slide 28）。
* **得分点 4（外推物理合理性，1分）**：高阶多体碰撞概率极低，四体及以上相互作用参数可忽略不计（$L_{ijkl} \approx 0$）。

---

### Question 5: Solidification Models: Equilibrium vs Scheil-Gulliver (6 Marks) 【Week 04 / L07】

> 📍 **精准课件与考点出处 (Slide & Note Sourcing)**:
> * **所属周次与讲次**：Week 04 — Lecture 06 & Lecture 07 (Scheil-Gulliver Solidification Model)
> * **官方课件 PDF**：`L07_calculationOfPhaseDiagram_ScheilModel.pdf` (Slide 4 至 Slide 22)
> * **复习全景笔记**：[[66_notes/Introduction to Materials Modelling/Note/Note04wk4.md#3-第二部分scheil-gulliver-非平衡凝固模型数学推导与边界极限对比the-scheil-model-derivation--limiting-cases|Note04wk4 §3, §4（Scheil推导与极限对比）]]、[[66_notes/Introduction to Materials Modelling/Note/Note06wk6.md#核心考题-10平衡凝固-vs-scheil-凝固模型数学推导与极限对比-5-marks|Note06wk6 考题10, 11]]

**Exam Prompt:**
> "Compare Equilibrium Solidification (Lever Rule) and Scheil-Gulliver Solidification. State their underlying physical assumptions, sketch/describe their solute concentration and phase fraction profiles, and explain why the Scheil model often predicts the formation of non-equilibrium eutectic phases in dilute alloys." [6 Marks]

#### 1. English Model Answer (Ready-to-Type in Exam)

* **1. Fundamental Physical Assumptions (`L07` Slide 4-7):**
  * **Equilibrium Solidification (Lever Rule):**
    1. Complete and infinitely fast diffusion in liquid ($D_l = \infty$).
    2. Complete and infinitely fast diffusion in solid ($D_s = \infty$).
    3. Thermodynamic equilibrium maintained across the entire system at all times.
  * **Scheil-Gulliver Solidification Model:**
    1. Complete and infinitely fast diffusion in liquid ($D_l = \infty$) (homogeneous liquid).
    2. **Zero diffusion in the solid phase ($D_s = 0$)** (no back-diffusion; solute is frozen once solidified).
    3. **Local thermodynamic equilibrium** is maintained strictly at the advancing solid/liquid interface ($C_s^* = k C_l^*$).

* **2. Solidification Behavior & Profiles Comparison (`L07` Slide 13-18):**
  * **Solute Profile in Solid ($C_s$):**
    * *Equilibrium:* Solid is completely homogeneous at any instant; final grain has a uniform composition equal to nominal alloy composition $C_0$.
    * *Scheil:* Severe solute segregation (**coring**). The dendrite core forms with a low solute concentration ($k C_0$), and solute concentration increases continuously toward the outer boundary as solid fraction $f_s \to 1$, governed by $C_s(f_s) = k C_0 (1 - f_s)^{k-1}$.
  * **Solidus Temperature & Freezing Range:**
    * *Equilibrium:* Solidification terminates at the true thermodynamic solidus temperature $T_{\text{solidus}}$.
    * *Scheil:* Solidification range is substantially broadened; solidification continues down to the terminal eutectic temperature $T_{\text{eutectic}}$.

* **3. Origin of Non-Equilibrium Eutectic in Dilute Alloys (`L07` Slide 19-22):**
  * For solute with partition coefficient $k < 1$, the solid rejects solute into the liquid.
  * Because $D_s = 0$, this rejected solute cannot diffuse back into the existing solid core.
  * Consequently, the remaining liquid volume shrinks while becoming exponentially enriched in solute ($C_l = C_0 (1 - f_s)^{k-1}$).
  * Even in very dilute alloys where the nominal composition $C_0$ is well below the solid solubility limit, the residual liquid will eventually reach the eutectic composition ($C_l \to C_E$), precipitating a terminal **non-equilibrium eutectic / intermetallic phase** at the final stage of solidification.

#### 2. 中文考点精析与得分关键点
* **得分点 1（物理假设，2分）**：平衡态 $D_l = \infty, D_s = \infty$；Scheil 模型 $D_l = \infty, D_s = 0$ 且界面局部平衡（`L07` Slide 5）。
* **得分点 2（成分分布与凝固温区，2分）**：平衡态固相均匀无偏析；Scheil 出现晶内偏析（Coring），凝固温区拉宽，终止于非平衡共晶点（`L07` Slide 14）。
* **得分点 3（非平衡共晶成因，2分）**：$k < 1$ 导致排斥溶质，固态零扩散导致残余液相不断富集溶质，最终达到共晶成分 $C_E$ 析出非平衡共晶相。

---

### Question 6: Microsegregation & Superalloy Heat Treatment Window Design (5 Marks) 【Week 04 / L08】

> 📍 **精准课件与考点出处 (Slide & Note Sourcing)**:
> * **所属周次与讲次**：Week 04 — Lecture 07 (Case Studies: Ni-base Superalloys)
> * **官方课件 PDF**：`L08_calculationOfPhaseDiagram_caseStudies.pdf` (Slide 20 至 Slide 35)
> * **复习全景笔记**：[[66_notes/Introduction to Materials Modelling/Note/Note04wk4.md#6-第五部分工程案例二单晶镍基高温合金涡轮叶片偏析与固溶热处理窗口设计case-study-2-ni-base-superalloy--solution-heat-treatment-design|Note04wk4 §6（高温合金固溶窗口设计）]]、[[66_notes/Introduction to Materials Modelling/Note/Note06wk6.md#核心考题-12工业案例深度汽车铝合金-mn-变质与单晶高温合金固溶窗口设计-5-marks|Note06wk6 考题12.2]]

**Exam Prompt:**
> "Single-crystal Ni-base superalloys exhibit severe microsegregation during casting solidification. Explain which elements segregate to the dendrite core versus interdendritic regions. How does this microsegregation affect the subsequent Solution Heat Treatment window, and how can incipient melting (初熔) be avoided?" [5 Marks]

#### 1. English Model Answer (Ready-to-Type in Exam)

* **1. Elemental Segregation Partitioning (`L08` Slide 22-26):**
  * **Dendrite Core ($k > 1$):** Refractory elements such as **Rhenium (Re), Tungsten (W), and Cobalt (Co)** segregate preferentially into the initial solidifying dendrite cores.
  * **Interdendritic Regions ($k < 1$):** Elements like **Aluminium (Al), Titanium (Ti), Tantalum (Ta), and Carbon (C)** partition strongly into the residual interdendritic liquid, forming coarse non-equilibrium $\gamma/\gamma'$ eutectic pools and carbides.

* **2. Solution Heat Treatment Window Constraints (`L08` Slide 27-31):**
  * The goal of solution treatment is to fully dissolve coarse $\gamma'$ precipitates and homogenize elemental segregation without melting the alloy.
  * **Lower Temperature Limit:** Must be higher than the **$\gamma'$ solvus temperature ($T_{\gamma'\text{-solvus}}$)** to ensure complete dissolution of $\gamma'$.
  * **Upper Temperature Limit:** Must be kept strictly below the **incipient melting temperature ($T_{\text{incipient}}$ / non-equilibrium eutectic melting point)**, which is significantly lower than the equilibrium solidus due to severe interdendritic microsegregation.
  * This creates a very narrow or even initially "negative" heat treatment processing window:  
    $$T_{\gamma'\text{-solvus}} < T_{\text{solution}} < T_{\text{incipient}}$$

* **3. Strategy to Avoid Incipient Melting (初熔) (`L08` Slide 32-35):**
  * **Multi-Step / Stepped Homogenization Heat Treatment (多级阶梯固溶退火):**
    * *Step 1:* Hold at a safe lower temperature (just below the incipient melting point $T_{\text{incipient}}$) for several hours. This allows fast-diffusing interstitial/solute atoms to back-diffuse and partially dissolve coarse interdendritic eutectic pools, thereby raising the local melting temperature.
    * *Step 2:* Incrementally ramp up the temperature to higher levels (above the initial incipient melting point but below the newly elevated local melting point) to homogenize slow-diffusing heavy refractory elements (Re, W).

#### 2. 中文考点精析与得分关键点
* **得分点 1（元素偏析分配，1.5分）**：枝晶干（$k>1$：Re, W, Co）；枝晶间（$k<1$：Al, Ti, Ta 及粗大 $\gamma/\gamma'$ 共晶）（`L08` Slide 24）。
* **得分点 2（热处理窗口定义，1.5分）**：下限为 $\gamma'$ solvus；上限为非平衡初熔温度（Incipient melting temperature）（`L08` Slide 29）。
* **得分点 3（多级阶梯退火防初熔，2分）**：先在初熔点以下保温反扩散溶解共晶、提升局部熔点，再升至更高温均匀化难熔元素（`L08` Slide 33）。

---

### Question 7: Thermodynamic Driving Force & Darken's Uphill Diffusion (5 Marks) 【Week 05 / L09】

> 📍 **精准课件与考点出处 (Slide & Note Sourcing)**:
> * **所属周次与讲次**：Week 05 — Lecture 08 & Lecture 09 (Diffusion Basics & Uphill Diffusion)
> * **官方课件 PDF**：`L09_Diffusion_basics.pdf` (Slide 25 至 Slide 38)
> * **复习全景笔记**：[[66_notes/Introduction to Materials Modelling/Note/Note05wk5.md#4-第三部分热力学驱动力下坡上坡扩散与-darken-经典扩散偶实验thermodynamic-driving-force-uphill-diffusion--darkens-experiment|Note05wk5 §4（扩散第一性驱动力与Darken实验）]]、[[66_notes/Introduction to Materials Modelling/Note/Note06wk6.md#核心考题-14扩散驱动力第一性原理上坡扩散与-darken-扩散偶实验-5-marks|Note06wk6 考题14]]

**Exam Prompt:**
> "Explain why the true thermodynamic driving force for solid-state diffusion is the chemical potential gradient rather than the concentration gradient. Use Darken's classic diffusion couple experiment (Fe-C-Si vs Fe-C) to demonstrate uphill diffusion." [5 Marks]

#### 1. English Model Answer (Ready-to-Type in Exam)

* **1. Thermodynamic Driving Force of Diffusion (`L09` Slide 25-29):**
  * Classically, Fick's first law assumes diffusion flux is driven by the concentration gradient: $J = -D \frac{\partial c}{\partial x}$.
  * However, fundamentally according to irreversible thermodynamics, atoms move to minimize the total Gibbs free energy of the system. Therefore, the **true first-principles driving force for diffusion is the gradient of chemical potential ($\nabla \mu_i$)**, where the flux is:
    $$J_i = - M_i c_i \frac{\partial \mu_i}{\partial x} = - M_i c_i \left( \frac{\partial \mu_i}{\partial c_i} \frac{\partial c_i}{\partial x} + \sum_{j \neq i} \frac{\partial \mu_i}{\partial c_j} \frac{\partial c_j}{\partial x} \right)$$
    (where $M_i$ is atomic mobility).
  * Diffusion occurs spontaneously from regions of **higher chemical potential (activity) to lower chemical potential**, even if this requires moving against a concentration gradient.

* **2. Darken's Classic Experiment & Uphill Diffusion (`L09` Slide 31-36):**
  * **Experimental Setup:** Darken welded two steel bars with the **same initial Carbon concentration (0.4 wt% C)**:
    * Left side: $\text{Fe} - 0.4\text{ wt}\% \text{ C} - 3.8\text{ wt}\% \text{ Si}$
    * Right side: $\text{Fe} - 0.4\text{ wt}\% \text{ C} - 0\text{ wt}\% \text{ Si}$
  * **Observation:** After annealing at $1050^\circ\text{C}$ (austenite region), carbon atoms diffused across the bonded interface from the high-Si side to the low-Si side. This resulted in carbon depletion on the Si-containing side ($\sim 0.3\text{ wt}\% \text{ C}$) and carbon accumulation on the Si-free side ($\sim 0.6\text{ wt}\% \text{ C}$).
  * **Physical Mechanism:** Silicon strongly increases the activity coefficient and chemical potential of Carbon in austenite ($\frac{\partial \mu_{\text{C}}}{\partial c_{\text{Si}}} > 0$). Therefore, carbon had a higher chemical potential on the Si-rich side and diffused "uphill" along its chemical potential gradient towards the lower chemical potential on the Si-free side, creating a pronounced concentration disparity.

#### 2. 中文考点精析与得分关键点
* **得分点 1（第一性驱动力，2分）**：说明扩散由化学势梯度 $\nabla \mu_i$ 驱动，本质是极小化体系总吉布斯自由能（`L09` Slide 26）。
* **得分点 2（Darken 实验现象，1.5分）**：初始等碳（0.4% C），一侧加 3.8% Si；退火后碳从有硅侧向无硅侧流动，造成宏观浓度反差（`L09` Slide 32）。
* **得分点 3（上坡扩散微观机理，1.5分）**：Si 提高了 C 的活度系数和化学势，碳原子顺着化学势梯度“下坡”流动，表现为逆浓度梯度的“上坡扩散”（`L09` Slide 35）。

---

### Question 8: Chained Modelling Workflow (Equilibrium ➔ Scheil ➔ DICTRA) (5 Marks) 【综合跨模块】

> 📍 **精准课件与考点出处 (Slide & Note Sourcing)**:
> * **所属周次与讲次**：Week 03、04、05 跨模块大综合 / Week 06 复习
> * **官方课件 PDF**：`L06b_CALPHADmethod_MSc_MaterialsModelling.pdf`, `L07_calculationOfPhaseDiagram_ScheilModel.pdf`, `L09_Diffusion_basics.pdf`
> * **复习全景笔记**：[[66_notes/Introduction to Materials Modelling/Note/Note06wk6.md#模块-6三大连环建模理论关联与跨模型深度对比阐释chained-modelling-synthesis|Note06wk6 模块6（三大连环建模理论）]]、[[66_notes/Introduction to Materials Modelling/Week06/Materials_Modelling_Resit_Cheatsheet.md#第三部分三大连环建模与比较解释|Resit Cheatsheet §3]]

**Exam Prompt:**
> "In alloy development, engineers often execute a chained modelling sequence: (1) Equilibrium Calculation ➔ (2) Scheil-Gulliver Solidification ➔ (3) DICTRA Diffusion Simulation. Explain the scientific role of each model in this sequence, how they link logically, and what critical engineering insight is gained from comparing them." [5 Marks]

#### 1. English Model Answer (Ready-to-Type in Exam)

* **1. The Three Links in the Modelling Chain:**
  1. **Equilibrium Stepping (Thermo-Calc Equilibrium):**
     * *Role:* Establishes the thermodynamic upper bound and baseline (`L06b` Slide 21).
     * *Output:* Thermodynamic liquidus ($T_{\text{liq}}$), equilibrium solidus ($T_{\text{sol}}$), stable phase constituents, and equilibrium solvus temperatures.
  2. **Scheil-Gulliver Solidification (Thermo-Calc Scheil):**
     * *Role:* Predicts non-equilibrium casting microstructures under practical cooling rates without solid diffusion (`L07` Slide 4).
     * *Output:* Solute segregation profiles (coring), realistic solidification temperature range, volume fraction of non-equilibrium terminal phases/eutectics, and the **incipient melting temperature ($T_{\text{incipient}}$)**.
  3. **DICTRA Moving Interface & Diffusion Simulation:**
     * *Role:* Captures real-time diffusion kinetics and spatial phase transformations during post-casting homogenization heat treatments (`L09` Slide 40).
     * *Output:* Time-dependent concentration profiles, dissolution rates of eutectic particles, and exact soaking times required for complete homogenization.

* **2. Logical Interconnection & Engineering Insights:**
  * **Link 1 ➔ 2 (Thermodynamic Boundary):** Comparing Equilibrium and Scheil curves reveals the severity of microsegregation (the gap between equilibrium solidus and Scheil terminal solidification temperature).
  * **Link 2 ➔ 3 (Defining Safe Heat Treatment Window):** Scheil calculation directly provides the as-cast initial solute profile and the incipient melting temperature $T_{\text{incipient}}$, which sets the strict upper safety limit for the annealing temperature in DICTRA.
  * **Link 3 ➔ 1 (Target Verification):** DICTRA simulates the diffusion annealing process to verify when the non-equilibrium as-cast structure finally approaches the desired homogeneous state predicted by the initial equilibrium model.

#### 2. 中文考点精析与得分关键点
* **得分点 1（三大模型各自职能，2分）**：平衡态（热力学基准）/ Scheil（铸态微观偏析与初熔点）/ DICTRA（扩散动力学与退火时间预测）。
* **得分点 2（因果逻辑传递，2分）**：Scheil 为 DICTRA 提供初始成分场和温度上限；DICTRA 验证何时达到平衡态所期望的组织。
* **得分点 3（工程闭环思维，1分）**：体现“热力学静态 $\to$ 凝固非平衡 $\to$ 动力学热处理”的完整材料设计链条。

---

# 【重点理论扩展题库】High-Yield Modular Question Bank（带精准课件溯源）

---

### Bank 1: Euler ODE Numerical Stability & Timestep Limit Criterion 【Week 01 / L02a】

> 📍 **精准课件出处**：`L02a_modelDerivation_MSc_MaterialsModelling.pdf` (Slide 15-32) & `Pwk1_ModelImplementation.pdf` (Slide 5-16)  
> 🔗 **笔记链接**：[[66_notes/Introduction to Materials Modelling/Note/Note01wk1.md#6-第五部分数值稳定性与时间步长深度剖析numerical-stability--timestep-analysis|Note01wk1 §6]]、[[66_notes/Introduction to Materials Modelling/Note/Note06wk6.md#核心考题-3常微分方程前向欧拉法与数值稳定性判据-5-marks|Note06wk6 考题3]]

**Exam Prompt:**
> "For a first-order decay ODE $\frac{dN}{dt} = -\frac{N}{\tau}$, write down the Forward Euler discretization. Derive the numerical stability condition for timestep $\Delta t$, explain the physical meaning of relaxation time $\tau$, and describe what happens when $\tau < \Delta t < 2\tau$ versus $\Delta t > 2\tau$."

#### Ready-to-Type Answer:
* **Forward Euler Discretization (`L02a` Slide 20):**
  $$\frac{N^{n+1} - N^n}{\Delta t} = -\frac{N^n}{\tau} \implies N^{n+1} = N^n \left( 1 - \frac{\Delta t}{\tau} \right)$$
* **Amplification Factor & Stability Condition (`L02a` Slide 31):**
  * For stability, the amplification factor $A = 1 - \frac{\Delta t}{\tau}$ must satisfy $|A| \le 1$:
    $$-1 \le 1 - \frac{\Delta t}{\tau} \le 1 \implies 0 < \Delta t \le 2\tau$$
* **Three Timestep Regimes (`L02a` Slide 32; `Pwk1` Slide 10):**
  1. **Stable & Non-oscillatory ($\Delta t < \tau$):** $0 < A < 1$. Numerical solution decays monotonically, mimicking physical reality smoothly.
  2. **Stable but Oscillating / Overshooting ($\tau < \Delta t < 2\tau$):** $-1 < A < 0$. Solution oscillates between positive and negative values while decaying towards zero (unphysical numerical overshoot).
  3. **Unstable & Diverging ($\Delta t > 2\tau$):** $A < -1$. Numerical error grows exponentially with alternating signs; simulation diverges to infinity.
* **Physical Meaning of $\tau$ (Relaxation Time):** $\tau$ is the characteristic material timescale required for the physical quantity to decay to $1/e$ ($\approx 36.8\%$) of its initial value. Numerical stability requires sampling at a frequency finer than the system's intrinsic relaxation response.

---

### Bank 2: Discretization Methods (FDM vs CVM/FVM vs FEM) 【Week 02 / L02c】

> 📍 **精准课件出处**：`L02c_otherNumericalMethods_MSc_MaterialsModelling.pdf` (Slide 2 至 Slide 25)  
> 🔗 **笔记链接**：[[66_notes/Introduction to Materials Modelling/Note/Note02wk2.md#3-第二部分空间与时间离散化数值方法深度剖析numerical-discretization-fdm-cvm-fem|Note02wk2 §3]]

**Exam Prompt:**
> "Compare Finite Difference (FDM), Control Volume (CVM/FVM), and Finite Element (FEM) methods for solving spatial PDEs in materials modelling."

#### Ready-to-Type Answer:
* **1. Finite Difference Method (FDM) (`L02c` Slide 4-10):**
  * *Principle:* Replaces continuous partial derivatives in differential equations with Taylor series difference approximations on structured grid points.
  * *Strengths:* Mathematically simple, easy to code (e.g., in Python or Excel), fast execution.
  * *Weaknesses:* Strictly confined to simple regular geometries (1D, 2D Cartesian boxes); does not inherently guarantee strict conservation of mass/energy across boundaries.
* **2. Control Volume / Finite Volume Method (CVM / FVM) (`L02c` Slide 11-17):**
  * *Principle:* Integrates governing equations over discrete control volumes; evaluates flux balances entering and leaving adjacent cell faces.
  * *Strengths:* **Strictly conservative by construction** (what leaves cell A enters cell B); physically intuitive for transport phenomena (mass diffusion, fluid flow, heat flux).
  * *Weaknesses:* Complex to formulate high-order approximations on distorted meshes.
* **3. Finite Element Method (FEM) (`L02c` Slide 18-25):**
  * *Principle:* Multiplies differential equations by test functions and integrates over elements (weak variational form).
  * *Strengths:* Superior capability in handling **highly complex curved engineering geometries**, adaptive unstructured meshes, and coupled mechanical stress-strain fields.
  * *Weaknesses:* Computationally intensive; complex mathematical formulation.

---

### Bank 3: 8 Microstructure Modelling Methods Comparison 【Week 02 / L04】

> 📍 **精准课件出处**：`L04_MicrostructureModellingMethods.pdf` (Slide 16 至 Slide 45)  
> 🔗 **笔记链接**：[[66_notes/Introduction to Materials Modelling/Note/Note02wk2.md#6-第五部分三大建模范式与八大微观组织建模方法精析8-microstructure-modelling-methods|Note02wk2 §6]]、[[66_notes/Introduction to Materials Modelling/Note/Note06wk6.md#核心考题-6材料科学八大微观组织建模方法精析-6-marks|Note06wk6 考题6]]

**Exam Prompt:**
> "Briefly explain the physical domain, governing mechanism, and primary application of: (1) Cellular Automata (CA), (2) Phase-Field Method (PF), and (3) Sharp Interface Models (e.g. DICTRA)."

#### Ready-to-Type Answer:
1. **Cellular Automata (CA) (`L04` Slide 24-29):**
   * *Mechanism:* Space is discretized into regular cells with discrete states; states evolve synchronously based on deterministic or probabilistic local neighborhood transition rules.
   * *Primary Application:* Simulating grain nucleation, dendritic growth morphology, and recrystallization kinetics at mesoscopic scales with high computational speed.
2. **Phase-Field Method (PF) (`L04` Slide 30-36):**
   * *Mechanism:* Uses continuous spatial order parameters ($\phi$) across **diffuse interfaces** (avoiding explicit interface boundary tracking). Governed by Cahn-Hilliard (conserved) and Allen-Cahn (non-conserved) thermodynamic kinetic equations.
   * *Primary Application:* Complex morphological evolution, dendrite branching, spinodal decomposition, and precipitate coarsening under anisotropic interfacial energy.
3. **Sharp Interface Models (e.g., DICTRA) (`L04` Slide 37-41):**
   * *Mechanism:* Treats phase boundaries as mathematical surfaces with zero thickness; couples 1D Fickian diffusion inside bulk phases with the Stefan local equilibrium flux balance condition at the moving boundary.
   * *Primary Application:* Accurate 1D quantitative kinetic predictions of phase transformation rates, coating diffusion, and homogenization annealing times.

---

### Bank 4: Gibbs Free Energy Models: Ideal ➔ Regular ➔ R-K ➔ CEF Sublattice 【Week 03 / L06a, L06b】

> 📍 **精准课件出处**：`L06a_ThermodynamicsOfAlloys_MSc_MaterialsModelling.pdf` (Slide 10-25) & `L06b_CALPHADmethod_MSc_MaterialsModelling.pdf` (Slide 6-20)  
> 🔗 **笔记链接**：[[66_notes/Introduction to Materials Modelling/Note/Note03wk3.md#4-第三部分吉布斯自由能数学模型体系演进thermodynamic-solution-models-ideal-regular-r-k--cef|Note03wk3 §4]]、[[66_notes/Introduction to Materials Modelling/Note/Note06wk6.md#核心考题-9吉布斯自由能模型体系演进ideal-regular-r-k-cef-6-marks|Note06wk6 考题9]]

**Exam Prompt:**
> "Trace the evolution of Gibbs free energy models in CALPHAD from Ideal Solution to Compound Energy Formalism (CEF)."

#### Ready-to-Type Answer:
* **1. Ideal Solution (`L06a` Slide 12):**
  * Assumes atoms mix randomly with zero enthalpy of mixing ($\Delta H_{\text{mix}} = 0$).
  * $G_m = x_A G_A^\circ + x_B G_B^\circ + RT (x_A \ln x_A + x_B \ln x_B)$
* **2. Regular Solution (`L06a` Slide 16-18):**
  * Introduces constant interaction parameter $\Omega$ to account for non-zero enthalpy of mixing ($\Delta H_{\text{mix}} = \Omega x_A x_B$).
  * $G_m = G_{\text{ideal}} + \Omega x_A x_B$
* **3. Redlich-Kister (R-K) Polynomial (`L06b` Slide 8-12):**
  * Accounts for asymmetric interactions where parameter $L(T, x)$ depends on composition:
  * $G_{\text{excess}} = x_A x_B \sum_{v=0}^n L_v(T) (x_A - x_B)^v$
* **4. Compound Energy Formalism (CEF) / Sublattice Model (`L06b` Slide 18-20):**
  * Formulated for ordered intermetallics and interstitial solutions with distinct crystallographic sublattices: $(A, B)_p (C, D, \text{Va})_q$.
  * Expressed in terms of **site fractions ($y_i^s$)** rather than bulk mole fractions, allowing description of stoichiometric variability, chemical ordering, and vacancy concentrations ($\text{Va}$) in phases like austenite $(\text{Fe, Ni})_1(\text{C, Va})_1$.

---

### Bank 5: Microstructure Modification: Al-Si-Mg-Fe Alloy with Mn Addition 【Week 04 / L08】

> 📍 **精准课件出处**：`L08_calculationOfPhaseDiagram_caseStudies.pdf` (Slide 3 至 Slide 18)  
> 🔗 **笔记链接**：[[66_notes/Introduction to Materials Modelling/Note/Note04wk4.md#5-第四部分工程案例一al-si-铸造铝合金微观组织控制与有害相-mn-变质改性case-study-1-al-si-mg-fe-mn-alloys--morphology-control|Note04wk4 §5]]、[[66_notes/Introduction to Materials Modelling/Note/Note06wk6.md#核心考题-12工业案例深度汽车铝合金-mn-变质与单晶高温合金固溶窗口设计-5-marks|Note06wk6 考题12.1]]

**Exam Prompt:**
> "Why is Iron (Fe) harmful in Al-Si casting alloys, and how does Manganese (Mn) addition modify the microstructure to mitigate this problem?"

#### Ready-to-Type Answer:
* **The Problem with Iron (Fe) (`L08` Slide 5-8):**
  * Iron has extremely low solid solubility in Aluminium.
  * During casting solidification, Fe forms brittle, plate-like/needle-like intermetallic phases known as **$\beta\text{-Al}_5\text{FeSi}$ (or $\beta\text{-phase}$)**.
  * In 2D cross-sections, these appear as sharp needles that act as severe stress concentrators and physically block molten metal feeding channels, leading to casting shrinkage porosity and drastically deteriorating alloy ductility and fracture toughness.
* **Modification Mechanism of Manganese (Mn) (`L08` Slide 9-16):**
  * Adding Mn (typically maintaining an $\text{Fe}:\text{Mn}$ ratio of $\approx 2:1$) shifts the solidification reaction pathway.
  * Mn substitutes for Fe to promote the formation of the cubic/globular **$\alpha\text{-Al}_{15}(\text{Fe, Mn})_3\text{Si}_2$ (Chinese-script morphology)** phase instead of the needle-like $\beta\text{-phase}$.
  * The rounded, compact "Chinese-script" morphology significantly minimizes stress concentration and eliminates feeding blockages, restoring tensile strength and elongation.

---

### Bank 6: Moving Phase Interface (Stefan Condition) & Geometry Selection in DICTRA 【Week 05 / L09】

> 📍 **精准课件出处**：`L09_Diffusion_basics.pdf` (Slide 39 至 Slide 52) & `Pwk11_thermocalc_diffusionSimulations.pdf` (Slide 4-15)  
> 🔗 **笔记链接**：[[66_notes/Introduction to Materials Modelling/Note/Note05wk5.md#6-第五部分移动相界面动力学沉淀相生长与几何坐标系选择moving-interface-kinetics-precipitate-growth--coordinate-geometries|Note05wk5 §6]]、[[66_notes/Introduction to Materials Modelling/Note/Note06wk6.md#核心考题-15多元扩散calphad-动力学架构与-dictra-模块机制-4-marks|Note06wk6 考题15]]

**Exam Prompt:**
> "State the Stefan condition for moving phase boundaries in diffusion simulations, and explain when to select Planar, Cylindrical, or Spherical coordinates in DICTRA."

#### Ready-to-Type Answer:
* **1. Stefan Boundary Condition (Flux Balance) (`L09` Slide 43-46):**
  * Mass conservation at a moving phase interface ($\alpha / \beta$) dictates that the velocity of the boundary ($v$) is proportional to the net solute flux discontinuity across the interface:
    $$v \left( C^\alpha - C^\beta \right) = J^\alpha - J^\beta = - D^\alpha \left. \frac{\partial C^\alpha}{\partial x} \right|_{\text{int}} + D^\beta \left. \frac{\partial C^\beta}{\partial x} \right|_{\text{int}}$$
    $$v = \frac{J^\alpha - J^\beta}{C^\alpha - C^\beta}$$
* **2. Coordinate Geometry Selection in DICTRA (`L09` Slide 47-51; `Pwk11` Slide 6):**
  * **Planar Geometry (1D Slab):** Selected for 1D flat diffusion couples, surface oxidation layers, thin film coatings, or wide planar phase interfaces.
  * **Cylindrical Geometry (1D Radial):** Selected for needle-like precipitates, fiber-reinforced composites, Widmanstätten ferrite laths, or grain boundary ditch diffusion.
  * **Spherical Geometry (1D Radial):** Selected for equiaxed precipitate particle growth/dissolution (e.g., spherical $\gamma'$ in superalloys, carbides), nodular graphite growth in cast iron, and Ostwald ripening coarsening kinetics.

---

# 打字考试通用防查重 Paraphrase 句型库

> **打字考试满分心法：** 阅卷老师非常反感生搬硬套 PPT 词句。使用以下句式可以展现深度思考，避免查重雷同：

1. **阐述模型本质时：**
   * *Do not write:* "A model is a set of mathematical equations describing reality."
   * *Write:* "A model serves as a purposeful idealization of physical systems, designed to capture dominant phenomena while deliberately filtering out secondary complexities to maintain computational tractability."
2. **解释为什么 CALPHAD 不受 3 元限制时：**
   * *Do not write:* "Thermo-Calc can do 20 elements because of databases."
   * *Write:* "The apparent three-component constraint is merely a limitation of 2D/3D human graphical visualization. Mathematically, CALPHAD constructs high-dimensional Gibbs energy hypersurfaces by extrapolating rigorously assessed binary and ternary interaction parameters, which is physically justified since quaternary multi-body atomic interactions are negligible."
3. **解释 Scheil 非平衡凝固时：**
   * *Do not write:* "Scheil has Ds=0 and Dl=infinite so it has coring."
   * *Write:* "Because solid-state diffusion is assumed to be negligible ($D_s = 0$) while liquid mixing is instantaneous, solute rejected at the advancing interface cannot back-diffuse into the dendrite core. This progressive solute enrichment in the dwindling liquid leads to pronounced microsegregation and drives the residual liquid to terminal eutectic solidification."
4. **解释上坡扩散与化学势驱动力时：**
   * *Do not write:* "Carbon diffuses uphill because of Silicon."
   * *Write:* "Diffusion is fundamentally governed by the minimization of total free energy, making the chemical potential gradient the true thermodynamic driving force. In the Fe-C-Si system, Silicon markedly elevates the activity coefficient of Carbon, compelling Carbon atoms to diffuse 'uphill' against their concentration gradient to equilibrate chemical potentials across the couple."

---
*End of Mock Exam & Revision Guide — Good luck with your exam!*
