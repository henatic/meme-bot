# meme-bot

A Discord bot that turns a prompt into a meme and uploads it to the channel.

## Setup

1. Create a Discord application and bot, then invite it with the `bot` and
   `applications.commands` scopes.
2. Install the dependencies:

   ```sh
   python -m pip install -r requirements.txt
   ```

3. Set the bot token and run it:

   ```sh
   export DISCORD_TOKEN="your-bot-token"
   python bot.py
   ```

   For immediate slash-command registration in one server, also set
   `DISCORD_GUILD_ID`. Without it, the command is registered globally and may
   take up to an hour to appear.

Use `/meme prompt:<your idea>` in a server where the bot has permission to send
messages and attach files.
