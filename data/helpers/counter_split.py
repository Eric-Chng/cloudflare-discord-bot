import json

# Original JSON data
data = {
    "shelly": "- Outrange, slow, or overwhelm with spawnables\n- Stu, Nita, Spike, Crow, Emz, Tara",
    "nita": "- Wall break opens up map to outrange Nita and quickly kill or pierce through Bruce (throwers)\n- Willow, Barley, Spike, Ruffs, Carl, Griff, Amber",
    "colt": "- Outrange or out maneuver\n- Piper, Max, Belle, Leon, Mortis, Darryl",
    "bull": "- Don't let him get close or out damage him in close range (why are you even looking up this counter)\n- Maisie, Lou, Surge, Cordelius, Emz, Gale",
    "brock": "- Use agro or hit hard from a long range\n- Piper, Nani, Max, Sam, Mandy",
    "el primo": "- Outrange or cancel/run away from him up close\n- Surge, Colette, Shelly, Cordelius, Otis, Stu, Gale",
    "barley": "- He's squishy so use assassins or break walls for throwers\n- Mortis, Mico, Leon, Edgar, Carl, Brock",
    "poco": "- Tank his shots and melt him down or slow\n- Emz, Mortis, Edgar, Bea, Griff, Crow",
    "rosa": "- Scout Rosa out before she jumps on you or easily deal with her as she's approaching you. Countered by stuns/slows\n- Charlie, Lou, El Primo, Crow, Emz, Griff, Gale, Shelly",
    "jessie": "- Find a way to beat Jessie 1v1 typically by outranging or agro, and quickly get rid of turret (throwers, long range)\n- Barley, Grom, Dynamike, Bo, Max, Piper, Leon",
    "dynamike": "- Dodge his main attack and get to him up close\n- Mico, Edgar, Mortis, Bibi, Gray, Stu",
    "tick": "- Pressure Tick up close or mid range\n- Mico, Darryl, Max, Sprout, Ash, Gene, Fang, Sam",
    "8 bit": "- Punish the player for being close to turret and being slow/tanky. Feed supers off him\n- Bo, Squeak, Penny, Colette, Belle, Dynamike",
    "rico": "- Since he's reliant on walls but can't break them, use throwers or assassins\n- Stu, Fang, Buzz, Mico, Edgar, Bonnie, Sprout, Grom",
    "darryl": "- Be prepared for when he rolls in and destroy him before he does or when he does\n- Surge, El Primo, Gale, Charlie",
    "penny": "- Break walls or shoot around walls to deal with her turret\n- Mr. P, Barley, Willow, Squeak, Carl, Grom, Amber",
    "carl": "- Interrupt his super when he gets up close\n- Surge, Fang, Gene, Buzz, Colette",
    "jacky": "- Outrange and mow her down or beat her 1v1\n- Rosa, Frank, Lou, Bea, Emz, Stu, Gale",
    "gus": "- Melt down his shield easily with high damage and usually getting up close. Low reload speed and can be outranged.\n- Piper, Nani, Mr. P, Sam, Mortis, Buzz, Fang, Edgar",
    "bo": "- Wiggle through his main attacks or stay out of range, then be aware of his mines or have some mobility to escape them or quickly trigger them\n- Stu, Mr. P, Max, Carl",
    "emz": "- Waste all her friend zoner gadgets and move in as an assassin/tank or outrange her by breaking down walls\n- Spike (vision gear on grassy maps), Mortis, Crow, Ruffs, Stu",
    "stu": "- Use spawnables to waste his ammo or have a wide attack that is hard to dodge\n- Ruffs, Spike, Pam, Crow, Poco",
    "piper": "- Use aggro, spawners, or outrange her with a longer range sniper or thrower\n- Charlie, Nani, Pearl, Mandy, Sprout, Max, Tick",
    "pam": "- Punish her HP and healing abilities\n- 8-bit, colette, Bo, Crow, Emz, Lou, Squeak",
    "frank": "- Punish his high HP and slow attacks. Any knockback destroys\n- Colette, El Primo, Lou, Shelly, Bull (PRIORITY: Colette and Lou), Maisie",
    "bibi": "- Outrange her and destroy her cover\n- Maisie, El Primo, Darryl, Stu, Surge, Griff",
    "bea": "- She has low HP and can't break walls, be careful of her range, slow, and damage, she also struggles against spawnables that don't charge her loaded shot\n- Edgar, Mortis, Mico, Piper, Nani, Byron, Angelo, Mandy",
    "nani": "- Find brawlers that can chip her to avoid giving Return to Sender value as well as easily dodge her main attack and super\n- Max, Leon, Gene",
    "edgar": "- Outrange him or deal with him up close with crowd control.\n- Cordelius, Surge, El Primo, Fang, Otis, Buzz, Stu, Shelly",
    "griff": "- Get out of his range which he spends a lot of time attacking in or beat him at midrange.\n- Stu, Bo, Bea, Spike",
    "grom": "- Get close and apply pressure\n- Fang, Mortis, Darryl, Mico, Edgar",
    "gale": "- Don't let him charge super by outranging him or peaking behind walls well and destroy walls so he can't utilize the stun with his super as much\n- Crow, Spike, Janet, Bea, Belle",
    "bonnie": "- Punish her Clyde form for slow attack and movement speed, find a way to best mitigate her Bonnie form\n- Colette, Fang, Meg",
    "hank": "- Use a brawler that can tank one shot from Hank and then melt him before he can deal another one, or outrange him before he can approach you and waste his big bubble\n- Shelly, Colette, Buzz, Fang, El Primo, Gale",
    "mortis": "- Don't let him get close to your or destroy him for trying to go through you\n- Shelly, Otis, Maisie, Surge",
    "tara": "- Splash through her shadows or destroy her grass for ambushes\n- Emz, Sandy, Nita, Amber, Janet, Poco",
    "gene": "- Expect a pull and have an instantly spawnable gadget/super that can tank it or try to dodge it. Slow reload means overwhelmed by spawners or aggro.\n- Mr. P, Eve, Ruffs, Ash",
    "max": "- Slow her down or be able to waste her ammo and tank/heal it off\n- Crow, Gale, Pam, Stu, Poco",
    "melodie": "- Outrange or use hard cc to stop her. Move into her super trajectory to minimize note dmg\n- Pearl, R-T (Super when she dashes onto you), Cordelius (shadow realm removes notes), Charlie, Tanks, Surge (soft)",
    "mr. p": "- He is quite weak without his porters and can't deal with aggro well\n- Mortis, Jacky, Buzz, Sam, Janet, Amber, Edgar",
    "sprout": "- Assassins destroy Sprout, if not an assassin try breaking walls or dodging to get close\n- Mortis, Darryl, Mico, Edgar, Buzz",
    "byron": "- Cripple his healing or destroy him due to low health. Weak to aggro.\n- Piper, Buzz, Edgar, Mortis, Mico, Crow, Angelo, Mandy, Leon, Lily",
    "squeak": "- Easily gets overwhelmed by aggro due to his slow damage output\n- Buzz, Leon, Mortis, Carl, Max, Edgar, Fang",
    "gray": "- He plays like an assassin so just make it hard for him to teleport on you. Low reload spd/dps\n- Mr. P, Mico, Tanks",
    "spike": "- Squishy brawler, deal a lot of damage to him quickly or find a way to attack through his life plant. Can't handle throwers.\n- Grom, Sprout, Piper, Nani, Angelo, Squeak",
    "crow": "- Have something to tank his main attack and jumps or outrange and quickly kill him\n- Spike, Piper, Nani, Angelo, Belle, Gene, Mr. P",
    "leon": "- Use brawlers that can scout easily or are able to deal with his surprise attacks to prevent super chaining. Tanks are soft counters since they feed super, but can help defend teammates.\n- Crow, Stu, Tara, Amber, Jacky",
    "sandy": "- Outrange and cripple Sandy or be able to tank his low DPS\n- Rosa, Jacky, Nita, Ash, El Primo, Piper, Gene (vision on grassy maps)",
    "amber": "- Waste her ammo by dodging her attacks or burst her up close. Be wary of gadget if she's hugging a wall nearby.\n- Crow, Piper, Leon",
    "meg": "- Slow and medium range while in mech. Once you knock her out of mech, barely a threat\n- Colette, Lou, Lola, Gale",
    "chester": "- Can't deal much damage at a range so either move around and dodge shots or out damage/range him in a lane/wall peak situation\n- Stu, Tara, Sandy",
    "surge": "- Don't let him get that first upgrade, if he can't he isn't a threat, if he does don't let him keep upgrading by having gadgets or spawnables to tank his shots due to slow reload\n- throwers, Spike, Tara, Eve, Mr. P",
    "colette": "- Don't be a tank and you already have a decent advantage into the matchup, swarm her with spawners since her damage is low against them or consistently heal/have a shield\n- Belle, Piper, Throwers, Griff (business resilience), Poco, Leon (invisiheal), Mr. P",
    "lou": "- Escape from his super or outrange him to avoid getting frozen. Or contest area denial.\n- Bo, Bea, Squeak, Buster, Max, Belle",
    "ruffs": "- Hit through his sandbags or be tanky enough to absorb his hits\n- (throwers), (assassins), Darryl, Carl",
    "belle": "- Outrange her with other snipers, or play agro/throwers\n- Nani, Piper, Mandy, Fang, Leon, Edgar",
    "buzz": "- Have a way to move away or to stun Buzz before he stuns you\n- Stu, Surge, Gale, Jacky, Maisie, Shelly, Otis",
    "ash": "- Splash through his rats, and find a way to stun him or prevent him from getting a lot of rage and hitting hard. Brawlers that can get on top of him and win 1v1 are good vs Ash.\n- Darryl, Rosa, El Primo, Lou, Gale, Buster",
    "lola": "- Punish Lola for using her ego by hitting both of them or outsnipe her\n- Belle, Penny, Janet, Amber, Jessie",
    "fang": "- Spawnables and some form of counter play when he jumps onto you is necessary, with the stun you have to be faster than him as well\n- Surge, Otis, R-T, Maisie, Jacky, Charlie, Cordelius",
    "eve": "- Splash her hatchlings and avoid the big egg shot to have her retreat for control\n- Penny, Janet, Poco, Max",
    "janet": "- Outrange her or be able to deal with her chip damage before she can fly away. Lacks DPS to beat aggro\n- Sam, Fang, Jacky, Bonnie, Piper, Nani",
    "otis": "- Outrange him and don't rely on up close burst damage or use a spawnable to tank the shot\n- Spike, Stu, Pearl, Piper, Lola",
    "sam": "- Don't let him get back his knucklebusters and be aware of them when he's coming for you so you can dodge or not get pulled\n- Gale, Maisie, Lou, El Primo",
    "buster": "- Don't let him get the surprise on you with his gadget or super, flank him to get past his super or be patient for it to run out. Tanks outdps him close range.\n- Jacky, Rosa, Surge, Darryl, Buzz, Mr. P",
    "mandy": "- Know where she is and always be aware of attacks you can't see, she is weak to agro or anything forcing her to move\n- Fang, Mr. P, Nani, Mico, Mortis, Angelo",
    "r t": "- Dodge his shots well since his attack is thin and be able to escape from him when he changes forms\n- Charlie, Bo, Nani, Mr. P",
    "maisie": "- Don't let her predict where you're going or slightly outrange her and be aware of her Disengage gadget and super.\n- Spike, Stu, Bo, Surge, Tara, Belle",
    "cordelius": "- Be aware of either him jumping on you with gadget or after shadow realm is over and using mute. You can waste shadow realm by being fidgety while he’s aiming it or running away when you get hit.\n- Spike, Tara, Stu",
    "charlie": "- Outburst her or outsustain her. Take advantage of slow projectile speed at max range on squishy brawlers. She has low dmg in 1v1 so if you have a way to handle spiders (pierce), you will win.\n- Janet, Tara, Emz, Buster, Sandy, Larry",
    "larry": "- Thrower counters and some way to deal with lawrie will help a lot.\n- Edgar, Mortis, Mico, Gray, Stu",
    "larry and lawrie": "- Thrower counters and some way to deal with lawrie will help a lot.\n- Edgar, Mortis, Mico, Gray, Stu",
    "lawrie": "- Thrower counters and some way to deal with lawrie will help a lot.\n- Edgar, Mortis, Mico, Gray, Stu",
    "willow": "- Usual thrower counters will do well vs willow. Willow also does poorly into tanks, esp if they can heal due to DoT.\n- Fang, Sam, Mico, Edgar, Mortis, Gray, Stu",
    "mico": "- Countered by any high hp brawler or fast brawler.\n- Fang, Edgar, Surge, Stu, tanks",
    "pearl": "- Aggressive playstyle to force her to shoot constantly will keep her dmg low.\n- colette, Charlie, Bo",
    "chuck": "- Weak 1v1. Assassinate him after he super to prevent him from superchaining.\n- Charlie (super), Lou, Crow (heal delay), 8-bit, Otis (super), Cordelius (super), Angelo, Eve",
    "doug": "- Don't let him get near you to charge his super. If you prevent him from super cycling and pumping dmg, not a major threat. \n- Any tank counter especially good. colette, Otis, Surge",
    "kit": "- Kit wants to jump on squishy brawlers. Any tank deletes Kit\n- Cordelius, Charlie, R-T, Fang, Edgar, Mico, Pearl",
    "lily": "- He can pop out of anywhere with vanish gadget. Tanks/shotgunners outdps him. Do not play 6k hp brawlers (colt, rico, etc.) or you will get one shot.\n- Frank, Meg, Chester, R-T, 8-bit, Tanks(Rosa,Jacky,etc)",
    "angelo": "- High upfront burst dmg, low overall dps and reload. Dodge his charged shot and he's not a major threat. Be careful hiding behind a wall if you're low due to his gadget.\n- Max, Draco, Throwers, Nani (gadget), Mr. P, Eve, Gray (50% less dmg SP)",
    "draco": "- Keep in mind his sweetspot and ban out healing comps that synergize with him (Kit, Byron)\n- Frank, Buzz, Cordelius (Soft Counter), Colette, Brawlers who interrupt his super work if you're fast (Gale, Surge)",
    "berry": "- Tanks and mobility overwhelm him. Same weaknesses as classic throwers\n- Melodie, Max, Mico, Mortis, Edgar, Lily, Bibi, Frank, etc.",
    "clancy": "- Weak vs long range brawlers or throwers on some maps who can stay out of range. Try not to feed him his upgrades.\n- Belle, Piper, Byron, etc.",
    "moe": "- Weak in small form if you are close. Be careful of diagonals for stacked shots.\n- R-T",
    "kenji": "- Similar counters to mortis. When he supers, look for small white smoke to see where he will be afters super.\n- Moe, Gale, Clancy, Surge, Rico (gadget), Stu, R-T",
    "juju": "- Too new but classic thrower counters are good and watch out for water maps preventing assassins from hitting her",
    "shade": "- Weak to tanks and wallbreaks (that aren't too squishy).\n- Jacky, Stu, Frank, Hank, R-T, Doug, Surge",
    "meeple": "- Meeple is low dps and slow reload. Also midrange so loses to snipers on long range maps.\n- Nita, majority of tanks, Mr. P, Tara (shadow gadget), Charlie (spiders)",
    "ollie": "- Extremely low dps. Just don't chase him when he supers to avoid getting hypnotized.\n - Tanks and Tank Counters"
}


# Processed JSON with "tips" and "counters" fields
processed_data = {}

for key, value in data.items():
    split_values = value.split("\n")
    if len(split_values) == 2:
        processed_data[key] = {
            "tips": split_values[0].strip(),
            "counters": split_values[1].strip()
        }
    else:
        processed_data[key] = {
            "tips": value.strip(),
            "counters": ""
        }

# Convert to JSON format
formatted_json = json.dumps(processed_data, indent=4)

# Save to file
with open("new_counters.json", "w") as f:
    f.write(formatted_json)
