# Datarin · brief para generar logos con IA (skill `design`)

Requiere `GEMINI_API_KEY` en el entorno (se toma al abrir una sesión nueva).

Dirección elegida:
- Tipo: símbolo + nombre.
- Referencias: Stripe / Linear (limpio, moderno, detalle fino) y Accenture / Deloitte (nombre + un gesto gráfico simple).
- Nada de la letra D como símbolo.
- Idea: muchos datos entran, una decisión clara sale. Consultoría de BI, analítica e IA.
- Color: tinta #0B0F17, cobalto #1F4BFF como único acento.

Comandos (desde la raíz del repo):

```bash
python3 library/skills/design/scripts/logo/search.py "data analytics consulting business intelligence" --design-brief -p "Datarin"
python3 library/skills/design/scripts/logo/generate.py --brand "Datarin" --style minimalist --industry consulting \
  --prompt "combination mark: abstract geometric symbol where scattered data points resolve into one solid block, plus lowercase wordmark 'datarin' in a tight modern grotesk, ink #0B0F17 with a single cobalt #1F4BFF accent, white background, Stripe and Linear level refinement"
```
