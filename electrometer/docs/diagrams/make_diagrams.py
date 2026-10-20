"""Generate the electrometer docs' diagrams as SVG (light and dark mode via prefers-color-scheme).

Edit the layouts below and rerun:  python3 electrometer/docs/diagrams/make_diagrams.py
Standard library only. Outputs sit next to this file and are embedded in ../01-requirements.md.
Style and helpers follow vibratory-bowl-seed-feeder/siggen-power-amp/docs/diagrams/make_diagrams.py,
plus a "set by hand" colour (man) and an HV colour (hv) for this board.
"""

from pathlib import Path

HERE = Path(__file__).resolve().parent

FONT = 'system-ui,-apple-system,"Segoe UI",sans-serif'
STYLE = f"""
<style>
  svg {{ --bg:#fcfcfb; --ink:#0b0b0b; --ink2:#52514e; --box:#ffffff; --edge:#898781;
        --group:#f3f2ee; --sig:#2a78d6; --ctl:#d95926; --man:#1a8f5a; --hv:#c62828; }}
  @media (prefers-color-scheme: dark) {{
    svg {{ --bg:#1a1a19; --ink:#f0efec; --ink2:#c3c2b7; --box:#262624; --edge:#6f6e69;
          --group:#222220; --sig:#3987e5; --ctl:#ec835a; --man:#52c48a; --hv:#ef6b6b; }}
  }}
  .bg {{ fill:var(--bg); }}
  .box {{ fill:var(--box); stroke:var(--edge); stroke-width:1.2; }}
  .group {{ fill:var(--group); stroke:var(--edge); stroke-width:1; }}
  .encl {{ fill:none; stroke:var(--edge); stroke-width:1.4; stroke-dasharray:7 4; }}
  .hvbox {{ fill:var(--box); stroke:var(--hv); stroke-width:1.4; }}
  .t {{ fill:var(--ink); font:600 13px {FONT}; }}
  .s {{ fill:var(--ink2); font:400 11.5px {FONT}; }}
  .k {{ fill:var(--ink); font:400 11.5px {FONT}; }}
  .g {{ fill:var(--ink2); font:600 11.5px {FONT}; letter-spacing:.02em; }}
  .lsig {{ fill:var(--sig); font:400 11.5px {FONT}; }}
  .lctl {{ fill:var(--ctl); font:400 11.5px {FONT}; }}
  .lman {{ fill:var(--man); font:600 11.5px {FONT}; }}
  .lhv {{ fill:var(--hv); font:600 11.5px {FONT}; }}
  .wire {{ fill:none; stroke:var(--ink); stroke-width:1.3; }}
  .sig {{ fill:none; stroke:var(--sig); stroke-width:2.2; stroke-linejoin:round; }}
  .ctl {{ fill:none; stroke:var(--ctl); stroke-width:1.6; stroke-dasharray:6 4; stroke-linejoin:round; }}
  .man {{ fill:none; stroke:var(--man); stroke-width:3; stroke-linejoin:round; }}
  .gang {{ fill:none; stroke:var(--man); stroke-width:1.6; stroke-dasharray:3 3; stroke-linejoin:round; }}
  .hv {{ fill:none; stroke:var(--hv); stroke-width:2.5; stroke-linejoin:round; }}
  .gnd {{ fill:none; stroke:var(--ink2); stroke-width:1.5; }}
  .lever-man {{ stroke:var(--man); stroke-width:2.2; }}
  .lever-ctl {{ stroke:var(--ctl); stroke-width:2.2; }}
  .term {{ fill:var(--box); stroke:var(--ink); stroke-width:1.3; }}
  .jack {{ fill:var(--box); stroke:var(--ink); stroke-width:1.5; }}
  .part {{ fill:var(--box); stroke:var(--ink); stroke-width:1.3; }}
  .plate {{ stroke:var(--ink); stroke-width:2.2; }}
  .node {{ fill:var(--ink); }}
  .cap0 {{ fill:var(--man); }}
  .hsig {{ fill:var(--sig); }} .hctl {{ fill:var(--ctl); }} .hman {{ fill:var(--man); }}
  .dot {{ fill:var(--ctl); stroke:var(--box); stroke-width:1.5; }}
</style>
<defs>
""" + "".join(
    f'  <marker id="a{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="10" markerHeight="10" '
    f'markerUnits="userSpaceOnUse" orient="auto-start-reverse"><path class="h{k}" d="M0,0 L10,5 L0,10 z"/></marker>\n'
    for k in ("sig", "ctl", "man")
) + "</defs>\n"


