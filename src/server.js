/**
 * The core server that runs on a Cloudflare worker.
 */

import { Router } from 'itty-router';
import {
  InteractionResponseType,
  InteractionType,
  verifyKey,
} from 'discord-interactions';
import { AWW_COMMAND, INVITE_COMMAND, DRAFT_COMMAND, COUNTER_COMMAND } from './commands.js';
import { getCuteUrl } from './reddit.js';
import { InteractionResponseFlags } from 'discord-interactions';

const Fuse = require('fuse.js');

const counters = require('../data/counters.json');
const drafts = require('../data/drafts.json');
const draftsFuzzyArray = Object.keys(drafts).map(key => ({ mapName: key, url: drafts[key] }));


const draftsFuzzySearch = new Fuse(draftsFuzzyArray, {
  // keys to search in (you can specify nested paths with dot notation)
  keys: ["mapName"],

  // Configure other options for fuzziness, etc.
  threshold: 0.4, // Adjust the threshold (0 = exact match, 1 = match anything)
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
router.get('/', (request, env) => {
  return new Response(`👋 ${env.DISCORD_APPLICATION_ID}`);
});

/**
 * Main route for all requests sent from Discord.  All incoming messages will
 * include a JSON payload described here:
 * https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object
 */
router.post('/', async (request, env) => {
  const { isValid, interaction } = await server.verifyDiscordRequest(
    request,
    env,
  );
  if (!isValid || !interaction) {
    return new Response('Bad request signature.', { status: 401 });
  }

  if (interaction.type === InteractionType.PING) {
    // The `PING` message is used during the initial webhook handshake, and is
    // required to configure the webhook in the developer portal.
    return new JsonResponse({
      type: InteractionResponseType.PONG,
    });
  }

  if (interaction.type === InteractionType.APPLICATION_COMMAND) {
    // Most user commands will come as `APPLICATION_COMMAND`.
    switch (interaction.data.name.toLowerCase()) {
      case AWW_COMMAND.name.toLowerCase(): {
        const cuteUrl = await getCuteUrl();
        return new JsonResponse({
          type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
          data: {
            content: cuteUrl,
          },
        });
      }
      case INVITE_COMMAND.name.toLowerCase(): {
        const applicationId = env.DISCORD_APPLICATION_ID;
        const INVITE_URL = `https://discord.com/oauth2/authorize?client_id=${applicationId}&scope=applications.commands`;
        return new JsonResponse({
          type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
          data: {
            content: `The bot is private due to hosting fees. If you would like to add it to your own server and are willing to pay a small subscription fee, contact Coolfood.`,
            flags: InteractionResponseFlags.EPHEMERAL,
          },
        });
      }
      case DRAFT_COMMAND.name.toLowerCase(): {
        const mapName = interaction.data.options.find(option => option.name === 'map')?.value;
        const mapQuery = mapName.toLowerCase().replace(/[^\w\s]|_/g, "");
        const draftInfo = `https://www.reddit.com/r/BrawlStarsCompetitive/comments/19a61lt/how_to_draft_in_season_22_a_power_league_meta/`;

        if (drafts[mapQuery] === undefined) {
          //fuzzy search time
          const draftsFuzzyResult = draftsFuzzySearch.search(mapQuery);
          if (draftsFuzzyResult.length === 0) {
            return new JsonResponse({
              type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
              data: {
                content: `Sorry, I couldn't find a draft for "${mapName}".\nYou can find more information on drafting here: ${draftInfo}`,
              },
            });
          }
          const matchedUrl = draftsFuzzyResult[0].item.url;
          return new JsonResponse({
            type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
            data: {
              content: ``,
              embeds: [{
                title: `Fuzzy Search Result for ${mapName}`,
                image: {
                  url: matchedUrl, 
                },
              }],
            },
          });
          
        } 

        return new JsonResponse({
          type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
          data: {
            content: ``,
            embeds: [{
              title: `Draft for ${mapName}`,
              image: {
                url: drafts[mapQuery], 
              },
            }],
          },
        });
      }
      case COUNTER_COMMAND.name.toLowerCase(): {
        var brawlerName = interaction.data.options.find(option => option.name === 'brawler')?.value.toLowerCase();
        const brawlerNameQuery = brawlerName.replace(/[^\w\s]|_/g, "");
        const counterInfo = counters[brawlerNameQuery] || 'No counter information available for this brawler.';
        //capitalize first letter of brawler name
        brawlerName = brawlerName.charAt(0).toUpperCase() + brawlerName.slice(1);
        return new JsonResponse({
          type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
          data: {
            content: `${brawlerName}: \n${counterInfo}`,
          },
        });
      }
      default:
        return new JsonResponse({ error: 'Unknown Type' }, { status: 400 });
    }
  }

  console.error('Unknown Type');
  return new JsonResponse({ error: 'Unknown Type' }, { status: 400 });
});
router.all('*', () => new Response('Not Found.', { status: 404 }));

async function verifyDiscordRequest(request, env) {
  const signature = request.headers.get('x-signature-ed25519');
  const timestamp = request.headers.get('x-signature-timestamp');
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
