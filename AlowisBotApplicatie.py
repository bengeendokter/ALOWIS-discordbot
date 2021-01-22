import discord
import os
import AlowisBot # noqa

# geef toestemming om on_member_join te kunnen gebruiken
intents = discord.Intents.default()
intents.members = True
intents.presences = True

# maakt client aan
client = discord.Client(intents=intents)

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

# checkt voor reacties van gebruikers

# toevoegen van reactie
@client.event
async def on_raw_reaction_add(payload):
    await Bot.reaction_add(payload)

# verwijderen van reactie
@client.event
async def on_raw_reaction_remove(payload):
    await Bot.reaction_remove(payload)

# LAATSTE LIJN
client.run(os.environ.get("ALOWISBOT"))
