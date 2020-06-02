from pybooru import Danbooru
import discord
import json
import os

client = Danbooru('danbooru')
with open("../json/forbiddenCharacter.json", "r") as input:
    data = input.read()
forbiddenChar = json.loads(data)

namelist = []
sublist = []
nsfwlist = []
cachedStamp = 0

"""# First call, to avoid having empty list
with open("../json/subBooru.json") as f:
    data = f.read()
    data_list = json.loads(data)
    for data in data_list["data"]:
        name = data["name"]
        ship = data["charlist"]
        namelist.append(name)
        sublist.append(ship)
        nsfwlist.append(data["nsfw"])"""


def loadSubList():
    file = "../json/subBooru.json"
    stamp = os.stat(file).st_mtime
    global namelist, sublist, nsfwlist, cachedStamp
    if cachedStamp is not None:
        if stamp!=cachedStamp:
            cachedStamp=stamp
            with open(file) as f:
                data = f.read()
            data_list = json.loads(data)
            print("file got changed")
            namelist.clear()
            sublist.clear()
            nsfwlist.clear()
            for data in data_list["data"]:
                name = data["name"]
                ship = data["charlist"]
                namelist.append(name)
                sublist.append(ship)
                nsfwlist.append(data["nsfw"])


def remove_duplicate_words(s):
    return ' '.join(dict.fromkeys(s.split()))


async def post(channel_sfw, channel_nsfw):
    with open("../json/lastId.json", "r") as input:
        data = input.read()
    x = json.loads(data)
    currentId = int(x["id"])

    loadSubList()

    image = client.post_list(tags="azur_lane", limit=1, page=1)
    for post in image:
        id = post['id']
        banned_artist = post['tag_string_artist']
        tag = post['tag_string_general']

    if not currentId == id and not "banned" in banned_artist and not "futanari" in tag and not "bestiality" in tag :
        currentId = id

        with open("../json/lastId.json", "w") as out:
            outlist = json.dumps({"id": currentId})
            out.write(outlist)

        for post in image:

            try:
                fileurl = post['large_file_url']
            except KeyError:
                try:
                    fileurl = post['file_url']
                except KeyError:
                    print("File url is broken")
                    return

            character = post['tag_string_character']
            nbChar = post['tag_count_character']
            artist = post['tag_string_artist']
            rating = post['rating']
        charList = ""
        nameShip = ""
        if nbChar > 1:
            character = character.split(" ")
            for char in character:

                try:
                    char_index = char.index("(")
                except ValueError:
                    char_index = -1

                if char_index != -1:
                    char = char[0:char.index("(")]
                    if not "(" in char or not ")" in char and char.index("_"):
                        char = char[0:char.rindex("_")]
                        char = char.title()
                        charList += char + " "
                elif char_index == -1:
                    charList += char.title() + ", "
            charList = charList[:-1]
            embedtitle = remove_duplicate_words(charList.replace(",", ''))
            for i in embedtitle:
                if i == " ":
                    nameShip += ", "
                else:
                    nameShip += i
            nameShip = nameShip.replace("_", " ")

        else:
            try:
                char_index = character.index("(")
            except ValueError:
                char_index = -1

            if char_index != -1:
                charList += character[0:character.index("(")]

            else:
                charList = character
            charList = charList.replace('_', ' ')
            nameShip = remove_duplicate_words(charList[:-1].title())
        if rating == "e" or rating == "q":
            if not any(loli in nameShip for loli in forbiddenChar["forbiddenChar"]):
                pass
            else:
                print('loli bad')
                return
        text = ''
        if "webm" in fileurl:
            text += "***" + nameShip + "***\nArtiste : ***" + artist.replace("_", " ").title(
            ) + "***, [https://danbooru.donmai.us/posts?tags=" + artist + "]\n" + fileurl
        else:
            text += "Artiste : [" + artist.replace("_",
                                                   " ").title() + "](" + "https://danbooru.donmai.us/posts?tags=" + artist + ")\n[Lien du post](https://danbooru.donmai.us/posts/" + str(
                currentId) + ")"
        embed = discord.Embed(title=nameShip, description=text)
        embed.set_image(url=fileurl)

        nameList = ''
        for i, j, k in zip(namelist, sublist, nsfwlist):
            if any(a in nameShip.strip().lower() for a in j):
                if rating == "s":
                    nameList += "<@!" + str(i) + "> "
                elif rating == "e" or rating == "q":
                    if k != "no":
                        nameList += "<@!" + str(i) + "> "

        if len(nameList) > 1:
            if rating == "s":
                if "webm" in fileurl:
                    await channel_sfw.send(text)
                else:
                    await channel_sfw.send(embed=embed)
                await channel_sfw.send(nameList)
            elif rating == "e" or rating == "q":
                if "webm" in fileurl:
                    await channel_nsfw.send(text)
                    await  channel_nsfw.send(nameList)
                else:
                    await channel_nsfw.send(embed=embed)
                    await channel_nsfw.send(nameList)
        else:
            if rating == "s":
                if "webm" in fileurl:
                    await channel_sfw.send(text)
                else:
                    await channel_sfw.send(embed=embed)
            elif rating == "e" or rating == "q":
                if "webm" in fileurl:
                    await channel_nsfw.send(text)
                else:
                    await channel_nsfw.send(embed=embed)
