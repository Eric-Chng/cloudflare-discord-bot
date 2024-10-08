import json

# Load the JSON content
file_path = "drafts.json"
with open(file_path, "r") as file:
    data = json.load(file)

# Updates based on user's input
updates = {
    "canal grande": "Take over middle grass and have brawlers to cover multiple niches (throwers and tanks). Brawlers with artillery capabilities (Penny, Squeak) can also be used.",
    "hideout": "Run snipers unless you're playing against pros. Other good classes are assassins (Mortis) and long range supports (8-Bit, R-T).",
    "shooting star": "Run snipers. If enemy has a thrower make sure you have a long range assassin or your own thrower.",
    "snake prarie": "Group up to be able to get revenge kills (not close enough for one enemy to teamwipe though). Make sure you have brawlers that have vision abilities/gear or are a tank.",
    "center stage": "Team comp should have a bush scouter and tank counter.",
    "penalty kick": "Throwers are OP (except for Moe and Kenji). Best throwers are Barley and Larry & Lawrie so use them or ban them. Very easy to get away with random nonsense so make sure you have a good tank counter as well.",
    "pinball dreams": "Throwers and wall breakers are really strong first picks. Later in draft go for damage dealers or assassins when you know it's safer.",
    "triple dribble": "Thrower heavy draft. If you're not going a thrower or thrower counter pick brawlers that are tanky enough to shrug off some damage to create space, fast enough to close distance against throwers, or good wall peakers.",
    "double swoosh": "Sneaky map, don't get caught lacking by being cautious with scouting and vision gear.",
    "hard rock mine": "Focus on getting a good lane brawler (Surge, Rico, Ruffs, etc) as there are a lot of good middle map brawlers.",
    "last stop": "Prioritize a good sniper as gem carrier in middle. In bushes you can run an anti agro, assassin, or brawler good at scouting.",
    "undermine": "Get a sniper in mid and then anti agro, assassin, scout brawler, or wall peaker in bushes. If skill issue in bushes double up in mid(do not triple stack) for more pressure or pinching",
    "bridge too far": "Long range and water brawlers good. Make sure you have at least one serious damage dealer on the safe that can't be ignored.",
    "hot potato": "BASE RACE, run tanks/throwers that can burst down safe or damage dealers that the tanks will eventually feed.",
    "kaboom canyon": "More snipers compared to other Heist maps, make sure you run a brawler that can burst safe for pressure.",
    "safe zone": "6th pick can make some dirty comps, beware double throwers if you have snipers and no throwers. Consider breaking open map and using snipers if enemy has only midrange brawlers.",
    "dueling beetles": "Larry & Lawrie and Barley as best throwers plus whatever newest brawlers in game are for first pick. Run assassins, tanks, and tank counters later in draft.",
    "open business": "Throwers strong. Options are just a cycle of throwers, wall breakers, tanks/assassins, and anti agro",
    "parallel plays": "Focus on defensive left lane with a high DPS mid to long range. Middle area will be a versatile long range, then right lane should have an assassin or other aggressive brawler.",
    "ring of fire": "Two people down middle, then another person preventing enemy from spawn camping in grass",
    "belles rock": "Late pick is very strong as throwers or assassins so be careful of those.",
    "flaring phoenix": "Run a thrower and sniper, then a brawler with good synergy or as an enemy counter.",
    "goldarm gulch": "Lock in a thrower, most snipers are versatile enough to deal with assassins, then pick an assassin yourself or brawler good when gas closes.",
    "out in the open": "Everyone will probably run a sniper. Assassins are a good last pick so make sure you have a mid range anti agro to create space against snipers or counter assassins."
}

# Apply the updates
for key, tip in updates.items():
    if key in data:
        data[key]["tips"] = tip
    else:
        data[key] = {"tips": tip}

# Save the updated JSON content back to the file
with open(file_path, "w") as file:
    json.dump(data, file, indent=4)

# Notify the user
print("Updates applied successfully.")
