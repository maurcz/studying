import os
import random

import discord
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")


# -------
# Example - Responding to events with subclasses

# class CustomClient(discord.Client):
#     async def on_ready(self):
#         print(f"{self.user} has connected to Discord!")


# client = CustomClient()
# client.run(TOKEN)


# -------

# Intents - new since the article came out. Toggles in the dev portal.
intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():

    # queries for info:
    # guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)

    # same data with helpers
    guild = discord.utils.get(client.guilds, name=GUILD)

    print(f"{client.user} has connected to Discord!")
    print(f"Currently connected to guild {guild.name}(id: {guild.id}) ")

    members = ", ".join([member.name for member in guild.members])
    print(f"Guild members: {members}")


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f"Hi {member.name}, welcome to my Discord server!")


@client.event
async def on_message(message):

    # important to prevent the bot from responding to its own messages
    if message.author == client.user:
        return

    sepultura_lyrics = [
        "Look at me, my feelings turn STRONGER THAN HATE",
        "Life ends, feeling death... SLAVES OF PAIN!",
        ("Nonconformity in my inner self," "Only I guide my inner self"),
    ]

    if message.content == "Sepultura!":
        response = random.choice(sepultura_lyrics)
        await message.channel.send(response)

    # way to force an exception to play with error-handling scenarios
    elif message.content == "raise-exception":
        raise discord.DiscordException


@client.event
async def on_error(event, *args, **kwargs):
    with open("error.log", "a") as f:
        if event == "on_message":
            f.write(f"Unhandled message: {args[0]}\n")
        else:
            raise


client.run(TOKEN)
