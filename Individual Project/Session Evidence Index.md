---
status: evidence-register
scope: project-wide
last_verified: 2026-07-29
---

# Session Evidence Index

> [!warning] Evidence-only session registry
> A session is marked `confirmed` only when a retained machine-readable or
> historical artifact explicitly records it. `not_available` means the project
> evidence does not retain a recoverable session identifier. `not_applicable`
> means the activity was deterministic or was a researcher decision rather
> than a model session. Missing fields must not be reconstructed from filenames,
> timestamps, model families, unretained interaction context or later outputs.
> The original prompts, responses, source artifacts, candidates and historical
> records referenced here were not edited to create this register. Absolute
> paths are provided only for local inspection; project-relative paths are the
> portable evidence references.

Project-level current scope remains in
[[Individual Project/README|Canonical Project Overview]]. Claim and artifact
mapping is in [[Individual Project/Thesis Evidence Index|Thesis Evidence Index]].

Path convention:

- **Project-relative** paths are relative to `Individual Project/`.
- The absolute root is
  `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/`.
- SHA-256 values identify the retained evidence file or the exact prompt,
  response or candidate where explicitly listed.

## Confirmed Sessions

### Confirmed CT07 Artifact Lineage

These hashes come directly from the candidate manifest. Each retained layer has
an explicit project-relative path and an absolute path for local inspection.

