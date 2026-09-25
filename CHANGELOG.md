# Changelog

Coordinate frame used everywhere: X right, Y toward the car front, Z up, Z = 0 at the top of the
upper chassis plate (same as the STL files).

## V8 — 2026-09-25 (current, not yet printed)
Feedback from the printed V7 on the car: the phone sits ~3 cm behind the mast (mass over the rear axle), there is a
~5 mm dead gap between the battery box and the rear foot, and the rail / plate outer faces have spare width.
- Tower moved 25 mm toward the car centre: plate Y −23 … −19.6 (was −48 … −44.6). The plate now merges with the V4
  mast (Y −19.9 … −17.6) into one bulkhead from Z 37 to 150. Its front face stays 2.0 mm behind the mast front face
  (wire margin chosen by the user; the geometric limit would have been 27 mm).
- Slot fit unchanged: 81.5 × 18.5, lips ±36.25, 2.5 mm lips, 45° chamfer, 14 mm groove, pads. Slot Y −41.5 … −23,
  lips −44 … −41.5, groove −37 … −23, phone bottom Z 54.
- Front gussets removed (in front of the plate is the wire margin, then the keep-out). Root = mast + arch + both bay
  walls. Rear gussets shifted with the tower (Y −44 … −63, apex Z 105).
- Rails / plate slimmed 1 mm: outer face X ±43.25 (was ±44.25), rail 2.5 mm (was 3.5). Not the 2 mm the photos allowed:
  2 mm would leave a 1.5 mm rail. Tray haunch / flare logic unchanged.
- Rear foot (fins, tie band, centre wedge, pad, wall ends) moved 4 mm toward the battery box as one rigid block: fin
  fronts Y −72.5 (was −76.5), part ends at Y −88 (was −92). Measured gap was ~5 mm; 4 mm keeps ~1 mm of clearance.
- Tail: 45° from (Y −44, Z 60) down to Z 35, then flat at Z 35 to the rear end.
- Keep-out proof, all intersect volumes 0 on both the V7 and V8 STLs (`verify_v7_v8.py`): wire chamber, above-mast,
  2 mm wire margin (Y > −19.55, Z > 65), front module, battery bay (X ±36 / Y −72.45 … −28 / Z < 31), mast wire arch,
  DC-plug window, USB‑C window, screw notches, nothing above Z 150.
- 89.2 cm³ (V7 104.3, −14 %). Part COM Y −26.8 (V7 −41.6); with a 200 g phone −28.2 (V7 −49.2). Islands 0, bridges =
  V4 only (the tower's 30 mm arch bridge is now backed along its front edge by the solid top of the mast), bed contact
  2013 mm².
- Scripts: `build_v8.py`, `verify_v7_v8.py`, `render_v8.py`, `stitch_v7_v8.py`. `lib_v5.printcheck` gained an optional
  `eps` grid offset so voxel centres do not sit exactly on the z22.5 / z35.5 / z7.5 faces (they read as phantom
  1-voxel islands); default 0 keeps the old behaviour.

## V7 — 2026-09-24 (printed 2026-09-25, superseded by V8)
- V6 was blocked before printing: on the car the wire bundle from the board headers loops up and forward inside the chamber in front of the mast; V6's tower plate (Y −20.9) and its gussets on the front wall tops sat inside it.
- Tower moved behind the mast: arched bulkhead at Y −48 … −44.6 (45° haunches from Z 37 to a 30 mm bridge at Z 58.2, plate Z 60 … 150), rails/lips Y −48 … −69, floor groove Y −62 … −48.
- Front gussets now on the battery-bay walls (Y −45.6 … −26, apex Z 118); rear gussets behind the lips (apex Z 105).
- Mast kept at the V4 height (Z 65). Front walls dropped to Z 40.5 beyond Y 39 and cut at Y 46. V4 wall windows filled. Rear tail 45° from (Y −69, Z 60).
- Keep-out proven by boolean intersection = 0: chamber X ±36.25 / Y > −17.55 / Z > 40; anything above Z 65 in front of the mast; anything beyond Y 46.
- 104.3 cm³. Islands 0, bridges = V4 + 30 mm arch, bed contact 1991 mm².

## V6 — 2026-09-24 (superseded, never printed)
- Fixed 90° vertical phone tower rooted in the V4 transverse "mast" wall (Y −20.9 … −17.5, Z 54 … 150).
- Phone slot: V4-verified 81.5 mm width, lips ±36.25 mm, 45° rail chamfer, 2.5 mm lips; depth reduced 20 → **18.5 mm**.
- Bottom groove 14 mm with 45° lead-in; floor pads 15 mm each side, 51 mm centre gap for USB‑C.
- Front gussets on the side-wall tops (Z 64 → 125), side trays with 45° haunch/flare, pentagon lightening window in the plate.
- Removed: 35° deck, deck ribs, corbel behind the tie band, V5 tread steps.
- Trimmed: rear walls to a 45° tail (Z 33), front walls to Z 35 beyond Y 14, rear fin comb to Z 30; 2 mm grounded pad under the fins.
- 93.4 cm³ (V4 150.5, −38 %). Islands 0, bridges identical to V4 (42/41/34/32/23 mm), bed contact 2080 mm².

## V5 — 2026-09-24 (concept only)
- 100° leaning tower with a 3-step tread floor giving 100/95/90° without moving parts. Dropped in favour of a fixed 90° (simpler, less rattle risk, lighter).

## V4 — 2026-09-19 (printed, installed)
- 35° deck ("spoiler") version with weight reduction (deck window, 2.4 mm mast and fin-ribs, wall windows). 150.5 cm³.
- Verified on the car: USB‑C window, mid screw notches, battery bays, wiring, DC-plug clearance.

## V1–V3 — 2026-09-18
- Reconstruction from the cardboard prototype scan; battery arches, screw-head notches, rear fins + tie band, one-piece printing without supports.
