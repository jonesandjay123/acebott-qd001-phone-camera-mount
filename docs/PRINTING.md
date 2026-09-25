# Printing (Bambu Lab A1 mini)

- File: `models/current/ACEBOTT_QD001_PhoneMount_V7_90deg_OnePiece.stl`
- Orientation: as exported — flat base on the bed, tower up. Do **not** rotate. Height 150 mm.
- Supports: **off**. Every overhang is ≤ 45° or a bridge that already printed fine on V4
  (42 mm battery-bay roof, 41 mm left gable, 34 mm mast arch, 32 mm USB‑C window, 23 mm tie band) plus the tower's 30 mm arch bridge at Z 58.
- Brim: 5 mm recommended (tall part, bed-slinger).
- Layer height: 0.28 mm "Extra Draft"-type profile is fine; 0.2 mm for nicer phone-contact faces.
- Walls: 3 perimeters. Most walls are 3.2–3.5 mm and print nearly solid; infill setting barely matters.
- Material: PLA/PLA+ or PETG. ~120 g PLA estimated. Time roughly 3–4.5 h at 0.28 mm (about 0.7× the V4 print).

## What to check after printing
1. Wire bundle loops freely in front of the mast; nothing touches it.
2. Phone slides in from the top and sits on the two floor pads; USB‑C plug fits through the centre gap.
3. Battery still slides out sideways under the arches.
4. DC plug / cable pass through the left-side window.
5. If the phone rattles at the lips (6.5 mm play at 90°), add a 1–2 mm felt/foam strip on the plate,
   or ask for a 2–3° rearward-lean variant.

## Design rules used (keep them for future edits)
- One piece, no sacrificial posts, no long free-standing columns.
- A continuous grounded footprint first; structure branches upward from existing walls.
- New overhangs only as 45° haunches/flares or gable tops — no new flat bridges.
- Verify with the voxel island check in `reference/scripts/lib_v5.py` (`printcheck`) before exporting.