| Candidate | Artifact layer | Status | Notes | Project-relative path | Absolute path (local inspection only) | SHA-256 |
|---|---|---|---|---|---|---|
| `deepseek_julia` | generation prompt | `confirmed` | retained artifact | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/deepseek_julia/prompt.md` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/deepseek_julia/prompt.md` | `e9dbbdbdb68acefc3e30c4db21c90efb5eb7a022d8788fba9c0c27092e072967` |
| `deepseek_julia` | recorded response | `confirmed` | retained artifact | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/deepseek_julia/response.md` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/deepseek_julia/response.md` | `23fa1e272a5db135fc8b3d2ace604fd4d45d140c12458e550b77873ac04c1ae1` |
| `deepseek_julia` | original generation source | `confirmed` | direct historical file | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/deepseek_julia/original_generation.jl` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/deepseek_julia/original_generation.jl` | `b4569be3c959cae6cafda9122ca4060fb2a2c18a12ee12ba055ad7892ae298d6` |
| `deepseek_julia` | fixture-normalized probe | `confirmed` | fixture-normalized derivative | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/deepseek_julia/fixture_normalized_probe.jl` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/deepseek_julia/fixture_normalized_probe.jl` | `0a1015853b82cf1c1ebc925861c87f3135364d6d3108d5c9563027e67a1e4f0d` |
| `deepseek_julia` | candidate-derived validation runner | `confirmed` | candidate-derived validated derivative | `CT07-PeakFreq-Validation/code/ct07/julia/deepseek_julia.jl` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/code/ct07/julia/deepseek_julia.jl` | `c9775f2cd7b87763a9484f93c4431ff580f7fbd7ef7baffae2520f3d104a6f29` |
| `deepseek_python` | generation prompt | `confirmed` | retained artifact | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/deepseek_python/prompt.md` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/deepseek_python/prompt.md` | `c17d27bee43ba6e5663055fc40d7ba656370849d01e5d0a0fae7295ad1bd6498` |
| `deepseek_python` | recorded response | `confirmed` | retained artifact | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/deepseek_python/response.md` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/deepseek_python/response.md` | `d01a0d485c354ef85d495badfc79d16a1f6395e397a4bccb042ffd2ea5f7bd60` |
| `deepseek_python` | original generation source | `confirmed` | direct historical file | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/deepseek_python/original_generation.py` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/deepseek_python/original_generation.py` | `c76666e7d7b87f2d7974d62e0d41e35ec6f57c859e85fe691dd7fb0e5591d72e` |
| `deepseek_python` | fixture-normalized probe | `confirmed` | `no_change_required`; probe uses the original-generation bytes | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/deepseek_python/original_generation.py` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/deepseek_python/original_generation.py` | `c76666e7d7b87f2d7974d62e0d41e35ec6f57c859e85fe691dd7fb0e5591d72e` |
| `deepseek_python` | candidate-derived validation runner | `confirmed` | candidate-derived validated derivative | `CT07-PeakFreq-Validation/code/ct07/python/deepseek_python.py` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/code/ct07/python/deepseek_python.py` | `70f18a4b3bb1367ea06a50efced61a257dc08625548525a81f66ca652c4a0b30` |
| `gemini_julia` | generation prompt | `confirmed` | retained artifact | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/gemini_julia/prompt.md` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/gemini_julia/prompt.md` | `d8ac73ab41651079fcefd29d87ba4a885d2cfe287562958c04314297904ebc0e` |
| `gemini_julia` | recorded response | `confirmed` | retained artifact | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/gemini_julia/response.md` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/gemini_julia/response.md` | `6c7e1dd51168f537af2acd48b2de04a2876c0cd85f998f169ede66a4cdb5a9fd` |
| `gemini_julia` | original generation source | `confirmed` | direct historical file | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/gemini_julia/original_generation.jl` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/gemini_julia/original_generation.jl` | `d64bd6e547783fdfd1c8059c82966e42528414f1f023914cc04396f8dee9ae30` |
| `gemini_julia` | fixture-normalized probe | `confirmed` | fixture-normalized derivative | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/gemini_julia/fixture_normalized_probe.jl` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/gemini_julia/fixture_normalized_probe.jl` | `cf2d9da1236782206a5c06c285348f773960c0d2246c1459907ded5e80fafec8` |
| `gemini_julia` | candidate-derived validation runner | `confirmed` | candidate-derived validated derivative | `CT07-PeakFreq-Validation/code/ct07/julia/gemini_julia.jl` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/code/ct07/julia/gemini_julia.jl` | `b13aeebf998f2412d0282ac9833a36949e0e1198bcaf9725992704edc93c6b5e` |
| `gemini_python` | generation prompt | `confirmed` | retained artifact | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/gemini_python/prompt.md` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/gemini_python/prompt.md` | `a4e516e26471b5ff1ee0db1eb1bcde39abc24d7fd23d80d0b45e86ffbd2b1ea0` |
| `gemini_python` | recorded response | `confirmed` | retained artifact | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/gemini_python/response.md` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/gemini_python/response.md` | `ebfda39c3150f7ca4d5d70e8930d8bffd07ae7f7cd8c1e410f19305dcf194daa` |
| `gemini_python` | original generation source | `confirmed` | direct historical file | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/gemini_python/original_generation.py` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/gemini_python/original_generation.py` | `76c5fc095e4829f00970f6958a0d6c4d335f33714f7bdb676126948bc3d66f88` |
| `gemini_python` | fixture-normalized probe | `confirmed` | `no_change_required`; probe uses the original-generation bytes | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/gemini_python/original_generation.py` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/gemini_python/original_generation.py` | `76c5fc095e4829f00970f6958a0d6c4d335f33714f7bdb676126948bc3d66f88` |
| `gemini_python` | candidate-derived validation runner | `confirmed` | candidate-derived validated derivative | `CT07-PeakFreq-Validation/code/ct07/python/gemini_python.py` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/code/ct07/python/gemini_python.py` | `762fca9eba75e18b4e8a76374a7cca90276994c2f69da973c1e335ba8a29c149` |
| `gpt55_julia` | generation prompt | `confirmed` | retained artifact | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/gpt55_julia/prompt.md` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/gpt55_julia/prompt.md` | `1c5d4c80741ac1280b6a5ec0d41cb5a925e6c7b53470af8db0a39c4f732a225c` |
| `gpt55_julia` | recorded response | `confirmed` | retained artifact | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/gpt55_julia/response.md` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/gpt55_julia/response.md` | `eb140e47db840a99040f456e36ff93a7564e580e4f0670e340fd3fd1876247b0` |
| `gpt55_julia` | original generation source | `confirmed` | direct historical file | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/gpt55_julia/original_generation.jl` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/gpt55_julia/original_generation.jl` | `f412a103418f8a5a631f7d039496cc7a716a2ceaaa251ce73cf42f65186becad` |
| `gpt55_julia` | fixture-normalized probe | `confirmed` | fixture-normalized derivative | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/gpt55_julia/fixture_normalized_probe.jl` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/gpt55_julia/fixture_normalized_probe.jl` | `4b320191fb2500da3be7f9222eb1f0625e9f8b34f60865eaa1f94142358f2bd8` |
| `gpt55_julia` | candidate-derived validation runner | `confirmed` | candidate-derived validated derivative | `CT07-PeakFreq-Validation/code/ct07/julia/gpt55_julia.jl` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/code/ct07/julia/gpt55_julia.jl` | `a5d89112e46c5d3fa5599d189a51048b72c1d2c52f2804239ddf1eca1ea45849` |
| `gpt55_python` | generation prompt | `confirmed` | retained artifact | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/gpt55_python/prompt.md` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/gpt55_python/prompt.md` | `e28069d3b05fe3d9066c85c05110cad4d82365d4ff426982588f27b13b97713c` |
| `gpt55_python` | recorded response | `confirmed` | retained artifact | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/gpt55_python/response.md` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/gpt55_python/response.md` | `dbb904d34c90d2a5568425a6aaa521eb29947a08e5965b3b8518e6d5868c3877` |
| `gpt55_python` | original generation source | `confirmed` | `reconstructed_from_record`; original byte-exact file: `not_available` | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/gpt55_python/original_generation.py` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/gpt55_python/original_generation.py` | `c13a2e082b1e1f9fbb92fb7f8a1ebfd48834d0092976f005a0f590a57e738595` |
| `gpt55_python` | fixture-normalized probe | `confirmed` | fixture-normalized derivative | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/gpt55_python/fixture_normalized_probe.py` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/gpt55_python/fixture_normalized_probe.py` | `233c14d996fd1ba7e1c8290265afd95301462ae500c67e2bb363501331313e02` |
| `gpt55_python` | candidate-derived validation runner | `confirmed` | candidate-derived validated derivative | `CT07-PeakFreq-Validation/code/ct07/python/gpt55_python.py` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/code/ct07/python/gpt55_python.py` | `5f8613823fb8818aa632faf9a80c6760b1f6360dab285ab521d0d65bd2f6e688` |
| `sonnet_julia` | generation prompt | `confirmed` | retained artifact | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/sonnet_julia/prompt.md` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/sonnet_julia/prompt.md` | `d8ac73ab41651079fcefd29d87ba4a885d2cfe287562958c04314297904ebc0e` |
| `sonnet_julia` | recorded response | `confirmed` | retained artifact | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/sonnet_julia/response.md` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/sonnet_julia/response.md` | `0ccc06b3c5dfdd7a6c14092a5014e5b2fdb9a766248c65c0fc6e05da02b4818e` |
| `sonnet_julia` | original generation source | `confirmed` | `reconstructed_from_record`; original byte-exact file: `not_available` | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/sonnet_julia/original_generation.jl` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/sonnet_julia/original_generation.jl` | `6ed1181cace171ae6a0bb2afb8f3cf547e0a798dadd2897d0017a6db61fb7132` |
| `sonnet_julia` | fixture-normalized probe | `confirmed` | fixture-normalized derivative | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/sonnet_julia/fixture_normalized_probe.jl` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/sonnet_julia/fixture_normalized_probe.jl` | `e77f0121ef601c4a17a270de5a77d10711ef7218429c65d43ebaad004e4579db` |
| `sonnet_julia` | candidate-derived validation runner | `confirmed` | candidate-derived validated derivative | `CT07-PeakFreq-Validation/code/ct07/julia/sonnet_julia.jl` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/code/ct07/julia/sonnet_julia.jl` | `baf5f4c4c88bf6ff205bce0b8976f10ec9c74cdcd1dded6deb6ac8e1f8220e13` |
| `sonnet_python` | generation prompt | `confirmed` | retained artifact | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/sonnet_python/prompt.md` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/sonnet_python/prompt.md` | `a4e516e26471b5ff1ee0db1eb1bcde39abc24d7fd23d80d0b45e86ffbd2b1ea0` |
| `sonnet_python` | recorded response | `confirmed` | retained artifact | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/sonnet_python/response.md` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/sonnet_python/response.md` | `cbfbdb031c7f0da910b526341ac2000556c8c56ac12f27b21cafb91cdd034404` |
| `sonnet_python` | original generation source | `confirmed` | `reconstructed_from_record`; original byte-exact file: `not_available` | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/sonnet_python/original_generation.py` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/sonnet_python/original_generation.py` | `2d7e5518cd91d36d4a58ead866343af4de292f53f585d3cd2ad55b6025b6996f` |
| `sonnet_python` | fixture-normalized probe | `confirmed` | `no_change_required`; probe uses the original-generation bytes | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/sonnet_python/original_generation.py` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidates/sonnet_python/original_generation.py` | `2d7e5518cd91d36d4a58ead866343af4de292f53f585d3cd2ad55b6025b6996f` |
| `sonnet_python` | candidate-derived validation runner | `confirmed` | candidate-derived validated derivative | `CT07-PeakFreq-Validation/code/ct07/python/sonnet_python.py` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/code/ct07/python/sonnet_python.py` | `d3b8ff4b61e378b2ac25902e5c78b86cd1515e45f45cb5de21cb23a0439b0151` |

