# -*- coding: utf-8 -*-
"""sanjiu-bridge CLI · 认知原语统一入口。

用法（在 service/ 目录下）：
  python3 cli.py encode "自然语言状态"              # 状态 → 9维向量
  python3 cli.py search "自然语言状态" --top 3       # → Top-N 最近邻卦
  python3 cli.py bridge <编号>                       # 编号 → 五域解读 + 深度象义
  python3 cli.py generalize "处境描述" [--domain D/R/T]  # 邻域泛化推理
  python3 cli.py domains                             # 列出五域
  python3 cli.py enhance "处境描述"                  # 符号骨架 + 泛化总结
"""
from __future__ import annotations

import os
import sys
import json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bridge import (  # noqa: E402
    encode, search, bridge_by_idx, bridge_by_text, DOMAINS,
)
from generalize import generalize, synthesize  # noqa: E402
from enhance import enhance  # noqa: E402


def _show_bridge(b, with_deep=True):
    fp = b["fingerprint"]
    print(f"编号 {b['idx']}  卦 {b['gua_core']}")
    print(f"指纹: {fp['tendency']} | {fp['tension']} (阳{fp['pos']}/阴{fp['neg']}/中{fp['zero']})")
    if with_deep and b["deep"]:
        print(f"深度象义: {b['deep']['ming']} — {b['deep']['qi']}")
        print(f"卦辞: {b['deep']['su']}")
    for d, r in b["domains"].items():
        print(f"  [{d}] {r['text']}")


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        print(__doc__)
        return 0
    cmd = argv.pop(0)
    if cmd == "encode":
        print(json.dumps({"text": argv[0], "vec": list(encode(argv[0]))},
                         ensure_ascii=False))
    elif cmd == "search":
        top = int(argv[2]) if len(argv) > 2 else 3
        v = encode(argv[0]); hits = search(v, top_n=top)
        print("向量:", v)
        for h in hits:
            print(f"  距{h['dist']:.3f}  卦{h['idx']}  {h['gua']}")
    elif cmd == "bridge":
        idx = int(argv[0])
        _show_bridge(bridge_by_idx(idx))
    elif cmd == "generalize":
        domain = argv[2] if len(argv) > 2 else None
        v, items = generalize(argv[0], top_n=3, domain=domain)
        print(f"处境: {argv[0]}  向量: {v}")
        for it in items:
            line = f"  距{it['dist']:.3f}  卦{it['idx']}  {it['deep']['ming']} — {it['deep']['qi']}"
            if domain:
                line += f"\n        [{domain}] {it['domain_text']}"
            print(line)
        print("泛化结论:", synthesize(argv[0], 3)["summary"])
    elif cmd == "enhance":
        r = enhance(argv[0])
        print("向量:", r["skeleton"]["vec"])
        print("最近邻:", [f"{i['idx']} {i['deep']['ming']}" for i in r["skeleton"]["items"]])
        print("总结:", r["summary"])
    elif cmd == "domains":
        for d in DOMAINS:
            m = DOMAINS[d]
            print(f"- {d}: {len(m['dims'])}维 {m['dims']}  位权{'正向' if m['bit_weight']==list(range(9)) else '反向'}")
    else:
        print(f"未知命令 {cmd}\n" + __doc__)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
