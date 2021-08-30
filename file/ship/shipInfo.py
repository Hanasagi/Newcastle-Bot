import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import asyncio
import difflib
import discord
import json
from azurlane.azurapi import AzurAPI

api = AzurAPI()


async def info(ctx, ship, bot):
    api.updater.update()
    isKai = False
    ship = ship.lower()
    info = api.getShip(ship=ship)
    shipName = info.get("names").get("en")
    shipClasse = info.get("class")
    shipImg = info.get("skins")[0].get("image")
    shipBuild = info.get("construction").get("constructionTime")
    shipRarity = info.get("rarity")
    shipType = info.get("hullType")
    shipNation = info.get("nationality")
    shipArtist = info.get("misc").get("artist").get('name') if info.get("misc").get("artist") != None else ""
    artistPixiv = info.get("misc").get("pixiv").get('url') if info.get("misc").get("pixiv") != None else ""
    shipClasseURL = "https://azurlane.koumakan.jp/Category:" + shipClasse.replace(" ", "_")
    shipVA = info.get("misc").get("voice").get("name")
    shipVAurl = info.get("misc").get("voice").get("url")

    def create_embed_field(embed,kai=False):
        embed.add_field(name="Wiki Page",value='['+shipName.replace(' ','_')+'](https://azurlane.koumakan.jp/'+shipName.replace(' ','_')+')',inline=False)
        embed.add_field(name="Construction", value=shipBuild, inline=True)
        embed.add_field(name="Rarity",  value=shipRarity,inline=True)
        embed.add_field(name="Nationality", value=shipNation, inline=True)
        if not kai:
            embed.add_field(name="Type", value=shipType, inline=True)
        else:
            embed.add_field(name="Type", value=shipTypeKai, inline=True)
        embed.add_field(name="Class", value="[" + shipClasse + "](" + shipClasseURL + ")", inline=True)
        embed.add_field(name="Pixiv", value="[" + shipArtist + "](" + artistPixiv + ")", inline=True)
        embed.add_field(name="Voice Actor", value="[" + shipVA + "](" + shipVAurl + ")", inline=True)
        return embed

    if info.get("retrofit"):
        isKai = True
        shipNameKai = shipName + " Retrofit"
        shipImgKai = info.get("skins")[1].get("image")
        shipTypeKai = api.getShip(ship=ship).get("retrofitHullType")
    embedBase = discord.Embed(title=shipName,)
    embedBase.set_image(url=shipImg)
    embedBase.set_thumbnail(url=info.get("thumbnail"))
    embedBase = create_embed_field(embedBase, False)
    embedList = [embedBase]
    if isKai:
        embedKai = discord.Embed(title=shipNameKai,)
        embedKai.set_image(url=shipImgKai)
        embedKai.set_thumbnail(url=info.get("thumbnail"))
        embedKai=create_embed_field(embedKai,True)
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
                l = index >= 0
                r = index != len(embedList)
                await msg.add_reaction(left)
                await msg.add_reaction(right)
                react, user = await bot.wait_for('reaction_add', check=predicate(msg, l, r), timeout=20)

                if react.emoji == left:
                    if index > 0:
                        index -= 1
                    elif index == 0:
                        index = len(embedList) - 1
                elif react.emoji == right:
                    if index < len(embedList) - 1:
                        index += 1
                    elif index == len(embedList) - 1:
                        index = 0
                action = msg.edit
            except asyncio.TimeoutError:
                await msg.clear_reactions()
                break
    else:
        await action(embed=embedList[0])

