---
name: update-draft-map-links
description: Inspect Discord CDN screenshots of Brawl Stars ranked cheat sheets, identify the map shown in each image, and update data/drafts.json with each image URL and the current date. Use when a user supplies one or more Discord image links for draft maps, including when an identified map is not already present in drafts.json.
---

# Update Draft Map Links

Update only `data/drafts.json`. Preserve existing tips and unrelated entries.

## Workflow

1. From the user's message, extract every image URL, including URLs embedded in Markdown links. Preserve each complete URL exactly, including its query string.
2. Download every image immediately to a temporary directory because signed Discord CDN URLs can expire. Quote URLs in shell commands and follow redirects.
3. Inspect every downloaded image with the available local image-viewing tool. Prefer a map name printed in the image. If no title is visible, identify the game mode and distinctive terrain, then compare the layout with current map references online and the candidates in `data/mappings.json` (`map_mapping`). Never infer a map solely from the filename, attachment ID, ordering, or nearby screenshots.
4. Cross-check the identified name against both `map_mapping` and existing keys in `data/drafts.json`. Use the canonical map name even when it is absent from one or both files. Require high confidence from visible text or a layout match; if two names remain plausible after closer inspection and reference checking, ask the user instead of guessing.
5. Review the existing `data/drafts.json` diff before editing so pre-existing user changes remain intact.
6. Run the bundled updater once with all confirmed pairs. First use `--dry-run`, then repeat without it:

   ```bash
   python3 .agents/skills/update-draft-map-links/scripts/update_drafts.py \
     --map-link "Map Name" "https://cdn.discordapp.com/.../image.png?..." \
     --map-link "Another Map" "https://cdn.discordapp.com/.../image.png?..." \
     --dry-run
   ```

   The script normalizes map keys to the format consumed by `src/server.js`, preserves all existing fields, updates `link`, and sets `last_updated` from the local current date. For a missing key it appends an object containing `link` and `last_updated`.
7. Validate the result:

   ```bash
   node -e "JSON.parse(require('fs').readFileSync('data/drafts.json', 'utf8'))"
   git diff --check -- data/drafts.json
   git diff -- data/drafts.json
   ```

8. Confirm that each requested map has the exact supplied URL and today's date, and that no unrelated entry changed. Report created and updated map keys separately.

## Guardrails

- Do not alter `tips` for an existing map.
- Do not add guessed or generated tips to a new map.
- Do not shorten, refresh, decode, or otherwise rewrite signed URLs.
- Do not update `data/mappings.json`, generated files, or application code unless the user separately requests it.
- Do not publish, deploy, stage, or commit the data change unless explicitly requested.