Three original-generation artifacts are explicitly marked
`reconstructed_from_record` in the candidate manifest:

- `gpt55_python`;
- `sonnet_julia`;
- `sonnet_python`.

They are not described as surviving byte-exact raw files.

### DTA Model Sessions

| Activity | Model / reasoning | Session ID | Started UTC | Status | Notes | Project-relative evidence | Absolute evidence | Evidence SHA-256 |
|---|---|---|---|---|---|---|---|---|
| MATLAB-source candidate generation | GPT-5.5 / xhigh | `019fa582-f69b-7061-878e-afb14d409ac4` | `2026-07-27T21:37:31Z` | `confirmed` | isolated candidate-generation session | `MistrasDTAJulia/experiments/experiment_evidence.toml` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/MistrasDTAJulia/experiments/experiment_evidence.toml` | `62236cdbfe32d79caa8bccafd5f356171400ee12e3b871c7be9f5e967b5be432` |
| Python-source candidate generation | GPT-5.5 / xhigh | `019fa58b-67a9-7f83-9bd1-34b4e6336a87` | `2026-07-27T21:46:44Z` | `confirmed` | isolated candidate-generation session | `MistrasDTAJulia/experiments/experiment_evidence.toml` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/MistrasDTAJulia/experiments/experiment_evidence.toml` | `62236cdbfe32d79caa8bccafd5f356171400ee12e3b871c7be9f5e967b5be432` |
| Parent evidence-recovery rollout | Codex CLI 0.140.0; no separate model field established for this row | `019fa0fb-8468-7f30-8c6e-0b827f0e13e1` | `not_available` in the evidence file | `confirmed` | evidence-recovery rollout only; final-reader authorship session remains `not_available` | `MistrasDTAJulia/experiments/experiment_evidence.toml` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/MistrasDTAJulia/experiments/experiment_evidence.toml` | `62236cdbfe32d79caa8bccafd5f356171400ee12e3b871c7be9f5e967b5be432` |

#### DTA Frozen Prompt and Candidate Bytes

| Artifact | Project-relative path | Absolute path | SHA-256 |
|---|---|---|---|
| Frozen task prompt | `MistrasDTAJulia/experiments/frozen_prompt.md` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/MistrasDTAJulia/experiments/frozen_prompt.md` | `70c8dcbd741c0ecdbbf9d1b4e3625843260e4060c97bb68e79b19893dc73fd81` |
| CLI invocation prompt | `MistrasDTAJulia/experiments/invocation_prompt.txt` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/MistrasDTAJulia/experiments/invocation_prompt.txt` | `d1dc99fe5e3b6bbed9e0c4265e22bd0e920e7ca0738cadbb6391cb63d78edcf3` |
| MATLAB-source raw response | `MistrasDTAJulia/experiments/matlab_source_raw_response.txt` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/MistrasDTAJulia/experiments/matlab_source_raw_response.txt` | `268988d6a80836f839676b70d24cb500b13bde15cd39d089bebe895136bfd6ec` |
| MATLAB-source candidate | `MistrasDTAJulia/experiments/matlab_source_candidate.jl` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/MistrasDTAJulia/experiments/matlab_source_candidate.jl` | `268988d6a80836f839676b70d24cb500b13bde15cd39d089bebe895136bfd6ec` |
| Python-source raw response | `MistrasDTAJulia/experiments/python_source_raw_response.txt` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/MistrasDTAJulia/experiments/python_source_raw_response.txt` | `fa0bbe3c33d3752406ae719d0adc745a4d5a51a820a4612a8d576920522dddf1` |
| Python-source candidate | `MistrasDTAJulia/experiments/python_source_candidate.jl` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/MistrasDTAJulia/experiments/python_source_candidate.jl` | `fa0bbe3c33d3752406ae719d0adc745a4d5a51a820a4612a8d576920522dddf1` |

The experiment evidence records that each raw response and candidate pair is
byte-identical and was frozen before first execution. Platform system
instructions were not recovered.

## Unconfirmed or Unavailable Sessions

### CT07 Original-Generation Sessions

The candidate manifest explicitly records every generation date and session ID
below as `not_available`. Model, interface and reasoning level are confirmed.

| Candidate | Model | Interface | Reasoning | Generation date | Session ID | Status | Project-relative evidence | Absolute evidence | Evidence SHA-256 |
|---|---|---|---|---|---|---|---|---|---|
| `deepseek_julia` | DeepSeek v4 Pro | Claude Code CLI via ccswitch | High | `not_available` | `not_available` | `not_available` | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidate_manifest.json` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidate_manifest.json` | `8657d7b0e966ecaaeb8451269c142a01930047c24b003a52c97f34b1c6ac93fa` |
| `deepseek_python` | DeepSeek v4 Pro | Claude Code CLI via ccswitch | XHigh | `not_available` | `not_available` | `not_available` | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidate_manifest.json` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidate_manifest.json` | `8657d7b0e966ecaaeb8451269c142a01930047c24b003a52c97f34b1c6ac93fa` |
| `gemini_julia` | Gemini 3.1 Pro | Antigravity CLI | High | `not_available` | `not_available` | `not_available` | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidate_manifest.json` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidate_manifest.json` | `8657d7b0e966ecaaeb8451269c142a01930047c24b003a52c97f34b1c6ac93fa` |
| `gemini_python` | Gemini 3.1 Pro | Antigravity CLI | High | `not_available` | `not_available` | `not_available` | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidate_manifest.json` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidate_manifest.json` | `8657d7b0e966ecaaeb8451269c142a01930047c24b003a52c97f34b1c6ac93fa` |
| `gpt55_julia` | GPT-5.5 | Codex CLI | XHigh | `not_available` | `not_available` | `not_available` | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidate_manifest.json` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidate_manifest.json` | `8657d7b0e966ecaaeb8451269c142a01930047c24b003a52c97f34b1c6ac93fa` |
| `gpt55_python` | GPT-5.5 | Codex CLI | XHigh | `not_available` | `not_available` | `not_available` | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidate_manifest.json` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidate_manifest.json` | `8657d7b0e966ecaaeb8451269c142a01930047c24b003a52c97f34b1c6ac93fa` |
| `sonnet_julia` | Claude Sonnet 4.6 | Claude Code Desktop | High | `not_available` | `not_available` | `not_available` | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidate_manifest.json` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidate_manifest.json` | `8657d7b0e966ecaaeb8451269c142a01930047c24b003a52c97f34b1c6ac93fa` |
| `sonnet_python` | Claude Sonnet 4.6 | Claude Code Desktop | High | `not_available` | `not_available` | `not_available` | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidate_manifest.json` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidate_manifest.json` | `8657d7b0e966ecaaeb8451269c142a01930047c24b003a52c97f34b1c6ac93fa` |

### Other Implementation or Debugging Sessions

| Case/activity | Activity classification | Status | Notes | Project-relative evidence | Absolute evidence | Evidence SHA-256 |
|---|---|---|---|---|---|---|
| CT07 fixture-normalization and validation-runner debugging | `agent_assisted_debugging` | `not_available` | model, interface, date and session are not retained as one attributable activity record | `CT07-PeakFreq-Validation/results/ct07/llm-validation/experiment_record.md` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/experiment_record.md` | `189ea541a2f223751c737c26ed1cdf3cac7ae9fc0a0df33adbc5980b79ac79d2` |
| SMOP recovery-path debugging | `agent_assisted_debugging` | `not_available` | model, interface, date and session are not retained | `CT07-PeakFreq-Validation/results/ct07/smop/运行问题与解决记录.md` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/smop/运行问题与解决记录.md` | `095eabe82373b50cbec37e7a51bcada3f87fdc248d9762b12dd4891eed0d1b3b` |
| Legacy Top-1 implementation/debugging | `agent_assisted_debugging` | `not_available` | model, interface, date and session are not retained | `CT07-PeakFreq-Validation/results/peak-frequency/legacy-t01-three-language/legacy-regression-current/comparison_summary.json` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/peak-frequency/legacy-t01-three-language/legacy-regression-current/comparison_summary.json` | `8a0e2f9d71a48a6f4b248c75fb2ab52b6479a9807fa5ae1379438c2af0259eab` |
| Adaptive/Top-3 strict-distance repair | `agent_assisted_debugging` | `not_available` | model, interface, date and session are not retained | `CT07-PeakFreq-Validation/results/peak-frequency/adaptive-three-language/experiment_record.md` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/peak-frequency/adaptive-three-language/experiment_record.md` | `e2c258da34407bfbd2e47390fe2175e92f213d4982ab2c1222a8e51ca6ef3cd1` |
| Scientific morphology/alignment/Top-3 analysis | `agent_assisted_debugging` | `not_available` | implementation/debugging model, interface, date and session are not retained | `CT07-PeakFreq-Validation/results/scientific/Scientific Interpretation Report.md` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/scientific/Scientific Interpretation Report.md` | `3c6e9589b2695ed766bc28936626bc2c70e9d74001fb0dd1abe9ab4327688e53` |
| DTA final-reader implementation | `agent_assisted_debugging` | `not_available` | separate final-reader authorship session is not retained; Python-source route selection is confirmed | `MistrasDTAJulia/experiments/experiment_evidence.toml` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/MistrasDTAJulia/experiments/experiment_evidence.toml` | `62236cdbfe32d79caa8bccafd5f356171400ee12e3b871c7be9f5e967b5be432` |
| WFS Julia reader implementation/debugging | `agent_assisted_debugging` | `not_available` | model, interface, date and session are not retained | `MistrasWFSJulia/results/final_validation.md` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/MistrasWFSJulia/results/final_validation.md` | `b4d1370f5b260cb61dc6d49fdc8d82880bc424c260d4c8eb97c5e9707813ffb7` |
| R260_2 streaming analysis implementation/debugging | `agent_assisted_debugging` | `not_available` | model, interface, date and session are not retained | `R2602Analysis/PROVENANCE.md` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/R2602Analysis/PROVENANCE.md` | `55969a85f5ea5bdff67a268855c67b297ad56aebbcd6a934fc732d4cdb6fee2f` |
| Final clean-rehearsal harness repair | `agent_assisted_debugging` | `not_available` | the interactive debugging session ID is not retained; the first environment-declaration failure and its bounded repair are recorded without inference | `CT07-PeakFreq-Validation/rehearsals/final-20260729/failure_classification.json` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/rehearsals/final-20260729/failure_classification.json` | `4305eba52b972065d2470c8822e0a81d00e9a5ee77e464cf34372ee2fc809062` |

