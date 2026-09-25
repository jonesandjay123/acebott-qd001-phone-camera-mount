# Printing (Bambu Lab A1 mini)

- File: `models/current/ACEBOTT_QD001_PhoneMount_V8_90deg_OnePiece.stl` (V7 STL kept next to it as the printed fallback)
- Orientation: as exported — flat base on the bed, tower up. Do **not** rotate. Height 150 mm.
- Supports: **off**. Every overhang is ≤ 45° or a bridge that already printed fine on V4
  (42 mm battery-bay roof, 41 mm left gable, 34 mm mast arch, 32 mm USB‑C window, 23 mm tie band). The tower's
  30 mm arch bridge at Z 58 (printed fine on V7) is now attached along its front edge to the solid top of the mast.
- Brim: 5 mm recommended (tall part, bed-slinger).
- Layer height: 0.28 mm "Extra Draft"-type profile is fine; 0.2 mm for nicer phone-contact faces.
- Walls: 3 perimeters. Most walls are 3.2–3.4 mm and print nearly solid; the rails are 2.5 mm (V7: 3.5); infill setting barely matters.
- Material: PLA/PLA+ or PETG. ~110 g PLA (89 cm³). Time roughly 0.85× the V7 print.

## What to check after printing
1. Wire bundle loops freely in front of the mast; the plate front face is 2 mm behind the mast plane, nothing touches the loop.
2. Phone slides in from the top and sits on the two floor pads; USB‑C plug fits through the centre gap (slot is the V7 one, moved 25 mm forward).
3. Battery still slides out sideways under the arches; about 1 mm gap between the box and the rear fin comb (V7: ~5 mm).
4. DC plug / cable pass through the left-side window.
5. If the phone rattles at the lips (6.5 mm play at 90°), add a 1–2 mm felt/foam strip on the plate,
   or ask for a 2–3° rearward-lean variant.

## Design rules used (keep them for future edits)
- One piece, no sacrificial posts, no long free-standing columns.
- A continuous grounded footprint first; structure branches upward from existing walls.
- New overhangs only as 45° haunches/flares or gable tops — no new flat bridges.
- Verify with the voxel island check in `reference/scripts/lib_v5.py` (`printcheck`) before exporting.
