# Heavy Metal Pro Stock: contexto para conectar Printify

Documento para pasar a otra sesión de Claude Code. Resume lo decidido hasta el 5 de octubre de 2026.

## 1. El negocio

- **Marca:** Heavy Metal Pro Stock, tractor de jalón "The Evil One" (pro stock, motor Cat 3208 V8, reverse flow). Waterloo, Wisconsin. Piloto y dueño: Chris Feller. EST. 2014.
- **Tienda:** heavymetalprostock.com, en Shopify. La producción es bajo pedido con Printify.
- **Dueña de la tienda:** Isela. Ella aprueba cada diseño.
- **Tono de los textos:** como dbrand. Seco, seguro de sí, gracioso y con remate en letra chica. Ver `COPY-DBRAND.md` y `PROMPT-MAESTRO.md`.

## 2. Reglas que no se rompen

- No hacer nada sin autorización de Isela, sobre todo borrar algo o publicar productos.
- Nunca pegar ni guardar API keys en el repo ni en el chat. El token de Printify va en una variable de entorno (por ejemplo `PRINTIFY_API_TOKEN`) o en los secretos del environment.
- A GitHub solo suben diseños aprobados. Nunca subir las vistas previas de `mo/piloto-prev/`.
- "3208" siempre va con "V8".
- No usar "TRACTOR PULLING" en diseños nuevos. Los aprobados viejos que lo tienen (01, 01d, 02, 03c, 03d) se quedan así, salvo que Isela pida quitarlo.
- No repetir la misma frase dos veces en una misma prenda (frente, espalda, pecho o manga).
- No usar la frase "Do not feed the tractor" (a Isela no le gusta). La manga DoNotFeed y la espalda 01k la tienen.
- Banderas de USA siempre normales, nunca espejeadas.
- Nada de salpicado ni de efecto de tierra.
- Texto mínimo impreso: unos 80 px en mangas y 100 px o más en espaldas, a 300 dpi.
- Skill de Shopify: nunca correr `scripts/log_skill_use.mjs` ni `scripts/log_feedback.mjs`.

## 3. Dónde están los archivos

Repo `dvillasisr-lab/claude`, rama `claude/inspiring-brahmagupta-qzekyp`, carpeta `heavy-metal/disenos/`. Todo es PNG a 300 dpi. Los diseños de prenda tienen fondo transparente. Cada carpeta trae vistas previas (`vista-previa-*.png`) y algunas traen descripciones para Shopify (`descripcion-shopify-*.html`).

| Carpeta | Archivos | Tamaño |
|---|---|---|
| `01-espalda-letras` | 01 letras, 01d hoja técnica, 01k pull ticket | 4500×5400 |
| `02-the-evil-one` | 02 The Evil One, 02 CAMO (frente camo) | 4500×5400 |
| `03-motor-3208` | 03c letras apiladas, 03c2 con "tractor pulling", 03d tiras, 03f hoja técnica + descripciones Shopify | 4500×5400 |
| `04-mangas` | DoNotFeed, FullPull, Horsepower, Lightning, Serial3208V8Evil, SideEffects | 1200×1200 |
| `05-chris-ilustrado` | 05 Chris ilustrado | 4500×5400 |
| `05-etiqueta-interior` | etiqueta interior | 1500×1500 |
| `06-mangas-largas` | manga larga 1 (logo), 2 (full pull) | 1080×3750 |
| `07-camo` | las 6 mangas en versión CAMO + descripción | 1200×1200 |
| `09-alien` | 09 alien, 09b alien rayos negros | 4500×5400 |
| `10-chris-senna` | 10b Chris Senna dos líneas | 4500×5400 |
| `11-pecho` | 11a placa bordado, 11b tractor perfil, 11d placa sin línea | 1500×1500 |
| `12-perro` | 12 perro, 12b perro lentes | 4500×5400 |
| `13-serie-f1` | 13a Senna casco, 13b Hamilton panel, 13e vertical, 13g estela | 4500×5400 |
| `14-serie-letras` | 14c espalda vertical; mangas 14g (smoke included), 14h (sorry, neighbors); pechos 14a, 14b, 14d, 14e, 14f | varios |
| `15-tazas` | 15b letras apiladas + full pull, 15c hoja técnica (con fondo negro impreso) | 2475×1155 |

**Fuente de los diseños:** dos canvas en claude.ai (son privados, solo los abre Isela):

- **Diseños de prenda:** https://claude.ai/code/artifact/8ad37623-9761-49bc-80ff-03167d6e51ca
- **Patrones de estampado total:** https://claude.ai/code/artifact/eb303d96-3aa6-4253-8e1a-4fc971980732

**Ya están en el canvas pero no aprobados ni exportados:**

- Tazas 15a, 15d, 15e y 15f.
- Frentes de sudadera con bolsa 16a a 16e (3600×2400, van arriba de la bolsa).
- Todos los patrones de estampado total, mosaicos de 1500×1500 que se repiten sin costura.

