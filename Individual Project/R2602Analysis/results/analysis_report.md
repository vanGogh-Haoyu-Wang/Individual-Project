# R260_2 补充分析报告

## 1. 数据与方法边界

- 源文件：`Copy of current R260_2.xlsx`
- 文件大小：103,740,621 bytes
- SHA-256：`2bf80527130a7eab326297a2dc1c17974dbae45cf3840217378169d227f8ea64`
- 工作表：`summar_R260_2`、`S1`–`S10`
- 方法：直接流式读取 XLSX ZIP/XML，不修改原文件，也不把 99 MB 工作簿整体载入内存。

工作簿内部反复使用 `R260_2` 和 `r260` 名称，但没有找到足以独立确认
steel grade、标准、化学成分、硬度和 specimen series 的元数据。因此本文仍使用：

> processed rail-steel AE dataset labelled `R260_2` in the source workbook

该工作簿包含处理后的 AE hit 特征和裂纹扩展计算，不含原始 ADC waveform 数组。
它可以支持 hit-level 与 crack-growth 数值案例，但不能验证 DTA/WFS 二进制解析、
FFT 重新计算或 waveform thresholding。

## 2. 跨 specimen 盘点

| Sheet | Used range | Cycles to failure | 识别到的共同完整 Mistras hit/waveform pairs | Cached formula errors |
|---|---:|---:|---:|---:|
| S1 | A1:BB493743 | 7,322 | 不适用：不同/部分 schema | 0 |
| S2 | A1:BW50231 | 64,476 | 25,110 | 0 |
| S3 | A1:BC8560 | 33,212 | 3,553 | 4 |
| S4 | A1:BC140611 | 49,325 | 70,301，另有 1 个末尾未配对 Msg-173 | 2 |
| S5 | A1:BB107154 | 55,022 | 53,573 | 2 |
| S6 | A1:AK421183 | 90,349 | 不适用：不同/部分 schema | 2 |
| S7 | A1:AV38982 | 72,694 | 不适用：不同/部分 schema | 7 |
| S8 | A1:AE130590 | 67,152 | 不适用：不同/部分 schema | 3 |
| S9 | A1:AD109428 | 77,991 | 不适用：不同/部分 schema | 2 |
| S10 | A1:AK72149 | 61,436 | 不适用：不同/部分 schema | 1 |

S2–S5 共识别到 152,537 个完整 Msg-173/Msg-1 配对。S1、S6–S10 的
“不适用”不表示没有 AE 数据，而是它们没有使用 S2–S5 的
`ID/CH/.../P-FRQ` 完整共同 schema；这些 sheet 必须先单独映射字段，不能用
同一 parser 强行合并。

十个 specimen 的顶部配置均记录 Max Load 6.5、Min Load 0.65、
R = 0.1 和 Frequency = 1。虽然这些值在工作簿中一致，单位与试验配置仍应由
原始实验说明或导师确认。

## 3. S3 hit-level 结果

S3 被选为首个补充案例，因为它规模较小且完整保留共同 Mistras 字段。

- 3,553 个 Msg-1 hits；
- 3,553 个 Msg-173 waveform markers；
- 3,553 个按时间和通道完全配对的记录；
- 0 个缺失、额外或重新排序；
- 所有 hit 都属于 channel 1；
- 记录时间从 9.78 s 到 11,940.38 s，跨度 11,930.60 s。

时间分布并不均匀：

- 前 50% 时间段共有 201 hits；
- 后 50% 时间段共有 3,352 hits，占 94.34%；
- 最后 10% 时间段有 1,490 hits，占 41.94%。

这说明 S3 的记录活动明显集中在试验后期，但 equal-duration time bins
不是 mechanical load stages；在完成时间—载荷—cycle 对齐前，不能把这一结果直接解释为
裂纹失稳或特定断裂阶段。

主要 hit 特征：