## Not Applicable Activities

| Case/activity | Activity classification | Status | Notes | Project-relative evidence | Absolute evidence | Evidence SHA-256 |
|---|---|---|---|---|---|---|
| CT07 MATLAB comparison | `automated_verification` | `not_applicable` | deterministic MATLAB-oracle comparison | `CT07-PeakFreq-Validation/results/ct07/llm-validation/comparison_summary.json` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/comparison_summary.json` | `eae63d4e1759f6ae90d3025b68c85c3515b35dbd9b758fbeec28f1a3bba50d85` |
| SMOP translation | deterministic transpilation | `not_applicable` | SMOP 0.41 deterministic transpilation | `CT07-PeakFreq-Validation/results/ct07/smop/environment_metadata.json` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/smop/environment_metadata.json` | `ddf13a67a29d4486f30a6a1c49e8d04bb7fd8d257334c0fd64e80adeec11748d` |
| SMOP recovery-path numerical comparison | `automated_verification` | `not_applicable` | deterministic MATLAB-oracle comparison | `CT07-PeakFreq-Validation/results/ct07/smop/smop_comparison_summary.json` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/smop/smop_comparison_summary.json` | `aa511f6b05b05dbf851aebed3b56aa0c6b27bf8dfe02347b12522c6d7d27d2c7` |
| Legacy Top-1 three-language comparison | `automated_verification` | `not_applicable` | deterministic symmetric row comparison | `CT07-PeakFreq-Validation/results/peak-frequency/legacy-t01-three-language/legacy-regression-current/comparison_summary.json` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/peak-frequency/legacy-t01-three-language/legacy-regression-current/comparison_summary.json` | `8a0e2f9d71a48a6f4b248c75fb2ab52b6479a9807fa5ae1379438c2af0259eab` |
| Adaptive/Top-3 algorithm contract | `researcher_decision` | `not_applicable` | researcher-defined numerical contract | `CT07-PeakFreq-Validation/results/peak-frequency/adaptive-three-language/experiment_record.md` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/peak-frequency/adaptive-three-language/experiment_record.md` | `e2c258da34407bfbd2e47390fe2175e92f213d4982ab2c1222a8e51ca6ef3cd1` |
| Adaptive/Top-3 three-language comparison | `automated_verification` | `not_applicable` | deterministic nine-group comparison | `CT07-PeakFreq-Validation/results/peak-frequency/adaptive-three-language/comparison_summary.json` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/peak-frequency/adaptive-three-language/comparison_summary.json` | `48e3c9fec1ac7e9fbb1ac49b4c50ef938785b2bf10023b3ca77c0e3d48a9e7ff` |
| Scientific morphology/alignment/Top-3 analysis | deterministic analysis and verification | `not_applicable` | deterministic execution and verification; implementation/debugging session is listed separately | `CT07-PeakFreq-Validation/results/scientific/Scientific Interpretation Report.md` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/scientific/Scientific Interpretation Report.md` | `3c6e9589b2695ed766bc28936626bc2c70e9d74001fb0dd1abe9ab4327688e53` |
| DTA validation | `automated_verification` | `not_applicable` | deterministic symmetric fixture comparison | `MistrasDTAJulia/results/comparison_summary.toml` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/MistrasDTAJulia/results/comparison_summary.toml` | `3e24dcebbe9e85dea6e2951ebbbbe9575f95a267181844485c287977bf67d94c` |
| WFS validation | `automated_verification` | `not_applicable` | deterministic symmetric fixture comparison | `MistrasWFSJulia/results/comparison_summary.toml` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/MistrasWFSJulia/results/comparison_summary.toml` | `20ef2afb94c09ce856bb1e446d9c223dcdec8a67ea0092b02e2b382b75c21673` |
| R260_2 bounded rerun | `automated_verification` | `not_applicable` | deterministic bounded rerun | `R2602Analysis/evidence/final-rerun-20260729/rehearsal_summary.json` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/R2602Analysis/evidence/final-rerun-20260729/rehearsal_summary.json` | `8944f7dd9342b15bc31367453b471bbf4fed6bde604432afc6b164ccc4256120` |
| R260_2 full package verification | `automated_verification` | `not_applicable` | deterministic manifest verification | `R2602Analysis/MANIFEST.sha256` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/R2602Analysis/MANIFEST.sha256` | `86a821d8e447ecad40a93d37bb41e7bce33a13bf10609cdf1f5d775f244727d5` |
| Final clean rehearsal | `automated_verification` | `not_applicable` | deterministic same-host clean-environment execution; 61/61 commands passed, staged and canonical verification passed, and protected hashes were unchanged | `CT07-PeakFreq-Validation/rehearsals/final-20260729-r2/rehearsal_summary.json` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/rehearsals/final-20260729-r2/rehearsal_summary.json` | `e9ff3fb9acc19e3c2f2871df2869c319e15a69f04cb0ad7933c9a8c6aeeb9506` |

