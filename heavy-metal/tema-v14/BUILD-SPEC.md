# BUILD SPEC: tema "HM v14" (Dawn 16 + diseño del boceto)

Contract every builder agent follows. Source of truth for design: `heavy-metal/boceto-v28/` (fully QA'd static mockup). Port it faithfully to Shopify OS 2.0. The Spanish `<p class="note">` blocks in each boceto page explain how each part must be editable in Shopify: follow them. Full data model: `heavy-metal/analisis/10-preparacion-shopify.md` sections 1, 2, 3 and 5.

## Folder and ownership
- Theme root: `/home/user/claude/heavy-metal/tema-v14/` (Dawn 16.0.0 copy). Keep Dawn files; add ours with the `hm-` prefix. Only edit files you own (listed in your task). Never edit another agent's files; if you need something from a shared file, write it in your report.
- Shared (owned by the FOUNDATION agent): `layout/theme.liquid`, `config/settings_schema.json`, `config/settings_data.json`, `assets/hm-base.css`, `assets/hm-core.js`, `sections/header-group.json`, `sections/footer-group.json`, `sections/hm-header.liquid`, `sections/hm-announcement.liquid`, `sections/hm-footer.liquid`, `sections/hm-sponsor-strip.liquid`, `snippets/hm-icon.liquid`, `snippets/hm-image.liquid`.
- Do not edit Dawn files except the ones your task names. Do not delete Dawn files.

## Design system
- `assets/hm-base.css` = boceto `hm.css` cleaned (no draftbar, no `.note`, no demo/skeleton-demo, no fake cookie banner, no sample catalog styles). All boceto global classes keep the same names (`.wrap`, `.h1`, `.h2`, `.h3`, `.label`, `.muted`, `.btn`, `.btn--ghost`, `.link`, `.input`, `.chip`, `.card`, `.thumb`, `.sect`, `.sect-head`, etc.), so page sections can reuse them. Tokens: `--ink`, `--bg`, `--surface`, `--line`, `--mute`, `--soft`, `--accent:#F5C400`, `--alert`, `--night`, `--f-head`, `--f-body`, `--t-*`, `--sect`, `--header`.
- Page-specific CSS: inside the section with `{% stylesheet %}` (no Liquid inside it). Use CSS variables in `style=""` for setting-driven values.
- Fonts: Archivo (headings, width axis 62 to 125) and the body font exactly as the boceto loads them; FOUNDATION decides (self-hosted woff2 in assets if downloadable, else Google Fonts with preconnect and `display=swap`).
- Owner rules (customer-facing text is US English): brand always `Heavy Metal Pro Stock: “The Evil One”`; “The Evil One” always with curly quotes; never the characters `–` or `—`; no direct email/phone except in policies; never mention Printify ("we print every item when you order it"); no SMS; no "Ride With"; horsepower "Unknown"; wins at 0 show "Coming soon"/"Soon"; no full pulls counter; special edition never numbered; mailing list = "The Evil List"; yellow marquee exactly `Full pull or nothing · This thing is f#ck!ng evil · Born in a lightning storm`; one filled primary button per section, others as underlined text links; never leave big empty space on the right; nothing saturated.

## Liquid rules
- Every new section has a complete `{% schema %}` with `name`, sensible `settings` (all customer text editable with English defaults copied from the boceto), `blocks` where the merchant manages lists, and `presets` when it should be addable from the editor. Use `{{ block.shopify_attributes }}` on block wrappers.
- Plain English strings in markup are fine for small UI labels (the site is English only); merchant copy goes in settings. Do not add keys to Dawn locale files.
- Snippets start with `{% doc %}`.
- Images: always `image_url` with `widths` + `image_tag` with `sizes`, `loading: 'lazy'` below the fold, `fetchpriority: 'high'` only on the LCP image, width/height always present. Static boceto photos become `image_picker` settings (merchant uploads them); when empty, render `placeholder_svg_tag` or a neutral block, never a broken image.
- Dynamic data comes from metaobjects (types below) via `shop.metaobjects.<type>.values` or metaobject list settings; sort by the `order` field; respect `status`/`active` fields. Loop limit 50: paginate when it can grow (Pit Log, galleries).
- Anything that depends on "today" (next pull, countdowns, special edition state, Last updated freshness) is computed in the browser JS from data attributes, never in Liquid (page cache).
- JS: one small file per feature in `assets/hm-<feature>.js` loaded with `defer` from its section (`<script src="{{ 'hm-x.js' | asset_url }}" defer></script>`), or `{% javascript %}`. No libraries. Must listen to `shopify:section:load` / `shopify:section:unload` to init/clean (editor re-renders), and cancel `requestAnimationFrame`/timers on unload.
- Accessibility: WCAG 2.2 AA. Focus visible, Escape closes overlays and returns focus, focus trap in dialogs, `aria-expanded`/`aria-controls`, live regions for form messages, 24px minimum targets, pause button for anything moving more than 5 s, `prefers-reduced-motion` respected.
- Forms: contact-type forms use `{% form 'contact' %}` with `contact[...]` fields (topic in `contact[topic]`); newsletter uses `{% form 'customer' %}` with `contact[tags]` (e.g. `evil-list`, `notify,notify-<handle>`). Show `form.posted_successfully?` and `form.errors`.

## Theme settings (FOUNDATION adds them; everyone may read them)
`settings.hm_season` (number, 2026), `settings.hm_free_shipping` (number, USD, empty = hide bar), `settings.hm_gift_threshold` (number), `settings.hm_gift_label` (text "Free sticker"), `settings.hm_feed_beast_product` (product), `settings.hm_feed_beast_amounts` (text "1,2,5"), `settings.hm_crew_pack_product` (product), `settings.hm_crew_cap_product` (product), `settings.hm_addons_collection` (collection), `settings.hm_best_sellers_collection` (collection), `settings.hm_facebook_url`, `settings.hm_instagram_url` (url, empty = hidden), `settings.hm_brand_name` (text, `Heavy Metal Pro Stock: “The Evil One”`), `settings.hm_ships_line` (text "Printed when you order · ships in 5 days").

## Metaobject types (already created in the store, Storefront access on)
Field keys exactly as listed. Option fields store the lowercase value shown.
- `pull_event`: event_name, date (date), start_time, season (int), calendar_label, city, league (ntpa|badger_state|ihra_ppl|other), type (competition|exhibition), status (upcoming|done|cancelled|hidden), result, place (int), full_pull (bool), distance_ft (decimal), video (url), website (url), gallery_album (ref album).
- `season_stats`: season (int), competitions (int), competitions_note, exhibitions (int), wins (int), test_days (int), updated (date).
- `sponsor_tier`: name, key (title|pit|crew), price (int), tagline, benefits (list text), featured (bool), status (available|limited|soldout|hidden), spots_left (int), order (int), updated (date).
- `sponsor`: name, logo (file image), tier (ref sponsor_tier), shape (round|square|wide), link (url), active (bool), order (int), season (int).
- `sponsor_stats`: pulls_per_season (int, 20), states (int, 10), fans_per_pull (int, 5000), social_text, show_plus (bool), estimated (bool), updated (date). Reach = pulls_per_season × fans_per_pull. One entry, handle `main`.
- `logo_placement`: name, icon (tractor|trailer|shirt|web|social|mic|pass), description (multi), packages (list ref sponsor_tier), package_details (list text), status (active|hidden), order (int), updated (date).
- `decal_zone`: name, pos_x, pos_y, label_x (int), row (top|bottom), size, tier (ref sponsor_tier), status (available|sold), description (multi), order (int), updated (date).
- `tractor_part`: name, value, text (multi), image (file image), image_position, pos_x, pos_y, label_x (int), row (top|bottom), order (int).
- `album` (web pages on, template `templates/metaobject/album.json`): event_name, date (date), season (int), kind (competition|exhibition|test), city, league, cover (file image), photos (list file image), videos (list url), pull_event (ref pull_event), pit_log_url (url), order (int).
- `booking_option`: name, icon (display|pull|meet|social), text (multi), needs, order (int).
- `crew_member`: name, role, group (driver|team|pit_crew|mascot), photo (file image), note, bio (multi), order (int).
- `size_chart`: style (tee|long_sleeve|hoodie|crewneck|kids|cap|beanie), unit, columns (list text), rows (list text, cells split by " | "), note (multi).
- `faq_item`: question, answer (rich text), category (orders|shipping|returns|sizing|products|drops|payments|account|evil_list|sponsors|special_edition|tractor), pages (list text: faq|machine|sponsors|evil_list), order (int).
Product metafields (namespace `custom`): guarantee_noun, design_story (multi), details (list text), size_chart (ref size_chart), complete_the_look (product ref), card_note, bundle_savings (int), drop_date (date_time), start_date, end_date (date_time), run_size (int), story (multi), updated (date). Article metafields: custom.gallery_album (ref album), custom.distance_ft (decimal).
Product status by tags: `coming-soon`, `new`, `best-seller`, `special-edition`, `bundle`. "Almost gone!" when total inventory is 1 to 5 (only if inventory is tracked).

## Validation (mandatory before you finish)
Run for all files you created or changed:
```
node /home/user/claude/.claude/skills/shopify/scripts/validate.mjs --api liquid --theme-path /home/user/claude/heavy-metal/tema-v14 --files <comma-separated relative paths> --model claude-opus-5-5 --client-name claude-code --client-version 1 --artifact-id <your-agent-name> --revision <n>
```
Fix every ERROR. Warnings: fix when reasonable. Also `node -e` JSON.parse every template JSON you write. Search docs when unsure: `node /home/user/claude/.claude/skills/shopify/scripts/search_docs.mjs "<query>" --api liquid --model claude-opus-5-5 --client-name claude-code --client-version 1`.
Do NOT run `log_skill_use.mjs` or `log_feedback.mjs`. Do NOT call any Shopify Admin API and do NOT upload anything: the coordinator uploads.

## Report
End with: files created/changed, what is editable how (in Spanish, short, for the owner), anything you needed from a shared file, and validation result.
