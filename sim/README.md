# Simulations

| ID | Folder | What | Status |
|---|---|---|---|
| — | `analytic/` | ENC budget per op-amp and shaping time (standard library) | Done, pass 1 |
| S-01 | `field/S-01-chamber/` | Axisymmetric field of the Part 1 chamber end, ion landing, peak fields | Done, pass 1 |

## Summary

- **Supported:** R-47 (ions steered onto the diodes: 95–99 % of field lines from the gas end on the array without help), R-38 and R-43 inside the chamber (peak field about 1.2 kV/mm with 0.5 mm edge radius on the tube ends, against roughly 3 kV/mm for air at 1 atm, `VERIFY`).
- **Marginal:** R-75's 5.0 mm cannot hold on the chamber side; the field rule replaces it there. Count rate (R-01): about two-thirds of the ions land where the four dies meet, so about 16 % per alpha.
- **Design changes:** A-10 ring on the +20 V PD bias (Q-24 settled), no sloped electrode, the tube ends' edges rounded to about 0.5 mm, the die-to-wall gap accepted.
- Environment: the repo's `.venv` (`MACHINES.md`).
