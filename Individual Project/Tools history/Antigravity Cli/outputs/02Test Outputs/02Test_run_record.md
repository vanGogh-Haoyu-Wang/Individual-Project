# 02Test Python 重新运行与调试记录

## 1. 本轮边界

本轮严格遵守以下约束：

- 原脚本只作为只读输入，不在其中实施任何修复；
- 所有修正版代码、测试、错误日志、正式运行日志、校验清单、Matplotlib 缓存和 5 张图片均位于 `outputs/02Test Outputs`；
- 输入 Excel 工作簿不修改；
- 最终使用 SHA-256、Git blob 和 scoped Git 状态确认原脚本未变化。

原脚本：

`/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/Tools history/Antigravity Cli/Test2 by Gemini 3.1pro high.py`

输入工作簿：

`/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/Tools history/Antigravity Cli/Commercial Tensile Tests.xlsx`

输出目录：

`/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/Tools history/Antigravity Cli/outputs/02Test Outputs`

## 2. 撤销后的状态检查

开始本轮时发现原脚本路径实际不存在，Git 状态为删除（`D`），说明上次修改被撤销时文件本身也被移除了。为了能够按用户指定路径重新测试，本轮先从 Git `HEAD` 逐字恢复原始文件，然后立即比较 Git blob：

```text
工作区原脚本 Git blob: 64ce66c18cb27158fceaae2cf96d0c8aab50e8a8
Git HEAD 基线 blob:     64ce66c18cb27158fceaae2cf96d0c8aab50e8a8
```

两者完全相同；恢复只是回到原始基线，不包含任何修复。后续所有修复均写入输出目录中的 `Test2_fixed.py`。

原脚本 SHA-256：

`76c5fc095e4829f00970f6958a0d6c4d335f33714f7bdb676126948bc3d66f88`

## 3. 运行环境

- Python 3.12.13
- pandas 2.2.3
- openpyxl 3.1.5
- matplotlib 3.11.0
- NumPy 2.4.6
- Pillow 12.2.0
- 绘图后端：`Agg`
- Matplotlib 缓存：`outputs/02Test Outputs/.matplotlib`

工作区 Python 本身不包含 Matplotlib。本轮复用了先前已存在的临时依赖目录 `/private/tmp/antigravity_cli_matplotlib`，没有在该目录生成新的交付文件；本轮产生的字体缓存则显式写入 `02Test Outputs/.matplotlib`。

## 4. 原脚本只读复现：问题与根因

### 问题 1：缺少 Matplotlib

不添加额外 Python 包路径运行原脚本，退出码为 1：

```text
ModuleNotFoundError: No module named 'matplotlib'
```

完整记录：`01_original_missing_dependency.log`。

处理方式：不修改原脚本，也不污染系统 Python；正式运行修正版副本时通过 `PYTHONPATH` 读取已有临时 Matplotlib 依赖。

### 问题 2：Excel 表头与数值混合导致绘图失败

补齐 Matplotlib 后，原脚本执行到第一张图时退出：

```text
TypeError: 'value' must be an instance of str or bytes, not a float
```

原脚本使用 `pd.read_excel(..., header=None)`，因此说明行、列名、单位和浮点数进入相同 Series。Matplotlib 先把字符串识别成分类数据，随后遇到浮点数而失败。

数据证据：

- 工作表 `CT07`：5,851 行 × 15 列；
- 机械列 `t1/strain/stress`：索引 3–1809，共 1,807 个配对数值；
- AE 列 `time/rms/cumrms/energy/cumenergy`：索引 1–5850，共 5,850 个配对数值；
- 最大应力：505.214799 MPa。

不能统一使用 `skiprows=3`，否则会删除 AE 列前两个有效数据点。修正版副本采用：

1. 对 8 个目标列分别调用 `pd.to_numeric(..., errors="coerce")`；
2. 将各列的文字和空白独立转换为 `NaN`；
3. 每张图根据自己的 X/Y 序列创建共同有效掩码；
4. 保留完整的 1,807 个机械点与 5,850 个 AE 点。

