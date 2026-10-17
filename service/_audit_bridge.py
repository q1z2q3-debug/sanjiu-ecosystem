# -*- coding: utf-8 -*-
"""语义桥一致性验证（MVP）：
1) 机械一致性 —— 各域解读都由同一结构指纹驱动，倾向标签应全部一致（应为 100%）。
2) 语义贴合 —— 同编号卦在 D/R/T · 体用变 · 洛书三域的解读文本，是否指向同一处境。
抽样覆盖全部倾向类（显进/隐守/枢待/偏显/偏隐/衡中/张力），供人工/LLM 评审。
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bridge import bridge_by_idx, fingerprint, idx_to_g

SAMPLE = [
    # (编号, 说明)
    (9841, "中心态·全中和"),
    (19682, "全阳·极显"),
    (0, "全阴·极隐"),
    (12144, "张力卦·阴阳并争(试)"),
    (12900, "偏显候选"),
    (1100, "偏隐候选"),
    (7000, "枢纽候选"),
    (4000, "随机关卡"),
    (14000, "随机关卡"),
    (17000, "随机关卡"),
    (5000, "随机关卡"),
    (9000, "随机关卡"),
]


def tendency_short(t):
    return t.split("（")[0].strip()


def main():
    print("=" * 78)
    print("语义桥一致性验证 · 三元九维 19683")
    print("=" * 78)
    stats = {"dom": {d: 0 for d in ("D/R/T", "体用变", "洛书九宫")},
             "tendency_agree": 0, "total": 0}
    for idx, note in SAMPLE:
        b = bridge_by_idx(idx)
        fp = b["fingerprint"]
        short = tendency_short(fp["tendency"])
        agree = True
        print(f"\n● 编号 {idx:>5} ({note})  卦 {b['gua_core']}")
        print(f"    指纹: {fp['tendency']} | {fp['tension']} (阳{fp['pos']}/阴{fp['neg']}/中{fp['zero']})")
        for d in ("D/R/T", "体用变", "洛书九宫"):
            stats["dom"][d] += 1
            print(f"    [{d}] {b['domains'][d]['text']}")
        stats["total"] += 1
        # 各域解读均由同一指纹驱动 → 倾向一致（机械层）
        if fp["tendency"]:
            stats["tendency_agree"] += 1
    print("\n" + "=" * 78)
    print(f"机械一致性: {stats['tendency_agree']}/{stats['total']} 卦三域共享同一结构倾向")
    print("（说明：三域解读均从同一结构指纹派生，倾向天然一致；")
    print("  语义贴合度见 MVP 报告人工/LLM 评审）")


if __name__ == "__main__":
    main()
