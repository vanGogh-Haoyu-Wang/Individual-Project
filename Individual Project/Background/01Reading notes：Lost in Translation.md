![[Lost in Translation.pdf]]
# 阅读笔记：Lost in Translation

**文献标题:** Lost in Translation: A Study of Bugs Introduced by Large Language Models while Translating Code  
**会议/年份:** ICSE 2024  
**研究主题:** 深入研究 [[Large Language Models (LLMs)]] 在跨编程语言进行 [[Code Translation]]（代码翻译）时引入的各类漏洞（Bugs），并提出基于提示词工程的缓解策略。  
## **核心观点与发现 (Key Findings)**  

- **LLM 在代码翻译中的表现存在局限：** 研究评估了 1,700 个代码样本，跨越 C、C++、Go、Java 和 Python 五种语言。整体来看，通用和代码 LLM 尚未能可靠地自动化代码翻译，成功率仅在 2.1% 到 47.3% 之间。  

- **真实项目面临极大挑战：** 在处理复杂的真实世界开源项目时，LLM 的表现极差，即便是表现最好的 GPT-4，成功率也仅为 8.1%，而其他模型成功率甚至为 0%。  

- **翻译漏洞分类学 ([[Bug Taxonomy]])：** 作者通过大量人工标注，将 LLM 引入的代码翻译漏洞归纳为 5 大类、15 个子类：  
    • **[[Data-related Bugs]] (数据相关漏洞)：** 占比最高（33.5%），主要表现为输入解析错误（Incorrect input parsing）和目标语言中数据类型选择错误（Incorrect data type）。  
    • **[[Syntactic and Semantic Differences]] (语法与语义差异)：** 占 30.5%，例如 API 行为在不同语言中的不匹配（Mismatch of API behavior）或直接照搬源语言的语法。  
    • **[[Dependency and Logic Bugs]] (依赖与逻辑漏洞)：** 占 24.2%，最常见的是缺失库导入（Missing library imports）和源逻辑缺失（Removal of logic in the source code）。  
    • **[[Model Specific Constraints]] (模型特定约束)：** 受限于上下文窗口等模型限制引起错误。  

- **非 LLM 工具与 LLM 的优劣对比：** 传统的转译器（如 CxGo, C2Rust）在确定性和项目上下文掌控上表现更好，但生成的代码不够符合目标语言习惯（Non-idiomatic）甚至存在安全风险（如 C2Rust 生成 Unsafe 代码）；而 LLM 生成的代码更具人类编程风格，但在复杂依赖上容易出错。  

- **[[Prompt Crafting]] (提示词构建) 策略：** 提供包含报错信息的上下文（如堆栈跟踪、编译错误日志、失败测试的输入输出）可以显著提升 LLM 的修复能力。这种迭代提示（Iterative Prompting）使所有研究模型的成功率提高了 5.5%，其中 GPT-4 的成功率提升了 12.33%。  


## **对毕设项目的启发 (Inspirations for the MSc Project)**  

1. **建立专属的 Bug 追踪数据库 (Issue Logging)：** 文献中提出的 15 个漏洞分类学 可以作为 Phase 2 阶段记录 LLM 翻译错误的绝佳模板。在 Obsidian 中，可以为每一个转换失败的 MATLAB 函数建立单独的卡片，并打上 [[Data-related Bugs]] 或 [[Mismatch of API behavior]] 等标签。特别是在处理矩阵运算时，MATLAB 与 Python NumPy 在维度和精度上的差异极易导致数据相关漏洞。  

2. **设计迭代反馈循环 (Iterative Prompting Workflow)：** 不要期望 LLM 能够一次性输出完美的 Python 代码。借鉴论文中的方法，如果在本地环境运行生成的 Python 代码报错，应当捕获具体的错误日志（Error Log）或堆栈跟踪（Stack Trace），连同原始 MATLAB 代码一起作为下一次 Prompt 的输入反馈给模型。  

3. **对比传统工具与 LLM (SMOP vs. LLMs)：** 论文对比了 C2Rust、CxGo 等传统工具与 GPT-4。这恰好印证了目前正在测试的非 LLM 工具 `[[SMOP]]` 的研究价值。在论文撰写时，可以设计一个对照实验：一组使用调试好的 SMOP 自动转译，另一组使用多种 LLM 进行翻译，对比它们在处理特定声发射算法时的性能差异和生成的代码风格（Idiomaticity）。  