Esos no van a Printify hasta que Isela los apruebe.

## 4. Decisiones de producción

**Proveedor:** elegirlo manualmente en cada producto, no usar Printify Choice. Así el negro, el amarillo y la técnica salen iguales en todos los pedidos. Printify Choice solo está bien para las tazas.

**Técnica por diseño:**

- **DTG** (ilustración, foto, humo, brillos): 02, 02 camo, 03c, 03c2, 03d, 05, 09, 09b, 10b, 12, 12b, 13a, 13b, 13g.
- **DTF** (letras y líneas): 01, 01d, 01k, 03f, 13e, 14c, todas las mangas y todos los pechos.
- **Sudaderas** (mezcla algodón/poliéster): DTF.
- **Tazas y patrones de estampado total:** sublimación.

Antes de crear cada producto, revisar en la ficha del proveedor qué técnica y qué marca de playera ofrece. Pedir muestras: una ilustración en DTG y una espalda de letras en DTF.

**Acomodo en la playera (decisión de Isela):** la ilustración va adelante y las letras atrás. Combinaciones propuestas:

| Frente (ilustración) | Espalda (letras) |
|---|---|
| 02 The Evil One | 01 letras |
| 09 Alien | 14c vertical con listas |
| 09b Alien rayos negros | 13e vertical |
| 12 Perro | 01k pull ticket |
| 12b Perro lentes | 01d hoja técnica |
| 05 Chris ilustrado | 03f motor hoja técnica |
| 10b Chris Senna | 01 letras |
| 03c letras apiladas con tractor | 14c vertical con listas |

Casi todos los diseños dicen "PRO STOCK · THE EVIL ONE" y la página web. Cuando el frente y la espalda los repitan, hay que hacer versiones de espalda sin esas líneas. Isela aún no lo aprueba.

**Sudaderas con bolsa:** la ilustración completa no cabe adelante porque la tapa la bolsa. Lleva ilustración en la espalda y un frente chico (diseños 16) o un pecho.

**Tamaño en la prenda:**

- Los diseños anchos (logo de lado a lado, ilustraciones Alien, Perro, The Evil One, 13a, 03c) van al 75-80% del cuadro.
- Los angostos y altos (13b, 13e, 14c) van al 90-100%.
- 01, 01d y 03f se ven bien como están.
- Medidas de referencia: frente con ilustración de 11 a 12 pulgadas de ancho, espalda de letras de 12 a 13 pulgadas, pecho de 3.5 a 4 pulgadas.
- Colocación: el frente empieza a 3-4 dedos del cuello y la espalda a 4-5 dedos.
- Los textos muy chicos de 13a y 03c casi no se leen en la prenda; se pueden agrandar o quitar.

**Tazas:** la medida que usamos (2475×1155) no está confirmada contra el producto de Printify. Hay que confirmarla con el blueprint y ajustar si cambia.

**Prendas:** todo sobre playera y sudadera negras.

## 5. Conectar Printify (para la siguiente sesión)

1. Isela crea un token personal en Printify (My account > Connections > API). Se guarda como secreto del environment. Nunca se pega en el chat.
2. API base: `https://api.printify.com/v1`, con el header `Authorization: Bearer $PRINTIFY_API_TOKEN`.
3. Pasos típicos:
   - `GET /shops.json` para obtener el `shop_id` de la tienda conectada a Shopify.
   - `GET /catalog/blueprints.json` para encontrar la playera, la sudadera o la taza.
   - `GET /catalog/blueprints/{id}/print_providers.json` y `.../print_providers/{pid}/variants.json` para escoger el proveedor (manual), las tallas y el color negro.
   - `POST /uploads/images.json` con `file_name` y `url` pública, o con `contents` en base64, para subir cada PNG del repo.
   - `POST /shops/{shop_id}/products.json` con `blueprint_id`, `print_provider_id`, `variants` y `print_areas` (las posiciones `front`, `back` y mangas según el blueprint), con escala y posición según la sección 4.
   - `POST /shops/{shop_id}/products/{id}/publish.json` publica en Shopify. **Solo con el visto bueno de Isela, producto por producto.**
4. Revisar en la documentación actual de Printify los campos exactos, porque cambian.
5. Primero crear todo como borrador y mostrarle a Isela los mockups. Publicar después.

## 6. Pendientes

- Confirmar con Isela las combinaciones frente/espalda y hacer las versiones de espalda sin frases repetidas.
- Exportar los diseños con la escala final (80% o 90%) y la posición para frente y espalda.
- Decidir con cuáles patrones se queda y exportarlos.
- Aprobar las tazas y los frentes de sudadera que faltan.
- Pedir muestras DTG y DTF antes de lanzar todo.
- Otros pendientes de la tienda: Knowledge Base con las respuestas de la FAQ; distinguir productos de hombre, mujer y unisex; catalogar fotos y videos cuando Isela los vuelva a subir.
