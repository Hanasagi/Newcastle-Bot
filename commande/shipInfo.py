import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from DAO import DAO
import asyncio
import difflib
import discord

async def info(ctx,ship1,ship2=None,ship3=None,ship4=None,bot=None,isKai=False):
    shipN=ship1
    if ship2 != None:
        shipN += " "+ship2
        if ship3 != None:
            shipN += " "+ship3
            if ship4 != None:
                shipN += " "+ship4

    nameList = [line.rstrip('\n') for line in open('./textfile/shipNameList.txt', 'r', encoding='utf8')]
    shipN = shipN.replace(' ','_').title()
    if not shipN.lower() in nameList:
        simili = difflib.get_close_matches(shipN,set(nameList))
        embedName = discord.Embed()
        sName = "**Correction possible**\n"
        for i in simili:
            sName+=i.replace('_',' ').title()+"\n"
        if(len(sName)>24):
            embedName.description = sName
            await ctx.send(embed=embedName)
        else:
            await ctx.send("Format: n!ship <Nom> (Exemple: n!ship Prinz Eugen)")
    else:
        dao = DAO()
        dao.select("ship",
                   ["Name", "Classe", "Image", "Chibi", "BuildTime", "Rarity", "Type", "Nation", "Pixiv", "PixivURL",
                    "ClasseURL", "ImageKai", "ChibiKai", "TypeKai"], "Name", shipN)
        result = dao.cursor.fetchall()
        for row in result:
            shipName=row[0]
            shipName=shipName.replace('_',' ')
            shipClasse=row[1]
            shipImg="https://azurlane.koumakan.jp"+row[2]
            shipChibi="https://azurlane.koumakan.jp"+row[3]
            shipBuild = row[4]
            shipRarity = row[5]
            shipType = row[6]
            shipNation = row[7]
            shipArtist=row[8]
            artistPixiv = row[9]
            shipClasseURL = "https://azurlane.koumakan.jp"+row[10]
            if row[11]!=None:
                isKai=True
                shipNameKai = shipName + " Kai"
                shipImgKai = "https://azurlane.koumakan.jp"+row[11]
                shipChibiKai = "https://azurlane.koumakan.jp"+row[12]
                shipTypeKai = row[13]
        dao.close()
        embedBase = discord.Embed(title=shipName, description='Rareté : **' + shipRarity + "**\n Nationalité : **" + shipNation + "** Type : **" + shipType +
                    "**\n Classe : **[" + shipClasse + "]("+ shipClasseURL+")**\n Artiste : **["+shipArtist+"]("+artistPixiv+")** Construction : **" + shipBuild + "**")
        embedBase.set_image(url=shipImg)
        embedBase.set_thumbnail(url=shipChibi)

        embedList = [embedBase]
        if isKai:
            embedKai = discord.Embed(title=shipName + " Kai", description='Rareté : **' + shipRarity + "**\n Nationalité : **" + shipNation + "** Type : **" + shipTypeKai +
                    "**\n Classe : **[" + shipClasse + "]("+ shipClasseURL+")**\n Artiste : **["+shipArtist+"]("+artistPixiv+")** Construction : **" + shipBuild + "**")
            embedKai.set_image(url=shipImgKai)
            embedKai.set_thumbnail(url=shipChibiKai)
            embedList.append(embedKai)
        left = '◀'
        right = '▶'

        def predicate(message, l, r):
            def check(reaction, user):
                if reaction.message.id != message.id or user == bot.user:
                    return False
                if l and reaction.emoji == left:
                    return True
                if r and reaction.emoji == right:
                    return True
                return False

            return check

        index = 0
        msg = None
        action = ctx.send
        if len(embedList) > 1:
            while True:
                try:
                    res = await action(embed=embedList[index])
                    if res is not None:
                        msg = res
                    l = index != 0
                    r = index != len(embedList) - 1
                    await msg.add_reaction(left)
                    await msg.add_reaction(right)
                    react, user = await bot.wait_for('reaction_add', check=predicate(msg, l, r), timeout=20)
                    if react.emoji == left:
                        if index == 0:
                            index = len(embedList) - 1
                        else:
                            index -= 1
                    elif react.emoji == right:
                        if index == len(embedList) - 1:
                            index = 0
                        else:
                            index += 1
                    action = msg.edit
                except asyncio.TimeoutError:
                    await msg.clear_reactions()
                    break
        else:
            await action(embed=embedList[0])


