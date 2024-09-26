/**
 * The core server that runs on a Cloudflare worker.
 */

import { Router } from 'itty-router';




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
  return new Response('Hello, world!');
  
});
router.all('*', () => new Response('Not Found.', { status: 404 }));

const server = {
  fetch: async function (request, env) {
    return router.handle(request, env);
  },
};

export default server;
