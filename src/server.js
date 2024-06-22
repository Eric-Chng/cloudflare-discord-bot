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
    const channel = interaction.channel_id;
    const roles = interaction.member.roles;
    const guild = interaction.guild_id;
    var messageFlags = 0;
    if (guild === `931249800790298645`) {
      if (channel !== botchannel) {
        const hasAcceptedRole = roles.some(role => acceptedRoles.includes(role));
        if (hasAcceptedRole === false) {
          messageFlags = InteractionResponseFlags.EPHEMERAL;
        }
      }
    }
    // Most user commands will come as `APPLICATION_COMMAND`.
    switch (interaction.data.name.toLowerCase()) {
      case HELP_COMMAND.name.toLowerCase(): {
        console.log(paid_servers);
        console.log("Credit = " + paid_servers[0]);
        console.log("cred inside" + paid_servers.includes(`931249800790298645`));
        return new JsonResponse({
          type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
          data: {
            content: `**Commands**\n**/draft** - Return power league drafts for a map. Only has updated maps for current PL rotation\n**/counter** - Return brawler counters for a brawler\n**/modifier** - Return brawler recommendations for a modifier\n**/build** - Get the best build for a brawler.\n**/invite** - Find out how to add the bot to your own server\n\nIf you would like to support the bot, check out: https://ko-fi.com/brawldraftbot`,
            flags: messageFlags,
          },
        });
      }
      case INVITE_COMMAND.name.toLowerCase(): {
        const applicationId = env.DISCORD_APPLICATION_ID;
        const INVITE_URL = `https://discord.com/oauth2/authorize?client_id=${applicationId}&scope=applications.commands`;
        return new JsonResponse({
          type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
          data: {
            content: `The bot is not free to invite due to hosting fees. \nIf you want to add it to your own server, either check out: https://ko-fi.com/brawldraftbot or boost this discord server: https://discord.gg/KDkyMhGuux \nKo-Fi is preferred!`,
            flags: InteractionResponseFlags.EPHEMERAL,
          },
        });
      }
      case DRAFT_COMMAND.name.toLowerCase(): {
        const mapName = interaction.data.options.find(option => option.name === 'map')?.value;
        const mapQuery = mapName.toLowerCase().replace(/[^\w\s]|_/g, "");
        const draftInfo = `https://www.youtube.com/watch?v=dF0NwoYGM2s&t=2s`;

        if (drafts[mapQuery] === undefined) {
          //fuzzy search time
          const draftsFuzzyResult = draftsFuzzySearch.search(mapQuery);
          if (draftsFuzzyResult.length === 0) {
            return new JsonResponse({
              type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
              data: {
                content: `Sorry, I couldn't find a draft for "${mapName}".\nTry an external resource like: ${draftInfo}`,
                flags: messageFlags,
              },
            });
          }
          const matchedUrl = draftsFuzzyResult[0].item.url;
          return new JsonResponse({
            type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
            data: {
              content: `# Fuzzy Search for ${mapName}\n${matchedUrl}`,
              flags: messageFlags,
              
            },
          });
          
        } 

        return new JsonResponse({
          type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
          data: {
            content: `# Draft for ${mapName}\n${drafts[mapQuery]}`,
            flags: messageFlags,
          },
        });
      }
      case COUNTER_COMMAND.name.toLowerCase(): {
        var brawlerName = interaction.data.options.find(option => option.name === 'brawler')?.value.toLowerCase();
        const brawlerNameQuery = brawlerName.replace(/[^\w\s]|_/g, "");
        if (counters[brawlerNameQuery] === undefined) {
          //fuzzy search time
          const countersFuzzyResult = countersFuzzySearch.search(brawlerNameQuery);
          if (countersFuzzyResult.length === 0) {
            return new JsonResponse({
              type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
              data: {
                content: `Sorry, I couldn't find any counter information for "${brawlerName}".`,
                flags: messageFlags,
              },
            });
          }
          var matchedCounterBrawler = countersFuzzyResult[0].item.brawlerName;
          matchedCounterBrawler = matchedCounterBrawler.charAt(0).toUpperCase() + matchedCounterBrawler.slice(1);
          const matchedCounterInfo = countersFuzzyResult[0].item.counterInfo;
          return new JsonResponse({
            type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
            data: {
              content: `Fuzzy Search for ${brawlerName} found **${matchedCounterBrawler}**: \n${matchedCounterInfo}`,
              flags: messageFlags,
            },
          });
        }
        const counterInfo = counters[brawlerNameQuery];
        brawlerName = brawlerName.charAt(0).toUpperCase() + brawlerName.slice(1);

        return new JsonResponse({
          type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
          data: {
            content: `${brawlerName}: \n${counterInfo}`,
            flags: messageFlags,
          },
        });
      }
      case MODIFIER_COMMAND.name.toLowerCase(): {
        var modifierNameInput = interaction.data.options.find(option => option.name === 'modifier')?.value;
        var cleanedModifierName = modifierNameInput.toLowerCase().replace(/[^\w\s]|_/g, "");
        const modifierFuzzyResult = modifiersFuzzySearch.search(cleanedModifierName);
        if (modifierFuzzyResult.length === 0) {
          return new JsonResponse({
            type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
            data: {
              content: `Sorry, I couldn't find any information for "${modifierNameInput}".`,
              flags: messageFlags,
            },
          });
        } else {
          const matchedModifierName = modifierFuzzyResult[0].item.modifierName;
          const matchedModifierInfo = modifierFuzzyResult[0].item.modifierInfo;
          return new JsonResponse({
            type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
            data: {
              content: `Fuzzy Search for ${modifierNameInput} found **${matchedModifierName}**: \n${matchedModifierInfo}`,
              flags: messageFlags,
            },
          });
      
        }
      }
      case BUILD_COMMAND.name.toLowerCase(): {
        var brawlerName = interaction.data.options.find(option => option.name === 'brawler')?.value.toLowerCase();
        const brawlerNameQuery = brawlerName.replace(/[^\w\s]|_/g, "");
        if (builds[brawlerNameQuery] === undefined) {
          //fuzzy search time
          const buildsFuzzyResult = buildsFuzzySearch.search(brawlerNameQuery);
          if (buildsFuzzyResult.length === 0) {
            return new JsonResponse({
              type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
              data: {
                content: `Sorry, I couldn't find any build information for "${brawlerName}".`,
                flags: messageFlags,
              },
            });
          }
          var matchedBuildBrawler = buildsFuzzyResult[0].item.brawlerName;
          matchedBuildBrawler = matchedBuildBrawler.charAt(0).toUpperCase() + matchedBuildBrawler.slice(1);
          const matchedBuildInfo = buildsFuzzyResult[0].item.buildInfo;
          var buildResponseContent = `Fuzzy Search for ${brawlerName} found **${matchedBuildBrawler}**: \n\n__**Gadgets**__:\n${matchedBuildInfo.gadget}\n\n__**Star Powers**__:\n${matchedBuildInfo.starpower}\n\n__**Gears**__:\n${matchedBuildInfo.gear}`;
          if ("tips" in matchedBuildInfo) {
            buildResponseContent += `\n\n__**Tips**__:\n${matchedBuildInfo.tips}`;
          }
          return new JsonResponse({
            type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
            data: {
              content: buildResponseContent,
              flags: messageFlags,
            },
          });
        }
        const buildInfo = builds[brawlerNameQuery];
        brawlerName = brawlerName.charAt(0).toUpperCase() + brawlerName.slice(1);
        var buildResponseContent = `${brawlerName}: \n\n__**Gadgets**__:\n${buildInfo.gadget}\n\n__**Star Powers**__:\n${buildInfo.starpower}\n\n__**Gears**__:\n${buildInfo.gear}`;
          if ("tips" in buildInfo) {
            buildResponseContent += `\n\n__**Tips**__:\n${buildInfo.tips}`;
          }
        return new JsonResponse({
          type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
          data: {
            content: buildResponseContent,
            flags: messageFlags,
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
