import discord
from commands import special_commands # noqa


# leest txt bestand en zet dit om in lijst
def commando_list():
    # lees txt bestand en haal commano's hier uit
    commands_txt = open("commands/commando.txt", "r", encoding="utf8")
    first_line = commands_txt.readline()  # sla voorbeeld lijn over
    first_line += ""  # doet niets

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

    return commando_lst


class Bot:

    def __init__(self):
        self.commando_lst = commando_list()
        self.message = None  # laatst verstuurde bericht

    # stuur bericht
    async def send(self, channel, bericht):
        message = await channel.send(content=None, embed=bericht)
        self.message = message  # sla bericht op als laatst verstuurde bericht

    # reactie functie
    async def reaction(self, emoji, message=None):
        if not message:
            message = self.message
        await message.add_reaction(emoji)

    # welcome funtie
    async def welkomsbericht(self, member):
        if not member.bot:
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

                    await self.send(channel, bericht)

    # controleert of gebruiker recht heeft op commando
    @staticmethod
    def controleer_recht(message, key):
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
                recht = False

        return recht

    # commando functie
    async def commmando(self, message):
        if not message.author.bot:
            # commando niet hoofdletter gevoelig
            commando = str(message.content)
            if commando:  # voorkomt error bij volgende lijn moest string leeg zijn
                if commando[0] == "!":  # als de string begint met "!"
                    commando_split = commando.split(" ")  # indien er een spacitie is word er gesplitst

                    # overloop lijst met commando's
                    for key in self.commando_lst:
                        if key[0] == commando_split[0].lower():

                            recht = self.controleer_recht(message, key)

                            # indien de juiste rechten
                            if recht:
                                if key[1][1] == "-1":  # indien een speciaal commando
                                    await special_commands.zoek(key[0], commando_split[1:], message, self)
                                    # zoek_speciaal_commando(!commando, specifiëring, bericht, send_functie)
                                else:
                                    titel = key[1][0]
                                    antwoord = key[1][1]

                                    # stuur bericht
                                    bericht = discord.Embed(title=titel, description=antwoord)
                                    await self.send(message.channel, bericht)  # stuur antwoord
