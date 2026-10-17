# 语义 manifest 索引

每个应用仓在「三元九维 19683 状态空间」上的**自适配语义**由一份 manifest 描述：
`state_alphabet`（三态→本仓语义词）+ `bit_weight_map`（本仓维序→core 规范）。

> manifest 实体文件统一存放在 **sanjiu-core/manifests/**（形式层仓库）。
> 本索引为生态层汇总清单。

## 已发布

| 仓 | manifest | 三元语义 |
|---|---|---|
| sanjiu-nine | [sanjiu_nine.json](../sanjiu-core/manifests/sanjiu_nine.json) | -1: D承载 · 0: R审定 · +1: T增益 |

## 待补（已列入生态地图，待逐仓写入）

| 仓 | 三元语义（据 README 初判） |
|---|---|
| tri9-cog | T时 / S空 / C因果 |
| cog-layer | 通用三值 0/1/2 |
| hexq-prod | 阴 / 和 / 阳 |
| meihua-yishu-app | 体 / 用 / 变（洛书九宫组织） |
| heal-belief | 体/用/变/时/空/势/因/果/缘 |
| xiuqiankun | -1/0/+1 通用三值 |
| btcu-harness | {-1,0,+1} 平衡三元 |

## 校验

任一 manifest 须通过 `sanjiu_core.validate.validate_manifest`：
- `space == 19683`
- `state_alphabet` 恰好覆盖三态键 -1/0/+1
- `bit_weight_map` 为 0..8 的排列
- 数据索引落于 0..19682 且唯一
