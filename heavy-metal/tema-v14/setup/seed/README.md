# Seed de metaobjetos (contenido real)

Cada archivo es un arreglo `{handle, fields:[{key, value}]}` con valores en texto, listos para `metaobjectUpsert`. Las referencias (paquetes, tier, álbum, imágenes) NO van aquí: están en `references.json` para enlazarlas después de crear todo.

Fuentes: boceto-v28 (páginas + hm.js), tema en vivo (`templates_page.about.json`, `templates_page.sponsors.json`) y PENDIENTES.md (datos confirmados).

| Tipo | Entradas | Archivo |
|---|---|---|
| crew_member | 13 (Chris F., 3 de equipo, 7 de pit crew, 2 mascotas) | crew_member.json |
| sponsor_tier | 3 (title-partner, pit-partner featured, crew-supporter) | sponsor_tier.json |
| sponsor_stats | 1 (`main`) | sponsor_stats.json |
| season_stats | 1 (`2026`) | season_stats.json |
| booking_option | 4 | booking_option.json |
| tractor_part | 6 | tractor_part.json |
| logo_placement | 6 | logo_placement.json |
| decal_zone | 6 | decal_zone.json |
| faq_item | 77 (62 de faq.html + 7 solo de The Machine + 6 solo de Sponsors + 2 solo de The Evil List) | faq_item.json |
| pull_event | 2 | pull_event.json |
| referencias | 16 | references.json |

## Qué se dejó fuera y por qué
- **season_stats**: solo `exhibitions` 3 y `wins` 0 (confirmados; la dueña dice 3 o 4). `competitions` (el boceto muestra 2 = Monroe + primer pull) y `test_days` quedan fuera hasta que la dueña confirme Monroe y el primer pull. `updated` = 2026-09-28 (fecha del boceto).
- **pull_event**: solo Green County Fall Nationals (Monroe, WI, Badger State) y First pull attempt (agosto 2026, "Ended early, minor issue"). Sin `date` porque no hay fecha exacta; sin ciudad ni liga en el primer pull ([pending]); sin `place`, `distance_ft`, `full_pull`. El video de Monroe sigue por confirmar (PENDIENTES): revisar antes de publicar. Los "Exhibition run", "County fair pull" y "Season finale pull" del Schedule son ejemplos: fuera.
- **decal_zone**: sin `size` (todas dicen "XX x XX in"). Solo Hood y Engine side panel tienen paquete (Title Partner); las demás quedan sin `tier` ("To confirm").
- **logo_placement**: "Pit passes" es la entrada de ejemplo del botón "+ Add placement": fuera. `package_details` va como "Title: biggest logo".
- **tractor_part**: las 6 partes de la anatomía (Engine, Displacement, Turbo, Body, Weight, Tires). Horsepower "Unknown" está en la ficha técnica (ajustes de sección), no en la anatomía, así que no es tractor_part. `image` va en references.json como archivo (`target_type: file`, nombre del archivo del boceto).
- **sponsor_tier**: beneficios y taglines del boceto (en vivo, Crew Supporter tenía "Built for local shops and fans" como beneficio; en el boceto es su tagline). Sin `spots_left`.
- **sponsor_stats**: `social_text` = "Growing" (boceto; en vivo decía "NEW").
- **crew_member**: roles del boceto (Isela = "Manager & PR"; en vivo decía "Manager, Marketing & PR"). Sin fotos. Bio de Chris: "20+ years in the sport." más la línea del boceto (idea 2014, primer tornillo 2020, la noche del rayo).
- **faq_item**: respuestas en rich text con links a `/pages/...`, `/account`, `/blogs/pit-log`, `/collections/...` (handles según analisis/10). "How much is shipping?" sin la frase "US orders over $XX ship free" (monto pendiente). "What is The Black Smoke Guarantee?" se cargó tal cual el boceto, pero el plazo y los términos siguen por confirmar con abogado. Preguntas que solo salen en The Machine, Sponsors o The Evil List tienen `pages` solo con esa página; las que se repiten ("Who drives it?", "How do I unsubscribe?") usan la respuesta del FAQ y llevan las dos páginas.
- **references.json**: `pull_event.gallery_album` apunta a álbumes `monroe-2026` y `first-pull-2026`, que no están en este seed (album no se pidió): crearlos o saltar ese enlace.
