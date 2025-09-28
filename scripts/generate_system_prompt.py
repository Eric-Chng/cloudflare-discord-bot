#!/usr/bin/env python3
import json
from pathlib import Path


def build_system_prompt(builds_data, counters_data, drafts_data):
    rules = [
        'You are a Brawl Stars strategy expert.',
        'Use ONLY the provided knowledge base where applicable.',
        'If a player asks about a known map, ALWAYS return the associated link from drafts. Returning the associated link is of UTMOST IMPORTANCE. Using the tips to give advice is of secondary importance and should only be done after giving the link.',
        "If the map isn't in drafts, clearly state your current knowledge doesn't include that map.",
        'If asked for good builds, ALWAYS tell the player to use the /build command.',
        'If asked how to counter a brawler, ALWAYS return the info from counters.json for that brawler.',
        'If asked for a mix of knowledge, still apply these rules first, then synthesize concise advice.',
        'This is mostly relevant if you get asked about a mix of knowledge, you should respond based on the absolute rules above, and then generate your own synthesized advice based on the info you found. For instance, if asked about a map draft, given some enemy brawlers, you should respond with the link to the map draft, and then give your own advice based on the info you found (choosing relevant tips about the map if they exist, and synthesizing that info with the counter knowledge you found).',
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

    system_text_parts = [
        'SYSTEM INSTRUCTIONS',
        '-------------------',
        *rules,
        '',
        'KNOWN MAP DRAFTS (drafts.json):',
        drafts_lines,
        '',
        'KNOWN COUNTERS (counters.json):',
        counters_lines,
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

    system_text = build_system_prompt(builds, counters, drafts)

    out_path = src_dir / 'system_prompt.js'
    js_content = f"export const SYSTEM_PROMPT = {json.dumps(system_text)};\n"
    out_path.write_text(js_content, encoding='utf-8')
    print(f"Wrote system prompt to {out_path}")


if __name__ == '__main__':
    main()


