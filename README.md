# 三元九维 · 生态中枢（sanjiu-ecosystem）

> 单一入口，统览整个「三元九维 19683 认知空间」生态。
> 设计原则：**形式统一 + 语义自适配** —— 数学底座唯一，领域语义各自适配。

```
              ┌─────────────────────────────┐
              │   sanjiu-core（形式层，唯一底座） │
              │  3⁹=19683 · 平衡三态 · 错综互变  │
              │  算子 · 索引 · 校验 · manifest   │
              └──────────────┬──────────────┘
                             │ 语义自适配（各仓 manifest）
   ┌──────────┬──────────┬───┴──────┬───────────┬──────────┐
   │ 诗词/卦典 │  占卜     │  中医      │  量化/交易 │  Agent记忆 │
   └──────────┴──────────┴──────────┴───────────┴──────────┘
```

## 认知服务 + 语义桥（MVP）

把 19683 从「符号库」升级为「认知引擎」：同一编号卦在各已适配领域
（D/R/T · 体用变 · 洛书九宫）各自从卦象义长出解读 —— 同一坐标、多语言说同一件事。

- 源码：[service/bridge.py](service/bridge.py)（认知坐标原语 + 五域语义桥 + 深度卦典）
- 泛化：[service/generalize.py](service/generalize.py)（台阶三雏形·邻域泛化推理）
- CLI：[service/cli.py](service/cli.py)（认知原语统一入口 encode/search/bridge/generalize/enhance）
- 增强接口：[service/enhance.py](service/enhance.py)（符号骨架 + LLM 注入点）
- LLM混合：[service/llm_mix.py](service/llm_mix.py)（接入即是我自己：主模型注入 + 人类解读）
- Agent工具：[service/agent_tool.py](service/agent_tool.py)（认知原语工具注册表 + decide 决策辅助）
- 认知引擎App：[app/cognitive-engine.html](app/cognitive-engine.html)（输入处境→定位卦→五域+卦典+决策建议，浏览器可直接运行，亦为 APK assets 基础）
- 认知引擎APK：[app/cognitive-engine.apk](app/cognitive-engine.apk)（v0.3.0：WebView + **全量卦典19683** + 自定义图标，签名，Release 附 [sanjiu-apk-builder v0.3.0](https://github.com/q1z2q3-debug/sanjiu-apk-builder/releases/tag/v0.3.0)）
- 全量卦典数据：[app/quanji_cog.js](app/quanji_cog.js)（19683 条，idx→[卦名,卦辞,启示]，WebApp 自动加载）
- 验证：[service/_audit_bridge.py](service/_audit_bridge.py)（一致性 12/12）
- 报告：[docs/MVP-语义桥-认知服务.md](docs/MVP-语义桥-认知服务.md)

## 生态地图（仓库导航）

> 📊 **可视化架构图**：[docs/ecosystem-map.html](docs/ecosystem-map.html)（浏览器打开，ECharts 分层关系图）

### 1. 形式层（唯一底座）
| 仓库 | 定位 |
|---|---|
| **[sanjiu-core](https://github.com/q1z2q3-debug/sanjiu-core)** | ★数学底座：19683 空间 + 三态 + 错/综/互/变算子 + 校验 + 语义 manifest |

### 2. 核心体系
| 仓库 | 定位 | 三元语义 |
|---|---|---|
| [sanjiu-nine](https://github.com/q1z2q3-debug/sanjiu-nine) | ★主仓：符号体系+诗词APK+深度卦典+人类卦辞 | D承载/R审定/T增益 |
| [tri9-cog](https://github.com/q1z2q3-debug/tri9-cog) | 三元九维认知空间 | T时/S空/C因果 |
| [cog-layer](https://github.com/q1z2q3-debug/cog-layer) | 九维三值认知层（Agent挂载） | 通用三值 |
| [btcu-harness](https://github.com/q1z2q3-debug/btcu-harness) | 平衡三元认知单元（LLM架构） | {-1,0,+1} |
| [hexq-fused](https://github.com/q1z2q3-debug/hexq-fused) | 灵助×HexQ×赫曦融合引擎 | 三进制·九爻·19683 |

### 3. 应用落地
| 领域 | 仓库 | 定位 |
|---|---|---|
| 诗词 | [sanjiu-apk-builder](https://github.com/q1z2q3-debug/sanjiu-apk-builder) | 诗词分类APK 一键脚手架 |
| 占卜 | [meihua-yishu-app](https://github.com/q1z2q3-debug/meihua-yishu-app) | 梅花易数×三元九维（体/用/变） |
| 占卜 | [xiuqiankun](https://github.com/q1z2q3-debug/xiuqiankun) | 袖里乾坤×小六壬×19683 |
| 中医 | [san-yuan-jiu-wei-ds](https://github.com/q1z2q3-debug/san-yuan-jiu-wei-ds) | 三元九维辨证推演 |
| 中医 | [NineDimTopology](https://github.com/q1z2q3-debug/NineDimTopology) | 九维药效向量方剂拓扑 |
| 疗愈 | [heal-belief](https://github.com/q1z2q3-debug/heal-belief) | 九维三元疗愈信念引擎 |
| Agent | [deepseek-pp-cognitive-system](https://github.com/q1z2q3-debug/deepseek-pp-cognitive-system) | 三元索引记忆库 |

### 4. 量化 / 交易
| 仓库 | 定位 |
|---|---|
| [archon-19683](https://github.com/q1z2q3-debug/archon-19683) | 19683 量化研究工作空间 |
| [cognitive-space-alpha-discovery](https://github.com/q1z2q3-debug/cognitive-space-alpha-discovery) | 19683 认知空间 Alpha 发现 |
| [hexq-prod](https://github.com/q1z2q3-debug/hexq-prod) | HexQ 卦枢交易生命体 |
| [sfw-cognitive](https://github.com/q1z2q3-debug/sfw-cognitive) | 九维概率云股票分析固件 |

## 版本矩阵

各组件版本与发布状态见 [docs/VERSIONS.md](docs/VERSIONS.md)。

## 语义适配（manifest）

每个应用仓在三态上的语义映射表见 **sanjiu-core/manifests/**（sanjiu-core 仓库内），
生态层提供 [manifests/index.md](manifests/index.md) 汇总索引。
