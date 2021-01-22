import random
import discord

# VOORBEREIDINGEN
# open en overloop slagzinnen.txt
zinnen = open("commands/slagzinnen.txt", "r", encoding="utf8")
zinnen_lst = []

# voeg zinnen toe aan lijst
for zin in zinnen:
    zinnen_lst.append(zin.strip("\n"))


# SPECIAALE COMMANDO'S

# poll functie
async def poll(specifiek_lst, message, bot):
    if len(specifiek_lst) <= 8:
        emoji_str = '🔴🟡🟢🔵🟣🟤⚫⚪'
        emoji = {}
        for index, symbool in enumerate(emoji_str):
            emoji[index + 1] = symbool
        # emoji = {1: "🔴", ...}

        bericht = discord.Embed(title="Poll")
        for nummer, optie in enumerate(specifiek_lst):
            bericht.add_field(value=emoji[nummer+1] + ' ' + optie, name="‍")
            # Zero Width Joiner zorgt voor betere layout on mobile

        await bot.send(message.channel, bericht)

        for number in range(1, len(specifiek_lst) + 1):
            await bot.reaction(emoji[number])


# random zin functie
async def loekentatjen(specifiek_lst, message, bot):

    # indien een extra gegeven en numeriek
    if specifiek_lst and specifiek_lst[-1].isdigit():
        index = int(specifiek_lst[-1])  # getal is index

        # indien gatal te groot, neem max getal
        if index > len(zinnen_lst):
            index = len(zinnen_lst)

    else:  # anders kies random index
        index = random.randint(1, len(zinnen_lst))

    antwoord = zinnen_lst[index - 1]
    titel = f"#{index}"

    bericht = discord.Embed(title=titel, description=antwoord)
    await bot.send(message.channel, bericht)  # stuur resultaat


# dobbel functie
async def dobbel(specifiek_lst, message, bot):
    index = 6
    if specifiek_lst and specifiek_lst[0].isdigit():
        index = int(specifiek_lst[0])

    getal = random.randint(1, index)

    bericht = discord.Embed(title=getal)
    await bot.send(message.channel, bericht)

# help functie
async def help_cmd(specifiek_lst, message, bot):
    specifiek_lst += []  # doet niets
    bericht = discord.Embed(title=f"Commando's voor {message.author.nick} in #{str(message.channel)}")

    for key in bot.commando_lst:
        if bot.controleer_recht(message, key):
            beschrijving = key[1][2] if key[1][2] else "?"
            bericht.add_field(name=key[0], value=beschrijving)

    await bot.send(message.channel, bericht)

# kapoenen ouder rol functie
async def kapoenen(specifiek_lst, message, bot):
    guild_id = message.guild.id
    guild = discord.utils.find(lambda g : g.id == guild_id, bot.client.guilds)

    role = discord.utils.get(guild.roles, name="Ouder van kapoen")
    member = discord.utils.find(lambda m : m.id == message.author.id, guild.members)
    
    bericht = discord.Embed(title=f"{message.author.nick} heeft nu de rol 'Ouder van kapoen'")
    await bot.send(message.channel, bericht)      
    await bot.role_add(role, member)

# funtie dictionairy
switcher = \
    {
        "!loeken": loekentatjen,
        "!poll": poll,
        "!dobbel": dobbel,
        "!help": help_cmd,
        "!kapoenen": kapoenen
    }


# EERST AANGEROEPEN ZOEK FUNCTIE
# zoekt juiste functie in de dictionairy
async def zoek(commando, specifiek_lst, message, bot):
    func = switcher[commando]
    await func(specifiek_lst, message, bot)
