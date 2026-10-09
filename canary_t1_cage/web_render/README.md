# web_render — exterior-only CAD line-art of the as-built Canary unit (2026-10-08)

**Purpose:** public-website renderings (light theme). Not a part; nothing here is printed or sliced.
**Disclosure posture:** exterior form only. The interior between the levels is an opaque mask block —
no wiring, boards, connectors, sensor placement, aircraft mounting hardware, battery brand, dimensions,
part numbers or text other than the optional etched CANARY wordmark on the deck. Radio + suction mount excluded.

| File | Role |
|---|---|
| `canary_unit_web.scad` | Massing model. `part="all"\|"body"\|"dome"\|"ledbar"` (colour groups), `wordmark=true\|false`. Echoes the envelope, asserts the layout (dome clear of case/deck edge, wordmark clear of the case, battery inside the end face). |
| `render_web.py` | Exports the three groups as binary STL via openscad, then an orthographic z-buffer hidden-line renderer (numpy + PIL + scipy): flat faces `#EEF1F5` (three orientation tones, dome one tone), navy `#0B1F3A` feature + silhouette edges, faint contact shadow, amber `#E29A1F` LED bar + glow on the `ledbar` variant. PNG transparent + white at 2400 px, SVG of the visible edge segments. |

Reproduce: `python3 render_web.py --out <dir> --width 2400 --ss 2`
(`--views hero,hero_led,opp,front,side,top,sheet`). Per-group STL by hand:
`openscad -q --backend=Manifold --export-format binstl -D 'part="body"' -o body.stl canary_unit_web.scad`.

**Geometry basis / simplifications:** 406 x 279 x 270 two-level 2020 frame per the 2026-10-08 photo brief
(the sideplates family reads the re-railed frame as 444.5 long and three rows — proportion only, no dimension
is shown); corner/T gussets and hex-vented plates on the long faces only (plain rectangular plates, no ears or
fasteners); vent cell coarsened to 8.0 AF / 2.5 web (house cell 5.0 / 1.6) so the vents read as line art;
compute case = chamfered box + square fan grille, no I/O; dome 110 on a short pedestal; generic V-mount-style
battery block on the -X end; open end faces show the mask block as recessed flat panels.

## 2026-10-09 variants (same kit, same style; outputs to `canary/company/generated/renders/canary-unit-2026-10-09/`, gitignored)

| File | Role |
|---|---|
| `render_kit.py` | Splits `render_web.py` into a geometry pass (z-buffer + per-group visible edges) and a compose step with per-group flat-colour / line-weight / opacity / screen-x fade, so one pass can feed many frames. Imports the rasteriser from `render_web.py` unchanged. |
| `canary_cabin_cutaway.scad` + `render_cabin.py` | **Scene A** — concept cut-away of the unit in the baggage bay of a GENERIC high-wing single cabin. Original rounded-tube shell with invented round proportions (inner 1050 x 1180, bay 895 long): cabin floor, raised baggage floor, aft bulkhead, raked seat-back blocks + cushions, baggage-door outline grooved on the far (right, -Y) wall so the cut-away shows it, tailcone hull fading out (screen-space opacity ramp to 6 %). The unit is a plain silhouette (box + deck, case block, plain dome, battery block) at 0.4x line weight / 45 % opacity. No restraint, strap, cable, antenna, sensor or mount anywhere. `grp=cabin|tail|unit`, `cut=iso|section|plan`. Label layer off. |
| `canary_unit_cutout.scad` + `render_cutout.py` | **Scene B** — the web massing with the hero-facing upper long-side plate re-cut as the CANARY stencil (house wordmark vector, 254 wide / ~27 cap, one line, between the rails) over a diffuser panel. The house glyphs are single closed outlines (A and R are open forms) so no stencil ties exist or are needed. Rebate from the back to a **0.8 mm skin** (render value; a printed skin is 1.2-1.8) because a 5 mm stencil wall hides ~70 % of a 5 mm stroke at the hero angle. Diffuser = flat dark `#1C283A` off, `#FFC247` on, glow spill composited under the edges. Nothing behind the plate but the diffuser; the interior stays the opaque mask. |

**Scene A `_ghost` rev (2026-10-09):** `python3 render_cabin.py --out <dir> --width 2400 --ss 2 --ghost` adds a
"you are here" locator — a whole-airframe hull (`grp=ghost` fuselage/empennage/gear/prop/struts + `grp=ghost_wing`,
never cut) whose side proportions are traced from the public site's generic high-wing side-profile line art
(`company-site/explorations/c-aircraft/index.html`, 8.05 mm per svg unit; the roof break is moved aft to the bulkhead
station so the cut-away sits exactly inside the hull) and whose plan proportions are invented round numbers (span 10.9 m,
root chord 1.75 m, stab span 3.4 m). Rendered in its own hidden-line passes sharing the frame: navy hairlines at 0.25x the
cut-away weight / 70 % opacity, 3 % navy tint, composited UNDER the full-weight section; dashed box (+90 mm) marks the
sectioned region. `ghost_fit=true` pulls the tailcone end section inside the hull. Outputs `A*_ghost_{white,transparent}.png`,
`A*_ghost.svg` (groups `airframe_ghost`, `section_marker`, then the section groups) and `A*_ghost_only.png` (ghost + box
alone, transparent). No badge, registration, glazing, doors, type name or real-aircraft geometry anywhere.

Reproduce: `python3 render_cabin.py --out <dir> --width 2400 --ss 2` and
`python3 render_cutout.py --out <dir> --still-width 2400 --frame-width 1600 --ss 2` (`--what stills,breathe,strobe`).
Breathe: 24 frames, k = (1 - cos 2πi/24)/2, 10 fps = 2.4 s loop. Strobe: 12 frames, 6 on / 6 off.
