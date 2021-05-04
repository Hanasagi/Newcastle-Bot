from pybooru import Danbooru
import discord
import json
import os
import asyncio
import sys
import random
import urllib
from nudenet import NudeClassifier
classifier = NudeClassifier()
client = Danbooru('danbooru')

forbiddenChar = None
namelist = []
sublist = []
nsfwlist = []
cachedStamp = 0
disable_check = False


def loadSubList():
    file = "../json/subBooru.json"
    stamp = os.stat(file).st_mtime
    global namelist, sublist, nsfwlist, cachedStamp, forbiddenChar
    if cachedStamp is not None:
        if stamp != cachedStamp:
            cachedStamp = stamp
            data_list = json.load(open(file))
            forbiddenChar = json.load(open("../json/forbiddenCharacter.json", "r"))
            print("Loaded/Reloaded")
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


async def post(channel_sfw, channel_nsfw, channel_check, bot):
    try:
        x = json.load(open("../json/lastId.json"))
        currentId = int(x["booru"].get("id"))
        image = client.post_list(tags="azur_lane", limit=1, page=1)
        for post in image:
            id = post['id']
            banned_artist = post['tag_string_artist']
            tag = post['tag_string_general']

        if not currentId == id:
            if not "banned" in banned_artist and not any(t in tag for t in ["futanari", "bestiality"]) and not "official_art" in post["tag_string_meta"]:
                currentId = id
                loadSubList()

                x["booru"]["id"] = currentId
                with open("../json/lastId.json", "w") as out:
                    json.dump(x, out)
                for post in image:
                    try:
                        fileurl = post['large_file_url']
                    except KeyError:
                        try:
                            fileurl = post['file_url']
                        except KeyError:
                            print("File url is broken")
                            return
                    urllib.request.urlretrieve(fileurl, "../image/danbooru_image.jpg")
                    character = post['tag_string_character']
                    nbChar = post['tag_count_character']
                    artist = post['tag_string_artist']
                    rating = post['rating']
                if not character:
                    character = "Non renseignÃ©"
                    nbChar = 1
                if not artist:
                    artist = "Non renseignÃ©"
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
                    if charList != "Non renseignÃ©":
                        charList = charList.replace('_', ' ')
                        nameShip = remove_duplicate_words(charList.title())
                    else:
                        nameShip = "Non renseignÃ©"
                if rating == "e" or rating == "q":
                    if not any(loli in nameShip for loli in forbiddenChar["forbiddenChar"]):
                        pass
                    else:
                        return
                text = ''
                name = nameShip if nameShip != "Non renseignÃ©" else "Non renseignÃ©"
                artistx = "[" + artist.replace("_",
                                               " ").title() + "](https://danbooru.donmai.us/posts?tags=" + artist + ")" if artist != "Non renseignÃ©" else "Non renseignÃ©"
                if "webm" in fileurl:
                    text += "\nArtiste : " + artistx + "\n" + fileurl
                else:
                    text += "Artiste : " + artistx + "\n[Lien du post](https://danbooru.donmai.us/posts/" + str(
                        currentId) + ")"
                embed = discord.Embed(title=name, description=text)
                embed.set_image(url=fileurl)

                content = embed if not "webm" in fileurl else text
                if not disable_check:
                    await check_content_ia(bot, content, channel_check, channel_sfw, channel_nsfw, nameShip, rating)
                else:
                    if rating == 's':
                        await post_content(content, channel_sfw, nameShip, rating)
                    else:
                        await post_content(content, channel_nsfw, nameShip, rating)
    except KeyError:
        print("Unavailable")


async def post_content(content, channel, nameShip, rating):
    nameList = check_nameList(nameShip, rating)
    if isinstance(content, discord.Embed):
        await channel.send(embed=content)
    else:
        await channel.send(content)
    if nameList != "":
        await channel.send(nameList)

