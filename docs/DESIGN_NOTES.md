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
| Mast (transverse wall) | Y −20 … −17.6, wire arch Z 32 … 54, 34 mm wide |
| Tower plate | Y −20.9 … −17.5, Z 54 … 150, X ±44.25; pentagon window X ±22, Z 66 … 138 |
| Phone slot | width 81.5, depth 18.5, lips at X ±36.25, phone bottom Z 54 |
| Bottom groove | Y −34.9 … −20.9 (14 mm), pads X 25.5 … 40.75 each side |
| Gussets | X ±36.2 … ±39.6, from wall top (Z 64, Y +10) to plate at Z 125 |
| Rear fins | 5 × 2.4 mm at X 0, ±13, ±26, Y −92 … −76.5, Z 0 … 30, on a 2 mm pad, tied by the band at Y −92 |

## Load path
Phone → tower plate (vertical, in-plane stiff sideways) → two front gussets (in-plane stiff fore/aft)
→ front side walls → feet. The tower's rear side rests on the side trays, which sit on the battery-bay
walls via 45° haunches. Transverse ties: mast (front), tower plate (middle), tie band + fins (rear).

## Clearances that must stay
- Nothing inside X ±36, Z < 31 over the battery (battery slides out sideways).
- Left wall Y −22 … −2 open below Z 25 for the DC plug.
- Board/wiring area (Y −18 … +36) open above the walls; wires loop up to ~Z 100 in front of the mast.
- Phone camera bar (top ~55 mm of the phone) must not be covered — tower top is at Z 150 = 96 mm above the phone bottom.
