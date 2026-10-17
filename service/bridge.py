# -*- coding: utf-8 -*-
"""三元九维 19683 · 认知坐标服务 + 语义桥（MVP）。

设计原则（沿「形式统一 + 语义自适配」）：
- sanjiu-core 只提供与领域无关的数学底座（索引/算子/距离），本模块不修改它。
- 语义桥 = 同一编号卦，在各已适配领域（D/R/T · 体用变 · 洛书九宫）各自"从卦象义长出来"的确定性解读。
  各域先用自身 manifest 的 bit_weight_map 把 core 规范向量映射到域内维序，再用域规则生成解读。
- 结构倾向（进/守/待/变/衡/张力）从 core 向量直接算出，跨域共享 —— 这是"同一坐标、多语言说同一件事"的可量化锚点。

公理锁定；本模块只做映射层创作与检索，不改数理。
"""
from __future__ import annotations

import os
import sys
import math

_HERE = os.path.dirname(os.path.abspath(__file__))
_CORE = os.path.normpath(os.path.join(_HERE, "..", "..", "sanjiu-core"))
_TRIG = os.path.normpath(os.path.join(_HERE, "..", "..", "trigram"))
for p in (_CORE, _TRIG):
    if p not in sys.path:
        sys.path.insert(0, p)

from sanjiu_core import (  # noqa: E402
    idx_to_g, g_to_idx, F_C, F_Z, F_CZ, F_H, F_B_multi, N,
)

# ======================================================================
# 台阶一 · 认知坐标服务原语
# ======================================================================

# 轻量自然语言→9维向量词表（对应 core 规范 g1..g9，上→下）
LEXICON = [
    (("显", "达成", "上位", "向外", "盛"), ("隐", "潜藏", "退", "收敛", "衰")),
    (("生发", "增益", "主导", "动"), ("减损", "被动", "静")),
    (("居间", "耦合", "过渡", "中"), ("偏", "极端", "失衡")),
    (("主动", "进", "张", "雄", "攻"), ("缩", "雌", "守", "退")),
    (("势能", "平衡", "稳", "蓄"), ("不稳", "倾", "泄")),
    (("生", "长", "升", "阳"), ("衰", "降", "阴")),
    (("通", "交", "联", "化"), ("隔", "滞", "塞")),
    (("明", "显于外", "成"), ("晦", "藏于内", "败")),
    (("下位", "根基", "本", "内", "实"), ("末", "枝", "外", "虚")),
]


def encode(text: str, lexicon=None) -> tuple:
    """自然语言状态 → 9 维向量（core 规范）。"""
    lex = lexicon or LEXICON
    vec = []
    for pos_kw, neg_kw in lex[:9]:
        if any(k in text for k in pos_kw):
            vec.append(1)
        elif any(k in text for k in neg_kw):
            vec.append(-1)
        else:
            vec.append(0)
    return tuple(vec)


def search(vec, top_n: int = 5):
    """给定 9 维向量 → 欧氏距离 Top-N 邻近卦（全套变换推演）。"""
    full = [idx_to_g(i) for i in range(N)]
    dists = []
    for i, g in enumerate(full):
        d = math.sqrt(sum((a - b) ** 2 for a, b in zip(g, vec)))
        dists.append((d, i, g))
    dists.sort(key=lambda x: (x[0], x[1]))
    out = []
    for d, i, g in dists[:top_n]:
        out.append({
            "idx": i, "dist": round(d, 4), "gua": g,
            "F_C": F_C(g), "F_Z": F_Z(g), "F_CZ": F_CZ(g), "F_H": F_H(g),
        })
    return out


def transform(g):
    """全套结构变换：错/综/错综/互（5维内核）+ 逐爻动变。"""
    return {
        "错卦 F_C": F_C(g), "综卦 F_Z": F_Z(g), "错综 F_CZ": F_CZ(g),
        "互卦 F_H(5维)": F_H(g),
        "变卦": {p + 1: F_B_multi(g, [p]) for p in range(9)},
    }


# ======================================================================
# 台阶二 · 结构倾向（跨域共享锚点）
# ======================================================================

