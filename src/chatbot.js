import { GEMINI_MODEL } from './constants.js';
import { SYSTEM_PROMPT } from './system_prompt.js';

export async function generateWithGemini(userMessage, env) {
  if (!env.GEMINI_API_KEY) {
    return 'Gemini API key is not set. Ask the admin to fix';
  }
  try {
    const endpoint = `https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}:generateContent?key=${env.GEMINI_API_KEY}`;
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
      },
      body: JSON.stringify({
        contents: [
          {
            role: 'user',
            parts: [
              { text: userMessage }
            ]
          }
        ]
      })
    });
    if (!response.ok) {
      return `Gemini API error: ${response.status}`;
    }
    const data = await response.json();
    const parts = data?.candidates?.[0]?.content?.parts || [];
    const text = parts.map(p => p.text || '').join('').trim();
    return text || 'No response from model.';
  } catch (err) {
    return `Gemini request failed: ${err.message}`;
  }
}

export async function chatWithSystemPrompt(userMessage, env, systemText = SYSTEM_PROMPT) {
  if (!env.GEMINI_API_KEY) {
    return { error: 'GEMINI_API_KEY not set' };
  }
  try {
    const endpoint = `https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}:generateContent?key=${env.GEMINI_API_KEY}`;
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
      },
      body: JSON.stringify({
        systemInstruction: { parts: [{ text: systemText || SYSTEM_PROMPT }] },
        contents: [
          {
            role: 'user',
            parts: [
              { text: userMessage }
            ]
          }
        ]
      })
    });
    if (!response.ok) {
      return { error: `Gemini API error: ${response.status}` };
    }
    const data = await response.json();
    const parts = data?.candidates?.[0]?.content?.parts || [];
    const text = parts.map(p => p.text || '').join('').trim();
    return { text: text || 'No response from model.' };
  } catch (err) {
    return { error: `Gemini request failed: ${err.message}` };
  }
}


