import discord
from commands import special_commands # noqa


# leest txt bestand en zet dit om in lijst
def commando_list():
    # lees txt bestand en haal commano's hier uit
    commands_txt = open("commands/commando.csv", "r", encoding="utf8")
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
        lijst = regel.strip("\n").split("|")

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


# dict met alle leiding voor wie is leiding cnt cmd
leiding = \
    {
        "kapoenen": [":Ben:", ":Cedric:", ":Robbe:"],
        "welpen": [":Senne:", ":Brecht:", ":Joshua:", ":Joachim:"],
        "jong": [":DaanT:", ":Niels:", ":Boris:"],
        "verkenner": [":Samuel:", ":Tom:", ":Joeri:"],
        "jin": [":Servaas:"]
    }


class Bot:

    def __init__(self, client):
        self.commando_lst = commando_list()
        self.message = None  # laatst verstuurde bericht
        self.client = client

    # stuur bericht
    async def send(self, channel, bericht):
        message = await channel.send(content=None, embed=bericht)
        self.message = message  # sla bericht op als laatst verstuurde bericht

    # bot voegt reactie toe functie
    async def reaction(self, emoji, message=None):
        if not message:
            message = self.message
        await message.add_reaction(emoji)

    # bot ziet reaction add
    async def reaction_add(self, payload):
        message_id = payload.message_id
        if message_id == 777223060288831509:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g : g.id == guild_id, self.client.guilds)

            if payload.emoji.name == "😉":
                role = discord.utils.get(guild.roles, name="gelukt")
                member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
                
                
                await self.role_add(role, member)


    # bot ziet reaction remove
    async def reaction_remove(self, payload):
        message_id = payload.message_id
        if message_id == 777223060288831509:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g : g.id == guild_id, self.client.guilds)

            if payload.emoji.name == "😉":
                role = discord.utils.get(guild.roles, name="gelukt")
                member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
                
                
                await self.role_remove(role, member)

    # bot voegt rang toe
    async def role_add(self, role, member):
        await member.add_roles(role)

    # bot verwijderd rang
    async def role_remove(self, role, member):
        await member.remove_roles(role)

    # welcome funtie
    async def welkomsbericht(self, member):
        if not member.bot:
            # zoek het juiste kanaal en plaats het welkoms bericht
            for channel in member.guild.channels:
                if str(channel) == "ouders-café☕":
                    beschrijving = str(f"Welkom **{member.name}** in Café ALOWIS. "
                                       + "De plaats waar jij als ouder/lid kan chatten met anderen, "
                                       + "vragen kan stellen aan leiding en "
                                       + "op de hoogte wordt gehouden van nieuwtjes binnen de scouts. "
                                       + "Verplaats u naar de juiste tak "
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

            # controleer of bericht dm is
            if isinstance(message.channel, discord.channel.DMChannel):
                return await self.dm(message)

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

                else:
                    # indien geen commando, controleer op context commando
                    await self.context_cmd(message)

    # context commando
    async def context_cmd(self, message):
        tekst = message.content.lower()

        # wie is leiding context commando
        if "wie" in tekst and ("zijn" in tekst or "is" in tekst) \
                and ("leiding" in tekst or "leider" in tekst):

            found = False  # beginwaarde

            # overloop takken
            for tak in sorted(list(leiding.keys())):

                if not found:
                    if tak in tekst:
                        taknaam = tak if tak != "jong" else "jongverkenner"

                        leiding_lst = leiding[tak]  # maak lijst met leiding namen
                        laatste_persoon = leiding_lst[-1].replace(":", "")

                        # bepaal is/zijn
                        if len(leiding_lst) != 1:
                            personen = ", ".join(leiding_lst[:-1]).replace(":", "")
                            antwoord = f"De {taknaam} leiding zijn {personen} en {laatste_persoon}"
                        else:
                            antwoord = f"De {taknaam} leiding is {laatste_persoon}"

                        # stuur antwoord
                        bericht = discord.Embed(title="", description=antwoord)
                        await self.send(message.channel, bericht)

                        # voeg emojis toe aan antwoord
                        for persoon in leiding_lst:
                            for emoji in message.guild.emojis:
                                if persoon.strip(":") == emoji.name:

                                    await self.reaction(emoji)

                        # indien een tak gevonden, stop met zoeken
                        found = True

    # dm commando
    async def dm(self, message):
        admin_id = [262900122264797185]

        recievers = [None]

        # try to find reciever
        if message.content[0] == "@" and message.author.id in admin_id:
            id_user = int(message.content[1:19]) if message.content[1:19].isdigit() else None
            recievers = [self.client.get_user(id_user)]

        # send message to reciever
        if recievers[0] is not None:
            bericht = message.content[20:]
            title = ""

        else:  # forward message to admins
            recievers = []
            for id_reciever in admin_id:
                recievers.append(self.client.get_user(id_reciever))
            id_user = message.author.id
            name_user = message.author.name
            title = f"Dm from {name_user} ({id_user})"
            bericht = message.content

        # send message
        for reciever in recievers:
            await self.send(reciever, discord.Embed(title=title, description=bericht))
