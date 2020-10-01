import discord
import os
import AlowisBot # noqa
client = discord.Client()

# maakt bot object aan
Bot = AlowisBot.Bot(client)


# stelt kijkt naar status in
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="type !help"))


# welkomsbericht
@client.event
async def on_member_join(member):
    await Bot.welkomsbericht(member)


# checkt voor commando's
@client.event
async def on_message(message):
    await Bot.commmando(message)

# LAATSTE LIJN
client.run(os.environ.get("ALOWISBOT"))
