/**
 * Share command metadata from a common spot to be used for both runtime
 * and registration.
 */

export const INVITE_COMMAND = {
  name: 'invite',
  description: 'Get an invite link to add the bot to your server',
};

export const DRAFT_COMMAND = {
  name: 'draft',
  description: 'Return power league drafts for a map',
  options: [
    {
      type: 3, 
      name: 'map',
      description: 'The name of the map to get drafts for',
      required: true,
    }
  ],
};

export const COUNTER_COMMAND = {
  name: 'counter',
  description: 'Return brawler counters for a brawler',
  options: [
    {
      type: 3, 
      name: 'brawler',
      description: 'The name of the brawler to counter',
      required: true,
    }
  ],
};

export const HELP_COMMAND = {
  name: 'help',
  description: 'See a list of commands and how to use them',
};