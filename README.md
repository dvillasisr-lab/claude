# Design skills para Claude Code

Skills instaladas en `.claude/skills/` (se cargan solas al abrir este repo en Claude Code):

| Fuente | Skills |
|---|---|
| [voltagent/awesome-design-md](https://github.com/voltagent/awesome-design-md) | `awesome-design-md` (DESIGN.md de ~70 marcas) |
| [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) / [tasteskill.dev](https://www.tasteskill.dev/) | `image-to-code`, `design-taste-frontend`, `design-taste-frontend-v1`, `gpt-taste`, `high-end-visual-design`, `minimalist-ui`, `industrial-brutalist-ui`, `redesign-existing-projects`, `stitch-design-taste`, `brandkit`, `imagegen-frontend-web`, `imagegen-frontend-mobile`, `full-output-enforcement` |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | `ui-ux-pro-max`, `design`, `design-system`, `ui-styling`, `brand`, `banner-design`, `slides` |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines) + [vercel.com/design/guidelines](https://vercel.com/design/guidelines) | `web-design-guidelines` (con copia local en `guidelines.md`) |
| [Playwright agent CLI](https://playwright.dev/agent-cli/introduction) | `playwright-cli` (el binario `@playwright/cli` se instala con el hook `SessionStart`) |

Local (fuera de la nube): `npm install -g @playwright/cli@latest`.
