# Machines

What each Mac uses for this repo: the detector project (root) and the electrometer (`electrometer/`). System-wide setup (what each Mac has installed, the macOS 13 limits, uv and Python rules) is in `~/Documents/system-config/machines/README.md`: read it before installing anything.

## Shared

- **Venv for `sim/field/`:** `requirements.txt` is the source of truth (numpy, scipy, matplotlib), Python pinned in `.python-version` (3.12.15). Build: `~/.local/bin/uv venv --managed-python .venv` then `~/.local/bin/uv pip install --python .venv -r requirements.txt` (wheels only). Run with `.venv/bin/python`.
- Standard library only, no venv needed:
  - `sim/analytic/enc_budget.py` and `electrometer/sim/analytic/budget.py`: run with `python3 -I`, output beside them in `*.out.txt`.
  - `docs/diagrams/make_diagrams.py` and the questions' diagram scripts: need `ELECTRONICS_TOOLS` set (they import `diagrams/svgdiagram.py` from there).
  - `electrometer/docs/diagrams/make_diagrams.py`: self-contained.
- Headless Google Chrome renders the SVGs for checking (`readme.MD` "Diagrams" in electronics-tools).
- No KiCad project yet. When one starts, both Macs use the same KiCad major version, and the Intel Mac sets the ceiling.

## Home Mac (home-mbp: MacBook Pro, Intel, x86_64)

Updated 2026-11-21. Checked on this Mac on that date.

| Item | Value | Checked with |
|---|---|---|
| macOS | 13.7.8 | `sw_vers -productVersion` |
| Python | 3.12.1, python.org framework build at `/Library/Frameworks/Python.framework/Versions/3.12/bin/python3`, used as is (standard library only, nothing installed into it) | `python3 --version`, `which python3` |
| Project venv | `.venv`, uv-managed Python 3.12.15, built with uv 0.13.1 (no-build). numpy 2.5.5, scipy 1.18.1, matplotlib 3.11.2, all from wheels | `.venv/bin/python --version`, `uv pip list --python .venv` |
| S-01 | `verify.py` and `run.py` run; about 4 minutes for `run.py` | 2026-11-21 |
| Script outputs | `enc_budget.py` and `budget.py` reproduce their committed `*.out.txt` exactly | `diff` |
| Google Chrome | 158.0.8127.36 | `Google Chrome --version` |
| KiCad | Installed in `/Applications/KiCad`, not used by this repo yet | `/Applications` listing |

## Work Mac (work-mini: Mac mini M4, arm64)

Known so far, not checked on that Mac: the venv has not been built there (`requirements.txt` pins are the Intel Mac's resolution). The electronics-tools `MACHINES.md` lists its Python (uv-managed 3.12.15), Chrome and KiCad 10.0.7.
