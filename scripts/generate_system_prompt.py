#!/usr/bin/env python3
import json
from pathlib import Path


def build_system_prompt(builds_data, counters_data, drafts_data, tierlist_data):
    rules = [
        'You are a Brawl Stars strategy expert.',
        'Use ONLY the provided knowledge base where applicable.',
        'If a player asks about a known map, ALWAYS return the associated link from drafts. Returning the associated link is of UTMOST IMPORTANCE. Using the tips to give advice is of secondary importance and should only be done after giving the link.',
        "If the map isn't in drafts, clearly state your current knowledge doesn't include that map.",
        'If asked for good builds, ALWAYS tell the player to use the /build command.',
        'If asked how to counter a brawler, ALWAYS return the info from counters.json for that brawler.',
        'If asked for a mix of knowledge, still apply these rules first, then synthesize concise advice.',
        'This is mostly relevant if you get asked about a mix of knowledge, you should respond based on the absolute rules above, and then generate your own synthesized advice based on the info you found. For instance, if asked about a map draft, given some enemy brawlers, you should respond with the link to the map draft, and then give your own advice based on the info you found (choosing relevant tips about the map if they exist, and synthesizing that info with the counter knowledge you found). Specific brawler suggestions are good if you feel confident about them.',
        'You will also have some knowledge about the tier list of brawlers. You can refer to it to gauge how strong a brawler is, but remember even low tier brawlers can be useful in the right situations and even high tier brawlers can be bad in the wrong situations. Being high tier doesnt mean they beat their counters. It is a good general guide to help you create team comps and give advice.',
        'Only mention the specific tier a brawler is if asked directly about how strong a brawler is. Try to avoid mentioning the specific tier when building team comps or providing counters. The tier list can still guide your thinking but do not expose it to the user unless relevant.'
        'While giving advice, also focus on keeping responses brief where possible to focus on the most important details.'
    ]

    # Maintain insertion order from JSON
    drafts_lines_parts = []
    for map_name, info in drafts_data.items():
        link = (info or {}).get('link', '')
        tips = (info or {}).get('tips', '')
        line = f"- Map: {map_name}\n  Link: {link}" + (f"\n  Tips: {tips}" if tips else '')
        drafts_lines_parts.append(line)
    drafts_lines = "\n".join(drafts_lines_parts)

    counters_lines_parts = []
    for brawler, info in counters_data.items():
        tips = (info or {}).get('tips', '')
        brawler_counters = (info or {}).get('brawler_counters', '')
        line = f"- Brawler: {brawler}\n  Tips: {tips}\n  Counters: {brawler_counters}"
        counters_lines_parts.append(line)
    counters_lines = "\n".join(counters_lines_parts)

    tierlist_lines_parts = []
    for tier, brawlers in tierlist_data.items():
        line = f"- Tier: {tier}\n  Brawlers: {brawlers}"
        tierlist_lines_parts.append(line)
    tierlist_lines = "\n".join(tierlist_lines_parts)

    system_text_parts = [
        'SYSTEM INSTRUCTIONS',
        '----------------',
        *rules,
        '',
        'KNOWN MAP DRAFTS (drafts.json):',
        drafts_lines,
        '',
        'KNOWN COUNTERS (counters.json):',
        counters_lines,
        '',
        'KNOWN TIER LIST (tierlist_extracted.json):',
        tierlist_lines,
        '----------------'
    ]
    return "\n".join(system_text_parts)


def main():
    repo_root = Path(__file__).resolve().parents[1]
    data_dir = repo_root / 'data'
    src_dir = repo_root / 'src'

    with (data_dir / 'builds.json').open('r', encoding='utf-8') as f:
        builds = json.load(f)
    with (data_dir / 'counters.json').open('r', encoding='utf-8') as f:
        counters = json.load(f)
    with (data_dir / 'drafts.json').open('r', encoding='utf-8') as f:
        drafts = json.load(f)
    with (data_dir / 'tierlist_extracted.json').open('r', encoding='utf-8') as f:
        tierlist = json.load(f)
    system_text = build_system_prompt(builds, counters, drafts, tierlist)

    out_path = src_dir / 'system_prompt.js'
    js_content = f"export const SYSTEM_PROMPT = {json.dumps(system_text)};\n"
    out_path.write_text(js_content, encoding='utf-8')
    print(f"Wrote system prompt to {out_path}")


if __name__ == '__main__':
    main()


