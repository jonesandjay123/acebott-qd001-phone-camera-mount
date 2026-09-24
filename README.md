# ACEBOTT QD001 Phone Camera Mount

3D-printable, one-piece phone mount for the ACEBOTT QD001 mecanum-wheel robot car.
The phone stands upright (90°) above the battery box so its **rear camera works as the
car's forward-looking camera**; the screen faces the rear of the car.

Designed for a **Bambu Lab A1 mini**, printed upright with **no supports**.

![V6 rear view with phone](docs/renders/v6/4_top34_rear.jpg)

## Files

| Path | What it is |
|---|---|
| `models/current/ACEBOTT_QD001_PhoneMount_V6_90deg_OnePiece.stl` | **Print this.** V6, fixed 90°, one piece, 93.4 cm³, 91 × 143 × 150 mm |
| `models/current/spoiler_v8_fable_v6.blend` | Blender source of V6 (object `V6_Body`; V5 concept kept in hidden collections) |
| `models/legacy/FableV4_OnePiece.stl` | V4 — 35° "spoiler" version. Printed and installed; its lower half is the verified base that V6 is built on |
| `models/legacy/spoiler_v7_fable_v5_stepped-angle-concept.blend` | V5 concept: 100° tower with a 3-step (90/95/100°) tread floor. Superseded by V6 |
| `docs/DESIGN_NOTES.md` | Geometry, constraints, load path, what was verified on the real car |
| `docs/PRINTING.md` | Slicer settings, orientation, risk notes |
| `docs/images/` | Photos of V4 on the car and the annotated side view used to plan V6 |
| `docs/renders/` | Blender renders of V6 and of the V5 concept |
| `reference/scripts/` | Python used in Blender to build/check/export the parts (`build_v6.py` reproduces V6 from the V4 STL) |
| `reference/photos/` | Full-size photos of V4 installed |

## Phone

Sized for a Pixel with a case: slot **81.5 mm** wide, **18.5 mm** deep, phone bottom ~54 mm above
the upper chassis plate. The top ~55 mm of the phone (camera bar) is left completely free.
USB‑C cable exits downward through the open centre of the floor.

## Status

- V4: printed, installed, verified fit (USB‑C window, screw notches, battery bay, wiring).
- V6: geometry verified in software only (watertight, no islands, all bridges identical to V4). **Not yet printed** — see `CHANGELOG.md`.

## License

MIT — see `LICENSE`.
