#!/usr/bin/env python3
"""Rebuild main_supplementary_combined.tex for the archive copy (self-contained for the online compiler).

Mirrors _build_combined_local.py, but for the supplementary driver.
Recursively inlines every \\input{...} (math_commands, sections/A_appendix_supp).
Source of truth: main_supplementary.tex + sections/. Run from the version folder.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
MAIN = ROOT / "main_supplementary.tex"
OUT = ROOT / "main_supplementary_combined.tex"

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
        return inlined.rstrip() + "\n"
    return pat.sub(repl, text)


src = MAIN.read_text(encoding="utf-8")
out = ("% AUTO-GENERATED (local build for verification) - do not edit by hand.\n"
       "% Source of truth: main_supplementary.tex + sections/A_appendix_supp.tex (+ math_commands).\n\n"
       + inline(src))
OUT.write_text(out, encoding="utf-8")

n_in = len(pat.findall(src))
print(f"[ok] wrote {OUT.name}: {OUT.stat().st_size} bytes; inputs inlined: {n_in}")
