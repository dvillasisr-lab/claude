# Brief: Heavy Metal business card (two-sided)

## Goal
The best business card this team could have. Portfolio / award quality (think Type Directors Club, Communication Arts, Behance "Featured"), the kind that gets saved and re-pinned on Pinterest. It must feel designed by a senior editorial designer, not generated.

## Client
- **Heavy Metal**, a ProStock tractor pulling team. Tractor name: **"The Evil One"** (always with quotes). Base: **Waterloo, Wisconsin**.
- Machine facts (real, use only these): CAT 3208 V8, 10,000 lb, ProStock class, rear tires 24.5-32, track 300 ft, "full pull" = reaching the end.
- Store: heavymetalprostock.com. Email: heavymetalevil72@gmail.com.
- Name, phone and role are unknown: use exactly `NOMBRE APELLIDO`, `(000) 000-0000`, `Team Owner · Driver` as placeholders.

## Non-negotiables from the client (from feedback so far)
1. **The tractor must be highly visible and NOT awkwardly cropped.** Stack, roll cage and wheels should read. (A deliberate, elegant crop is fine only if the machine is still clearly whole-feeling; the client disliked a heavy crop.)
2. **"HEAVY METAL" must be unmistakably prominent.** Use the real logo SVGs, never retype the name in a font.
3. **Brand palette:** black base, then silver, white, and yellow `#F5C400` as the single accent. Yellow is used sparingly and with intent.
4. **Editorial**, not a Facebook banner shrunk down. Strong idea, confident hierarchy, generous negative space, precise alignment.
5. Direction the tractor faces: **left** (the pull goes left). If a finish/300 ft device is used, it sits ahead of the tractor, on the left.
6. No em or en dashes in any copy. No italic headlines. No gradients-as-decoration, no generic stock textures.

## Client taste learned from direct feedback (weight these heavily)
- Rejected ALL round-0 candidates (`print/swarm/a-editorial`, `b-machined`, `c-motorsport`; council notes in `ROUND0_FEEDBACK.md`). They are the floor.
- Wants HEAVY METAL **big**. Complained twice that the name "doesn't show enough".
- Prefers the logo in **flat white** (said "que las letras HEAVY METAL sean solo blancas"), not chrome gradients. Yellow logo is acceptable as a single accent.
- Complained the tractor was "cortado" (cropped) when stack/cage/wheels were cut. Wants the tractor bigger and fully visible.
- Rejected a design that looked like the Facebook banner shrunk down. Wants real editorial design, portfolio/award level, Pinterest-viral.
- Likes: "“THE EVIL ONE”" in yellow with quotes, black background, the engine-open photo, the finish line ahead on the left, the profile badge ring idea.

## What the client liked
- The chrome/white logo on black, the yellow accent, the real engine-open tractor photo, "THE EVIL ONE" in yellow.
- The Facebook cover and profile badge in `ref/` define the brand look. The card should belong to the same family but be its own, better, piece.
- Current best attempt: `ref/v4-frente.png`, `ref/v4-reverso.png`. Beat it clearly.

## Print specs (hard)
- US standard 3.5 × 2 in. Build at 300 dpi **with 0.125 in bleed**: canvas **1125 × 675 px**. Trim box inset 37.5 px. **Safe zone inset 75 px**: all text, logo, QR must be inside x∈[75,1050], y∈[75,600].
- Backgrounds/images that should bleed must extend to the canvas edge.
- QR (`assets/qr-tienda.svg`, links to the store) must stay scannable: dark modules on a light field, at least ~112 px (0.37 in) square plus quiet zone.
- Minimum text size ~11 px at this scale (≈ 6.5 pt). Contact text should be comfortably readable.

## Assets (`print/swarm/assets/`)
- `tractor-motor-abierto-cutout.png` 1671×846 RGBA: the real tractor, engine side open, facing left, clean cutout. Primary hero.
- `tractor-perfil-cutout.png`: second angle (faces right; mirror with CSS if used).
- `foto-motor-abierto.jpg`, `foto-pista-cielo.jpg`: original photos (full scenes), `foto-emblema-v8.jpg`: machined "V8 3208 PRO STOCK" plate.
- `emblema-v8-3208-mask.png`: clean white-on-black vector-style redraw of that emblem.
- `logo-apilado.svg` (HEAVY / METAL stacked), `logo-linea.svg` (one line). Fill is `#F2F0E9`; replace the fill string to recolor. The line logo has a `<g transform="translate(1123 -296)">` group for METAL (matters for gradients).
- `qr-tienda.svg` (fill `#0a0b0c`).
- Fonts (local TTF, load with `@font-face{src:url(file://<FONTS>/Name.ttf)}`): `/root/.claude/skills/synced/9983f56a-2d7a-4333-8a10-0941713cc597_0d8f03d3-28eb-42fc-935b-5b47bbd87cf0/canvas-design/canvas-fonts/` (BigShoulders-Bold, IBMPlexMono-Regular/Bold, InstrumentSerif-Regular, JetBrainsMono, GeistMono, WorkSans, Outfit, BricolageGrotesque, etc.). Google Fonts are NOT reachable from the renderer.

## How to build and render
- Write one HTML file with two `.card` divs `#front` and `#back`, each exactly 1125×675 px. Embed images as base64 data URIs (or absolute file:// paths).
- Render with Playwright (Node, global modules at `/opt/node22/lib/node_modules`, run with `NODE_PATH=$(npm root -g) node script.js`). Chromium is preinstalled; do NOT run `playwright install`. `print/swarm/render-template.js` shows the pattern (screenshot each `.card` by id; for the PDF open the page with a `#print` hash that adds `zoom:.32; break-after:page` to `.card`, `@page{size:3.75in 2.25in;margin:0}`, then `page.pdf({width:'3.75in',height:'2.25in',printBackground:true})`).
- **Look at your own renders** (Read the PNG) and fix what you see before returning. Check safe zone, overlaps, legibility, crop.
