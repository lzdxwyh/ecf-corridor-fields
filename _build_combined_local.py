#!/usr/bin/env python3
"""Rebuild main_combined.tex for the archive copy (self-contained for the online compiler).

Recursively inlines every \\input{...} (math_commands, sections/*, figures/fig1_motivation)
with % ===== begin/end markers, mirroring the format of the previous combined build.
Source of truth: main.tex + sections/ + figures/. Run from the version folder.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
MAIN = ROOT / "main.tex"
OUT = ROOT / "main_combined.tex"

pat = re.compile(r"^\\input\{([^}]+)\}\s*$", re.M)

def inline(text: str, depth: int = 0) -> str:
    def repl(m: re.Match) -> str:
        rel = m.group(1).strip()
        f = ROOT / (rel + ".tex")
        if not f.is_file():
            f = ROOT / rel
        if not f.is_file():
            return m.group(0)  # leave unknown inputs untouched
        body = f.read_text(encoding="utf-8")
        inlined = inline(body, depth + 1) if depth < 8 else body
        return (f"\n% ===== begin inlined {rel}.tex =====\n"
                + inlined.rstrip() + "\n"
                + f"% ===== end inlined {rel}.tex =====\n")
    return pat.sub(repl, text)

src = MAIN.read_text(encoding="utf-8")
out = ("% AUTO-GENERATED (local build for verification) - do not edit by hand.\n"
       "% Source of truth: 我的论文/ECF论文_留存版本/01_最终完整版_20261002_2038_r16/main.tex + sections/ + figures/\n\n"
       + inline(src))
OUT.write_text(out, encoding="utf-8")

n_in = len(pat.findall(src))
print(f"[ok] wrote {OUT.name}: {OUT.stat().st_size} bytes; top-level inputs inlined from main.tex")
