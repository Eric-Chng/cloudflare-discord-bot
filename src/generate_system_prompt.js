// Builds a strict system prompt from project JSON data and provides
// helpers to create a cached system instruction and chat with it.

import builds from '../data/builds.json' with { type: 'json' };
import counters from '../data/counters.json' with { type: 'json' };
import drafts from '../data/drafts.json' with { type: 'json' };
import { GEMINI_MODEL } from './constants.js';

function buildSystemPrompt() {
  const rules = [
    'You are a Brawl Stars strategy expert.',
    'Use ONLY the provided knowledge base where applicable.',
    'If a player asks about a known map, ALWAYS return the associated link from drafts. Returning the associated link is of UTMOST IMPORTANCE. Using the tips to give advice is of secondary importance and should only be done after giving the link.',
    "If the map isn't in drafts, clearly state your current knowledge doesn't include that map.",
    'If asked for good builds, ALWAYS tell the player to use the /build command.',
    'If asked how to counter a brawler, ALWAYS return the info from counters.json for that brawler.',
    'If asked for a mix of knowledge, still apply these rules first, then briefly synthesize concise advice.',
    'Keep responses brief where possible.'
  ];

  const draftsLines = Object.entries(drafts)
    // .filter(([_, info]) => info?.last_updated === "Sep 26, 2025")
    .map(([mapName, info]) => {
      const link = info?.link || '';
      const tips = info?.tips || '';
      return `- Map: ${mapName}\n  Link: ${link}` + (tips ? `\n  Tips: ${tips}` : '');
    })
    .join('\n');

//   const buildsLines = Object.entries(builds)
//     .map(([brawler, info]) => {
//       const gadget = info?.gadget || '';
//       const starpower = info?.starpower || '';
//       const gear = info?.gear || '';
//       const hypercharge = info?.hypercharge ? `\n  Hypercharge: ${info.hypercharge}` : '';
//       const tips = info?.tips ? `\n  Tips: ${info.tips}` : '';
//       return `- Brawler: ${brawler}\n  Gadgets: ${gadget}\n  Star Powers: ${starpower}\n  Gears: ${gear}${hypercharge}${tips}`;
//     })
//     .join('\n');

  const countersLines = Object.entries(counters)
    .map(([brawler, info]) => {
      const tips = info?.tips || '';
      const brawlerCounters = info?.brawler_counters || '';
      return `- Brawler: ${brawler}\n  Tips: ${tips}\n  Counters: ${brawlerCounters}`;
    })
    .join('\n');

  const systemText = [
    'SYSTEM INSTRUCTIONS',
    '-------------------',
    ...rules,
    '',
    'KNOWN MAP DRAFTS (drafts.json):',
    draftsLines,
    // '',
    // 'KNOWN BUILDS (builds.json):',
    // buildsLines,
    '',
    'KNOWN COUNTERS (counters.json):',
    countersLines,
  ].join('\n');

  return systemText;
}

export function buildSystemPromptFrom() {
  return buildSystemPrompt();
}

export async function createCachedSystemPrompt(env, systemTextInput) {
  if (!env.GEMINI_API_KEY) {
    return { error: 'GEMINI_API_KEY not set' };
  }
  const systemText = systemTextInput || buildSystemPrompt();
  try {
    // Create cached content for reuse
    const createResp = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/cachedContents?key=${env.GEMINI_API_KEY}`,
      {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({
          model: `models/${GEMINI_MODEL}`,
          systemInstruction: { parts: [{ text: systemText }] },
          ttl: '86400s'
        })
      }
    );
    if (!createResp.ok) {
      return { error: `cache create error: ${createResp.status}` };
    }
    const createData = await createResp.json();
    const cachedContentId = createData?.name || createData?.cachedContentId || null;
    return { cachedContentId, systemText };
  } catch (e) {
    return { error: `cache create failed: ${e.message}` };
  }
}

export async function chatWithSystemPrompt(message, env, options = {}) {
  if (!env.GEMINI_API_KEY) {
    return { error: 'GEMINI_API_KEY not set' };
  }
  const { cachedContentId, systemText } = options;
  const body = {
    contents: [
      {
        role: 'user',
        parts: [{ text: message }]
      }
    ]
  };
  if (cachedContentId) {
    body['cachedContent'] = cachedContentId;
  } else {
    body['systemInstruction'] = { parts: [{ text: systemText || buildSystemPrompt() }] };
  }
  try {
    const resp = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}:generateContent?key=${env.GEMINI_API_KEY}`,
      {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify(body)
      }
    );
    if (!resp.ok) {
      return { error: `generate error: ${resp.status}` };
    }
    const data = await resp.json();
    const parts = data?.candidates?.[0]?.content?.parts || [];
    const text = parts.map(p => p.text || '').join('').trim();
    return { text: text || 'No response from model.' };
  } catch (e) {
    return { error: `generate failed: ${e.message}` };
  }
}

export function __debug_buildSystemPrompt() {
  return buildSystemPrompt();
}