class Svg:
    def __init__(self, w, h, title, shift=0):
        """shift moves the whole drawing down, so a layout can use negative y for a frame around it."""
        self.w, self.h, self.items = w, h, []
        self.title, self.shift = title, shift

    def add(self, s):
        self.items.append(s)

    def box(self, x, y, w, h, title, sub=None, cls="box", ctl=False):
        self.add(f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="6"/>')
        cx = x + w / 2
        if sub:
            lines = sub if isinstance(sub, list) else [sub]
            ty = y + h / 2 - 3 - 8 * (len(lines) - 1)
            self.add(f'<text class="t" x="{cx}" y="{ty}" text-anchor="middle">{title}</text>')
            for i, line in enumerate(lines):
                self.add(f'<text class="s" x="{cx}" y="{ty + 17 + 15 * i}" text-anchor="middle">{line}</text>')
        else:
            self.add(f'<text class="t" x="{cx}" y="{y + h / 2 + 4.5}" text-anchor="middle">{title}</text>')
        if ctl:
            self.add(f'<circle class="dot" cx="{x + w}" cy="{y}" r="5"/>')

    def text(self, x, y, s, cls="s", anchor="start"):
        self.add(f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}">{s}</text>')

    def line(self, pts, kind="sig", arrow=True, start_arrow=False):
        d = " ".join(f"{x},{y}" for x, y in pts)
        a = (f' marker-end="url(#a{kind})"' if arrow else "") + (f' marker-start="url(#a{kind})"' if start_arrow else "")
        self.add(f'<polyline class="{kind}" points="{d}"{a}/>')

    def wire(self, pts):
        self.line(pts, "wire", arrow=False)

    # Schematic symbols, all horizontal (left terminal at x) unless noted
    def switch(self, x, y, kind="man"):
        """Open SPST from x to x+34."""
        self.add(f'<line class="lever-{kind}" x1="{x + 4.5}" y1="{y}" x2="{x + 30}" y2="{y - 11}"/>')
        self.add(f'<circle class="term" cx="{x + 2.5}" cy="{y}" r="2.5"/>')
        self.add(f'<circle class="term" cx="{x + 32}" cy="{y}" r="2.5"/>')

    def switch_closed_v(self, x, y):
        """Closed SPST, vertical, from y to y+30."""
        self.add(f'<line class="lever-man" x1="{x}" y1="{y + 2.5}" x2="{x}" y2="{y + 27.5}"/>')
        self.add(f'<circle class="term" cx="{x}" cy="{y + 2.5}" r="2.5"/>')
        self.add(f'<circle class="term" cx="{x}" cy="{y + 27.5}" r="2.5"/>')

    def resistor(self, x, y, w=60):
        self.add(f'<rect class="part" x="{x}" y="{y - 6}" width="{w}" height="12"/>')

    def capacitor(self, x, y):
        """Plates at x and x+8."""
        for px in (x, x + 8):
            self.add(f'<line class="plate" x1="{px}" y1="{y - 9}" x2="{px}" y2="{y + 9}"/>')

    def ground(self, x, y):
        for i, half in enumerate((12, 8, 4)):
            yy = y + 5 * i
            self.add(f'<line class="gnd" x1="{x - half}" y1="{yy}" x2="{x + half}" y2="{yy}"/>')

    def node(self, x, y, r=4):
        self.add(f'<circle class="node" cx="{x}" cy="{y}" r="{r}"/>')

    def write(self, name):
        body = "\n".join(self.items)
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
               f'width="{self.w}" height="{self.h}" role="img" aria-label="{self.title}">\n'
               f'<title>{self.title}</title>\n{STYLE}\n'
               f'<rect class="bg" x="0" y="0" width="{self.w}" height="{self.h}" rx="10"/>\n'
               f'<g transform="translate(0,{self.shift})">\n{body}\n</g>\n</svg>\n')
        (HERE / name).write_text(svg)