## Summary

### Status Contract

| Status | Meaning in this register |
|---|---|
| `confirmed` | A retained artifact explicitly records the session or field. |
| `not_available` | The retained evidence does not contain a recoverable value. |
| `unconfirmed` | A value is alleged or suggested but is not established by retained evidence. |
| `not_applicable` | No model session applies to the deterministic activity or researcher decision. |

Status cells use only these four exact values. Reconstruction, artifact origin,
scope qualifications and other explanations are kept in `Notes`, not encoded
as additional statuses.

### Fields Recorded as `not_available`

- CT07: all eight original-generation session IDs and generation dates.
- CT07: one attributable session record for later normalization, repair and
  candidate-derived runner construction.
- SMOP: agent/tool session for the two recovery-path implementations.
- Legacy Top-1: model/interface/session provenance for the retained final
  Python and Julia implementations.
- Adaptive/Top-3: model/interface/session provenance for the Python/Julia
  implementation and strict-distance repair.
- Scientific analysis: implementation/debugging session provenance.
- DTA: a separately established final-reader authorship session. The two
  generation sessions and parent evidence-recovery rollout are confirmed.
- WFS: model/interface/session provenance for the Julia reader.
- R260_2: model/interface/session provenance for the streaming analysis.
- Final clean rehearsal: the interactive agent-assisted harness-repair session
  identifier.

No missing field is completed from unretained interaction metadata or memory.
Original evidence files remain untouched; this register only records paths,
hashes and evidence status.
