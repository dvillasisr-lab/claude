# Design skills para Claude Code

Skills instaladas en `.claude/skills/` (se cargan solas al abrir este repo en Claude Code):

| Fuente | Skills |
|---|---|
| [voltagent/awesome-design-md](https://github.com/voltagent/awesome-design-md) | `awesome-design-md` (DESIGN.md de ~70 marcas) |
| [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) / [tasteskill.dev](https://www.tasteskill.dev/) | `image-to-code`, `design-taste-frontend`, `design-taste-frontend-v1`, `gpt-taste`, `high-end-visual-design`, `minimalist-ui`, `industrial-brutalist-ui`, `redesign-existing-projects`, `stitch-design-taste`, `brandkit`, `imagegen-frontend-web`, `imagegen-frontend-mobile`, `full-output-enforcement` |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | `ui-ux-pro-max`, `design`, `design-system`, `ui-styling`, `brand`, `banner-design`, `slides` |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines) + [vercel.com/design/guidelines](https://vercel.com/design/guidelines) | `web-design-guidelines` (con copia local en `guidelines.md`) |
| [Playwright agent CLI](https://playwright.dev/agent-cli/introduction) | `playwright-cli` (el binario `@playwright/cli` se instala con el hook `SessionStart`) |
| [kylezantos/design-motion-principles](https://github.com/kylezantos/design-motion-principles) | `design-motion-principles` |
| [usehallmark.com](https://www.usehallmark.com/) ([nutlope/hallmark](https://github.com/nutlope/hallmark)) | `hallmark` |
| [Framer external agents](https://www.framer.com/agents/external/) (`@framer/agent`) | `framer`, `framer-code-components` (requieren `npx @framer/agent@latest setup` y login en navegador) |
| [threejs.org](https://threejs.org/) ([CloudAI-X/threejs-skills](https://github.com/CloudAI-X/threejs-skills)) | `threejs-fundamentals`, `-geometry`, `-materials`, `-lighting`, `-textures`, `-animation`, `-loaders`, `-shaders`, `-postprocessing`, `-interaction` |

## Plugins (en `.claude/settings.json`)

Se instalan solos al abrir el repo en Claude Code (marketplaces en `extraKnownMarketplaces`, activados en `enabledPlugins`).

| Fuente | Plugin | Contexto fijo aprox. |
|---|---|---|
| [obra/superpowers](https://github.com/obra/superpowers) | `superpowers@superpowers-dev` | ~0.8k tokens |
| [affaan-m/ECC](https://github.com/affaan-m/ECC) | `ecc@ecc` (386 skills, 68 agentes, hooks) | ~43.6k tokens |
| [mattpocock/skills](https://github.com/mattpocock/skills) | `mattpocock-skills@mattpocock` | ~1.6k tokens |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | `marketing-skills@marketingskills` | ~13.6k tokens |
| [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | `caveman@caveman` | ~1.8k tokens |
| [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) | 10 plugins `voltagent-*@voltagent-subagents` (subagentes) | bajo |

Para desactivar uno, cambia su valor a `false` en `enabledPlugins`.

Local (fuera de la nube): `npm install -g @playwright/cli@latest`.