完整记录：`02_original_data_type_error.log`。

### 问题 3：原脚本只显示窗口，不保存文件

原脚本末尾只有 `plt.show()`，没有 `savefig()`。在 `Agg` 无界面后端中，即使前面的数据错误不存在，也不会产生 5 个 PNG 文件。

处理方式：只在输出目录中的 `Test2_fixed.py` 增加：

- `--input` 绝对工作簿路径；
- `--sheet CT07`；
- `--output-dir`；
- `--no-show`；
- 5 次 `savefig(..., dpi=160, bbox_inches="tight")`。

## 5. 测试驱动过程

先在输出目录创建 `verify_five_outputs.py`，要求：

- 原脚本 SHA-256 在运行前后必须保持不变；
- 修正版进程退出码为 0；
- 必须在本次测试开始后重新写入恰好 5 个预期名称的 PNG；
- 每张图片大于 20,000 字节；
- 分辨率至少 640×480；
- Pillow `Image.verify()` 通过；
- 灰度直方图色阶足够，排除空白图。

第一次运行测试时，`Test2_fixed.py` 尚不存在，测试按预期失败：

```text
can't open file '.../outputs/02Test Outputs/Test2_fixed.py': [Errno 2] No such file or directory
```

随后仅在输出目录创建 `Test2_fixed.py`。第二次运行测试：

```text
PASS: regenerated and validated exactly five PNG images; original unchanged
```

## 6. 正式运行结果

正式运行退出码：`0`。

```text
Mechanical paired points: 1807
AE paired points: 5850
```

完整输出：`03_final_run.log`。

| 文件 | 分辨率 | 大小 | SHA-256 |
|---|---:|---:|---|
| `01_strain_vs_stress.png` | 1582×943 | 84,439 B | `18657b6aafd2808708502ccb11dbb1458ec70e4068cda049aa24bbc1157d64b3` |
| `02_normalised_rms_profile.png` | 1581×943 | 118,869 B | `97c617d4d1943a892869f54b0a62dc85c820edd27d9c91ced48ed3f7ece4b160` |
| `03_normalised_cumulative_rms.png` | 1581×943 | 113,062 B | `942a09758d78487e396e8df3c99063c9ed172a50ab3808be9df553e8a0631dae` |
| `04_normalised_ae_energy.png` | 1581×943 | 108,563 B | `e822037d104abf00644b99813f768f83109474c089377b099804fff4dc86f48c` |
| `05_normalised_cumulative_ae_energy.png` | 1581×943 | 114,012 B | `a6837db940767cd91e9af0cb3cbca6ff415c7d1c2053dc1d8d3c22c8f08fca99` |

5 张图还经过逐张目视检查：曲线/散点存在，双 Y 轴颜色正确，标题与标签可读，无空白、裁切或破损。

第二张图标题仍为原代码中的 `T09 Commercial Normalised RMS Profile`。这与 `CT07`/其他 `T07` 标题存在语义不一致，但属于原始实验标识，本轮没有擅自修改。

## 7. 原脚本未修改的最终证据

正式运行后再次验证：

```text
原脚本 SHA-256（运行前）: 76c5fc095e4829f00970f6958a0d6c4d335f33714f7bdb676126948bc3d66f88
原脚本 SHA-256（运行后）: 76c5fc095e4829f00970f6958a0d6c4d335f33714f7bdb676126948bc3d66f88
工作区 Git blob:          64ce66c18cb27158fceaae2cf96d0c8aab50e8a8
HEAD 基线 Git blob:        64ce66c18cb27158fceaae2cf96d0c8aab50e8a8
```

原脚本 scoped Git 状态为空。即原脚本内容与 Git 基线逐字一致，没有被本轮修复改动。

哈希清单：`manifest.sha256`。
