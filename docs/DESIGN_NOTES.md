# Design notes

## Origin
The mount started as a cardboard prototype built directly on the car, 3D-scanned, and turned into a
printable part (V1–V4, 35° deck). V4 was printed and installed; its lower half (side walls, USB‑C
window, screw-head notches, battery arches, DC-plug window, rear fins) is treated as verified and is
reused unchanged by every later version — later versions are built by importing `FableV4_OnePiece.stl`
into Blender and cutting/adding geometry (`reference/scripts/build_v6.py`).

## Why 90°
With the phone lying at 35° its rear camera points at the ceiling. For the camera to look forward the
phone must stand upright. V6 is fixed at 90°; V5 explored 100° with three tread positions but was
dropped to keep the part simpler and lighter.

## Key dimensions (Z = 0 at the upper plate top)
| Feature | Value |
|---|---|
| Side walls | X ±36.3 … ±39.5 (3.2 mm), Y −92 … +51 |
| Battery bay | Y −76 … −28, roof Z 22.5 (right) / gable to 35.5 (left, includes DC plug zone to Y −2) |
| USB‑C window (left wall) | Y 10 … 42, Z 11 … 25 |
| Screw-head notches | Y 7 … 22, Z 0 … 7.5, both walls |
| Mast (transverse wall) | Y −20 … −17.6, Z 32 … 65, wire arch Z 32 … 54, 34 mm wide |
| Tower plate (V7) | Y −48 … −44.6, arched bottom (springs Z 37 at the walls, 30 mm bridge at Z 58.2), plate Z 60 … 150, X ±44.25; pentagon window X ±22, Z 66 … 138 |
| Phone slot | width 81.5, depth 18.5, lips at X ±36.25, phone bottom Z 54 |
| Bottom groove | Y −62 … −48 (14 mm), pads X 25.5 … 40.75 each side; lips Y −66.5 … −69 |
| Front gussets | X ±36.2 … ±39.6 on the bay walls, Y −45.6 … −26, apex Z 118 (behind the mast) |
| Rear gussets | same walls behind the lips, Y −69 … −88, apex Z 105 |
| Rear fins | 5 × 2.4 mm at X 0, ±13, ±26, Y −92 … −76.5, Z 0 … 30, on a 2 mm pad, tied by the band at Y −92 |

## Load path
Phone → arched tower plate (vertical, in-plane stiff sideways; its arch ties the two bay walls)
→ front gussets on the bay walls (in-plane stiff fore/aft) → walls → feet. Rails + plate form a C
channel; rear gussets behind the lips stop the rails bending outward. Transverse ties: mast (front),
arched tower plate (middle), tie band + fins (rear).

## Clearances that must stay
- Nothing inside X ±36, Z < 31 over the battery (battery slides out sideways).
- Left wall Y −22 … −2 open below Z 25 for the DC plug.
- **Wire keep-out (learned the hard way with V6):** the Dupont bundle from the board headers loops up
  to ~Z 100–110 and forward to the ultrasonic module, entirely INSIDE the chamber in front of the mast.
  Nothing may occupy X ±36.25 / Y > −17.55 / Z > 40, nothing above Z 65 in front of the mast, and
  nothing beyond Y 46 (front module). `build_v7.py` proves this with boolean intersections = 0.
  The chamber could shrink ~10 mm per side if ever needed, but the structure must live behind the mast.
- Phone camera bar (top ~55 mm of the phone) must not be covered — tower top is at Z 150 = 96 mm above the phone bottom.
