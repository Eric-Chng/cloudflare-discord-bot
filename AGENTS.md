# Repository Guidelines

## Project Structure & Module Organization
Source lives in `src/`, with `server.js` exposing the Worker entry point, `commands.js` and `chatbot.js` handling Discord logic, and `system_prompt.js` generated from `scripts/generate_system_prompt.py`. Shared data artifacts (tier lists, embeddings) sit in `data/`, while integration tests live under `test/` (current pattern: `*.test.js`). Use `scripts/` for helper CLIs, `coverage/` for c8 output, and keep Cloudflare settings in `wrangler.toml` plus `.dev.vars` for local secrets.

## Build, Test, and Development Commands
Note that we do not have any tests as is, and that's fine.
- `npm run start`: launches `wrangler dev` against the Worker on port 8787. Pair with `npm run ngrok` if Discord needs a public tunnel.
- `npm run register`: registers slash commands using the payload in `src/register.js`.
- `npm run chat:local -- "<prompt>"`: exercises the local chat CLI with `GEMINI_API_KEY` set.
- `npm test`: runs `c8 mocha test`, producing coverage in `coverage/`.
- `npm run lint` / `npm run fix`: lint all JS files with ESLint + Prettier, optionally auto-fixing.
- `npm run publish`: `wrangler deploy` to Cloudflare Workers (requires `wrangler login` beforehand).

## Coding Style & Naming Conventions
Code is modern ESM targeting Node 18+. Follow ESLint’s recommended rules plus Prettier formatting (2-space indent, single quotes per `.prettierrc.json`). Prefer descriptive camelCase for functions/variables and SCREAMING_CASE for constants defined in `src/constants.js`. Co-locate helper modules in `src/` and export pure utilities for easy testing.

## Testing Guidelines
We have no tests so it's fine

## Commit & Pull Request Guidelines
Git history favors short, imperative subjects (`bugfix`, `temp update tier list`). Match that tone, reference issues when relevant (`fix: ... #123`), and keep commits scoped to a single concern. PRs should include: overview of behavior changes, manual/test evidence (`npm test` output or wrangler logs), screenshots of Discord command changes when visual, and any required secrets or config updates.

## Security & Configuration Tips
Store secrets via `wrangler secret put` or `wrangler secret:bulk data/secrets.json`; never commit `.dev.vars`. Update `wrangler.toml` with the correct Worker name before deploying. When experimenting locally, guard API keys by exporting them inline (`GEMINI_API_KEY=... npm run chat:local`) and avoid echoing them in logs.
