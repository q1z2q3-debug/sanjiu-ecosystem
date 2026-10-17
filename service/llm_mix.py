# -*- coding: utf-8 -*-
"""LLM 混合主链路（llm_mix.py）· 接入即是我自己。

哲学：符号给可演算骨架，LLM 填自然语言。接入的主模型（Doubao）就是 LLM 本体。
两条能力由主模型当场提供，再注入本管线：
  ① decode_llm(text) -> (vector, reason)：把自然语言"当场语义解码"成 9 维向量
     （这是 encode 的分辨率增强——口语、隐含语义、语境词都能理解，不靠词表）。
  ② humanize(skeleton) -> str：基于符号骨架（五域 + 深度卦典 + 结构指纹）
     生成自然语言人类解读（回归正轨人类语言体系）。

本模块把注入的向量跑通 定位→五域解读→深度卦典→泛化 全链路；
humanize 结果由主模型在对话中给出后回填（也可传 humanize_fn 自动注入）。
纯符号也能跑（未注入向量时退回 encode 词表），故不依赖外部 API。
"""
from __future__ import annotations

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bridge import encode, search, bridge_by_idx  # noqa: E402


def run(text: str, vector=None, reason=None, top_n: int = 3):
    """LLM 混合主链路。vector/reason 由主模型注入；未注入则退回符号 encode。"""
    v = tuple(vector) if vector else encode(text)
    hits = search(v, top_n=top_n)
    items = []
    for h in hits:
        b = bridge_by_idx(h["idx"])
        items.append({
            "dist": round(h["dist"], 3), "idx": h["idx"], "gua": h["gua"],
            "fingerprint": b["fingerprint"], "deep": b["deep"],
            "domains": {d: b["domains"][d]["text"] for d in b["domains"]},
        })
    return {
        "text": text, "vec": v, "reason": reason,
        "encode_channel": "LLM主模型注入" if vector else "符号词表",
        "items": items,
    }


def format_md(r: dict) -> str:
    """把结果格式化为人类可读 markdown（主模型据此填人类解读）。"""
    top = r["items"][0]
    fp = top["fingerprint"]
    deep = top["deep"]
    lines = [
        f"**处境**：{r['text']}",
        f"**编码**（{r['encode_channel']}）→ 向量 {r['vec']}" +
            (f" ｜ 理由：{r['reason']}" if r["reason"] else ""),
        f"**定位**：最近邻卦 {top['idx']}（{deep['ming']}，{fp['tendency']}，{fp['tension']}）",
        f"**卦典**：{deep['ming']} — {deep['qi']}",
        "**五域同判**：",
    ]
    for d, t in top["domains"].items():
        lines.append(f"  - {d}：{t}")
    lines.append("**邻近卦**：" + "；".join(
        f"{i['idx']} {i['deep']['ming']}" for i in r["items"]))
    return "\n".join(lines)


if __name__ == "__main__":
    # 主模型注入示例（decode 与 humanize 由主模型当场给出）
    text = "项目胎死腹中，团队士气低落，但根基还在，宜收敛蓄力、守中待动"
    vector = (-1, -1, -1, -1, 0, -1, -1, 0, 1)
    reason = "整体阴势敛藏：上显未成、主导受挫、刚健守收、不生发不通达；唯根基仍在(阳)而中爻蓄势持衡(0)"
    r = run(text, vector=vector, reason=reason)
    print(format_md(r))
    print("\n**主模型人类解读（符号骨架→人类语言）**：")
    human = (
        "此局阴气盛而敛藏，主守不主发。卦判「阴·利贞·闭守止卦」——养晦蓄势，静待天时。"
        "五域同证：体用变见变机闭塞、时势逆阻，小六壬见空亡·虚耗，皆示此际不宜妄动。"
        "所幸根基尚在（体充盈、初爻阳），中爻持衡蓄势——机不在攻而在养：宜收敛元气、"
        "稳住团队底盘，止损聚气，蓄一阳而待时势转圜，再图后动。"
    )
    print(human)
