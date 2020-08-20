import discord
import os
from commands import special_commands # noqa
client = discord.Client()


# commando_dic wordt aangemaakt
# lees txt bestand en haal commano's hier uit
commands_txt = open("commands/commando.txt", "r", encoding="utf8")
first_line = commands_txt.readline()  # sla voorbeeld lijn over

# maak nodige lijsten en dictionairies aan
commando_lst = []

categorie_dic = {}
kanaal_dic = {}
user_dic = {}

# overloop alle commando's
for regel in commands_txt:

    # onderscheid de gegevens van elkaar in een lijst
    lijst = regel.strip("\n").split(",")

    # verdeel elk gegeven verder en geef een duidelijke naam
    commando_str = lijst[0]
    tit_ant_bes_lst = [lijst[1], lijst[2], lijst[6]]

    categorie_str_lst = lijst[3].split(";")
    kanaal_str_lst = lijst[4].split(";")
    user_str_lst = lijst[5].split(";")

    # houd rechten voor commando's bij in apparte dictionairies
    for categorie in categorie_str_lst:
        if categorie:
            categorie_dic[categorie] = categorie_dic.get(categorie, []) + [{commando_str: tit_ant_bes_lst}]
    for kanaal in kanaal_str_lst:
        if kanaal:
            kanaal_dic[kanaal] = kanaal_dic.get(kanaal, []) + [{commando_str: tit_ant_bes_lst}]
    for user in user_str_lst:
        if user:
            user_dic[user] = user_dic.get(user, []) + [{commando_str: tit_ant_bes_lst}]

    # hou alles bij in een lijst van lijsten
    recht_lst = [categorie_str_lst, kanaal_str_lst, user_str_lst]

    commando_lst.append([commando_str, tit_ant_bes_lst, recht_lst])


# nieuw lid
@client.event
async def on_member_join(member):

    # zoek het juiste kanaal en plaats het welkoms bericht
    for channel in member.guild.channels:
        if str(channel) == "ouders-café☕":
            beschrijving = str(f"Welkom **{member.name}** in Café ALOWIS. "
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

    # commando niet hoofdletter gevoelig
    commando = str(message.content).lower()
    if commando:  # voorkomt error bij volgende lijn moest string leeg zijn
        if commando[0] == "!":  # als de string begint met "!"
            commando_split = commando.split(" ")  # indien er een spacitie is word er gesplitst

            # overloop lijst met commando's
            for key in commando_lst:
                if key[0] == commando_split[0]:
                    recht = True  # indien er een match is, stel standaard waarde in

                    # controleer rechten

                    # categorie recht
                    if key[2][0][0]:
                        if str(message.channel.category) not in key[2][0]:
                            recht = False

                    # kanaal recht
                    if key[2][1][0]:
                        if str(message.channel) not in key[2][1]:
                            recht = False

                    # gevruiker recht
                    if key[2][2][0]:
                        if str(message.author) not in key[2][2]:
                            recht = True

                    # indien de juiste rechten

                    if recht:
                        if key[1][1] == "-1":  # indien een speciaal commando
                            titel, antwoord = special_commands.special(key[0], commando_split[1:])
                        else:
                            titel = key[1][0]
                            antwoord = key[1][1]

                        # stuur bericht
                        bericht = discord.Embed(title=titel, description=antwoord)
                        await message.channel.send(content=None, embed=bericht)  # stuur antwoord


# laatste lijn
client.run(os.environ.get("ALOWISBOT"))
