# Changelog

Coordinate frame used everywhere: X right, Y toward the car front, Z up, Z = 0 at the top of the
upper chassis plate (same as the STL files).

## V7 — 2026-09-24 (current, not yet printed)
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
