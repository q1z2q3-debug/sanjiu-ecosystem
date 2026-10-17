# 三元九维生态 · 版本矩阵

> 统一语义化版本（SemVer）。形式层 core 为唯一数理源；各应用仓在 core 上自适配语义。
> 大文件（全量 19683 数据）走各仓 GitHub Release asset，不入库。

## 形式层

| 组件 | 版本 | 仓库 | 说明 |
|---|---|---|---|
| sanjiu-core | 0.1.0 | [sanjiu-core](https://github.com/q1z2q3-debug/sanjiu-core) | 19683 空间 + 算子 + 校验 + manifest（pip） |

## 核心体系

| 组件 | 版本 | 仓库 | 三元语义 |
|---|---|---|---|
| sanjiu-nine | 1.0.0 | [sanjiu-nine](https://github.com/q1z2q3-debug/sanjiu-nine) | D/R/T |
| tri9-cog | — | [tri9-cog](https://github.com/q1z2q3-debug/tri9-cog) | T/S/C |
| cog-layer | — | [cog-layer](https://github.com/q1z2q3-debug/cog-layer) | 通用三值 |
| btcu-harness | — | [btcu-harness](https://github.com/q1z2q3-debug/btcu-harness) | {-1,0,+1} |
| hexq-fused | — | [hexq-fused](https://github.com/q1z2q3-debug/hexq-fused) | 三进制九爻 |

## 应用落地

| 组件 | 版本 | 仓库 | 领域 |
|---|---|---|---|
| sanjiu-apk-builder | 0.1.1 (PyPI) | [sanjiu-apk-builder](https://github.com/q1z2q3-debug/sanjiu-apk-builder) | 诗词 APK 脚手架 |
| meihua-yishu-app | v1.3.0 | [meihua-yishu-app](https://github.com/q1z2q3-debug/meihua-yishu-app) | 梅花易数·占卜 |
| xiuqiankun | — | [xiuqiankun](https://github.com/q1z2q3-debug/xiuqiankun) | 小六壬·占卜 |
| san-yuan-jiu-wei-ds | — | [san-yuan-jiu-wei-ds](https://github.com/q1z2q3-debug/san-yuan-jiu-wei-ds) | 中医辨证 |
| NineDimTopology | — | [NineDimTopology](https://github.com/q1z2q3-debug/NineDimTopology) | 中医方剂 |
| heal-belief | — | [heal-belief](https://github.com/q1z2q3-debug/heal-belief) | 疗愈信念 |
| deepseek-pp-cognitive-system | — | [deepseek-pp-cognitive-system](https://github.com/q1z2q3-debug/deepseek-pp-cognitive-system) | Agent 记忆 |

## 量化 / 交易

| 组件 | 版本 | 仓库 |
|---|---|---|
| archon-19683 | — | [archon-19683](https://github.com/q1z2q3-debug/archon-19683) |
| cognitive-space-alpha-discovery | — | [cognitive-space-alpha-discovery](https://github.com/q1z2q3-debug/cognitive-space-alpha-discovery) |
| hexq-prod | — | [hexq-prod](https://github.com/q1z2q3-debug/hexq-prod) |
| sfw-cognitive | — | [sfw-cognitive](https://github.com/q1z2q3-debug/sfw-cognitive) |

## 版本约定

- 公理/算子变更 → 升**主版本**并显式记录。
- 全量 19683 数据（>5MB）走 Release asset，仓库内保留轻量/内嵌版。
- 各应用仓接入 core 后，须过 core 校验（`validate_manifest` + `validate_indices`）。