def fingerprint(g):
    """跨域结构指纹：阳性/阴性/中性计数 + 倾向标签 + 张力。"""
    pos = sum(1 for x in g if x > 0)
    neg = sum(1 for x in g if x < 0)
    zero = 9 - pos - neg
    bal = pos - neg
    en = pos + neg
    if zero >= 5:
        tend = "枢·待（中性维多，处于枢纽/过渡，宜静观）"
    elif bal >= 3 and en >= 6:
        tend = "显·进（阳气盛而贯通，宜主动推进）"
    elif bal <= -3 and en >= 6:
        tend = "隐·守（阴气盛而收敛，宜守正待时）"
    elif bal >= 1:
        tend = "偏显·渐（阳气略胜，可缓进勿躁）"
    elif bal <= -1:
        tend = "偏隐·渐守（阴气略胜，宜蓄力勿进）"
    else:
        tend = "衡·中（阴阳相持，宜居中权衡）"
    tension = "张力高（阴阳并争）" if (pos >= 3 and neg >= 3) else "张力低（势单一致）"
    return {
        "pos": pos, "neg": neg, "zero": zero,
        "balance": bal, "energy": en, "tendency": tend, "tension": tension,
    }


# ======================================================================
# 台阶二 · 语义桥：三域规则（manifest 位权映射 + 各域语义）
# ======================================================================

# 各域：dims=域内 9 维名（序=manifest bit_weight_map 映射后的域内序）；bit_weight_map；trit 语义
DOMAINS = {}

# --- 域 A · D/R/T（主仓 sanjiu-nine，位权恒等：core g1..g9 即 D/R/T 上→下）---
DOMAINS["D/R/T"] = {
    "bit_weight": [0, 1, 2, 3, 4, 5, 6, 7, 8],
    "dims": ["承载", "审定", "增益", "承载", "审定", "增益", "承载", "审定", "增益"],
    "trit": {"-1": "亏/隐", "0": "衡/待", "+1": "盈/显"},
    "render": lambda v: _render_drt(v),
}

# --- 域 B · 体用变（cog-layer / heal-belief，位权反向：域内位0=体=最低位=core g9）---
DOMAINS["体用变"] = {
    "bit_weight": [8, 7, 6, 5, 4, 3, 2, 1, 0],
    "dims": ["体", "用", "变", "时", "空", "势", "因", "果", "缘"],
    "trit": {"-1": "不足", "0": "中和", "+1": "充盈"},
    "render": lambda v: _render_tiyong(v),
}

# --- 域 C · 洛书九宫（meihua，位权恒等：core g1=坎最高…g9=离最低）---
DOMAINS["洛书九宫"] = {
    "bit_weight": [0, 1, 2, 3, 4, 5, 6, 7, 8],
    "dims": ["坎水", "坤土", "震木", "巽木", "中土", "乾金", "兑金", "艮土", "离火"],
    "trit": {"-1": "气敛", "0": "气枢", "+1": "气旺"},
    "render": lambda v: _render_luoshu(v),
}


def _map_to_domain(g, dom):
    """core 规范向量 → 域内向量（按 manifest 位权）。"""
    bw = DOMAINS[dom]["bit_weight"]
    out = [0] * 9
    for i, j in enumerate(bw):       # core g[j] → 域内维 i
        out[i] = g[j]
    return tuple(out)


def _to_core_from_domain(v, dom):
    bw = DOMAINS[dom]["bit_weight"]
    out = [0] * 9
    for i, j in enumerate(bw):
        out[j] = v[i]
    return tuple(out)


def _render_drt(v):
    """D/R/T：以承载/审定/增益三组×上中下判强弱明晦（五档）。"""
    def _level(grp):
        s = sum(grp)
        if s >= 2:
            return "盈·强", "明·彻", "丰·足"
        if s == 1:
            return "略盈·可任", "略明·可察", "略增·有余"
        if s == 0:
            return "中平·堪任", "持衡·可判", "平允·相称"
        if s == -1:
            return "略亏·吃力", "略晦·欠察", "略耗·见绌"
        return "亏·难任", "晦·难判", "耗·虚损"
    c_s, j_s, g_s = (_level(g)[i] for i, g in enumerate(
        [(v[0], v[3], v[6]), (v[1], v[4], v[7]), (v[2], v[5], v[8])]))
    return f"承载{c_s}；审定{j_s}；增益{g_s}。"