async def check_content_ia(bot, content, channel_check, channel_sfw, channel_nsfw, nameShip, rating):
    r = classifier.classify("../image/danbooru_image.jpg")

    if r["../image/danbooru_image.jpg"]["unsafe"]>=0.80:
        await post_content(content,channel_nsfw,nameShip,"e")
    elif r["../image/danbooru_image.jpg"]["safe"]>=0.80:
        if rating=="s":
            await post_content(content,channel_nsfw,nameShip,"s")
        else:
            await post_content(content, channel_sfw, nameShip, "e")
    elif r["../image/danbooru_image.jpg"]["unsafe"]<=0.80 and r["../image/danbooru_image.jpg"]["safe"] >= 0.30:
        await check_content(bot, content, channel_check, channel_sfw, channel_nsfw, nameShip, rating)
    elif r["../image/danbooru_image.jpg"]["safe"]<=0.80 and r["../image/danbooru_image.jpg"]["unsafe"] >= 0.30:
        await check_content(bot, content, channel_check, channel_sfw, channel_nsfw, nameShip, rating)

async def check_content(bot, content, channel_check, channel_sfw, channel_nsfw, nameShip, rating):
    ratingmsg = await channel_check.send("Rating: " + rating)
    if isinstance(content, discord.Embed):
        msg = await channel_check.send(embed=content)
    else:
        msg = await channel_check.send(content)
    sfw = '👍'
    nsfw = '👎'
    delete = '🚫'

    def check(reaction, user):
        if user != bot.user:
            if reaction.emoji == sfw:
                return reaction.emoji == sfw
            if reaction.emoji == nsfw:
                return reaction.emoji == nsfw
            if reaction.emoji == delete:
                return reaction.emoji == delete
        return False

    await msg.add_reaction(sfw)
    await msg.add_reaction(nsfw)
    await msg.add_reaction(delete)

    has_been_checked = False
    while True:
        try:
            react, user = await bot.wait_for('reaction_add', check=check,
                                             timeout=300)
            if react.emoji == str(sfw):
                await post_content(content, channel_sfw, nameShip, "s")
                await msg.clear_reactions()
                await discord.Message.delete(ratingmsg)
                await discord.Message.delete(msg)
                has_been_checked = True
            elif react.emoji == str(nsfw):
                await post_content(content, channel_nsfw, nameShip, "e")
                await msg.clear_reactions()
                await discord.Message.delete(ratingmsg)
                await discord.Message.delete(msg)
                has_been_checked = True
            elif react.emoji == str(delete):
                await msg.clear_reactions()
                await discord.Message.delete(ratingmsg)
                await discord.Message.delete(msg)
                has_been_checked = True
        except asyncio.TimeoutError:
            if not has_been_checked:
                if rating == 's':
                    await post_content(content, channel_sfw, nameShip, "s")
                else:
                    await post_content(content, channel_nsfw, nameShip, "e")
                await msg.clear_reactions()
                await discord.Message.delete(ratingmsg)
                await discord.Message.delete(msg)
            break


async def check(ctx, state):
    global disable_check
    if state == "n":
        disable_check = True
        await ctx.send("Checking dÃ©sactivÃ©")
    elif state == "y":
        disable_check = False
        await ctx.send("Checking activÃ©")
    else:
        await ctx.send(disable_check)


def check_nameList(nameShip, rating):
    nameList = ''
    for i, j, k in zip(namelist, sublist, nsfwlist):
        if any(a in nameShip.strip().lower() for a in j):
            if rating == "s":
                nameList += "<@!" + str(i) + "> "
            elif rating == "e":
                if k != "no":
                    nameList += "<@!" + str(i) + "> "
    return nameList


async def search_picture(ctx, character, number):
    if number <= 10:
        image = client.post_list(tags=character + '_(azur_lane)', limit=number, random=True)
        for post in image:

            try:
                fileurl = post['large_file_url']
            except KeyError:
                try:
                    fileurl = post['file_url']
                except KeyError:
                    print("File url is broken")
                    return

            artist = post['tag_string_artist']
            rating = post['rating']
            id = post["id"]
            embed = discord.Embed(description="Artiste : [" + artist.replace("_",
                                                                             " ").title() + "](" + "https://danbooru.donmai.us/posts?tags=" + artist + ")\n[Lien du post](https://danbooru.donmai.us/posts/" + str(
                id) + ")")
            embed.set_image(url=fileurl)
            await ctx.send(embed=embed)

    else:
        await ctx.send("Maximum 10 images.")
