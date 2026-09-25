# ACEBOTT QD001 Phone Camera Mount

3D-printable, one-piece phone mount for the ACEBOTT QD001 mecanum-wheel robot car.
The phone stands upright (90°) above the battery box so its **rear camera works as the
car's forward-looking camera**; the screen faces the rear of the car.

Designed for a **Bambu Lab A1 mini**, printed upright with **no supports**.

![V8 rear view with phone](docs/renders/v8/4_top34_rear.jpg)

## Files

| Path | What it is |
|---|---|
| `models/current/ACEBOTT_QD001_PhoneMount_V8_90deg_OnePiece.stl` | **Print this next.** V8: the V7 tower moved 25 mm toward the car centre, rear foot pulled 4 mm in, rails slimmed 1 mm. 89.2 cm³, 91 × 134 × 150 mm. **Not yet printed** |
| `models/current/spoiler_v10_fable_v8.blend` | Blender source of V8 (object `V8_Body`) |
| `models/current/ACEBOTT_QD001_PhoneMount_V7_90deg_OnePiece.stl` | V7: printed and installed, fit verified on the car. Kept unchanged as the fallback until V8 is printed. 104.3 cm³, 91 × 138 × 150 mm |
| `models/current/spoiler_v9_fable_v7.blend` | Blender source of V7 (object `V7_Body`) |
| `models/legacy/ACEBOTT_QD001_PhoneMount_V6_…_DO-NOT-PRINT.stl` | V6 — tower stood on the mast and blocked the wire bundle. Kept for reference only |
| `models/legacy/FableV4_OnePiece.stl` | V4 — 35° "spoiler" version. Printed and installed; its lower half is the verified base that every later version is built on |
| `models/legacy/spoiler_v7_fable_v5_stepped-angle-concept.blend` | V5 concept: 100° tower with a 3-step (90/95/100°) tread floor. Superseded by V6 |
| `docs/DESIGN_NOTES.md` | Geometry, constraints, load path, what was verified on the real car |
| `docs/PRINTING.md` | Slicer settings, orientation, risk notes |
| `docs/images/` | Photos of V4 on the car and the annotated side view used to plan V6 |
| `docs/renders/` | Blender renders of V8 (`v8/compare/` = V7 and V8 from identical cameras), V7, V6 and the V5 concept |
| `reference/scripts/` | Python used in Blender to build/check/export the parts (`build_v8.py` reproduces V8 from the V4 STL; `verify_v7_v8.py`, `render_v8.py`, `stitch_v7_v8.py` produce the V7-vs-V8 checks and renders) |
| `reference/photos/` | Full-size photos of V4 installed |

## Phone

Sized for a Pixel with a case: slot **81.5 mm** wide, **18.5 mm** deep, phone bottom ~54 mm above
the upper chassis plate. V8 keeps the V7 slot geometry exactly (verified fit); only its position changed.
The top ~55 mm of the phone (camera bar) is left completely free.
USB‑C cable exits downward through the open centre of the floor.

## Status

- V4: printed, installed, verified fit (USB‑C window, screw notches, battery bay, wiring).
- V6: never printed — its tower sat inside the wire-bundle space in front of the mast (see `docs/DESIGN_NOTES.md`, "Wire keep-out").
- V7: printed and installed (2026‑09‑25). Fit verified: phone slot, USB‑C, battery bay, wire loop in front of the mast.
  Found on the car: the phone hangs ~3 cm behind the mast (mass over the rear axle), a ~5 mm dead gap between the
  battery box and the rear foot, and spare width on the rail / plate outer faces.
- V8: tower moved 25 mm forward (plate front face 2 mm behind the mast plane; every keep-out re-proven by boolean
  intersection = 0 on both the V7 and V8 STLs), rear foot 4 mm forward, rails 2.5 mm. Verified in software only
  (watertight, no islands, V4 bridges only). **Not yet printed.**

## License

MIT — see `LICENSE`.
