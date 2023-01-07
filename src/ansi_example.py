import discord
from discord.ext import commands
from io import BytesIO
from os import environ

import libs.chat_exporter as chat_exporter
from libs.chat_exporter.chat_exporter import Transcript

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=("t.",), case_insensitive=True, intents=intents)

TOKEN = environ["TOKEN"]


@bot.event
async def on_ready():
    chat_exporter.init_exporter(bot)
    print("READY")


bb = "\u001b[34;1m" # bright blue
w = "\u001b[37m" # white
r = "\u001b[31m" # red
g = "\u001b[32m" # green
b = "\u001b[1m" # bold
u = "\u001b[4m" # underline
re = "\u001b[0m" # reset
ansi = f"```ansi\n" \
       f"{bb+b+u}All Plugins:{re}\n\t{w}automod, modmail, giveaways, tickets, config{re}\n\u200b\n" \
       f"{bb+b+u}Enabled Plugins:{re}\n\t{g}modmail, tickets, config{re}\n\u200b\n" \
       f"{bb+b+u}Disabled Plugins:{re}\n\t{r}automod, giveaways{re}\n\u200b\n" \
       f"```"


@bot.command(aliases=["ex"])
async def example(ctx):
    await ctx.send(ansi)

    messages = [message async for message in ctx.channel.history(limit=20)]
    transcript: Transcript = await chat_exporter.raw_export(ctx.channel, messages)

    # using `transcript.encoded` will avoid weird characters showing up (encoding="cp1252")
    # use `transcript.html` if you want the standard html string
    file = discord.File(BytesIO(transcript.encoded), "transcript.html")

    msg = await ctx.channel.send("Logging Channel...", file=file)

    # By sending the file first, we can the url of that file and add it to the url of the online file viewer
    await msg.edit(content="Channel logged.",
                   embed=discord.Embed(
                       title="Transcript",
                       description=f"[Link to transcript](https://fileviewer.janvh.tk?url={msg.attachments[0].url})"
                   ))


bot.run(TOKEN)
