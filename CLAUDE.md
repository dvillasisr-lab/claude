# Biblioteca de skills bajo demanda

Trabajo principal: diseño de tiendas Shopify, merch, decks estilo consultoría, correos HTML y automatizaciones.

Siempre activas en `.claude/skills/`: `hallmark` (diseño de páginas y tiendas) y `consulting-deck` (decks estilo McKinsey). Todo lo demás está apagado para no gastar tokens y no se carga solo.

Cuando el usuario diga "revisa qué hay", "usa una skill", o pida algo donde una skill ayude:
1. Lee `library/CATALOG.md` (índice corto).
2. Si hace falta una fuente externa, lee `library/catalog/<fuente>.md` y corre `library/fetch-source.sh <fuente>`.
3. Lee solo el SKILL.md elegido y síguelo como instrucciones. Para un subagente, lee su .md y pásalo como prompt a un agente general.
4. Di en una línea qué skill vas a usar y por qué, y sigue.

Si el usuario agrega o quita skills, regenera el índice con `python3 library/build-catalog.py` (después de `library/fetch-source.sh all`).
