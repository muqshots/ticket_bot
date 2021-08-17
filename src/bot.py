from io import BytesIO
import libs.chat_exporter as chat_exporter
from random import sample
from os import environ
from discord.ext import commands
import discord
from discord_slash.client import SlashCommand
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
import asyncio

bot = commands.Bot(command_prefix=("t.",), case_insensitive=True)
slash = SlashCommand(bot, sync_commands=True)
bot.remove_command("help")

TOKEN = environ["TOKEN"]


@bot.event
async def on_ready():

    chat_exporter.init_exporter(bot)

    print("READY")


@bot.event
async def on_guild_join(guild):

    cat = discord.utils.get(guild.categories, name="Open tickets")

    if not cat:
        cat = await guild.create_category(name="Open tickets")


@bot.command()
async def ticketchannel(ctx):
    action_row = create_actionrow(
        *[
            create_button(
                style=ButtonStyle.blue,
                label="Blue Button fuck yea",
                emoji="🎟",
                custom_id="create_ticket"
            )
        ]
    )

    await ctx.send("Create a new ticket here!", components=[action_row])


@slash.component_callback()
async def create_ticket(ctx):

    gen_id = "".join(sample(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], 5))
    ticket_name = f"{ctx.author.name.lower()}-{gen_id}"

    cat = discord.utils.get(ctx.guild.categories, name="Open tickets")

    if not cat:
        cat = await ctx.guild.create_category(name="Open tickets")

    ticket_channel = await ctx.guild.create_text_channel(
        name=ticket_name,
        category=cat,
        position=0,
        reason="New Ticket Opened"
    )
    await ticket_channel.set_permissions(ctx.author, read_messages=True, send_messages=True, read_message_history=True)

    action_row = create_actionrow(
        *[
            create_button(
                style=ButtonStyle.red,
                label="Close da Ticket",
                emoji="❌",
                custom_id="close_ticket"
            )
        ]
    )

    await ticket_channel.send(f"Yo press dis to close ticket", components=[action_row])
    await ticket_channel.send(f"{ctx.author.mention}, Type in your issue here!")
    delete_soon = await ctx.send("Ticket created!, I've pinged you in the channel.")
    await asyncio.sleep(1)
    await delete_soon.delete()


@slash.component_callback()
async def close_ticket(ctx):

    log_channel = discord.utils.get(ctx.guild.text_channels, name="ticket-logs")

    if not log_channel:

        action_row = create_actionrow(
            *[
                create_button(
                    style=ButtonStyle.red,
                    label="Force close",
                    emoji="❌",
                    custom_id="force_close_ticket"
                )
            ]
        )

        await ctx.send("No channel named ticket-logs, force closing this ticket will not log the contents.", components=[action_row])

        return

    await log_channel.send("logging ticket")

    transcript = await chat_exporter.export(ctx.channel)

    if not transcript:
        log_channel.send(f"{ctx.channel.name} closed without any messages sent")
        return

    transcript_file = discord.File(BytesIO(transcript.encode()),
                                   filename=f"{ctx.channel.name}-transcript.html")

    await log_channel.send(f"{ctx.channel.name}-transcript.html", file=transcript_file)

    await ctx.channel.delete()


@slash.component_callback()
async def force_close_ticket(ctx):
    await ctx.channel.delete()


bot.run(TOKEN)
