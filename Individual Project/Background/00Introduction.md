以下是 MSc_project_P15_2026_VB的详细内容介绍：
###  **1. 项目基本信息** 
- **标题**：Migration to an Open-Source Computational Framework for Acoustic Emission Analysis applied to Steel Structures （钢结构声发射分析开源计算框架迁移） 
- **所属机构**：University of Birmingham – School of Metallurgy and Materials 
- **导师**：Prof. Mayorkinos Papaelias（m.papaelias@bham.ac.uk） 
- **合作导师**：Dr. Vincenzo Brachetta（v.brachetta@bham.ac.uk） 
- **学生**：Haoyu Wang（hxw702@student.bham.ac.uk）
###  **2. 核心主题与反思** 
项目围绕以下关键主题展开，要求学生深入学习和思考： 
- **生成式 AI 在高等教育和科学计算中的作用与局限性** 
- **开源科学软件的原则与实践** 
- **可重复性、透明性及 FAIR（可查找、可访问、可互操作、可重用）数据/软件原则** 
- **数据机密性及使用大型语言模型（LLM）的风险** 
- **MATLAB 与 Python/Julia 在科学工作流中的对比分析** 
- **现有声发射分析代码的目的和结构**（重点研究 UoB-NDT 组的内部代码） 
- **代码复杂性评估与重构策略** 
- **自动化代码翻译中可能引入的错误** 
- **LLM 在调试、性能分析和代码优化中的应用**
###  **3. 研究方法与工作计划** 
项目分为三个阶段： 
#### **阶段 1：熟悉与初步分析** - **文献综述**：相关主题的阅读与理解。 
- **研究现有 MATLAB 代码**： 
- 理解算法目标。 
- 识别变量、输入/输出及数据流。 
- 绘制代码架构的结构化流程图。 
- **定义翻译后系统的功能需求**。 
#### **阶段 2：翻译与 AI 辅助开发** 
- **设计结构化提示（Prompts）**：将 MATLAB 代码翻译为 Python 或 Julia。 
- **评估和比较不同 LLM 的输出**（如 ChatGPT、Gemini、Claude 等）。 
- **记录所有提示、响应和迭代改进** 以确保可重复性。 
- **实现翻译后的代码**，并与原始 MATLAB 输出对比验证。 
- **利用 LLM 辅助**： - 解释错误信息。 
- 调试和重构建议。 - 代码优化。 
- **维护问题日志**：记录问题、修正和设计决策。
#### **阶段 3：验证、优化与最终确认** 
- **验证数值和功能等价性**：确保翻译后的代码与原始代码一致。 
- **代码优化**：提升性能和可读性。 
- **系统测试**：使用代表性数据集进行测试。 
- **评估健壮性**：识别并处理边界情况。 
- **评估 AI 辅助代码生成的风险**（如逻辑错误、幻觉函数等）。
### **4. 推荐阅读材料** 
- **AI 辅助代码翻译的错误研究**： 
- Pan et al. (2024) *Lost in Translation: A Study of Bugs Introduced by Large Language Models while Translating Code*. 
- **AI 与仿真工具集成**： 
- Giabbanelli et al. (2025) *From Over-Reliance to Smart Integration: Using Large-Language Models as Translators between Specialized Modeling and Simulation Tools*. 
- **人机协同翻译**： 
- De Siano et al. (2025) *Translating code with Large Language Models and human-in-the-loop feedback*. 
- **AI 在学术写作中的应用**： 
- Khalifa & Albadawy (2024) *Using artificial intelligence in academic writing and research: An essential productivity tool*. 
### **5. 指南与工具** 
#### **指南链接** 
- [[00Why and How to Translate Scientific code from MATLAB to Python：A Guide for Researchers]]
- [伯明翰大学研究生关于道德使用生成式 AI 工具的指南](https://intranet.birmingham.ac.uk/student/libraries/asc/student-guidance-gai.aspx) 
- [[00Russell Group principles on the use of generative AI tools in education]]
#### **工具** 
- **编程语言**：Python 3.0+ 或 Julia 1.12+ 
- **IDE**：VSCodium（或 VSCode） 
- **翻译工具**：SMOP（Small MATLAB/Octave to Python 编译器）[GitHub 链接](https://github.com/victorlei/smop) 
- #### **LLM 工具** - **商业模型**： 
- OpenAI ChatGPT 5.3 
- Google Gemini 3 Flash 
- Anthropic Claude Sonnet 4.6 
- DeepSeek-AI DeepSeek 3.2 
- **伯明翰大学 AI 试点项目提供的模型**： 
- OpenAI ChatGPT 5.2 
- Anthropic Opus 4.6 
- Meta Llama 4 Maverick 
### **6. 项目目标**
将 UoB-NDT 组的 **声发射分析 MATLAB 代码** 迁移到开源框架（Python 或 Julia），确保： 
1. **功能等价性**：翻译后的代码与原始代码输出一致。 
2. **性能优化**：提升代码效率和可读性。 
3. **可重复性**：记录所有翻译步骤和决策，确保过程可追溯。 
4. **AI 辅助**：合理利用 LLM 提高翻译和调试效率，同时规避潜在风险。 
### **7. 学生任务总结** - 学习开源科学计算的原则和实践。 
- 分析现有 MATLAB 代码，理解其架构和算法。 
- 使用 AI 工具辅助翻译代码，并验证结果。 
- 记录并优化翻译过程，确保代码质量和性能。 
- 评估 AI 在项目中的作用及局限性。

---
