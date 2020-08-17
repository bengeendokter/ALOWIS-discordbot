import discord
import os

client = discord.Client()


# nieuw lid
@client.event
async def on_member_join(member):
    for channel in member.guild.channels:
        if str(channel) == "ouders-café☕":
            beschrijving = str(f"Welkom {member.mention} in Café ALOWIS. "
                               + "De plaats waar jij als ouder kan chatten met andere ouders, "
                               + "vragen kan stellen aan leiding en "
                               + "op de hoogte wordt gehouden van nieuwtjes binnen de scouts. "
                               + "Verplaats u naar de juiste tak van uw zoon "
                               + "of blijf gerust wat hangen in deze chat.\n\n"
                               + "Stevige scoutslinker, de AlowisBot!")

            bericht = discord.Embed(description=beschrijving)

            await channel.send(content=None, embed=bericht)


# commando's
@client.event
async def on_message(message):
    categories = ["Leiding ⚜", "Comités 🛠"]  # lijst met toegestane categorieën

    if str(message.channel.category) in categories:
        if message.content == "!drive":  # drive commando
            titel = "Link naar de leidingsdrive"
            beschrijving = "https://drive.google.com/drive/folders/1QVF_1TXRfwHasr0Qwde_DiljD6XcrzWG?usp=sharing"

            bericht = discord.Embed(title=titel, description=beschrijving)

            await message.channel.send(content=None, embed=bericht)


# laatste lijn
client.run(os.environ.get('ALOWISBOT'))
