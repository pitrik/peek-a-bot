import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import os
import re
import time
import logging
import aiohttp

logging.basicConfig(level=logging.DEBUG)

TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

tree = bot.tree

def parse_time_string(time_string: str) -> int:
    time_string = time_string.lower().strip()
    match = re.match(r"(\d+)\s*(seconds?|minutes?|hours?)", time_string)
    if not match:
        raise ValueError("Invalid time format. Use formats like '10 minutes', '2 hours', etc.")
    
    amount = int(match.group(1))
    unit = match.group(2)

    if 'second' in unit:
        return amount
    elif 'minute' in unit:
        return amount * 60
    elif 'hour' in unit:
        return amount * 3600
    else:
        raise ValueError("Invalid time unit.")

@bot.event
async def on_ready():
    try:
        print(f'Logged in as {bot.user}!')
        synced = await tree.sync()
        print(f"Synced {len(synced)} commands: {[cmd.name for cmd in synced]}")
    except Exception as e:
        print(f"Error during on_ready: {e}")

@tree.command(name="expire", description="Upload an image to expire after a delay")
@app_commands.describe(
    image="The image you want to expire",
    delay="How long until deletion (e.g. '10 minutes', '2 hours')",
    show_name="Whether to show your username in the deletion message (default True)",
    caption="Optional caption text to display below the image",
    spoiler="Whether to mark the image as a Discord spoiler (default False)"
)
async def expire(
    interaction: discord.Interaction,
    image: discord.Attachment,
    delay: str,
    show_name: bool = True,
    caption: str = None,
    spoiler: bool = False
):
    await interaction.response.defer(ephemeral=True)

    try:
        delay_seconds = parse_time_string(delay)

        if delay_seconds > 86400:
            await interaction.followup.send("Sorry, maximum delay is 24 hours.", ephemeral=True)
            return

        content = ""
        if caption:
            caption = caption.strip()
            if caption:
                content = f'\n\n"{caption}"'

        # Properly apply spoiler: download and rename file
        filename = f"SPOILER_{image.filename}" if spoiler else image.filename
        async with aiohttp.ClientSession() as session:
            async with session.get(image.url) as resp:
                if resp.status != 200:
                    await interaction.followup.send("Failed to download the image.", ephemeral=True)
                    return
                data = await resp.read()

        with open(filename, "wb") as f:
            f.write(data)

        file = discord.File(filename)

        sent_message = await interaction.channel.send(file=file, content=content)

        os.remove(filename)

        await interaction.followup.send(f"Your image will be deleted in {delay}!", ephemeral=True)

        await asyncio.sleep(delay_seconds)
        await sent_message.delete()

        if show_name:
            await interaction.channel.send(
                f"🧹 An image uploaded by {interaction.user.mention} was deleted after {delay}."
            )
        else:
            await interaction.channel.send(
                f"🧹 An image was deleted after {delay}."
            )

    except ValueError as ve:
        await interaction.followup.send(str(ve), ephemeral=True)
    except Exception as e:
        print(e)
        await interaction.followup.send("Something went wrong. Please try again.", ephemeral=True)

@tree.command(name="peekabot", description="Show instructions for using Peek-a-bot")
async def peekabot_help(interaction: discord.Interaction):
    help_text = (
        "**Peek-a-bot Usage Instructions**\n\n"
        "- **/expire** — Upload an image you want to delete after a certain amount of time.\n"
        "  - **Image**: Upload your picture 📷\n"
        "  - **Delay**: How long to wait before deleting (e.g., '10 minutes', '2 hours', '1 day')\n"
        "  - **Show Name**: Choose if you want your username shown in the deletion message (default: yes)\n"
        "  - **Caption**: (Optional) Add a short message under your image\n"
        "  - **Spoiler**: (Optional) Blur image behind spoiler until clicked\n\n"
        "❗ **Note**: Deleting an image also removes any reactions attached to it."
    )

    await interaction.response.send_message(help_text, ephemeral=True)

@tree.command(name="testdelete", description="Simple test to send and delete a message after 10 seconds")
async def testdelete(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    try:
        msg = await interaction.channel.send("This is a test message and will auto-delete in 10 seconds.")
        await interaction.followup.send("Test message sent — it will delete soon!", ephemeral=True)
        await asyncio.sleep(10)
        await msg.delete()
    except Exception as e:
        print(e)
        await interaction.followup.send("Failed to send or delete message.", ephemeral=True)

while True:
    try:
        bot.run(TOKEN)
    except Exception as e:
        print(f"Bot crashed: {e}")
        print("Restarting in 5 seconds...")
        time.sleep(5)