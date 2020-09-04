import discord
import os
import AlowisBot # noqa
client = discord.Client()


Bot = AlowisBot.Bot()


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="type !help"))


@client.event
async def on_member_join(member):
    await Bot.welkomsbericht(member)


@client.event
async def on_message(message):
    await Bot.commmando(message)

# LAATSTE LIJN
client.run(os.environ.get("ALOWISBOT"))
