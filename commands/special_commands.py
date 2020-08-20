import random

# open en overloop slagzinnen.txt
zinnen = open("commands/slagzinnen.txt", "r", encoding="utf8")
zinnen_lst = []

# voeg zinnen toe aan lijst
for zin in zinnen:
    zinnen_lst.append(zin.strip("\n"))


# random zin functie
def loekentatjen(specifiek_lst):

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

    return titel, antwoord  # stuur resultaat


# funtie dictionairy
switcher = \
    {
        "!loeken": loekentatjen
    }


# zoekt juiste functie in de dictionairy
def special(commando, specifiek_lst):
    func = switcher[commando]
    return func(specifiek_lst)
