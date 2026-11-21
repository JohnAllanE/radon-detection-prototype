# Candidates: photodiode

**Need:** a bare silicon photodiode chip that detects alphas through a thin dead layer, four of them in a 2×2 array inside a 21–22 mm bore (R-06, R-39).

**Pick:** Excelitas VTH2110, firm: fixed by the user. 5.67 mm chip, 5 mm active.

**Relied on by:** A-02 (photodiode), A-03 (mounting), A-04 (bias), R-06 (four diodes), R-39 (bore), R-47 (ion steering), the noise budget ($C_{pd}$, dark current).

## Candidates

Only two: the user fixed the part. Price, stock and lead time are open (pass 2). No alternate is chosen, and VTH2120 is a size variant, not a drop-in.

| Part | Maker | Price (CAD) | Stock or supplier | Package vs assembly | SPICE model | Lets the design | Costs the design |
|---|---|---|---|---|---|---|---|
| **VTH2110** | Excelitas | open | open, lead time unknown | Bare chip: conductive-epoxy die attach plus a 0.4 mm top bond pad. Carrier option (p1) | none needed | 2×2 array fits the bore with 2.1–2.6 mm to the wall | Hand bonding. Electrode polarity not stated (Q-11) |
| VTH2120 | Excelitas | open | open | Bare chip, 10 mm | none needed | Larger area | More capacitance, so more noise. Four don't fit the bore |

## What the pick sets

| Quantity | Value | From |
|---|---|---|
| Die, active area | 5.67 mm square, 5 mm active | VTH2110.json p1 |
| Capacitance | < 30 pF at 20 V (spec), about 32 pF (curve), about 21 pF at 50 V | p1, p3, Fig 3 |
| Dark current | 0.15 nA typical, 2 nA maximum at 20 V; 5 nA max at 40 V | p1, p3 |
| Bias | Specified at 20 V and 40 V, breakdown > 100 V, no recommended point | p1 |
| Depletion at 20 V | > 90 µm | p1 |
| Dead layer | 150 nm | p1 |
| Responsivity | 0.74 A/W peak | p3 |
| Humidity | 60 % RH, non-condensing | p2 |

## Sources

- `datasheets/VTH2110.json` and `VTH2110.pdf` (the PDF came from a JLCPCB mirror, Excelitas blocks scripted downloads). Not yet in component-data.
