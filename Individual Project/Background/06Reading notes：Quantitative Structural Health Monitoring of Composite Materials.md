![[IIW_215_Gee.pdf]]
# 复合材料的定量结构健康监测

## 摘要:

纤维增强复合材料在制造高价值结构工程部件中得到了广泛应用。这类材料存在复杂的损伤机制，而使用传统的非破坏性检测方法来检测它们则存在困难，因此迫切需要有效的结构健康监测系统。结构健康监测系统能够实时评估在服役状态下的纤维增强复合材料部件，从而减少停机时间，并降低意外灾难性故障的风险。在本研究中，我们介绍了一种定制的声发射系统的开发情况。该系统能够捕捉完整的波形，并通过多种算法对其进行分析。通过这种新颖的方法，我们在进行拉伸和弯曲测试时，成功地对纤维增强复合材料样品在损伤发生和演变过程中的特征进行了识别、表征和量化分析。移动 RMS 算法就是被用于这项研究中的一种算法。在测试的各个 FRC 试样在加载直至断裂过程中的损伤识别与量化。通过获得的实验结果，我们能够识别并量化损伤的发生过程，包括试样中出现的分层现象等关键事件。

## 1. 引言

纤维增强复合材料（FRC）结合了轻质、高强度和高抗腐蚀性等优点。这些材料是制造关键航空部件、风力及潮汐涡轮机叶片、高性能及军用陆地车辆的结构部件，以及高端运动器材如自行车和滑雪板的首选材料。FRC 制造技术的进步使得风力涡轮机的叶片尺寸可以增大数倍，叶片长度甚至可达 131 米。这一进展使得最大的海上风力涡轮机能够达到 14 兆瓦以上的功率输出。然而，风力涡轮机叶片的故障不仅会导致电力生产中断，还会对风力涡轮机造成无法修复的损坏。因此，对风力涡轮机叶片及其他关键结构部件的完整性进行精确的远程监测是非常必要的。FRCs 在评估过程中扮演着重要角色。声发射技术已被广泛用于定性评估 FRCs 在运行中的结构完整性。已有多项研究致力于分析声发射信号，以识别这些材料中出现的损伤模式，包括基质开裂、纤维断裂、纤维脱落、脱粘以及层离等现象（4-6）。然而，大多数此类研究仅实现了对声发射信号的定性或半定量评估，无法提供精确的定量结果。在本文中，我们提出了一种基于实验室条件下对样品进行的力学测试与声发射监测相结合的新型 FRCs 损伤定量评估方法。

## 2. 方法论

本文中用于分析的数据集是通过对机械性能测试过程的监测而获得的。该成果是在伯明翰大学进行的 H2020 Carbo4Power 项目范围内完成的。该项目的核心目标是改进与风力涡轮机生产及运行相关的材料和技术，其中特别关注 WTB 领域。因此，并没有哪种单一材料或测试方法被特别重视；考虑到 WTB 的结构特性，碳纤维增强聚合物（CFRP）和玻璃纤维增强聚合物（GFRP）都被纳入了研究范围并进行了测试。除非另有说明，否则所提出的结论适用于这两种材料。

### 2.1 声发射监测

在材料的声学监测方面，我们使用了两个独立的信号采集系统。其中一个是来自 Physical Acoustics Corporation 公司的商用系统，另一个则是 UoB 内部自行开发的定制系统。这个定制系统依靠 UoB 自主研发的数据采集软件来运行。为了连接硬件和软件，我们采用了 National Instruments 的 NI-9223 数据采集卡，该卡能够同时捕获 4 个通道的数据，采样速率达到 1 MS/s，测量范围可达+/- 10V。

### 2.2 已测试的材料

所有样品试样都是按照 ASTM 标准制造的。在拉伸测试中，试样的尺寸为 250 毫米×25 毫米，厚度在 1 到 2 毫米之间；具体厚度取决于所使用的加固材料类型。在弯曲测试中，试样的尺寸为 150 毫米×25 毫米，厚度约为 1.01 毫米到 1.3 毫米。在三点弯曲测试中，两个固定点之间的距离为 40 毫米。

