import os
import json
from dotenv import load_dotenv

import discord
from discord import app_commands

load_dotenv()
intents = discord.Intents.default()  # message_content not needed for slash commands


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

KEYWORDS = load_json("keywords.json")
MODELS = load_json("models.json")
TEST_GUILD_ID = int(os.getenv("TEST_GUILD_ID"))


class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):

        guild = discord.Object(id = TEST_GUILD_ID)


        self.tree.copy_global_to(guild=guild)
        # Syncs your slash commands with Discord so they show up in the client.
        await self.tree.sync(guild=guild) # remove guild=guild to push the bot globally

    async def on_ready(self):
        print(f"Logged on as {self.user}!")

client = MyClient()

lookup_group = app_commands.Group(name="lookup", description="Look up rules info")

@lookup_group.command(name="keyword", description="Get info about a keyword")
@app_commands.describe(keyword="The keyword you want info about")
async def lookup_keyword(interaction: discord.Interaction, keyword: str):
    info = KEYWORDS.get(keyword.lower())
    if info:
        await interaction.response.send_message(info)
    else:
        await interaction.response.send_message(f"No info found for '{keyword}'.")

@lookup_group.command(name="model", description="Get a model's warband entry")
@app_commands.describe(model="The model's name")
async def lookup_model(interaction: discord.Interaction, model: str):
    entry = MODELS.get(model.lower())
    if not entry:
        await interaction.response.send_message(f"No model found for '{model}'.")
        return

    embed = discord.Embed(
        title=f"{entry['name']} — Cost: {entry['cost']}",
        description=entry["description"],
        color=discord.Color.dark_red(),
    )
    embed.add_field(name="Movement", value=entry["movement"], inline=True)
    embed.add_field(name="Ranged", value=entry["ranged"], inline=True)
    embed.add_field(name="Melee", value=entry["melee"], inline=True)
    embed.add_field(name="Armour", value=entry["armour"], inline=True)
    embed.add_field(name="Base", value=entry["base"], inline=True)
    embed.add_field(name="Battlekit", value=entry["battlekit"], inline=False)
    embed.add_field(name="Abilities", value=entry["abilities"], inline=False)
    embed.add_field(name="Keywords", value=entry["keywords"], inline=False)

    await interaction.response.send_message(embed=embed)

client.tree.add_command(lookup_group)

def main():
    print("Hello from strategic-prophesizer-bot!")
    client.run(os.getenv("DISCORD_TOKEN"))

if __name__ == "__main__":
    main()