4. **应对“真实项目”复杂性 (Handling Real-world Complexity)：** 论文指出 LLM 在处理复杂真实项目时极易失败，因为模型缺乏对整个项目文件依赖和声明的全局认知。这提醒我们在处理 UoB-NDT 组的声发射分析代码时，绝对不能将整个工程直接丢给模型，而应该使用程序分解技术，按功能模块或单个脚本（Fragment）分批输入，最后再在 Python 环境中进行手动组装和连接。

---
# English Version

**Paper Title:** Lost in Translation: A Study of Bugs Introduced by Large Language Models while Translating Code
**Conference/Year:** ICSE 2024
**Research Topic:** An in-depth study of the various bugs introduced by [[Large Language Models (LLMs)]] during cross-language [[Code Translation]], proposing mitigation strategies based on prompt engineering.

## **Key Findings**

- **Limitations of LLMs in code translation:** The study evaluated 1,700 code samples across five languages: C, C++, Go, Java, and Python. Overall, general and code-specific LLMs are not yet able to reliably automate code translation, with success rates ranging only from 2.1% to 47.3%.

- **Extreme challenges in real-world projects:** When dealing with complex, real-world open-source projects, LLMs performed extremely poorly. Even the best-performing model, GPT-4, achieved only an 8.1% success rate, while other models had a 0% success rate.

- **[[Bug Taxonomy]]:** Through extensive manual annotation, the authors categorized the code translation bugs introduced by LLMs into 5 main categories and 15 subcategories:
    • **[[Data-related Bugs]]:** The highest proportion (33.5%), primarily manifesting as incorrect input parsing and incorrect data type selection in the target language.
    • **[[Syntactic and Semantic Differences]]:** Accounting for 30.5%, such as mismatch of API behavior across different languages or directly copying the syntax of the source language.
    • **[[Dependency and Logic Bugs]]:** Accounting for 24.2%, most commonly missing library imports and removal of logic in the source code.
    • **[[Model Specific Constraints]]:** Errors caused by model limitations, such as context window constraints.

- **Comparison between non-LLM tools and LLMs:** Traditional transpilers (like CxGo, C2Rust) perform better in terms of determinism and project context mastery, but the generated code is often non-idiomatic to the target language and may even present security risks (e.g., C2Rust generating unsafe code). In contrast, LLM-generated code has a more human-like programming style but is prone to errors with complex dependencies.

- **[[Prompt Crafting]] Strategies:** Providing context containing error information (such as stack traces, compilation error logs, and inputs/outputs of failed tests) can significantly improve the repair capabilities of LLMs. This iterative prompting increased the success rate of all studied models by 5.5%, with GPT-4 seeing a 12.33% increase.

## **Inspirations for the MSc Project**

1. **Establish a dedicated Bug Tracking Database (Issue Logging):** The 15 bug taxonomies proposed in the literature can serve as an excellent template for logging LLM translation errors in Phase 2. In Obsidian, I can create a separate card for each MATLAB function that fails to translate, tagging them with [[Data-related Bugs]] or [[Mismatch of API behavior]]. Especially when dealing with matrix operations, the differences in dimensionality and precision between MATLAB and Python's NumPy can easily lead to data-related bugs.

2. **Design an Iterative Prompting Workflow:** Do not expect LLMs to output perfect Python code in a single pass. Drawing from the paper's methodology, if the generated Python code throws an error when run in the local environment, I should capture the specific Error Log or Stack Trace. Feed this back to the model as input for the next prompt, along with the original MATLAB code.

3. **Compare Traditional Tools with LLMs ([[SMOP]] vs. LLMs):** The paper compared traditional tools like C2Rust and CxGo with GPT-4. This validates the research value of the non-LLM tool [[SMOP]] which are currently testing. When writing my dissertation, I can design a controlled experiment: one group using the debugged SMOP for automatic transpilation, and another using various LLMs for translation. Compare their performance differences and the idiomaticity of the generated code when handling specific acoustic emission algorithms.

4. **Handling Real-world Complexity:** The paper points out that LLMs easily fail when handling complex real-world projects because they lack a global understanding of project file dependencies and declarations. This reminds us that when dealing with the acoustic emission analysis code of the UoB-NDT group, we must absolutely not throw the entire project at the model. Instead, we should use program decomposition techniques, inputting the code in batches by functional modules or single scripts (Fragments), and finally assembling and connecting them manually in the Python environment.