# 03Test Julia 运行与问题解决记录

## 1. 任务结论

- 执行日期：2026-06-18（Europe/London，BST）
- Julia：1.12.6（Apple Silicon / aarch64）
- 输入文件：`/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/Tools history/Claude code Desktop Sonnet 4.6/Commercial Tensile Tests.xlsx`
- 数据工作表：`CT07`
- 有效数据行：5,848 行
- 最终结果：成功生成并验证 5 张 PNG；均为 600 × 400、RGB、非交错 PNG。

## 2. 遇到的问题、证据与解决方法

### 问题 1：Julia 启动器无法在沙箱中创建锁文件

第一次执行 `julia --version` 时出现：

```text
Error: The Julia launcher failed to load a configuration file.
Caused by:
    Could not create lockfile `/Users/vangogh/.julia/juliaup/.juliaup-lock`:
    Operation not permitted (os error 1).
```

根因是 `juliaup` 启动器需要写入用户目录 `~/.julia`，而默认沙箱只允许写工作区。获得运行许可后，改用已安装 Julia 1.12.6 的实际二进制文件，绕过启动器锁文件步骤：

```text
/Users/vangogh/.julia/juliaup/julia-1.12.6+0.aarch64.apple.darwin14/Julia-1.12.app/Contents/Resources/julia/bin/julia
```

### 问题 2：脚本依赖未安装

直接运行脚本后首先失败于：

```text
ArgumentError: Package XLSX not found in current path.
- Run `import Pkg; Pkg.add("XLSX")` to install the XLSX package.
```

根因是 Julia 当前项目没有脚本声明的 `XLSX`、`DataFrames`、`Plots`。为避免污染全局项目，在本结果文件夹建立隔离项目并安装、预编译依赖：

```julia
using Pkg
Pkg.add(["XLSX", "DataFrames", "Plots"])
Pkg.precompile()
```

实际解析版本：

- XLSX 0.11.10
- DataFrames 1.8.2
- Plots 1.41.6

对应环境文件为 `Project.toml` 和 `Manifest.toml`。

### 问题 3：脚本硬编码了不存在的工作簿文件名

依赖安装后，原脚本可复现错误为：

```text
File  : Tensile-processed.xlsx
Sheet : CT-07
XLSXError: File Tensile-processed.xlsx not found.
```

根因是脚本 `main()` 写死了 `Tensile-processed.xlsx`，与用户指定的 `Commercial Tensile Tests.xlsx` 不一致。修复为基于脚本目录构造绝对路径：

```julia
filepath = abspath(joinpath(@__DIR__, "Commercial Tensile Tests.xlsx"))
```

这既指向用户提供的绝对位置，又避免从其他工作目录运行时失效。

### 问题 4：脚本工作表名与实际工作簿不一致

只读检查工作簿得到：

```text
sheets=CT07, CT09
```

原脚本使用 `CT-07`，实际工作簿使用 `CT07`。因此将：

```julia
sheet_name = "CT-07"
```

改为：

```julia
sheet_name = "CT07"
```

### 问题 5：`XLSX.readtable` 自动检测使原始 Excel 列号错位

修正文件名和 sheet 后，脚本失败于：

```text
BoundsError: attempt to access data frame with 9 columns at index [10]
```

证据如下：

- CT07 工作表物理范围是 `A1:O6020`，共有 15 列。
- 第 1 行 A:D 为空，从 E:M 才开始连续非空。
- `XLSX.readtable(filepath, "CT07")` 默认寻找第一段连续非空单元格，所以只读取 E:M。
- 自动读取结果为 `size=(5850, 9)`，列名依次是 `Time`、`RMS`、`Cumulative RMS` 等。
- 原脚本仍按原始 Excel 位置访问第 10、12、14 列，因而越界。

先用只读探针验证显式范围方案：

```julia
DataFrame(XLSX.readtable(path, "CT07", "A:O";
    first_row=4, header=false, stop_in_empty_row=false))
```

探针结果：

```text
size=(5848, 15)
selected_types=Union{Missing, Float64} | Union{Missing, Float64} |
               Union{Missing, Float64} | Float64 | Float64 | Float64 |
               Float64 | Float64
```

这保留了 A:O 的原始列位置，并从真正的数值数据区第 4 行开始读取，最终用于修复 `load_ae_data`。

