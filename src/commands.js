
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
  description: 'Return ranked drafts for a map',
  options: [
    {
      type: 3, 
      name: 'map',
      description: 'The name of the map to get drafts for',
      required: true,
    }
  ],
};

export const TEST_COMMAND = {
  name: 'test',
  description: 'test embeds',
  options: [
    {
      type: 3,               // STRING
      name: 'map',
      description: 'Select a map',
      required: true,
      autocomplete: true
    },
    {
      type: 3,
      name: 'team1_brawler1',
      description: 'Team 1 slot 1',
      required: true,
      autocomplete: true
    },
    {
      type: 3,
      name: 'team1_brawler2',
      description: 'Team 1 slot 2',
      required: true,
      autocomplete: true
    },
    {
      type: 3,
      name: 'team1_brawler3',
      description: 'Team 1 slot 3',
      required: true,
      autocomplete: true
    },
    {
      type: 3,
      name: 'team2_brawler1',
      description: 'Team 2 slot 1',
      required: true,
      autocomplete: true
    },
    {
      type: 3,
      name: 'team2_brawler2',
      description: 'Team 2 slot 2',
      required: true,
      autocomplete: true
    },
    {
      type: 3,
      name: 'team2_brawler3',
      description: 'Team 2 slot 3',
      required: true,
      autocomplete: true
    }
  ]
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

export const MODIFIER_COMMAND = {
  name: 'modifier',
  description: 'Get tips for a specific modifier',
  options: [
    {
      type: 3, 
      name: 'modifier',
      description: 'Modifier Name',
      required: true,
    }
  ],
};

export const BUILD_COMMAND = {
  name: 'build',
  description: 'Return best build for a brawler',
  options: [
    {
      type: 3, 
      name: 'brawler',
      description: 'The name of the brawler to build',
      required: true,
    }
  ],
};

export const EVENT_COMMAND = {
  name: 'event',
  description: 'Get tips for the current event.',
};

export const HELP_COMMAND = {
  name: 'help',
  description: 'See a list of commands and how to use them',
};

export const TIER_LIST_COMMAND = {
  name: 'tierlist',
  description: 'Get the current tier list',
  options: [
    {
      type: 3, // 3 corresponds to STRING type
      name: 'category',
      description: 'Select which tier list to view',
      required: true,
      choices: [
        {
          name: 'Brawlers',
          value: 'brawlers',
        },
        {
          name: 'Hypercharges',
          value: 'hypercharges',
        },
      ],
    },
  ],
};