| Feature | Median | P95 | Max |
|---|---:|---:|---:|
| COUN | 9 | 53 | 2,200 |
| ENER | 5 | 32 | 24,829 |
| DURATION | 211 | 804 | 19,143 |
| AMP | 56 | 65 | 99 |
| RMS | 0.0026 | 0.0034 | 0.3416 |
| P-FRQ | 131 | 175 | 351 |

P-FRQ 最常见的记录值是 131（1,299 hits），之后是 107（575）、
175（447）、92（417）和 112（360）。工作簿没有给出足够的字段定义来独立
确认其单位，因此报告保留原始数值，不自动写成 kHz。

AMP 的 3,553 个值中，2,590 个位于 50–59，947 个位于 60–69，
14 个不低于 80。2012 rail-steel 论文中的约 40 dB machine-noise 观察依赖其
特定实验配置，不能直接作为本工作簿的分类阈值。

## 4. S3 crack-growth 与 AE interval 指标

排除初始零间隔行和存在公式缺陷的 failure 行后，剩余 9 个可用 interval：

- `log10(da/dN)` 与 `log10(ΔK)` 的 Pearson `r = 0.930`；
- 对应线性斜率为 `6.070`，截距为 `-14.817`；
- `da/dN` 与 AE count/cycle 的 Pearson `r = 0.721`；
- `da/dN` 与 AE energy/cycle 的 Pearson `r = 0.573`；
- `da/dN` 与 AE duration/cycle 的 Pearson `r = 0.726`。

这些只是 n = 9 的探索性相关结果。它们说明该工作簿可以构成
“processed AE metrics 与 crack-growth calculation 的数值适用性案例”，
但不能证明 AE 指标能够独立预测裂纹扩展，更不能构成检测准确率验证。

## 5. 已确认的数据质量问题

### S3 failure row

S3 row 26 的 AE count 公式为：

```text
SUMIFS(Z:Z,Y:Y,"<=33060")
```

该公式缺少上一 interval 的 lower bound，却把结果除以最后 80 cycles。
因此它重新累计此前几乎全部数据，产生异常高的末段 rate。该行必须从
interval correlation 或 regression 中排除，除非回到原实验定义后修正为明确的
lower/upper bounds。

此外：

- 顶部 `Cycles to failure` 为 33,212；
- failure row 的 cycles 为 33,140；
- 两者相差 72 cycles。

这个差异需要根据原始试验日志确认，不能自行选择其中一个作为 ground truth。

### Cached formula errors

S3 有 4 个缓存错误，全部位于初始零间隔 row 16：

- `LOG(0)` 导致 1 个 `#NUM!`；
- 三个除以零公式导致 3 个 `#DIV/0!`。

这些 boundary errors 可以通过分析时排除初始行处理，但不应直接覆盖原始工作簿。

S4 还存在 1 个文件末尾未配对的 Msg-173 marker。进行 S4 深入分析前应先确认它是
正常终止记录、缺失 hit，还是导入过程留下的尾部数据。

## 6. 可用于论文的保守结论

> The processed workbook labelled R260_2 contains specimen-level crack-growth
> calculations and Mistras/AEWin-style hit features. In the S3 case, 3,553
> hit records were paired consistently with waveform markers, and exploratory
> interval analysis showed positive associations between cached crack-growth
> rate and several AE activity metrics. These results demonstrate numerical
> workflow applicability to a rail-steel-labelled dataset, while dataset
> provenance, field units, formula defects and the absence of raw waveforms
> prevent claims of independent crack-detection validation.

## 7. 下一步边界

1. 向导师确认 R260 grade、specimen series、P-FRQ 等字段单位，以及
   `Cycles to failure` 的权威来源。
2. 修正或明确排除 S3 failure interval，再决定是否把相关系数写入正文。
3. 单独建立 S1、S6–S10 的 schema mapping；不要把缺失共同 header 误报为零 hits。
4. 如时间有限，论文正文只使用 S3，S2/S4/S5 作为规模与一致性补充。
