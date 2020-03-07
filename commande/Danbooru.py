from pybooru import Danbooru
import discord
import json

client = Danbooru('danbooru')
with open("../json/forbiddenCharacter.json","r") as input:
    data = input.read()
forbiddenChar=json.loads(data)

def remove_duplicate_words(s):
    return ' '.join(dict.fromkeys(s.split()))


async def post(channel_sfw, channel_nsfw):

    with open("../json/lastId.json", "r") as input:
        data = input.read()
    x = json.loads(data);
    currentId = int(x["id"])

    image = client.post_list(tags="azur_lane", limit=1, page=1)
    for post in image:
        id = post['id']
        banned_artist= post['tag_string_artist']

    if not currentId == id and not "banned" in banned_artist:
        currentId = id

        with open("../json/lastId.json", "w") as out:
            outlist = json.dumps({"id": currentId})
            out.write(outlist)

        for post in image:
            fileurl = post['large_file_url']
            character = post['tag_string_character']
            nbChar = post['tag_count_character']
            artist = post['tag_string_artist']
            rating = post['rating']
            charList = "";
            nameShip = "";
        if nbChar > 1:
            print(character.index("("))
            character = character.split(" ")
            for char in character:
                if char.index("(") != None:
                    char = char[0:char.index("(")]
                if not "(" in char or not ")" in char and char.index("_") != -1:
                    char = char[0:char.rindex("_")]
                    char = char.title()
                    charList += char + " "
                elif char.index("_") == None:
                    charList += char + ", "
            charList = charList[:-1]
            embedtitle = remove_duplicate_words(charList.replace(",", ''))
            for i in embedtitle:
                if i == " ":
                    nameShip += ", "
                else:
                    nameShip += i
            nameShip = nameShip.replace("_", " ")
        else:
            charList += character[0:character.index("(")]
            charList = charList.replace('_', ' ')
            nameShip = remove_duplicate_words(charList[:-1].title())
        embed = discord.Embed(title=nameShip, description="Artiste : [" + artist.replace("_", " ").title() + "](" + "https://danbooru.donmai.us/posts?tags=" + artist + ")")
        embed.set_image(url=fileurl)

        if "Bache" not in nameShip:
            if rating == "s":
                await channel_sfw.send(embed=embed)
            elif rating == "e" or rating == "q":
                if not any(loli in nameShip for loli in forbiddenChar):
                    await channel_nsfw.send(embed=embed)

