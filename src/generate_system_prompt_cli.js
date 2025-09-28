import { buildSystemPromptFrom } from './generate_system_prompt.js';
import fs from 'node:fs/promises';
import path from 'node:path';


async function main() {
  const systemText = buildSystemPromptFrom();
  const outPath = path.resolve(process.cwd(), 'src', 'system_prompt.js');
  const output = `export const SYSTEM_PROMPT = ${JSON.stringify(systemText)};\n`;
  await fs.writeFile(outPath, output, 'utf8');
  console.log(`Wrote system prompt to ${outPath}`);
}

main().catch((e) => {
  console.error('Failed to generate system prompt:', e);
  process.exit(1);
});