需要注意的是，这些测试的开展并非为了获得物质认证，而是为了让他们用于自动检测的工具。基于这种思路，对于机械性能方面的考虑就相对较少了，因为重点仅仅在于识别是否存在损坏现象。

### 2.3 机械性能测试

采用了两种机械测试方式，即拉伸测试和弯曲测试（三点弯曲）。拉伸测试使用的是 Zwick Roell 公司生产的 1484 型电液式测试机，该设备具有 200 kN 的载荷能力，伸缩仪的长度为 10 毫米，测试时的横梁移动速度为 2 毫米/分钟。三点弯曲测试则使用 Dartec 测试机进行，由于 1 kN 载荷传感器无法获得，因此使用了 50 kN 的载荷传感器，横梁移动速度仍为 1 毫米/分钟。

## 3. 结果

需要注意的是，通过实际应用来过滤所有机械噪声并不现实。因为根据测试的特性，测试过程中噪声的幅度会有很大的波动，那些幅度较大的噪声会与那些与设备损坏相关的信号重叠在一起。因此，我们只能尽力减少噪声对自动声学信号及其可识别信息的影响。所采用的传感器类型旨在帮助减少机械噪声对自动声学信号采集产生的干扰。

在这种情况下，可以通过评估信号的早期部分来确定上下阈值。例如，5 秒的初始样本数据就可以用来判断。在这个范围内，数据的加载不会足够显著以至于导致损坏的发生，因此，可以认为与拉伸试验机运行相关的机械噪声是观察到的声发射峰值的主要来源。实际上，对这一范围的判断有助于评估机械正常运行时所产生的活动情况。这一点不应与标准化的采集阈值混淆，后者是商业系统中使用的标准，类似于这里所使用的并行处理方式。对于那些系统来说，当超过某个预定值时，就会触发信号的采集。在这里，采集过程是恒定的，这个阈值仅仅是一个额外的预处理步骤，用于减少噪声对信号的影响。实际使用的阈值会更低，并且是动态确定的。

### 3.1 均方根的应用

均⽅根值 (RMS) 表⽰信号在⼀系列点上的平均幅度。它可以通过以下⽅式计算：

