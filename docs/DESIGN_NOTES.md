# Design notes

## Origin
The mount started as a cardboard prototype built directly on the car, 3D-scanned, and turned into a
printable part (V1–V4, 35° deck). V4 was printed and installed; its lower half (side walls, USB‑C
window, screw-head notches, battery arches, DC-plug window, rear fins) is treated as verified and is
reused unchanged by every later version — later versions are built by importing `FableV4_OnePiece.stl`
into Blender and cutting/adding geometry (`reference/scripts/build_v8.py`, earlier `build_v6.py` / `build_v7.py`).

## Why 90°
With the phone lying at 35° its rear camera points at the ceiling. For the camera to look forward the
phone must stand upright. V6–V8 are fixed at 90°; V5 explored 100° with three tread positions but was
dropped to keep the part simpler and lighter.

## V7 → V8 (what the printed V7 taught)
V7 was printed and fits (slot, USB‑C, battery, wiring). On the car three things stood out:
1. The tower stood ~3 cm behind the mast, so the phone's mass sat over the rear axle. That gap was never a
   keep-out — V7 only needed it as run-up length for its front gussets. V8 moves the whole phone assembly
   25 mm forward so the plate merges with the mast. The geometric limit is 27 mm (plate front face on the
   mast front face); 25 mm leaves a deliberate 2 mm margin for the real wire loop and print tolerance.
2. ~5 mm of dead gap between the battery box and the rear fin comb. V8 moves the rear foot 4 mm toward the box
   (≈1 mm clearance kept; the measurement was a ruler reading).
3. The rail / plate outer faces had spare width. V8 takes 1 mm (rail 3.5 → 2.5 mm). The 2 mm the photos suggested
   would leave a 1.5 mm rail, so strength won. The slot's inner fit dimensions are untouched.

## Key dimensions (Z = 0 at the upper plate top, Y+ = car front)
| Feature | V8 | V7 |
|---|---|---|
| Side walls | X ±36.3 … ±39.5 (3.2 mm), Y −88 … +46 | Y −92 … +46 |
| Battery bay | Y −72.5 … −28, roof Z 22.5 (right) / gable to 35.5 (left, includes DC plug zone to Y −2) | Y −76.5 … −28 |
| USB‑C window (left wall) | Y 10 … 42, Z 11 … 25 | same |
| Screw-head notches | Y 7 … 22, Z 0 … 7.5, both walls | same |
| Mast (transverse wall) | Y −19.9 … −17.6, Z 32 … 65, wire arch 30 mm bridge at Z 54 with 45° haunches | same |
| Tower plate | Y −23 … −19.6, merged with the mast; arch springs Z 37 at the walls, 30 mm bridge Z 58.2 (backed by the mast top), plate Z 60 … 150, X ±43.25; pentagon window X ±22, Z 66 … 138 | Y −48 … −44.6, free-standing, X ±44.25 |
| Phone slot | width 81.5, depth 18.5, lips at X ±36.25, phone bottom Z 54, slot Y −41.5 … −23 | slot Y −66.5 … −48 |
| Bottom groove | Y −37 … −23 (14 mm), pads X 25.5 … 40.75 each side; lips Y −41.5 … −44 | Y −62 … −48; lips −66.5 … −69 |
| Rails | X ±40.75 … ±43.25 (2.5 mm), Y −44 … −23, Z 54 … 150 | X ±40.75 … ±44.25 (3.5 mm) |
| Front gussets | none | Y −45.6 … −26 on the bay walls, apex Z 118 |
| Rear gussets | X ±36.2 … ±39.6 behind the lips, Y −44 … −63, apex Z 105 | Y −69 … −88 |
| Tail | 45° from (Y −44, Z 60) to (Y −69, Z 35), flat Z 35 to Y −88 | 45° from (−69, 60) to (−100, 29) |
| Rear foot | 4 fins × 2.4 mm at X ±13, ±26, Y −87.7 … −72.5, Z 0 … 30; tie band Y −88 … −85 (Z 18 … 30) + centre wedge; 2 mm pad Y −87.6 … −72.6 | Y −91.7 … −76.5; band at −92 |
| Volume / mass | 89.2 cm³ / ~111 g PLA | 104.3 cm³ / ~129 g |
| Part COM (Y) | −26.8; with a 200 g phone −28.2 | −41.6; with phone −49.2 |

## Load path (V8)
Phone → plate → mast + arched bulkhead (one 5.4 mm wall Y −23 … −17.6 from Z 37 to 65, tied into both side walls)
→ walls → feet. Rails + plate form a C channel rooted in the tray flares on the walls; the rear gussets behind the
lips stop the rails bending fore/aft and outward. There are no front gussets: in front of the plate is the 2 mm
wire margin and then the keep-out. Transverse ties: mast/plate bulkhead (front-middle), tie band + fins (rear).

## Clearances that must stay
All of these are proven by boolean intersection = 0 in `build_v8.py`, and re-checked on both the V7 and V8 STLs by
`verify_v7_v8.py`.
- Nothing inside X ±36, Z < 31 over the battery bay (Y −72.45 … −28): the box slides out sideways. The bay is now
  44.5 mm long; the box measured ~43.5 (5 mm gap behind it in V7), so ~1 mm remains. Do not shorten further.
- Left wall Y −22 … −2 open below Z 25 for the DC plug; USB‑C window and screw notches untouched.
- **Wire keep-out (learned the hard way with V6):** the Dupont bundle from the board headers loops up
  to ~Z 100–110 and forward to the ultrasonic module, entirely INSIDE the chamber in front of the mast.
  Nothing may occupy X ±36.25 / Y > −17.55 / Z > 40, nothing above Z 65 in front of the mast, and
  nothing beyond Y 46 (front module). **V8 adds a 2 mm margin: nothing above Z 65 in front of Y −19.55 either.**
  The structure must live behind that plane; the V7 gap behind the mast was never a keep-out.
- The mast's wire arch (30 mm bridge at Z 54, 45° haunches) must stay open through the merged bulkhead; the plate's
  arch opening is larger than the mast's, so the mast governs.
- Phone camera bar (top ~55 mm of the phone) must not be covered — tower top is at Z 150 = 96 mm above the phone bottom.

## Slot detail worth knowing
In the 4.5 mm chamfer zone between the groove and the lips (Y −41.5 … −37) the side walls stand at full height
(Z 65) inside the phone width on both sides. V7 had the same stub on the right (window fill to Z 64.5) and a lower
one on the left; the phone's screen plane is 2 mm in front of it, so the back-tilt play near the floor is 2 mm
instead of the 6.5 mm at the lips — exactly as on the printed V7.
