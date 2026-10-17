# 语义 manifest 索引

每个应用仓在「三元九维 19683 状态空间」上的**自适配语义**由一份 manifest 描述：
`state_alphabet`（三态→本仓语义词）+ `bit_weight_map`（本仓维序→core 规范）。

> manifest 实体文件统一存放在 **sanjiu-core/manifests/**（形式层仓库）。
> 本索引为生态层汇总清单。

## 已发布（7 份）

| 仓 | manifest | 三元语义 | 状态 |
|---|---|---|---|
| sanjiu-nine | [sanjiu_nine.json](../sanjiu-core/manifests/sanjiu_nine.json) | -1:D承载 · 0:R审定 · +1:T增益 | 位权已核（恒等） |
| tri9-cog | [tri9_cog.json](../sanjiu-core/manifests/tri9_cog.json) | T时 / S空 / C因果 | 位权待核 |
| cog-layer | [cog_layer.json](../sanjiu-core/manifests/cog_layer.json) | 通用三值 | 位权待核 |
| hexq-prod | [hexq_prod.json](../sanjiu-core/manifests/hexq_prod.json) | 阴 / 和 / 阳 | 位权待核（含π坐标） |
| meihua-yishu-app | [meihua_yishu_app.json](../sanjiu-core/manifests/meihua_yishu_app.json) | 体/用/变 + 洛书九宫 | **结构需特判**（洛书位权→core待对齐） |
| heal-belief | [heal_belief.json](../sanjiu-core/manifests/heal_belief.json) | 体/用/变/时/空/势/因/果/缘 | 位权待核 |
| xiuqiankun | [xiuqiankun.json](../sanjiu-core/manifests/xiuqiankun.json) | -1/0/+1 通用三值 | 位权待核 |

## 校验

任一 manifest 须通过 `sanjiu_core.validate.validate_manifest`：
- `space == 19683`
- `state_alphabet` 恰好覆盖三态键 -1/0/+1
- `bit_weight_map` 为 0..8 的排列
- 数据索引落于 0..19682 且唯一

> 注：标注"位权待核"的仓，接入 core 时必须先独立核实维序/索引约定，
> 再据实更新 `bit_weight_map`，不得直接套用恒等映射。
> meihua 的洛书九宫组织与 core 九维不同构，需额外做结构映射。
