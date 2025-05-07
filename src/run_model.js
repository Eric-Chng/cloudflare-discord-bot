// features.js
const { score } = require('./rf_model');
// Load your mappings JSON
const mappings = require('../data/mappings.json');
// features.js (ES module style)
// import mappings from './mappings.json' assert { type: 'json' };
const { feature_cols, mode_mapping, map_mapping, all_brawlers } = mappings;

/**
 * Build a feature array in the same order as your trained model expects.
 * If an error occurs, returns an error string.
 * @param {string} mode     – e.g. 'Gem Grab'
 * @param {string} mapName  – e.g. 'Minecart Madness'
 * @param {string[]} team1  – array of three brawler IDs for team1
 * @param {string[]} team2  – array of three brawler IDs for team2
 * @returns {number[]|string} – feature vector or error message
 */
export function buildFeatureArray(mode, mapName, team1, team2) {
  try {
    // Validate & encode Mode/Map
    if (!(mode in mode_mapping)) {
      throw new Error(`Unknown mode: "${mode}". Valid modes: ${Object.keys(mode_mapping).join(', ')}`);
    }
    if (!(mapName in map_mapping)) {
      throw new Error(`Unknown map: "${mapName}". Valid maps: ${Object.keys(map_mapping).join(', ')}`);
    }

    // Start with Mode/Map codes
    const sample = {
      Mode: mode_mapping[mode],
      Map:  map_mapping[mapName]
    };

    // One-hot encode each brawler flag
    all_brawlers.forEach(b => {
      sample[`T1_has_${b}`] = team1.includes(b) ? 1 : 0;
      sample[`T2_has_${b}`] = team2.includes(b) ? 1 : 0;
    });

    // Build the final array, filling any missing features with 0
    return feature_cols.map(colName =>
      typeof sample[colName] === 'number' ? sample[colName] : 0
    );
  } catch (err) {
    return `Error building feature array: ${err.message}`;
  }
}
