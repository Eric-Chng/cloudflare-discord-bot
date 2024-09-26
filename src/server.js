/**
 * The core server that runs on a Cloudflare worker.
 */

import { Router } from 'itty-router';
import {
  InteractionResponseType,
  InteractionType,
  verifyKey,
} from 'discord-interactions';
import { INVITE_COMMAND, DRAFT_COMMAND, COUNTER_COMMAND, HELP_COMMAND, MODIFIER_COMMAND, BUILD_COMMAND } from './commands.js';
import { InteractionResponseFlags } from 'discord-interactions';

const botchannel = `931255199627112458`;
const acceptedRoles = [`931250396435972136`, `1168295996166516848`, `935264620325765191`,`931250435745022013`, `931250488836493313`];

const paid_servers = require('../data/paid_servers.json');

const Fuse = require('fuse.js');

const counters = require('../data/counters.json');
const countersFuzzyArray = Object.keys(counters).map(key => ({ brawlerName: key, counterInfo: counters[key] }));
const drafts = require('../data/drafts.json');
const draftsFuzzyArray = Object.keys(drafts).map(key => ({ mapName: key, url: drafts[key] }));
const modifiers = require('../data/modifiers.json');
const modifiersFuzzyArray = Object.keys(modifiers).map(key => ({ modifierName: key, modifierInfo: modifiers[key] }));
const builds = require('../data/builds.json');
const buildsFuzzyArray = Object.keys(builds).map(key => ({ brawlerName: key, buildInfo: builds[key] }));


const draftsFuzzySearch = new Fuse(draftsFuzzyArray, {
  // keys to search in (you can specify nested paths with dot notation)
  keys: ["mapName"],

  // Configure other options for fuzziness, etc.
  threshold: 0.4, // Adjust the threshold (0 = exact match, 1 = match anything)
});
const countersFuzzySearch = new Fuse(countersFuzzyArray, {
  // keys to search in (you can specify nested paths with dot notation)
  keys: ["brawlerName"],
  threshold: 0.25,
});
const modifiersFuzzySearch = new Fuse(modifiersFuzzyArray, {
  // keys to search in (you can specify nested paths with dot notation)
  keys: ["modifierName"],
  threshold: 0.6,
});
const buildsFuzzySearch = new Fuse(buildsFuzzyArray, {
  // keys to search in (you can specify nested paths with dot notation)
  keys: ["brawlerName"],
  threshold: 0.25,
});


class JsonResponse extends Response {
  constructor(body, init) {
    const jsonBody = JSON.stringify(body);
    init = init || {
      headers: {
        'content-type': 'application/json;charset=UTF-8',
      },
    };
    super(jsonBody, init);
  }
}

const router = Router();

/**
 * A simple :wave: hello page to verify the worker is working.
 */
router.get('*', (request, env) => {
  return new Response(`👋 ${env.DISCORD_APPLICATION_ID}`);
});

/**
 * Main route for all requests sent from Discord.  All incoming messages will
 * include a JSON payload described here:
 * https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object
 */
router.post('*', async (request, env) => {
  return new JsonResponse({ error: 'Unknown Type' }, { status: 400 });
  
});
router.all('*', () => new Response('Not Found.', { status: 404 }));

async function verifyDiscordRequest(request, env) {
  const signature = request.headers.get('x-signature-ed25519');
  const timestamp = request.headers.get('x-signature-timestamp');
  console.log(signature);
  const body = await request.text();
  const isValidRequest =
    signature &&
    timestamp &&
    verifyKey(body, signature, timestamp, env.DISCORD_PUBLIC_KEY);
  if (!isValidRequest) {
    return { isValid: false };
  }

  return { interaction: JSON.parse(body), isValid: true };
}

const server = {
  verifyDiscordRequest: verifyDiscordRequest,
  fetch: async function (request, env) {
    return router.handle(request, env);
  },
};

export default server;
