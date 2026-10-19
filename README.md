# Ego-Corridor Fields

LaTeX source and figures for **"Ego-Corridor Fields: Differentiable Corridor
Rasterization for Referring Rail Segmentation"** (IEEE Transactions on Circuits
and Systems for Video Technology, submitted).

A Sa2VA-style `[SEG]` hidden state is mapped by a small ParamHead to 20 corridor
parameters (vanishing point, centerline control points, left/right width samples,
topology logits), and a parameter-free differentiable rasterizer renders them into
the referring-segmentation mask. The SAM2 mask decoder is bypassed on the evaluated
path.

## Contents

| Path | Description |
|---|---|
| `main.tex` | IEEEtran driver (`journal`, 10 pt, two columns) |
| `sections/` | `00_abstract` … `05_conclusion`, plus the supplementary appendix sources |
| `references.bib` | 26 references, `IEEEtran` style |
| `figures/` | the eight figures included by the manuscript |
| `_build_combined_local.py` | inlines `\input` recursively into a single-file `main_combined.tex` |

## Building

```bash
pdflatex main
bibtex   main
pdflatex main
pdflatex main
```

`main.tex` expects a full TeX Live installation (IEEEtran, `dblfloatfix`,
`natbib`, `hyperref`, `booktabs`, `tabularx`). If you only have an online
compiler, run `python _build_combined_local.py` first and upload the generated
`main_combined.tex` together with `figures/` and `references.bib`.

## Notes

- The manuscript reports one benchmark introduced in this work (FIRC2234) and one
  training run; all numbers are fp32, single checkpoint, `n = 208` test frames.
- Code, checkpoints, and evaluation scripts are released separately. This
  repository currently carries the manuscript source and figures only.
- Figure files are the exact ones used in the compiled paper; retired versions
  are not tracked here.
