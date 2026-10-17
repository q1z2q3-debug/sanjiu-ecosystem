# -*- coding: utf-8 -*-
"""台阶三雏形 · 邻域泛化推理（generalize.py）

思想：19683 空间是"可定位 + 可泛化"的认知坐标。
已知一个真实处境（自然语言）→ encode 到 9 维向量 → 欧氏距离找最近邻 Top-N 卦，
用最近邻卦的**深度卦典启示**（人类语言解读）作为可迁移知识，推断该处境的走向与策略。

这正是"已知态 → 最近邻 → 推未知态"：借邻域卦的解读，对未知/未定状态做泛化。
纯符号实现（不依赖 LLM），为后续"符号给骨架 + LLM 填自然语言"铺底。

公理锁定；本模块只做检索与知识迁移演示，不改数理。
"""
from __future__ import annotations

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bridge import encode, search, bridge_by_idx, DOMAINS


def generalize(text: str, top_n: int = 3, domain: str | None = None):
    """处境 → 最近邻 Top-N 卦 → 各卦深度象义 + （可选）单域解读。"""
    vec = encode(text)
    hits = search(vec, top_n=top_n)
    out = []
    for h in hits:
        b = bridge_by_idx(h["idx"])
        item = {
            "dist": h["dist"], "idx": h["idx"], "gua": h["gua"],
            "fingerprint": b["fingerprint"],
            "deep": b["deep"],
        }
        if domain:
            item["domain_text"] = b["domains"][domain]["text"]
        out.append(item)
    return vec, out


def synthesize(text: str, top_n: int = 3):
    """把最近邻卦的启示综合为一段泛化结论（确定性拼接，非 LLM）。"""
    vec, items = generalize(text, top_n=top_n)
    qis = [f"[{it['idx']}] {it['deep']['ming']}：{it['deep']['qi']}" for it in items]
    # 取最近邻卦作主判
    top = items[0]
    yinyang = top["deep"]["yinyang"]
    fp = top["fingerprint"]
    head = f"输入'{text}' → 向量{vec} → 最近邻卦 {top['idx']}（距 {top['dist']}）。"
    body = "泛化启示：以最近邻卦" + top["deep"]["ming"] + "为镜，" + top["deep"]["qi"] + "。"
    return {
        "vec": vec,
        "primary": {"idx": top["idx"], "ming": top["deep"]["ming"], "qi": top["deep"]["qi"]},
        "tendency": fp["tendency"],
        "summary": head + body,
        "neighbors": qis,
    }


DEMO = [
    "起手资金有限，根基单薄，但想稳步扩张，不冒进",
    "长期疲劳，气血亏损，需要静养调补，忌消耗",
    "新学一门语言，起步慢，需要耐心积累，不急于求成",
    "行情剧烈震荡，多空争夺，应观望避险，不宜重仓",
    "团队人心不齐，有人争执，需先协调关系再谈推进",
    "产品已成熟，市场向好，时机成熟，宜大力投放",
]


def main():
    print("=" * 74)
    print("台阶三雏形 · 邻域泛化推理（已知态→邻域卦→推未知态）")
    print("=" * 74)
    for text in DEMO:
        v, items = generalize(text, top_n=3)
        print(f"\n■ 处境：{text}")
        print(f"   →向量 {v}（写进 19683 坐标）")
        for it in items:
            print(f"   · 距 {it['dist']:>5}  卦 {it['idx']:>5}  {it['deep']['ming']} — {it['deep']['qi']}")
        s = synthesize(text, top_n=3)
        print(f"   ↳ 泛化结论：{s['summary']}")


if __name__ == "__main__":
    main()
