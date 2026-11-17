"""Discord entrypoint for the prompt-powered meme bot."""

from __future__ import annotations

import os

import discord
from discord import app_commands

from meme_generator import generate_meme


class MemeBot(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.none()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        guild_id = os.getenv("DISCORD_GUILD_ID")
        if guild_id:
            guild = discord.Object(id=int(guild_id))
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        else:
            await self.tree.sync()


bot = MemeBot()


@bot.tree.command(name="meme", description="Generate a meme from a prompt.")
@app_commands.describe(prompt="What should the meme say?")
async def meme(interaction: discord.Interaction, prompt: str) -> None:
    await interaction.response.defer()
    try:
        image = generate_meme(prompt)
    except ValueError as error:
        await interaction.followup.send(str(error), ephemeral=True)
        return

    await interaction.followup.send(file=discord.File(image, filename="meme.png"))


def main() -> None:
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_TOKEN environment variable is required.")
    bot.run(token)


if __name__ == "__main__":
    main()
