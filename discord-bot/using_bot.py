import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# interesting - with `Client` you get more flexibility, with `commands.Bot` you're
# bound to the well-known pattern of using prefixes.
# update - there's actually more to it - list of cmds, converting args, validations
bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


@bot.command(name="sepultura", help="Responds with a random excerpt from Sepultura lyrics")
async def sepultura(ctx):

    sepultura_lyrics = [
        "Look at me, my feelings turn STRONGER THAN HATE",
        "Life ends, feeling death... SLAVES OF PAIN!",
        ("Nonconformity in my inner self," "Only I guide my inner self"),
    ]

    response = random.choice(sepultura_lyrics)
    await ctx.send(response)


# Function annotations will force the conversion from `str` to desired type
@bot.command(name="roll_dice", help="Simulates rolling dice.")
async def roll_dice(ctx, number_of_dice: int, number_of_sides: int):
    dice = [str(random.choice(range(1, number_of_sides + 1))) for _ in range(number_of_dice)]
    await ctx.send(", ".join(dice))


@bot.command(name="create-channel")
@commands.has_role("admin")
async def create_channel(ctx, channel_name):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)

    if existing_channel:
        await ctx.send(f"Channel {channel_name} already exists.")
        return

    print(f"Creating channel {channel_name}...")
    await guild.create_text_channel(channel_name)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("You do not have the correct role for this command.")


bot.run(TOKEN)
