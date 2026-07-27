University of Birmingham – School of Metallurgy and Materials
MSci project P 15 – UoB-NDT group

**Title:** ‘Migration to an Open-Source Computational Framework for Acoustic Emission Analysis applied to Steel Structures’

**Supervisor**: Prof. Mayorkinos Papaelias ([m.papaelias@bham.ac.uk](mailto:m.papaelias@bham.ac.uk))
**Co-supervisor**: Dr Vincenzo Brachetta ([v.brachetta@bham.ac.uk](mailto:v.brachetta@bham.ac.uk))
**Student**: Haoyu Wang ([hxw702@student.bham.ac.uk](mailto:hxw702@student.bham.ac.uk))

**Key Themes for Reflection and Study**

-       Role and limitations of generative AI in higher education and scientific computing

-       Principles and practice of open-source scientific software

-       Reproducibility, transparency, and FAIR data/software principles

-       Data confidentiality and risks associated with using large language models

-       Comparative analysis of MATLAB vs Python/Julia in scientific workflows

-       Purpose and structure of the existing in-house Acoustic Emission analysis code

-       Code complexity assessment and refactoring strategies

-       Identification of potential errors introduced during automated code translation

-       Use of LLMs for debugging, performance analysis, and code optimisation

**Methodology and Work Plan**

**Phase 1 – Familiarisation and Preliminary Analysis**
-       Review relevant literature

-       Study the existing MATLAB codebase:

o   Understand algorithmic objectives

o   Identify variables, inputs, outputs, and data flow

o   Produce a structured flowchart of the code architecture

-       Define functional requirements for the translated system

**Phase 2 – Translation and AI-Assisted Development**
-       Design structured prompts for code translation into Python or Julia

-       Evaluate and compare outputs from different LLMs

-       Document all prompts, responses, and iterative improvements in a reproducible format

-       Implement translated code and validate against original MATLAB outputs

-       Use LLMs to assist with:

o   Interpretation of error messages

o   Debugging and refactoring suggestions

o   Code optimisation

-       Maintain a clear log of issues, corrections, and design decisions

**Phase 3 – Validation, Optimisation, and Finalisation**
-       Validate numerical and functional equivalence between implementations

-       Refine and optimise code for performance and readability

-       Conduct systematic testing using representative datasets

-       Assess robustness and potential edge cases

-       Evaluate risks of AI-assisted code generation (_e.g._ logic errors, hallucinated functions)

**Selected readings**
-       Pan, R., Ibrahimzada, A.R., Krishna, R., Sankar, D., Pouguem Wassi, L., Merler, M., Sobolev, B., Pavuluri, R., Sinha, S. and Jabbarvand, R. (2024) _Lost in Translation: A Study of Bugs Introduced by Large Language Models while Translating Code_. In: Proceedings of the IEEE/ACM 46 th International Conference on Software Engineering (ICSE 2024).

-       Giabbanelli, Philippe J. and Beverley, John and David, Istvan and Tolk, Andreas, _From Over-Reliance to Smart Integration: Using Large-Language Models as Translators between Specialized Modeling and Simulation Tools_ (June 11, 2025). Available at SSRN: https://ssrn.com/abstract=5365069 or http://dx.doi.org/10.2139/ssrn.5365069

-       De Siano, G.D., Fasolino, A.R., Sperlí, G. and Vignali, A. (2025) _Translating code with Large Language Models and human-in-the-loop feedback_. Information and Software Technology, 186, 107785. Available at: [https://doi.org/10.1016/j.infsof.2025.107785](https://doi.org/10.1016/j.infsof.2025.107785)

-       Khalifa, M. and Albadawy, M. (2024) ‘Using artificial intelligence in academic writing and research: An essential productivity tool’, _Computer Methods and Programs in Biomedicine Update_, Vol. 5, 100145.

**Guidelines**
-       Why and How to Translate Scientific code from MATLAB to Python: A Guide for Researchers. [https://neuroinformatics.dev/blog/matlab_to_python.html](https://neuroinformatics.dev/blog/matlab_to_python.html), Accessed 27 March 2026

-       Student and PGR guidance on using GenAI tools ethically for work [https://intranet.birmingham.ac.uk/student/libraries/asc/student-guidance-gai.aspx](https://intranet.birmingham.ac.uk/student/libraries/asc/student-guidance-gai.aspx), Accessed

-       Russell Group principles on the use of generative AI tools in education, [https://www.russellgroup.ac.uk/sites/default/files/2025-01/Russell%20Group%20principles%20on%20generative%20AI%20in%20education.pdf](https://www.russellgroup.ac.uk/sites/default/files/2025-01/Russell%20Group%20principles%20on%20generative%20AI%20in%20education.pdf) Accessed 21 April 2026

-       Principles on the use of generative AI tools in education [https://www.russellgroup.ac.uk/policy/policy-briefings/principles-use-generative-ai-tools-education](https://www.russellgroup.ac.uk/policy/policy-briefings/principles-use-generative-ai-tools-education) Accessed 21 April 2026

**Tools**
-       Python v 3.0 or greater
-       Julia v 1.12 or greater
-       VSCodium (or VSCode)
-       Small MATLAB and Octave to Python compiler (SMOP)[https://github.com/victorlei/smop](https://github.com/victorlei/smop), Accessed 27 March 2026

**LLMs tools**
-       OpenAI ChatGPT GPT 5.3: ([https://chatgpt.com](https://chatgpt.com/))
-       Google Gemini 3 Flash: ([https://gemini.google.com](https://gemini.google.com/))
-       Anthropic Claude Sonnet 4.6: ([https://claude.ai](https://claude.ai/))
-       DeepSeek-AI DeepSeek 3.2: ([https://www.deepseek.com](https://www.deepseek.com/))

**Additional LLMs tools available through the UoB AI Pilot Scheme**
-       OpenAI ChatGPT GPT 5.2: ([https://chatgpt.com](https://chatgpt.com/))
-       Anthropic Opus 4.6: ([https://claude.ai](https://claude.ai/))
-       Meta Llama 4 Maverick ([https://www.llama.com](https://www.llama.com))