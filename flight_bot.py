import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from gpt4_summary import generate_summary

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="f!", intents=intents)


@bot.command()
async def summarize(ctx, id):
    channel = await ctx.guild.fetch_channel(id)
    messages = []

    async for message in channel.history(limit=150):
        if message.reference is not None:
            replied_message = await channel.fetch_message(message.reference.message_id)
            messages.append(f"{message.author.display_name}: {message.content} (replying to: {replied_message.content})")
        else:
            messages.append(f"{message.author.display_name}: {message.content}")

    messages = "\n".join(messages[1:][::-1])
    summary = generate_summary(messages)
    with open("summary.txt", "w") as file:
        file.write(summary)

    with open("summary.txt", "rb") as file:
        await ctx.send("DISCLAIMER: The following summary is generated using AI "
                       "and may not be completely accurate.", file=discord.File(file, filename="summary.txt"))


bot.run(TOKEN)