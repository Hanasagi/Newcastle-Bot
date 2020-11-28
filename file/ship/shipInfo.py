import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from DAO import DAO
import asyncio
import difflib
import discord
import json
from azurlane.azurapi import AzurAPI

api = AzurAPI()


async def info(ctx, ship1, ship2=None, ship3=None, ship4=None, bot=None, isKai=False):
    api.updater.update()
    shipN = ship1
    if ship2 != None:
        shipN += " " + ship2
        if ship3 != None:
            shipN += " " + ship3
            if ship4 != None:
                shipN += " " + ship4

    shipN = shipN.replace(' ', '_').title()
    info = api.getShip(ship=shipN)
    shipName = info.get("names").get("en")
    shipClasse = info.get("class")
    shipImg = info.get("skins")[0].get("image")
    shipBuild = info.get("construction").get("constructionTime")
    shipRarity = info.get("rarity")
    shipType = info.get("hullType")
    shipNation = info.get("nationality")
    shipArtist = info.get("misc").get("artist").get('name')
    artistPixiv = info.get("misc").get("pixiv").get('url')
    shipClasseURL = "https://azurlane.koumakan.jp" + shipClasse.replace(" ", "_")
    shipVA = info.get("misc").get("voice").get("name")
    shipVAurl=info.get("misc").get("voice").get("url")
    print(type(shipRarity))
    print(type(shipClasse))
    print(type(shipType))
    print(type(shipBuild))
    print(type(shipNation))
    print(shipArtist)
    print(artistPixiv)
    print(type(shipClasseURL))
    print(shipVA)
    if info.get("retrofit"):
        isKai = True
        shipNameKai = shipName + " Retrofit"
        shipImgKai = info.get("skins")[1].get("image")
        shipTypeKai = api.getShip(ship=shipN).get("retrofit_hullType")

    embedBase = discord.Embed(title=shipName,
                              description='Rarity : **' + shipRarity + "**\n Nationality : **" + shipNation + "** Type : **" + shipType +
                                          "**\n Class : **[" + shipClasse + "](" + shipClasseURL + ")**\n Artist : **[" + shipArtist + "](" + artistPixiv + ")** Construction : **" + shipBuild + "**"+ "**\nVoice Actor : **[" + shipVA+"]("+shipVAurl+")**")
    embedBase.set_image(url=shipImg)
    embedBase.set_thumbnail(url=info.get("thumbnail"))

    embedList = [embedBase]
    if isKai:
        embedKai = discord.Embed(title=shipNameKai,
                                 description='Rareté : **' + shipRarity + "**\n Nationalité : **" + shipNation + "** Type : **" + shipTypeKai +
                                             "**\n Classe : **[" + shipClasse + "](" + shipClasseURL + ")**\n Artiste : **[" + shipArtist + "](" + artistPixiv + ")** Construction : **" + shipBuild + "**"+ "**\nVoice Actor : **[" + shipVA+"]("+shipVAurl+")**")
        embedKai.set_image(url=shipImgKai)
        embedKai.set_thumbnail(url=info.get("thumbnail"))
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
