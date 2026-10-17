# 语义 manifest 索引

每个应用仓在「三元九维 19683 状态空间」上的**自适配语义**由一份 manifest 描述：
`state_alphabet`（三态→本仓语义词）+ `bit_weight_map`（本仓维序→core 规范）+ `idx_convention`。

> manifest 实体文件统一存放在 **sanjiu-core/manifests/**（形式层仓库）。
> 本索引为生态层汇总清单。**全部位权已逐仓源码核实**（2026-10）。

## 位权核实结论（两类）

1. **正向（恒等，与 core 同构）**：`bit_weight_map=[0..8]`，`idx_convention=g1_high`
2. **反向**：`bit_weight_map=[8..0]`（本仓维度 0 = 最低位），`idx_convention=other`

## 已发布（7 份）

| 仓 | 三元语义（state_alphabet） | 位权 | 索引约定 | 备注 |
|---|---|---|---|---|
| sanjiu-nine | D承载 / R审定 / T增益 | 正向 [0..8] | g1_high | 主仓·事实源头 |
| tri9-cog | T时/S空/C因果（digit 0/1/2） | 正向 [0..8] | g1_high | T1 最高位 |
| cog-layer | 不足·收缩 / 中和·待定 / 充盈·展开 | **反向 [8..0]** | other | 位0=体最低位 |
| heal-belief | 隐·收 / 衡·中 / 显·发 | **反向 [8..0]** | other | 位0=体最低位 |
| hexq-prod | 阴 / 和 / 阳 | **反向 [8..0]** | other | **idx 1-based(+1)**；含π坐标 |
| meihua-yishu-app | 气敛·止 / 气枢·转 / 气旺·行 | 正向 [0..8] | g1_high | 洛书九宫坎一最高位；三元体用变=9宫3组投影 |
| xiuqiankun | 通用三值 | 正向 [0..8] | g1_high | vector[0]最高位 |

## 关键差异（接入 core 须注意）

- **反向组**（cog-layer/heal-belief/hexq-prod）：维度 0（体）在**最低位**，与 core 的 g1 最高位相反，互转必须用 `bit_weight_map=[8..0]`。
- **hexq-prod 额外偏移**：`idx ∈ 1..19683`（1-based），转 core 需 `core_idx = hexq_idx - 1`。
- **meihua 三元体/用/变**：是 9 宫分 3 组的多数票投影（27 格局），**非**每爻三态，属语义自适配层，九宫编码本身与 core 同构。

## 校验

任一 manifest 须通过 `sanjiu_core.validate.validate_manifest`：
- `space == 19683`
- `state_alphabet` 恰好覆盖三态键 -1/0/+1
- `bit_weight_map` 为 0..8 的排列
- 数据索引落于 0..19682 且唯一（hexq 需先 -1）