### 问题 6：原脚本只 `display`，不会生成磁盘图片

原入口对 5 个图仅调用 `display(fig)`。在无图形窗口环境里，即使绘图成功，也不会在目标文件夹留下结果。

解决方法：

- 在加载 Plots 前设置 `ENV["GKSwstype"] = "100"`，使用 GR 无窗口渲染。
- 建立 `outputs/03Test Outputs`。
- 对 5 个图逐一调用 `savefig`，使用固定、可检查的文件名。
- 每保存一张图就打印绝对路径。

### 问题 7：第 2 张图标题错误写成 T09

首次视觉检查发现第 2 张图使用 CT07 数据，但标题是 `T09 Commercial Normalised RMS Profile`。脚本注释也说明这是原 MATLAB 脚本的复制错误。

增加标题断言后先得到失败退出码 1，再将标题改为：

```text
T07 Commercial Normalised RMS Profile
```

断言随后通过，并重新生成全部 5 张图。

## 3. 脚本中的必要修改

修改的是工作区原脚本 `Test3 by sonnet4.6high ae_analysis.jl`，主要位置如下：

- 第 28 行：启用 GR 无窗口渲染。
- 第 68 行：显式读取 CT07 的 A:O、从第 4 行开始、保留 15 列位置。
- 第 167 行：将 Figure 2 标题从 T09 修正为 T07。
- 第 293–295 行：设置正确工作簿、sheet 与输出目录。
- 第 313–325 行：为 5 张图定义固定文件名并逐一 `savefig`。

没有改变应力、应变、RMS、累计 RMS、AE 能量、累计 AE 能量的绘图函数和列映射含义。

## 4. 测试过程

### 端到端失败测试（修复前）

`test_generate_outputs.sh` 运行真实 Julia 脚本，并要求 5 个指定 PNG 都存在、非空且目录中恰好有 5 个 PNG。修复前，它先后捕获了文件名错误和 9 列越界错误，因此证明测试能检测到原问题。

### 标题失败测试（修复前）

`test_ct07_title.sh` 要求 Figure 2 标题识别 CT07 数据集。修复前退出码为 1，修复后输出：

```text
PASS: Figure 2 title identifies the CT07 dataset.
```

### 最终端到端测试（修复后）

最终运行命令：

```zsh
zsh 'outputs/03Test Outputs/test_generate_outputs.sh'
```

关键结果：

```text
Loaded 5848 data points.
All five figures saved successfully.
PASS: generated exactly 5 non-empty PNG files.
```

完整成功输出另存为 `final_run.log`。

## 5. 最终图片验证

| 文件 | 字节数 | SHA-256 |
|---|---:|---|
| `01_ct07_strain_stress.png` | 28,750 | `49166322ec9caf79b4ddfacd8cad6b67f148f4d34d0eb5b5f06b059e16e8385c` |
| `02_ct07_normalised_rms.png` | 43,326 | `9024e9f814ab6d001eb646308821e4f2dd94812529448b1ee4ecbc0730524034` |
| `03_ct07_normalised_cumulative_rms.png` | 40,516 | `625e9a702f416c40f94d71aa026b93f1a2be58a89a0c1525bb4c8e1ac93fe865` |
| `04_ct07_normalised_ae_energy.png` | 38,531 | `56d79d37f41e69f82df939be97c3cd969aec5cf11b9fa983e6e9b939990a9592` |
| `05_ct07_normalised_cumulative_ae_energy.png` | 41,486 | `05825d48202a17319d909a69fd699b32aba76964c9b701b62b95e21bf4676dff` |

`file` 与 `sips` 均确认每个文件是 600 × 400 的有效 PNG。随后逐张打开视觉检查：标题、坐标轴、蓝色应力曲线、红色 AE 曲线/散点均正常显示，没有空白图、截断文件或渲染失败。

## 6. 结果文件夹内容

- 5 张最终 PNG。
- `03Test运行与问题解决记录.md`：本详细记录。
- `final_run.log`：最终成功运行输出。
- `Project.toml`、`Manifest.toml`：可复现 Julia 依赖环境。
- `test_generate_outputs.sh`：端到端出图验证。
- `test_ct07_title.sh`：CT07 标题验证。

最终没有遗留阻止出图的问题。
