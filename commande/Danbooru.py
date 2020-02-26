from pybooru import Danbooru
import discord

client = Danbooru('danbooru')
arrayLoli = (
    "Unicorn", "Ayanami", "Laffey", "Z23", "Javelin", "Eldridge", "Sims", "Hammann", "Hibiki", "Mutsu", "Nagato",
    "Kisaragi", "Saratoga", "Yukikaze", "Belchan", "Shouhou", "Akagi-chan", "Hiei-chan", "Zeppelin-chan", "Juneau",
    "Pamiat", "Grozny", "Carabiniere", "Dace")


def remove_duplicate_words(s):
    return ' '.join(dict.fromkeys(s.split()))


async def post(channel_sfw, channel_nsfw):
    f = open("lastId.txt", 'r')
    currentId = f.read()
    currentId = int(currentId)
    f.close()
    image = client.post_list(tags="azur_lane", limit=1, page=1)
    for post in image:
        id = post['id']
    if not currentId == id:
        currentId = id
        f = open("./textfile/lastId.txt", "w")
        f.write(str(currentId))
        f.close()
        for post in image:
            fileurl = post['large_file_url']
            character = post['tag_string_character']
            nbChar = post['tag_count_character']
            artist = post['tag_string_artist']
            rating = post['rating']
            charList = "";
            nameShip = "";
        if nbChar > 1:
            character = character.split(" ")
            for char in character:
                if char.index("(") != -1:
                    char = char[0:char.index("(")]
                if not "(" in char or not ")" in char and char.index("_") != -1:
                    char = char[0:char.rindex("_")]
                    char = char.title()
                    charList += char + " "
                elif char.index("_") == -1:
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
        embed = discord.Embed(title=nameShip, description="Artiste : [" + artist.replace("_",
                                                                                         " ").title() + "](" + "https://danbooru.donmai.us/posts?tags=" + artist + ")")
        embed.set_image(url=fileurl)

        if "Bache" not in nameShip:
            if rating == "s":
                await channel_sfw.send(embed=embed)
            elif rating == "e" or rating == "q":
                if not any(loli in nameShip for loli in arrayLoli):
                    await channel_nsfw.send(embed=embed)
        if "Bache" not in nameShip:
            arrayTiti = ("St. Louis", "Honolulu")
            # arrayKuro = ("Cleveland","Yamashiro","Sheffield","Washington","Z23")
            arrayTsuki = ("Cleveland", "Saratoga", "Kasumi")
            arrayKaiser = ("Cleveland")
            pingList = ""
            if "Tirpitz" in nameShip:
                pingList += " <@231467986165301249> "
            if any(char in nameShip for char in arrayTiti):
                pingList += " <@194876496752410624> "
            #  if any(char in embedtitle for char in arrayKuro):
            #     pingList += " <@142682730776231936> "
            if any(char in nameShip for char in arrayTsuki):
                pingList += " <@302837596600664065> "
            if rating == "s":
                await channel_sfw.send(pingList)
            if rating == "e" or rating == "q" and not any(loli in nameShip for loli in arrayLoli):
                await channel_nsfw.send(pingList)
