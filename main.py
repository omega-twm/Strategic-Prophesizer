import os
import json
from dotenv import load_dotenv

import discord
from discord import app_commands

load_dotenv()

intents = discord.Intents.default()  # message_content not needed for slash commands

def load_keywords():
    with open("keywords.json", "r", encoding="utf-8") as f:
        return json.load(f)

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        guild = discord.Object(id = os.getenv("TEST_GUILD_ID"))
        self.tree.copy_global_to(guild=guild)
        # Syncs your slash commands with Discord so they show up in the client.
        await self.tree.sync(guild=guild) # remove guild=guild to push the bot globally

    async def on_ready(self):
        print(f"Logged on as {self.user}!")

client = MyClient()

# Placeholder data — replace with your real keyword info (dict, file, DB, etc.)
KEYWORDS = load_keywords()

@client.tree.command(name="lookup", description="Get info about a keyword")
@app_commands.describe(keyword="The keyword you want info about")
async def keyword(interaction: discord.Interaction, keyword: str):
    info = KEYWORDS.get(keyword.lower())
    if info:
        await interaction.response.send_message(info)
    else:
        await interaction.response.send_message(f"No info found for '{keyword}'.")

def main():
    print("Hello from strategic-prophesizer-bot!")
    client.run(os.getenv("DISCORD_TOKEN"))

if __name__ == "__main__":
    main()
