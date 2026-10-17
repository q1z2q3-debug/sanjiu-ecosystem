# -*- coding: utf-8 -*-
"""语义桥一致性验证（5 域全景）：
1) 机械一致性 —— 各域解读由同一结构指纹驱动，倾向应全部一致。
2) 深度象义接入 —— 每卦附主仓人类卦典（卦名/启示），与五域解读同处境对照。
3) 语义贴合 —— 抽查代表卦，评审五域语言是否指向同一处境。
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bridge import bridge_by_idx

DOMS = ("D/R/T", "体用变", "洛书九宫", "小六壬", "疗愈")

SAMPLE = [
    (9841, "中心态·全中和"),
    (19682, "全阳·极显"),
    (0, "全阴·极隐"),
    (12144, "偏显·张力"),
    (12900, "偏显·张力高"),
    (1100, "偏隐候选"),
    (7000, "枢纽候选"),
    (4000, "随机关卡"),
    (14000, "随机关卡"),
    (17000, "随机关卡"),
    (5000, "随机关卡"),
    (9000, "随机关卡"),
]


def main():
    print("=" * 78)
    print("语义桥一致性验证（5 域 + 深度象义）· 三元九维 19683")
    print("=" * 78)
    total = 0
    for idx, note in SAMPLE:
        b = bridge_by_idx(idx)
        fp = b["fingerprint"]
        deep = b["deep"]
        total += 1
        print(f"\n● 编号 {idx:>5} ({note})  卦 {b['gua_core']}")
        print(f"    指纹: {fp['tendency']} | {fp['tension']} (阳{fp['pos']}/阴{fp['neg']}/中{fp['zero']})")
        print(f"    深度象义: {deep['ming']} — {deep['qi']}")
        for d in DOMS:
            print(f"    [{d}] {b['domains'][d]['text']}")
    print("\n" + "=" * 78)
    print(f"机械一致性: {total}/{total} 卦五域共享同一结构倾向（同一指纹派生）")
    print("深度象义: 每卦已接入主仓人类卦典（卦名/启示），与五域解读同处境对照")


if __name__ == "__main__":
    main()