![](https://ima-notebook-prod.image.myqcloud.com/2/b3BNCe4oURTNnffp5fRfj9A/file_manager/019ef4f0d24e7b519e90584b33c6fa23.webp?q-sign-algorithm=sha1&q-ak=AKID9IDtLZZKqGRO7hVFnMn0zjXTXovoTtAN&q-sign-time=1782227433%3B1782256233&q-key-time=1782227433%3B1782256233&q-header-list=&q-url-param-list=&q-signature=0cadd801f6d8228b34a5fcdde88027677319f027)

其中 N = 数据点数 (7)。为了将 RMS 应⽤于捕获的信号，应采⽤移动扫描⽅法。这一过程涉及对数据应用一个可移动的均匀窗口机制。窗口的长度与参数 N 的值相对应，而在连续窗口之间会引入重叠现象。通过使用 MATLAB 中的现有算法，如 dsp.MovingRMS（8），可以更高效地完成上述操作。与在 MATLAB 中自行实现相关函数相比，使用这些现成的算法能够更高效地实现该过程，因此建议优先使用这些算法。

### 3.2 窗口长度影响的调查

给定的信号分配合适的窗口长度，对于确保信息的质量至关重要。在调整窗口长度精度与系统性能之间找到平衡是非常关键的。可以根据所需的信息级别，采用多种不同的窗口长度组合。

![](https://ima-notebook-prod.image.myqcloud.com/2/b3BNCe4oURTNnffp5fRfj9A/file_manager/019ef4f3515b74dda4332818276c1fd4.webp?q-sign-algorithm=sha1&q-ak=AKID9IDtLZZKqGRO7hVFnMn0zjXTXovoTtAN&q-sign-time=1782227433%3B1782256233&q-key-time=1782227433%3B1782256233&q-header-list=&q-url-param-list=&q-signature=d39cf3e02d3f6e013f1db1dbed3c87481710963c)

**图 1. 所生成表示的窗口长度比较**

图 1 展示了在相同的 AE 信号和拉伸测试数据的情况下，改变窗口长度所产生的影响。本示例所使用的测试数据来自 T02 试样的拉伸测试，因为该数据最能清晰地显示出所关注的可观测因素。图中四个曲线中的突出峰点分别对应了第一次明显的层剥离事件。当使用较小的窗口长度时，在识别出的层剥离事件附近会出现其他峰值；尤其是在窗口长度为 200 时这一点表现得尤为明显。

**表1.窗⼝⻓度N对数值RMS表⽰的影响**

| N 数量     | 数据点           | 减少因素        | 确定分层时间   |
| -------- | ------------- | ----------- | -------- |
| 5x10^5   | 473           | 2.4545x10^5 | 157.4237 |
| 2.5x10^5 | 989           | 2.6087x10^5 | 157.2024 |
| 10^4     | 2.5757x10^4   | 1.0017x10^4 | 157.0478 |
| 2x10^2   | 1.296407x10^6 | 199.0116    | 157.0475 |

在确定正确的窗口长度时，需要考虑上述观察到的各种因素。这一点非常重要。

在扫描窗口技术的应用中，重叠度被设定为+1。由于使用了统一的窗口大小，因此无需像其他窗口类型那样引入较大的重叠区域来保留信号信息。使用最小重叠度的另一个好处是能够真正保留信号的原始特征，这对于正确评估和处理损伤事件及其相关的时间向量至关重要。

## 3.3 损害模式的分配

根据这种方法所提供的信息，对损失进行准确且恰当的分配，可以说是衡量其适用于扩展和持续使用效果的最重要因素。

### 3.3.1 基于强度的方法

一种基于 AE 信息的损伤模式分配方法，就是评估由损伤发生所产生的 AE 响应所对应的峰值幅度。这种方法的原理是，可以将特定的损伤模式直接归因于某些特定的幅度值范围，而该峰值的位置就落在这些范围内。不过，由于不同系统之间存在放大效应及其他参数差异，因此直接使用精确文献中的数值可能并不合适。这是一种相当简单的损伤分配方法，仅关注峰值或主导损伤模式。如果将 RMS 视为信号的均值，那么可以采用类似的原理来评估这种方法。不过，由于峰值幅度被封装在窗口化信号中，因此无法直接对其进行评估。了解具体的损伤机制后，就可以更精确地确定损伤模式的相对位置了。

另一种被广泛采用的方法是对 AE 能量进行评估，实际上就是指波形本身所包含的能量。对于这种能量的计算，有两种方法可供选择：一种是计算整流信号包络下的能量（MARSE），另一种则是计算真实能量，即信号平方包络下的面积。不过，这两种方法都存在一些固有的问题。对于 MARSE 方法，只有处于正范围的信号被考虑在内；而真实能量的计算方法则考虑了所有信号点，因为信号被平方了。不过，当将所有数据都用同一种表示方式来表示时，就会引入误差，比如在负载周期初期，由于 AE 事件较少，数值会显得较为稳定；而在负载周期后期，由于 AE 事件的频率较高，信号会变得非常饱和，从而导致数值出现偏差（10,11）。

这些工具用于评估损伤的方式各不相同。不过，这些工具在具体应用时的逻辑原理却是大致相同的逻辑。这两种情况都可以与所观察到的相关破坏机制的能量相关联，它们相对于其他模式的定位大致反映了各自机制所需的能量。对于这两种方法，关于某些破坏模式的具体定位存在一些争议。不过，关于矩阵开裂、层离以及纤维断裂的定位，似乎已经达成了共识；而纤维-基质脱离和纤维拔出则处于不同的位置。对于基于振幅的方法来说，由于有一个固定的范围，因此可以提供精确的数值来进行比较。然而，文献中提供的数值差异很大。这表明这种差异取决于一系列变量，主要是材料类型，以及考虑响应时使用的不同单位（12-15）。不过，这些数值仍然符合上述已确定的趋势。在复合材料中识别损伤事件发生的关键手段，是通过监测系统所承受累积能量变化率来实现的。需要注意的是，如果已知单个峰值的能量最大值，那么可以在系统内部比较各个振动能量的数值。这样就能将类似于基于振幅的方法所观察到的趋势，应用到该系统中的不同能量范围内。这些趋势遵循预期的排列顺序：基质开裂对应的能量最低，其次是层离现象，最后是纤维断裂。关于如何将脱粘和拔出现象与之前讨论的内容联系起来，这里也观察到了类似的现象（16）。

对于各种不同方法的评估，以及这些方法与 RMS 之间确立的关联，其实可以采取一种混合式的评估方式。这种方式能够充分利用所讨论的各种替代方案，同时运用上述已确定的趋势进行分析。从某种意义上说，这种评估方式具有固定的数值范围；不过，可观测的 RMS 值与导致损害模式之间的对应关系则较难确定，因为存在许多因素会影响这一关系。这些因素在某些方面也可以被视为其他方法的变量，因此在运用 AE 进行评估时需要考虑这些因素。采用扫描式方法时，移动 RMS 所呈现的结果与其他讨论过的技术类似，因为在简单层面上，它只能准确地指出窗口内占主导地位的损害模式。所讨论的这项技术与其他技术的主要区别在于，它始终能够保持原始信号的真实再现。

由于该技术的应用是基于对定制系统所获取的信号进行处理，因此它非常适合处理原始数据的情况。不过，商业系统的 RMS 值确实反映了所强调的趋势，因此类似的逻辑也可以应用于这些系统中。需要注意的是，在接下来的章节中，所提出的观点和假设都是基于定制系统所提供的条件而言的。

### 3.3.2 提取相应的波形

尽管这种技术与其他确定主导损伤模式的方法之间存在一些相似之处，但采用这种技术确实有一个真正的优势。那就是它能够将相关的损伤事件分离出来进行提取，因为相应的声发射响应会在处理过程中被划分到相应的窗口中。这种方法使得这种技术能够作为一种实时持续监控的方法，并可以直接访问相关的声发射数据。这与传统的方法不同，在传统方法中，需要将这些数据导出，而这些数据的质量则存在争议。

当然，这种方法并非没有问题，还需要进一步考虑一些因素。这些问题可能会影响信号处理过程中计算出的数值，以及相应的波形形态。主要的问题在于，单个信号可能会被分割，导致多个窗口之间的数据交叉；此外，在捕获的窗口内也可能出现数据遗漏的情况。对单个波形的分割并非这种技术的特有现象，在其他系统中也观察到这种情况——实际上，就是将波形跨越两个独立窗口的边界进行分割。随着窗口长度缩短，这种风险会增加，不过这个问题相对容易解决，只需提取两个相关窗口的数据即可。最值得关注的是，这会对计算出的均方根值产生的影响。不过，通过仔细评估所得到的表示结果，可以确认这种问题的存在。在一段固定的窗口长度内，如果存在多个连续的峰值，那么噪声混入的风险就会对计算出的 RMS 值产生影响。这些噪声的主要来源可能是电子或机械方面的因素。虽然已经采取了一些预防措施来应对这一问题，比如通过应用动态阈值来过滤噪声，但随着机械测试强度的增加，噪声的产生量也有可能会增加。总体而言，对于那些包含 AE 事件的窗口来说，这种噪声的影响对计算出的 RMS 值影响很小。不过，对于那些只产生这种 RMS 峰值的窗口，可以通过适当的过滤处理来消除这些问题，因为这些窗口产生的峰值强度会非常微弱。

另一个需要考虑的因素是那些前兆信号或后续信号的存在情况。这些信号可能包含在波形中，也可能以某种形式与波形相关联。如前所述，这些信号可能会导致它们被从孤立信号中排除出去。不过，理论上这种情况只适用于使用较短的窗口长度时。至于这一点对损伤模式评估的影响，不仅取决于信号分离的程度，还取决于这些信号之间的关系——它们是本质相关的，还是仅仅位于主信号附近而已。这些信号也可能归属于构成 AE 信号的不同类型的波形。

此外，这些现象还伴随着各种不同的相关参数。这些波在行为特性和特征上都是确定性的，比如波速就可以直接归因于观测到的到达时间。这种现象是由于各个波在相关材料中传播的方式所导致的，不过，波的类型并不是由损伤类型来决定的。

采用这种方法的明显优势在于，可以轻松地将进一步的信号处理技术应用于特定的窗口区域，而无需经过复杂的评估过程。这种方法有助于确认，通过 RMS 表示法确定的损伤模式在更严格的调查下是否仍然有效。采用这种方法的另一个好处是，能够减少作为输入数据的数据量，从而避免使用那些计算复杂度较高的算法。其中一种进一步的信号处理技术就是傅里叶变换，它可用于评估相关频率成分。

### 3.3.3 使用傅里叶变换确认损伤模式

虽然对振幅的评估是一种成熟且被广泛使用的技术，但它仍存在一些固有的局限性和缺陷。实际上，这种评估基于这样一个假设：各种损伤模式是独立发生的，但实际上有些损伤模式是相互关联的。此外，这类事件也可能同时发生，或者在不同时间、不同地点出现。为了充分理解这些复杂且相互关联的事件，就需要采用更为全面的信号处理技术。通过对相应均方根窗口中提取的信号包络进行傅里叶变换，就可以对之前评估得出的结论进行最终确认。这种技术能够评估输入信号的频率成分。每种不同的损伤模式都对应着特定的频率范围，因此可以全面识别给定信号中出现的各种损伤模式。

根据奈奎斯特定理（17），按照既定的方法，能够精确采样的最大频率是 500 kHz，这相当于 1 MS/s（MHz）采样率的一半。这样做是为了与复合材料中可能出现的损坏频率相吻合。如果采样率低于这个数值，就会导致高频成分被忽略；而采样率高于此数值则可能会带来一些好处。不过，总体而言，这样的采样方式会产生大量不必要的数据，而这些数据对于准确分析来说并不是必需的。

与之前讨论的振幅方法类似，如何为各种损伤模式分配相应的频率范围也是个有争议的问题。不过，在分配频率范围给不同损伤模式时，同样采用了类似的逻辑：相关波的频率可以直接反映源头的能量大小，频率越高，对应的能量就越大。

![](https://ima-notebook-prod.image.myqcloud.com/2/b3BNCe4oURTNnffp5fRfj9A/file_manager/019ef4f9df6d7e9fb9f1cfd1060ec7af.webp?q-sign-algorithm=sha1&q-ak=AKID9IDtLZZKqGRO7hVFnMn0zjXTXovoTtAN&q-sign-time=1782227433%3B1782256233&q-key-time=1782227433%3B1782256233&q-header-list=&q-url-param-list=&q-signature=8d4db83f08369af2c8b3e4676668ae9b5fe2d816)

图 2. 提取的波长以及对应的傅里叶变换结果，用于识别主要的层剥离事件

具体来说，在本案中，由于窗口的时间长度有限，因此选择了离散形式的傅里叶变换。这些离散数据的处理是通过 MATLAB 内置算法完成的，同时采用了适用于噪声信号的特定处理程序（18,19）。对于损伤的频域分析来说，其结果往往具有不确定性，这与其他信号处理方法的情况类似。确定与损伤模式相关的具体数值或范围是一个具有挑战性的问题。在上述图中，两个明显的峰值分别对应于矩阵的裂纹和剥离现象，其中剥离现象的强度更高。这一结果与应力曲线中的现象相符，进一步证实了从均方根分析法得出的结论是正确的。

## 4. 结论

这种基于 RMS 方法的 AE 数据评估方法，可以为 FRP 损伤评估提供另一种选择。研究表明，该方法能够以与现有技术相同的详细程度和准确性来获取相同的信息。同时，该方法还能保持数据的真实表示，并允许提取相关的原始波形，从而可以在相关窗口内对数据实施进一步的信号处理。这可以说是这种技术结合定制化的 AE 采集系统所带来的真正优势。这里介绍的方法可以被视为开发真正定量评估方法的初步阶段，它能够更深入地评估系统的整体损伤情况，同时仍然能够方便地对主要损伤模式进行简单评估。此外，值得注意的是，商业系统提供的均方根信息也与这里的结论一致。这意味着可以使用该简化版本的技术，结合其他可用的数值来确认损伤模式的分配。

# 参考文献

1. Qureshi J. A Review of Fibre Reinforced Polymer Structures. Vol. 10, Fibers. MDPI; 2022
2. Nehls G. China’s Sany Renewable rolls out 131-meter wind blade. Composites World [Internet]. 2024 Feb 1 [cited 2024 May 30]; Available from: https://www.compositesworld.com/news/chinas-sany-renewable-rolls-out-131-meter-wind-blade-
3. Musial W, Spitsen P, Duffy P, Beiter P, Shields M, Mulas Hernando D, et al. Offshore Wind Market Report: 2023 Edition [Internet]. 2023 [cited 2024 May 30]. Available from: https://www.energy.gov/eere/wind/articles/offshore-wind-market-report-2023-edition
4. Standard Practice for Determining Damage-Based Design Stress for Glass Fiber Reinforced Plastic (GFRP) Materials Using Acoustic Emission. ASTM International; Designation: E2478 − 11 (Reapproved 2022).
5. Saeedifar M, Zarouchas D. Damage characterization of laminated composites using acoustic emission: A review. Vol. 195, Composites Part B: Engineering. Elsevier Ltd;
6. Scholey JJ, Wilcox PD, Wisnom MR, Friswell MI. Quantitative experimental measurements of matrix cracking and delamination using acoustic emission. Compos Part A Appl Sci Manuf. 2010 May;41(5):612–23.
7. Mahajan H, Banerjee S. Quantitative Investigation of Acoustic Emission Waveform Parameters from Crack Opening in a Rail Section Using Clustering Algorithms and Advanced Signal Processing. Sensors. 2022 Nov 1;22(22).
8. https://uk.mathworks.com/help/dsp/ref/dsp.movingrms-system-object.html [Internet]. 2023. Moving root mean square.
9. Carrasco Á, Méndez F, Leaman F, Molina Vicuña C. Short Review of the Use of Acoustic Emissions for Detection and Monitoring of Cracks. Vol. 49, Acoustics Australia. Springer; 2021. p. 273–80.
10. Unnþórsson R. Hit Detection and Determination in AE Bursts. In: Acoustic Emission - Research and Applications. InTech; 2013.
11. Vidya Sagar R. An Experimental Study on Acoustic Emission Energy and Fracture Energy of Concrete [Internet]. 2009. Available from: [https://www.ndt.net/?id=9850](https://www.ndt.net/?id=9850)
12. Zheng G, Buckley MA, Kister G, Fernando GF. Blind deconvolution of acoustic emission signals for damage identification in composites [Internet]. Available from: [http://spiedl.org/terms](http://spiedl.org/terms)
13. Daneshmehr A, Asa A, Abazary S. A Study on the Failure Mechanisms of CompositLaminates using Acoustic Emission Monitoring [Internet]. Vol. 2. 2012. Available from: [http://inpressco.com/category/ijcet](http://inpressco.com/category/ijcet)
14. Liu PF, Chu JK, Liu YL, Zheng JY. A study on the failure mechanisms of carbon fiber/epoxy composite laminates using acoustic emission. Mater Des. 2012 May;37:228–35.
15. Rubio-González C, de Urquijo-Ventura M del P, Rodríguez-González JA. Damage progression monitoring using self-sensing capability and acoustic emission on glass fiber / epoxy composites and damage classification through principal component analysis. Compos B Eng. 2023 Apr 1;254.
16. Azadi M, Alizadeh M, Jafari SM, Farrokhabadi A. Cumulative acoustic emission energy for damage detection in composites reinforced by carbon fibers within low-cycle fatigue regime at various displacement amplitudes and rates. Polymers and Polymer Composites. 2021 Nov 1;29(9_suppl):S36–48.
17. Cunningham M, Bibby G. Electrical Measurement. In: Electrical Engineer’s Reference Book. Elsevier; 2003. p. 11.8.8.1.
18. [https://www.fftw.org/](https://www.fftw.org/) [Internet]. FFTW.
19. M. Frigo, S. G. Johnson. FFTW: An Adaptive Software Architecture for the FFT. In: Proceedings of the International Conference on Acoustics, Speech, and Signal Processing. 1998. p. 1381–4.

---
