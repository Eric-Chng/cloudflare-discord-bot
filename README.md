# Brawl Draft Discord bot

Brawl Draft bot is a simple bot that utilizes Cloudflare's free Worker hosting to host a serverless bot with multiple commands. Command functionality is powered by json files and easily modifiable or extendable, even for non technically literate people.

The tutorial for building awwbot is [in the developer documentation](https://discord.com/developers/docs/tutorials/hosting-on-cloudflare-workers)
But kind of sucks unless you are very experienced building discord bots.

## Generate system prompt (Python)
```bash
python3 scripts/generate_system_prompt.py
```
This writes `src/system_prompt.js` with identical output to the Node CLI.

## Personal Recommendations/Tips
- Make a json of secrets and do `wrangler secret:bulk <filename>` to upload secrets to cloudflare
- Google how to add secrets to repo. Add cloudflare secrets to repo
- Ensure you are running Node 18+
- Imo test/lint workflows were not very helpful and too strict to be all that useful
- Don't forget to edit wrangler.toml to match your worker/bot name
- `wrangler login` to login to wrangler
  

Test locally like: 
GEMINI_API_KEY=<key> npm run chat:local -- "How do I draft on hard rock mine?"