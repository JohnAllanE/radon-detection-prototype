# Part 1 chamber: geometry and expected count rate

**Conclusion:** The 21–22 mm bore tube with boards 76 mm apart holds 26–29 cm³, which at 100 Bq/m³ gives roughly 2–5 counts/hour for the whole chamber. A 10 % statistical uncertainty then takes days indoors and weeks outdoors: fine for comparing boards, low sensitivity at ambient levels, good at mine levels.

**Relied on by:** R-01 (Part 1 detects radon progeny), R-14 (event rate), R-39 (chamber bore), Q-04 (target sensitivity), the architecture's shaping-time choice.

## Working

### Geometry (D-22)

- VTH2110 die 5.67 mm square, 5 mm active (VTH2110.json p1).
- A 2×2 array with 0.5 mm gaps is about 11.8 mm per side and has a 16.75 mm diagonal.
- Bore 21–22 mm (3/4 in NPS pipe, ground and lapped, D-22): die corner to wall about 2.1 mm (21 mm) to 2.6 mm (22 mm). The earlier 16 mm ID (D-09) could not hold four dies.
- Gap to wall is confirmed by the field simulation; bore tolerance and etch go in the mechanical drawing.

### Count rate (preliminary, `VERIFY` all; assumptions in bold)

- Volume: $\pi \times 1.05^2 \times 7.6 \approx 26$ cm³ (21 mm) to $\pi \times 1.1^2 \times 7.6 \approx 29$ cm³ (22 mm).
- At 100 Bq/m³ (0.1 Bq/L, a typical indoor level): $0.1 \times 0.026 \approx 2.6$ mBq of radon, about 9.5 radon decays per hour (about 10.4 at 22 mm).
- Each decay can give two alphas (Po-218, later Po-214). **If the overall collection and detection efficiency is 10–25 % per alpha**, the chamber sees roughly 2–5 counts/hour at 100 Bq/m³ and 0.2–0.5 counts/hour at 10 Bq/m³ (outdoor level).
- The efficiency is a guess. It is what the field simulation must tell us.
- For a 10 % statistical uncertainty (100 counts): indoor air takes of order days, outdoor air weeks. That fits the user's plan of hours to days, a week or more for calibration.

### Consequences

- Radon rates of about 1 count/hour allow long shaping (4–10 µs) at no pile-up cost.
- A 2 ms conversion still allows about 500 events/s, so a fast ADC path matters only for calibration with a strong source.

## Sources

- `datasheets/VTH2110.json` p1.
- Decisions D-09, D-22.
