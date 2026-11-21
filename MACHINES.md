# Machines

What each Mac uses for this repo: the detector project (root) and the electrometer (`electrometer/`). System-wide setup (what each Mac has installed, the macOS 13 limits, uv and Python rules) is in `~/Documents/system-config/machines/README.md`: read it before installing anything.

## Shared

- **No venv and no requirements file:** every script here uses the Python standard library only.
  - `sim/analytic/enc_budget.py` and `electrometer/sim/analytic/budget.py`: run with `python3 -I`, output beside them in `*.out.txt`.
  - `docs/diagrams/make_diagrams.py`: needs `ELECTRONICS_TOOLS` set (it imports `diagrams/svgdiagram.py` from there) and doesn't use `Svg.math()`, so no matplotlib.
  - `electrometer/docs/diagrams/make_diagrams.py`: self-contained.
- If a script ever imports a package, add `requirements.txt` and `.python-version` (3.12.15) and build a `.venv` per the system-config rules.
- Headless Google Chrome renders the SVGs for checking (`readme.MD` "Diagrams" in electronics-tools).
- No KiCad project yet. When one starts, both Macs use the same KiCad major version, and the Intel Mac sets the ceiling.

## Home Mac (home-mbp: MacBook Pro, Intel, x86_64)

Updated 2026-11-20. Checked on this Mac on that date.

| Item | Value | Checked with |
|---|---|---|
| macOS | 13.7.8 | `sw_vers -productVersion` |
| Python | 3.12.1, python.org framework build at `/Library/Frameworks/Python.framework/Versions/3.12/bin/python3`, used as is (standard library only, nothing installed into it) | `python3 --version`, `which python3` |
| Script outputs | `enc_budget.py` and `budget.py` reproduce their committed `*.out.txt` exactly | `diff` |
| Google Chrome | 158.0.8127.36 | `Google Chrome --version` |
| KiCad | Installed in `/Applications/KiCad`, not used by this repo yet | `/Applications` listing |

## Work Mac (work-mini: Mac mini M4, arm64)

Known so far, not checked on that Mac: nothing in this repo records it. The electronics-tools `MACHINES.md` lists its Python (uv-managed 3.12.15), Chrome and KiCad 10.0.7.