def _render_tiyong(v):
    """体用变时空势因果缘：体用为纲，变时势为机，因果缘为链。"""
    ti, yong, bian = v[0], v[1], v[2]
    shi, kong, shi2 = v[3], v[4], v[5]
    yin, guo, yuan = v[6], v[7], v[8]
    ti_s = {1: "体充盈，根基厚实", 0: "体中平，根基稳当", -1: "体不足，根基薄弱"}[ti]
    yong_s = {1: "用有盈，施为得力", 0: "用中和，施为平实", -1: "用虚耗，施为乏力"}[yong]
    bian_s = {1: "变机已现，转捩在即", 0: "变候待发，机尚在伏", -1: "变机闭塞，转折难成"}[bian]
    shi_s = {1: "时势顺遂", 0: "时势平缓", -1: "时势逆阻"}[shi]
    yuan_s = {1: "外缘聚拢，得助可期", 0: "外缘平正，援而不强", -1: "外缘散逸，多靠自立"}[yuan]
    return f"{ti_s}；{yong_s}；{bian_s}；{shi_s}；{yuan_s}。"


def _render_luoshu(v):
    """洛书九宫：坎坤震巽中乾兑艮离，宫气旺衰 + 中宫枢纽。"""
    wang = [d for d, x in zip(DOMAINS["洛书九宫"]["dims"], v) if x > 0]
    lian = [d for d, x in zip(DOMAINS["洛书九宫"]["dims"], v) if x < 0]
    hub = v[4]  # 中土
    hub_s = {1: "中宫气旺，枢纽当行", 0: "中宫气枢，主权衡待定", -1: "中宫气敛，枢纽沉寂"}[hub]
    wang_s = ("气旺之宫：" + "、".join(wang) + "；") if wang else "无气旺之宫；"
    lian_s = ("气敛之宫：" + "、".join(lian) + "。") if lian else "无气敛之宫。"
    return f"{hub_s}；{wang_s}{lian_s}"


# ======================================================================
# 语义桥 · 同编号卦 → 多域并行解读
# ======================================================================

def render(domain: str, g):
    """单域解读：core 向量 → 域内 → 域解读 + 共享结构倾向。"""
    if domain not in DOMAINS:
        raise KeyError(f"未知领域 {domain}；可选 {list(DOMAINS)}")
    v = _map_to_domain(g, domain)
    text = DOMAINS[domain]["render"](v)
    return {"domain": domain, "vec_domain": v, "text": text}


def bridge(g):
    """同一编号卦 → 各域并行解读（核心产品：同一坐标，多语言说同一件事）。"""
    fp = fingerprint(g)
    return {
        "idx": g_to_idx(g) if isinstance(g, tuple) else g,
        "gua_core": idx_to_g(g) if not isinstance(g, tuple) else g,
        "fingerprint": fp,
        "domains": {d: render(d, idx_to_g(g) if not isinstance(g, tuple) else g)
                    for d in DOMAINS},
    }


# ---- 便捷入口 ----
def bridge_by_idx(idx: int):
    return bridge(idx_to_g(idx))


def bridge_by_text(text: str, top_n: int = 1):
    vec = encode(text)
    hits = search(vec, top_n=top_n)
    return vec, hits, [bridge(h["gua"]) for h in hits]


if __name__ == "__main__":
    print("=" * 66)
    print("认知坐标服务 + 语义桥 MVP · 三元九维 19683")
    print("=" * 66)
    for idx in (9841, 19682, 0, 13000):
        b = bridge_by_idx(idx)
        print(f"\n【编号 {b['idx']}】卦 {b['gua_core']}  指纹 {b['fingerprint']['tendency']}")
        for d, r in b["domains"].items():
            print(f"  [{d}] {r['text']}")
    print("\n-- 自然语言定位示例 --")
    vec, hits, bridges = bridge_by_text("根基稳固，主动进取，增益丰盈，时势顺遂", top_n=1)
    print("  输入→向量:", vec)
    print("  Top1 卦:", hits[0]["idx"], hits[0]["gua"])