def switching_concept():
    d = Svg(1200, 940, "Electrometer concept: the chamber, detector board and electrometer sit in a grounded tin; one "
                       "probe cable is moved by hand between the per-channel switch connectors; range elements stay at "
                       "the summing node in the head; HV supply and radio antenna are outside the tin", shift=70)

    # ---- The tin, then panels, so wires and labels draw on top of their fills ----
    d.add('<rect class="encl" x="8" y="-28" width="1184" height="588" rx="12"/>')
    d.text(24, -10, "COOKIE TIN: GROUNDED, LIGHT-TIGHT. TIN, COAX SHIELDS AND ELECTROMETER COMMON BONDED TO THE "
                    "DETECTOR BOARD 0 V AT ONE POINT", "g")
    d.add('<rect class="group" x="20" y="20" width="330" height="520" rx="10"/>')
    d.add('<rect class="group" x="375" y="20" width="470" height="370" rx="10"/>')
    d.add('<rect class="group" x="870" y="20" width="310" height="370" rx="10"/>')

    # ---- Chamber end ----
    d.text(36, 44, "CHAMBER END", "g")
    d.box(50, 70, 290, 50, "Chamber tube, +1 kV", "photodiodes face into it", cls="hvbox")
    d.box(50, 140, 290, 370, "", cls="box")
    d.text(195, 162, "Detector board (≤ 20 mm), back side", "t", "middle")

    # One channel in detail: the probe is on IN2's switch connector
    d.box(62, 250, 50, 30, "PD2")
    d.wire([(112, 265), (150, 265)])
    d.node(131, 265, 3)
    d.add('<rect class="part" x="150" y="245" width="55" height="40" rx="3"/>')
    d.text(177, 270, "SWF", "k", "middle")
    d.text(177, 236, "switch connector", "s", "middle")
    d.wire([(177, 285), (177, 310)])
    d.box(137, 310, 80, 30, "CSA2")
    d.text(224, 330, "idles at 0 V", "s")
    d.line([(205, 265), (395, 265)], "man", arrow=False)
    d.text(214, 257, "probe → SMA coax", "lman")
    d.box(62, 365, 268, 45, "IN1, IN3, IN4", "connector unmated: node stays on its CSA")
    d.box(62, 430, 268, 60, "PicoBlade", "PD bias, ring, TEST, ±4.5 V, GND")

    # Source into the ring (or PD bias) through the PicoBlade breakout
    d.line([(420, 460), (332, 460)], "man")
    d.text(376, 452, "source", "lman", "middle")

    # Filtered pass-through to the outside
    d.wire([(270, 490), (270, 600)])
    d.add('<rect class="part" x="263" y="552" width="14" height="16" rx="2"/>')
    d.text(282, 590, "filtered pass-through: MCU board, PD bias", "s")

    # External HV, outside the tin
    d.line([(35, 600), (35, 95), (50, 95)], "hv", arrow=False)
    d.add('<rect class="hvbox" x="27" y="552" width="16" height="16" rx="2"/>')
    d.text(48, 585, "HV feedthrough, lid interlock", "lhv")
    d.box(20, 600, 160, 50, "External HV", "≤ 1.1 kV, HV board", cls="hvbox")

    # ---- Electrometer head ----
    d.text(590, 44, "ELECTROMETER HEAD (SHIELDED)", "g")
    d.text(590, 62, "feedback network at the summing node;")
    d.text(590, 77, "values are examples, set in phase 2")

    d.box(395, 245, 75, 40, "", cls="box")
    d.text(432, 262, "input", "k", "middle")
    d.text(432, 277, "protection", "k", "middle")
    d.text(470, 310, "summing node: mm long,", "s", "middle")
    d.text(470, 325, "PTFE or air, guarded", "s", "middle")

    d.wire([(470, 265), (595, 265)])
    d.wire([(530, 130), (530, 265)])
    d.wire([(770, 130), (770, 280)])
    d.node(530, 265)

    # Range branches (manual switches)
    for y, value, fs in ((130, "10 MΩ", "1 µA FS"), (165, "1 GΩ", "10 nA FS")):
        d.wire([(530, y), (545, y)])
        d.switch(545, y, "man")
        d.wire([(579, y), (640, y)])
        d.resistor(640, y)
        d.wire([(700, y), (770, y)])
        d.text(670, y - 10, value, "k", "middle")
        d.text(735, y - 6, fs, "s", "middle")

    # Integrator capacitor, always in
    d.wire([(530, 200), (666, 200)])
    d.capacitor(666, 200)
    d.wire([(674, 200), (770, 200)])
    d.text(670, 186, "10 pF, always in", "k", "middle")

    # Reset switch (MCU)
    d.wire([(530, 232), (545, 232)])
    d.switch(545, 232, "ctl")
    d.wire([(579, 232), (770, 232)])

    # Op-amp
    d.add('<polygon class="part" points="595,250 595,310 665,280"/>')
    d.text(601, 270, "−", "k")
    d.text(601, 300, "+", "k")
    d.add('<polyline class="gnd" points="595,295 575,295 575,335"/>')
    d.ground(575, 335)
    d.text(575, 364, "0 V (guard)", "s", "middle")
    d.text(675, 305, "ADA4530-1 (candidate)", "s")
    d.wire([(665, 280), (770, 280)])

    # Vout to the ADC
    d.line([(770, 280), (888, 280)], "sig")
    d.text(815, 272, "Vout", "lsig", "middle")

    # Range-switch gang and position readback
    d.line([(562, 160), (562, 30), (856, 30), (856, 180), (1028, 180)], "gang", arrow=False)
    d.line([(1010, 180), (1028, 180)], "man")
    d.text(945, 172, "range position", "lman", "middle")

    # Reset control
    d.line([(1030, 216), (584, 216)], "ctl")
    d.text(945, 208, "reset", "lctl", "middle")

    # ---- Control ----
    d.text(886, 44, "CONTROL (ESP32)", "g")
    # Radio: the tin blocks 2.4 GHz, so the antenna sits outside on a bulkhead
    d.line([(1095, 140), (1095, -64)], "ctl", arrow=False)
    d.add('<rect class="part" x="1088" y="-35" width="14" height="14" rx="2"/>')
    d.add('<polyline class="wire" points="1081,-62 1095,-48 1109,-62"/>')
    d.text(1075, -50, "antenna outside the tin", "lctl", "end")
    d.text(1075, -36, "ESP-NOW → lab-gateway → script", "lctl", "end")

    d.box(890, 260, 95, 40, "24-bit ADC")
    d.line([(985, 280), (1028, 280)], "sig")
    d.box(1030, 140, 130, 170, "MCU", ["auto-ranges by", "integration time"])

    # Source, set by the MCU
    d.line([(1095, 310), (1095, 460), (642, 460)], "ctl")
    d.text(870, 452, "level, polarity, slew", "lctl", "middle")
    d.box(420, 435, 220, 50, "±50 V source", "DAC + HV amp, ≤ 100 µA", ctl=True)

    # ---- Inset: T-switch (below the tin) ----
    d.add('<g transform="translate(0,80)">')
    d.box(680, 520, 500, 262, "", cls="group")
    d.text(696, 544, "DETAIL: ONE RANGE BRANCH, SWITCHED OFF (T-SWITCH)", "g")

    d.node(720, 620)
    d.text(720, 646, "summing", "k", "middle")
    d.text(720, 661, "node ≈ 0 V", "k", "middle")
    d.wire([(724, 620), (745, 620)])
    d.switch(745, 620, "man")
    d.text(762, 598, "Sa", "lman", "middle")
    d.wire([(779, 620), (845, 620)])
    d.node(820, 620, 3.5)
    d.switch(845, 620, "man")
    d.text(862, 598, "Sb", "lman", "middle")
    d.wire([(879, 620), (905, 620)])
    d.resistor(905, 620, 55)
    d.text(932, 606, "R or C", "k", "middle")
    d.wire([(960, 620), (1010, 620)])
    d.node(1010, 620)
    d.text(1010, 646, "Vout", "k", "middle")
    d.text(1010, 661, "up to ±10 V", "k", "middle")

    d.wire([(820, 620), (820, 640)])
    d.switch_closed_v(820, 640)
    d.add('<line class="gnd" x1="820" y1="670" x2="820" y2="684"/>')
    d.ground(820, 684)
    d.text(840, 690, "Sc closed: midpoint held at 0 V", "lman")

    for i, s in enumerate(("Sa has ≈ 0 V across it, so it leaks nothing into the input.",
                           "Sb sees Vout, but its leakage goes to 0 V through Sc.",
                           "One DPDT toggle per branch (or one rotary wafer) does this.",
                           "The MCU's reset switch across the 10 pF needs the same trick.")):
        d.text(696, 718 + 18 * i, s, "k")
    d.add('</g>')

    # ---- Key ----
    d.text(32, 684, "KEY", "g")
    d.line([(32, 702), (62, 702)], "man", arrow=False)
    d.text(72, 706, "set by hand: probe cable, source lead, range switch", "k")
    d.line([(32, 722), (62, 722)], "ctl", arrow=False)
    d.text(72, 726, "set by the MCU (logic, radio)", "k")
    d.line([(32, 742), (62, 742)], "gang", arrow=False)
    d.text(72, 746, "switch gang + position readback to the MCU", "k")
    d.line([(32, 762), (62, 762)], "sig", arrow=False)
    d.text(72, 766, "analog signal", "k")
    d.line([(32, 782), (62, 782)], "hv", arrow=False)
    d.text(72, 786, "HV from outside the tin, interlocked", "k")

    d.write("switching-concept.svg")


if __name__ == "__main__":
    switching_concept()
