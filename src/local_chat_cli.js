import { chatWithSystemPrompt } from './generate_system_prompt.js';
import { SYSTEM_PROMPT } from './system_prompt.js';

async function main() {
  const apiKey = process.env.GEMINI_API_KEY;
  const message = process.argv.slice(2).join(' ').trim();
  if (!message) {
    console.error('Usage: GEMINI_API_KEY=... node src/local_chat_cli.js "your question"');
    process.exit(1);
  }
  if (!apiKey) {
    console.error('Set GEMINI_API_KEY in your environment before running this script.');
    process.exit(1);
  }
  const env = { GEMINI_API_KEY: apiKey };
  const { text, error } = await chatWithSystemPrompt(message, env, { systemText: SYSTEM_PROMPT });
  if (error) {
    console.error('Error:', error);
    process.exit(1);
  }
  console.log(text);
}

main().catch(err => { console.error('Unexpected error:', err); process.exit(1); });


