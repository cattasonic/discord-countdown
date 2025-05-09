import discord
from discord.ext import commands
from datetime import datetime
import pytz  # Use pytz for time zone support
import os

TOKEN = os.environ.get("TOKEN")

# Define the Vancouver timezone using pytz
vancouver_tz = pytz.timezone("America/Vancouver")

# The final date (March 27, 2026, 5:00 PM Vancouver time)
END_DATE = datetime(2026, 3, 27, 17, 0, 0)
END_DATE = vancouver_tz.localize(END_DATE)  # Localize to Vancouver time

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command(name="done")
async def countdown(ctx):
    now = datetime.now(vancouver_tz)
    remaining = END_DATE - now

    if remaining.total_seconds() > 0:
        days = remaining.days
        hours, remainder = divmod(remaining.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        await ctx.send(f"We're done in **{days}d {hours}h {minutes}m {seconds}s**.")
    else:
        await ctx.send("We're already done!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    triggers = [
        "when are we done?",
        "are we done yet?",
        "how much longer?",
        "how long until we're done?",
        "when is it over?",
        "when are we graduating?",
        "finish now?",
        "we done yet?",
        "done?",
        "we done?",
        "finito?"
    ]

    if message.content.lower().strip() in triggers:
        now = datetime.now(vancouver_tz)
        remaining = END_DATE - now

        if remaining.total_seconds() > 0:
            days = remaining.days
            hours, remainder = divmod(remaining.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            await message.channel.send(f"We're done in **{days}d {hours}h {minutes}m {seconds}s**.")
        else:
            await message.channel.send("We're already done!")

    await bot.process_commands(message)

bot.run(TOKEN)
